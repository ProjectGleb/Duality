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

    function handleRecordButtonClick() {
        recordButton.classList.toggle('recording-active');
        
        if (recordButton.classList.contains('recording-active')) {
            recordText.textContent = 'Stop';
            addMessageToChatLog("Recording in progress", 'agent');
        } else {
            recordText.textContent = 'Record Task';
            addMessageToChatLog("Recording Stopped. \nWhat would you like to name the task?", 'agent');
        }
        
        scrollChatToBottom();
    }
    
    function getCSRFToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]').value;
    }

    async function handleSubmit() {
        const message = content.value.trim();
        if (message) {
            addMessageToChatLog(`${message}`, 'user');
            clearInput();
            scrollChatToBottom();
            console.log(`Task Executing: ${message}`);

            try {
                const response = await fetch('http://127.0.0.1:8000/home/process_input/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCSRFToken(),
                    },
                    body: JSON.stringify({ 'user_input': message }),
                });

                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }

                const data = await response.json();
                addMessageToChatLog(`Agent: ${data.result}`, 'agent');
                scrollChatToBottom();
            } catch (error) {
                console.error('Error:', error);
                alert('There was a problem with your request.');
            }
        }
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
