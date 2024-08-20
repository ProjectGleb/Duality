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

# Global variables to manage recording state
recording_thread = None
stop_recording = threading.Event()

SNAPSHOT_DIR = Path(__file__).resolve().parent
output_folder = SNAPSHOT_DIR / "recording_outputs"


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

def record_function():
    # Load environment variables from the .env file
    load_dotenv()
    
    # Use pathlib for cross-platform compatibility
    output_folder.mkdir(parents=True, exist_ok=True)

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

def gpt_video_parser_view(folder_path):
    load_dotenv()

    # Set the API key as an environment variable
    os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')

    # Initialize the OpenAI client without passing the API key
    openai_client = OpenAI()

    def describe_descriptions(frames, transcribed_text, iterations=3, skip_frames=10):
        system_prompt = f"You're an AI agent that based on a user web interaction video transcribes user actions one at a time. If it's a 'Type' action, it must be in the format of 'Type': 'element_to_be_interacted_with': 'text_to_be_typed_in'.\n If it's a 'Click' action, it must be in the format of 'Click': 'element_to_be_interacted_with'.\n The element_to_be_interacted_with must end with '_btn' if it's a button or '_box' if it's a text box.\n Always start with 'Website: ' as the first line, followed by the website of focus. The second task is almost always accept all cookies button.  Here is the user explaining what they're doing, use this to make sense of the video as well: {transcribed_text}. Don't use natural language. Don't provide any other explanation."

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
    
    with open(folder_path / "new_task.txt", "w") as text_file:
        text_file.write(summary)

    print("Task steps have been generated and saved to new_task.txt")