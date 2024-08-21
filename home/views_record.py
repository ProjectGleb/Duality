from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import threading
import cv2
import numpy as np
import os
import time
import sounddevice as sd
import soundfile as sf
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path
from mss import mss
import base64
import shutil

# Global variables to manage recording state
recording_thread = None
stop_recording = threading.Event()

SNAPSHOT_DIR = Path(__file__).resolve().parent
output_folder = SNAPSHOT_DIR / "recording_outputs"

def clear_output_folder(folder):
    for item in folder.iterdir():
        if item.is_file() or item.is_symlink():
            item.unlink()
        elif item.is_dir():
            shutil.rmtree(item)

@csrf_exempt
def recording_start(request):
    global recording_thread, stop_recording

    if request.method == 'POST':
        if not recording_thread:
            # Start recording
            stop_recording.clear()
            recording_thread = threading.Thread(target=record_function)
            recording_thread.start()
            return JsonResponse({'status': 'Recording started'})
        else:
            return JsonResponse({'status': 'Recording already in progress'}, status=400)

    return JsonResponse({'status': 'Invalid request'}, status=400)

def record_function():
    # Load environment variables from the .env file
    load_dotenv()
    
    # Use pathlib for cross-platform compatibility
    output_folder.mkdir(parents=True, exist_ok=True)

    # Clear the output folder before starting a new recording
    clear_output_folder(output_folder)

    # Initialize audio recording parameters
    audio_output_file = output_folder / "output_audio.wav"
    samplerate = 44100
    chunk = 1024  # Number of frames per buffer

    def record_audio():
        print("Recording audio...")
        try:
            # Determine the number of input channels
            device_info = sd.query_devices(sd.default.device[0], 'input')
            channels = device_info['max_input_channels']
            
            # Initialize an empty list to store audio frames
            audio_frames = []
            
            # Start the stream
            with sd.InputStream(samplerate=samplerate, channels=channels) as stream:
                while not stop_recording.is_set():
                    audio_frames.append(stream.read(chunk)[0])
            
            print("Audio recording finished.")
            
            # Check if any audio was recorded
            if audio_frames:
                # Convert list of audio frames to a numpy array
                audio_frames = np.concatenate(audio_frames, axis=0)
                
                # Save the recorded audio to a file
                sf.write(str(audio_output_file), audio_frames, samplerate)
                print(f"Audio saved to {audio_output_file}")
            else:
                print("No audio data was recorded.")
        except Exception as e:
            print(f"An error occurred while recording audio: {e}")

    # Start audio recording in a separate thread
    audio_thread = threading.Thread(target=record_audio)
    audio_thread.start()

    no_of_frames = 0

    # Initialize mss for screen capture
    sct = mss()

    try:
        while not stop_recording.is_set():
            try:
                # Capture the entire screen
                screen = sct.grab(sct.monitors[0])
                
                # Convert to numpy array
                frame = np.array(screen)
                
                # Convert BGRA to RGB
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGRA2RGB)

                # Save the frame in RGB format
                frame_filename = output_folder / f"frame_{no_of_frames:04d}.png"
                cv2.imwrite(str(frame_filename), cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR))

                no_of_frames += 1
            except Exception as e:
                print(f'Screenshot error: {e}')
                time.sleep(1)  # Add a small delay to avoid rapid looping on error

    except Exception as e:
        print(f'Recording error: {e}')

    stop_recording.set()
    audio_thread.join()
    cv2.destroyAllWindows()

    print('Number of frames:', no_of_frames)

    # Check if audio file exists before processing
    if audio_output_file.exists():
        # Load OpenAI API key from environment
        openai_api_key = os.getenv('OPENAI_API_KEY')

        if openai_api_key:
            openai_client = OpenAI(api_key=openai_api_key)
        else:
            print('Please set the OPENAI_API_KEY environment variable.')
            return

        with open(audio_output_file, "rb") as audio_file:
            transcription = openai_client.audio.transcriptions.create(
                model="whisper-1", 
                file=audio_file,
                language="en"
            )

        print('Transcribed text:')
        print(transcription.text)

        with open(output_folder / "transcription.txt", "w") as text_file:
            text_file.write(transcription.text)
    else:
        print("Audio file not found. Skipping transcription.")

@csrf_exempt
def recording_end(request):
    global recording_thread, stop_recording

    if request.method == 'POST':
        if recording_thread:
            # Stop recording
            stop_recording.set()
            recording_thread.join()
            recording_thread = None
            
            # Process the recorded data
            gpt_video_parser_view(output_folder)
            
            return JsonResponse({'status': 'Recording stopped and processed'})
        else:
            return JsonResponse({'status': 'No recording in progress'}, status=400)

    return JsonResponse({'status': 'Invalid request'}, status=400)


def gpt_video_parser_view(folder_path):
    load_dotenv()

    # Set the API key as an environment variable
    os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')

    # Initialize the OpenAI client without passing the API key
    openai_client = OpenAI()

    def describe_descriptions(frames, transcribed_text, iterations=3, skip_frames=10):
        system_prompt = f"""You're an AI transcription agent that takes in a video of a user interracting with the web and transcribes his actions one at a time. Your goal is to transcribe those actions in a json format.
        - Given there are only two actions a user can take, click or type, if it's a 'Type' action, it must be in the double nested dictionary json format format like so: {{"Type": {{"web_page_element": "text_that_was_typed"}}}}. If it's a 'Click' action, it must be in a simple dictionary json format like so: {{"Click": "element_to_be_interacted_with"}}.
        - In the transcription you should ensure web_page_element ends with '_btn' if it's a button or '_box' if it's a text box.
        - By default, the first two actions you must put in in the json transcript are 'Click0': 'accept_all_btn' and the second one is'Type0': {{"google_search_box": "text_that_was_typed"}} entering the website that user typed in in place of text_that_was_typed.acordingly. Everything that follows is as per your observation of user actions.
        - Hre is a voice note transcipt by the useer explaining what actions he is taking as he is making them. Use it to make sense of the video as well and make your json transcript. Voice_Note_Transcript: {transcribed_text}. 
        - Lastly, don't add any natural language or other explanations. Your output must be in json format, meaning it should begin and end with curly braces.
        EXAMPLE OF A GOOD OUTPUT: {{"Click0": "accept_all_btn", "Type0": {{"google_search_box": "codeverse.uk"}}}}\n
        Dont use ```json and ```to begin and end the file. Just use curly brackets."""


        PROMPT_MESSAGES = [
        {
            "role": "user",
            "content": [
                system_prompt,
                *map(lambda x: {"image": x, "resize": 500}, frames[0::skip_frames]),
            ],
            },
        ]
        
        last_response = None 

        for _ in range(iterations):     
            params = {
                "model": "gpt-4o",  # This is the current model name for vision tasks
                "messages": PROMPT_MESSAGES,
                "max_tokens": 200,
            }
            try:
                result = openai_client.chat.completions.create(**params)
                last_response = result.choices[0].message.content
            except Exception as e:
                print(f"An error occurred while calling the OpenAI API: {e}")
                last_response = "Error: Unable to process the video at this time."

            print('Intermediate Response : ')
            print(last_response)
            print('##########################################')

            # Feed the model's output back into itself
            PROMPT_MESSAGES.append({"role": "assistant", "content": last_response})
            PROMPT_MESSAGES.append({"role": "user", "content": 'The above are your previous attempts. Please analyze them to make your new answer even better. Try to identify mistakes and rectify them.'})

        return last_response

    # Get list of image files from the folder
    frame_files = sorted([os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(('.png', '.jpg', '.jpeg'))])
    base64Frames = []
    for frame in frame_files[5:-5]:
        img_frame = cv2.imread(frame)
        _, buffer = cv2.imencode(".png", img_frame)
        base64Frames.append(base64.b64encode(buffer).decode("utf-8"))

    with open(folder_path / "transcription.txt", "r") as text_file:
        transcribed_text = text_file.read()
    
    print('transcribed text : ', transcribed_text)

    # Summarize descriptions
    summary = describe_descriptions(base64Frames, transcribed_text, iterations=1, skip_frames=20)

    # Attempt to parse the summary as JSON
    try:
        json_data = json.loads(summary)
    except json.JSONDecodeError:
        print('JSON parsing failed. Saving raw summary.')
        json_data = {"error": "JSON parsing failed", "raw_summary": summary}

    # Write the JSON data to the file
    with open(folder_path / "new_task.json", "w") as json_file:
        json.dump(json_data, json_file, indent=4)

    print("Task steps have been generated and saved to new_task.json")


# ------------------------------------------    
# Save the task and project to the database
# ------------------------------------------    


# ------------------------------------------    Add chatGPT funciton calling to save the task as json properly ------------------------------------------

# json file saved to database prematurely and isnt saved to jaon. 
# Review why. Is it not saved because of x? or because of y?


from django.views.decorators.http import require_POST
import json
from .models import Task, Project
from django.contrib.auth.models import User

@csrf_exempt
@require_POST
def save_task_to_project(request):
    try:
        data = json.loads(request.body)
        task_name = data.get('task_name')
        project_name = data.get('project_name')

        # Assuming the user is authenticated, get the current user
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'status': 'error', 'message': 'User not authenticated'}, status=401)

        # Get or create the project
        project, created = Project.objects.get_or_create(
            name=project_name,
            user=user
        )

        # Check if the new_task.json file exists and wait for it if necessary
        json_file_path = output_folder / "new_task.json"
        wait_time = 0
        while not json_file_path.exists() and wait_time < 60:  # Wait up to 60 seconds
            time.sleep(1)
            wait_time += 1

        if not json_file_path.exists():
            return JsonResponse({'status': 'error', 'message': 'Task processing not complete'}, status=400)

        # Read and parse the JSON file
        with open(json_file_path, "r") as json_file:
            task_steps = json.load(json_file)

        # Create the task
        task = Task.objects.create(
            name=task_name,
            project=project,
            steps=task_steps 
        )
        print(f"Saved Project: {project.name} (ID: {project.id})")
        print(f"Saved Task: {task.name} (ID: {task.id})")
        print(f"Task Steps: {task.steps}")


        return JsonResponse({'status': 'success', 'message': 'Task details saved successfully'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)    