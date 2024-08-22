# Duality: An AI employee that can control your computer.
![Duality-demo](https://github.com/user-attachments/assets/3d9fa8c5-fd6a-4cac-b392-f817ebab7481)

## Overview 🔎
Duality is an AI agent crew that can take over your browser and complete tasks for you. 

## Features 🧰:
1. **Create a Screen Recording:**
    - Record how you complete a task. The agent will use vision and audio to understand the steps you are taking.
2. **Transcription:**
    - The recording is parsed into actionable steps using GPT4o.
3. **Interaction:**
    - The agent then initiates a browser session, parses through HTML, finds the relevant page elements and interacts with them according to the query.

---

## Set-up 🔧
Create anaconda environment
```
conda create -n agent_env python=3.10 -y 
conda activate agent_env
```

Install dependencies
```
pip install -r requirements.txt
```

Create a .env file and set up the api keys
```
AGENTQL_API_KEY=<AGENTQL_API_GOES_HERE>
OPENAI_API_KEY=<OPENAI_API_GOES_HERE>
```

## Run 💥🏃‍♂️🔥
To use the application:
1. Run ``` python manage.py runserver``` to host a local server using django.
2. Open the browser and type in the port as url ```http://127.0.0.1:8000/```.
3. Enjoy :) Record tasks, execute them, and have a productive day!

P.S: Dockerisation is under construction. If i manage to resolve docker conflicts you will be able to run the agent using it.
