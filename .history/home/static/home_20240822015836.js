document.addEventListener('DOMContentLoaded', function() {
    const content = document.getElementById('content');
    const submitButton = document.getElementById('submitButton');
    const chatLog = document.getElementById('chatLog');
    const button1 = document.getElementById('button1');
    const button2 = document.getElementById('button2');
    const button3 = document.getElementById('button3');
    const button4 = document.getElementById('button4');
    const recordButton = document.getElementById('recordButton');
    const recordText = document.querySelector('.record-text');

    submitButton.addEventListener('click', handleSubmit);
    content.addEventListener('keydown', handleKeyDown);
    content.addEventListener('input', handleInput);

    button1.addEventListener('click', handleButton1Click);
    button2.addEventListener('click', handleButton2Click);
    button3.addEventListener('click', handleButton3Click);
    button4.addEventListener('click', handleButton4Click);
    recordButton.addEventListener('click', handleRecordButtonClick);

    let isRecording = false;
    let isNamingTask = false;
    let isSelectingProject = false;
    let currentTaskName = '';

    function handleRecordButtonClick() {
        const newRecordingState = !isRecording;
        const url = newRecordingState ? `${window.location.origin}/home/recording_start/` : http://127.0.0.1:8000/home/recording_end/';
        
        // Immediately update UI
        isRecording = newRecordingState;
        updateRecordButtonUI();

        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCSRFToken(),
            },
        })
        .then(response => response.json())
        .then(data => {
            console.log(data.status);
        })
        .catch(error => {
            console.error('Error:', error);
            alert('There was a problem with the recording request.');
            // Revert the UI if there was an error
            isRecording = !newRecordingState;
            updateRecordButtonUI();
        });
    }

    function updateRecordButtonUI() {
        recordButton.classList.toggle('recording-active', isRecording);
        recordText.textContent = isRecording ? 'Stop' : 'Record Task';
        
        if (isRecording) {
            addMessageToChatLog("Recording in progress", 'agent');
        } else {
            askForTaskName();
        }
        
        scrollChatToBottom();
    }

    function askForTaskName() {
        addMessageToChatLog("What would you like to name the task?", 'agent');
        scrollChatToBottom();
        isNamingTask = true;
    }

    function askForProjectName() {
        addMessageToChatLog("What project would you like to save this task to?", 'agent');
        scrollChatToBottom();
        isSelectingProject = true;
    }

    function handleSubmit() {
        const message = content.value.trim();
        if (message) {
            if (isNamingTask) {
                submitTaskName(message);
            } else if (isSelectingProject) {
                submitProjectName(message);
            } else {
                submitRegularMessage(message);
            }
            clearInput();
            scrollChatToBottom();
        }
    }

    function submitTaskName(taskName) {
        addMessageToChatLog(`Task name: ${taskName}`, 'user');
        currentTaskName = taskName;
        isNamingTask = false;
        askForProjectName();
    }

    function submitProjectName(projectName) {
        addMessageToChatLog(`Project name: ${projectName}`, 'user');
        sendTaskDetailsToBackend(currentTaskName, projectName);
        isSelectingProject = false;
        addMessageToChatLog("Task processing in progress...!", 'agent');
    }

    function submitRegularMessage(message) {
        addMessageToChatLog(`${message}`, 'user');
        console.log(`Task Executing: ${message}`);

        fetch(`${window.location.origin}/home/process_input/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),
            },
            body: JSON.stringify({ 'user_input': message }),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            addMessageToChatLog(`Agent: ${data.result}`, 'agent');
            scrollChatToBottom();
        })
        .catch(error => {
            console.error('Error:', error);
            alert('There was a problem with your request.');
        });
    }

    function sendTaskDetailsToBackend(taskName, projectName) {
        const data = JSON.stringify({ 
            'task_name': taskName,
            'project_name': projectName
        });

        console.log('Sending data:', data); // Log the data being sent

        fetch('http://127.0.0.1:8000/home/save_task_to_project/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),
            },
            body: data,
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Task details saved:', data);
            addMessageToChatLog(`Task "${taskName}" saved to project "${projectName}"`, 'agent');
            scrollChatToBottom();
        })
        .catch(error => {
            console.error('Error saving task details:', error);
            addMessageToChatLog('Error saving task details. Please try again.', 'agent');
            scrollChatToBottom();
        });
    }
    
    function getCSRFToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]').value;
    }

    function handleKeyDown(event) {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            handleSubmit();
        }
    }

    function handleInput() {
        if (content.value.trim()) {
            submitButton.classList.add('active');
        } else {
            submitButton.classList.remove('active');
        }
    }

    function addMessageToChatLog(message, type) {
        const messageWrapper = document.createElement('div');
        messageWrapper.classList.add('message');

        if (type === 'user') {
            messageWrapper.classList.add('user-message');
        } else if (type === 'agent') {
            messageWrapper.classList.add('agent-message');
        }

        const messageElement = document.createElement('p');
        messageElement.textContent = message;

        messageWrapper.appendChild(messageElement);
        chatLog.appendChild(messageWrapper);
    }

    function clearInput() {
        content.value = '';
        submitButton.classList.remove('active');
    }

    function scrollChatToBottom() {
        chatLog.scrollTop = chatLog.scrollHeight;
    }

    async function handleButton1Click() {
        console.log('Button 1 clicked, redirecting to the projects page...');
        window.location.href = 'http://127.0.0.1:8000/home/';
    }

    async function handleButton2Click() {
        console.log('Button 2 clicked, redirecting to the projects page...');
        window.location.href = 'http://127.0.0.1:8000/projects/';
    }

    async function handleButton3Click() {
        console.log('Button 3 clicked, redirecting to another page...');
        window.location.href = 'http://127.0.0.1:8000/discover/'; 
    }

    async function handleButton4Click() {
        console.log('Button 4 clicked, redirecting to another page...');
        window.location.href = 'http://127.0.0.1:8000/settings/'; 
    }

    content.focus();
});