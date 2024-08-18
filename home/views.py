from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response

import json
import time
from pathlib import Path
import os
import agentql
from dotenv import load_dotenv

load_dotenv()

@login_required
def home_view(request):
    return render(request, 'index.html')

@login_required
def projects_view(request):
    return render(request, 'projects.html')

def load_json_file(user_inp):
    # Adjust this path to match your Django project structure
    memory_path = Path(__file__).resolve().parent.parent / 'task_memory'
    
    print(f"Searching for matching task in: {memory_path}")
    print(f"User input: {user_inp}")
    
    for file_path in memory_path.glob('*.json'):
        print(f"Checking file: {file_path}")
        with open(file_path, 'r') as file:
            data = json.load(file)
            keywords = file_path.stem.split('_')
            print(f"Keywords for this file: {keywords}")
            if any(keyword in user_inp.lower() for keyword in keywords):
                print(f"Match found in file: {file_path}")
                return data
    print("No match found in any file")
    return None

def agent_logic(user_inp):
    def agentql_logic():
        elements = load_json_file(user_inp)
        if elements is None:
            return "No matching task found in memory for the query."

        print("Starting agentql session...")
        time.sleep(4)
        session = agentql.start_session("https://www.google.com")
        page = session  # main page

        username = os.getenv('USERNAME')
        password = os.getenv('PASSWORD')

        for key, value in elements.items():
            if isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    if sub_value == "username":
                        elements[key][sub_key] = username
                    elif sub_value == "password":
                        elements[key][sub_key] = password

        output = "Successfully executed the actions."

        for action, value in elements.items():
            print(f"Executing action: {action}")
            if 'Click' in action:
                Query = f"""
                {{
                    {value}
                }}
                """
                try:
                    response = page.query(Query)
                    element = getattr(response, value)
                    element.click(force=True)
                    print(f"Clicked element: {value}")
                except Exception as e:
                    print(f"Error during clicking {value}: {e}")

            elif 'Type' in action:
                for item, text in value.items():
                    Query = f"""
                    {{
                        {item}
                    }}
                    """
                    try:
                        response = page.query(Query)
                        element = getattr(response, item)
                        element.type(text)
                        print(f"Typed '{text}' into {item}")
                    except Exception as e:
                        print(f"Error during typing {text} into {item}: {e}")

        print("Waiting before stopping the session...")
        time.sleep(5)  # Wait before stopping the session to see the task completed
        session.stop()
        print("Session stopped.")
        return output

    print(f"Agent logic called with input: {user_inp}")
    result = agentql_logic()
    print(f"Agent logic result: {result}")
    return result


# Existing POST handler function
@api_view(['POST', 'GET'])  # Allow both POST and GET requests
def process_input(request):
    if request.method == 'POST':
        # Handle POST request logic
        user_input = request.data.get("user_input", "")
        print(f"Received user input: {user_input}")
        result = agent_logic(user_inp=user_input)
        print(f"Final result: {result}")
        return Response({"result": result})
    
    elif request.method == 'GET':
        # Handle GET request logic
        # For example, you can return a predefined message or perform a different logic
        print("Received a GET request")
        return Response({"result": "This is a response to a GET request"})

    # Return 405 Method Not Allowed if the request method is not supported
    return Response({"detail": "Method not allowed"}, status=405)