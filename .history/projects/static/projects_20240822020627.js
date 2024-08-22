document.addEventListener('DOMContentLoaded', function() {
    const button1 = document.getElementById('button1');
    const button2 = document.getElementById('button2');
    const button3 = document.getElementById('button3');
    const button4 = document.getElementById('button4');
    const projectsTable = document.getElementById('projectsTable');
    const tasksTable = document.getElementById('tasksTable');
    const tableTitle = document.getElementById('tableTitle');

    button1.addEventListener('click', handleButton1Click);
    button2.addEventListener('click', handleButton2Click);
    button3.addEventListener('click', handleButton3Click);
    button4.addEventListener('click', handleButton4Click);

    // Add event listeners for project rows
    const projectRows = document.querySelectorAll('.project-row');
    projectRows.forEach(row => {
        row.addEventListener('click', handleProjectClick);
    });

    // Add event listeners for edit, delete, and run buttons
    const editButtons = document.querySelectorAll('.edit-btn');
    const deleteButtons = document.querySelectorAll('.delete-btn');
    const runButtons = document.querySelectorAll('.run-btn');
    editButtons.forEach(button => button.addEventListener('click', handleEditClick));
    deleteButtons.forEach(button => button.addEventListener('click', handleDeleteClick));
    runButtons.forEach(button => button.addEventListener('click', handleRunClick));

    tasksTable.addEventListener('click', function(event) {
        if (event.target.classList.contains('run-btn')) {
            handleRunClick(event);
        }
    });

    function handleProjectClick(event) {
        if (event.target.classList.contains('edit-btn') || event.target.classList.contains('delete-btn') || event.target.classList.contains('run-btn')) {
            return; // Don't trigger row click for edit, delete, and run buttons
        }
        const projectId = event.currentTarget.getAttribute('data-project-id');
        const projectName = event.currentTarget.querySelector('.project-name').textContent;
        console.log(`Project ${projectId} clicked. Showing tasks for ${projectName}.`);
        projectsTable.style.display = 'none';
        tasksTable.style.display = 'table';
        tableTitle.textContent = projectName;
        tableTitle.classList.add('clickable-title');
        tableTitle.addEventListener('click', showProjects);
        
        // Fetch tasks for the selected project
        fetch(`/projects/tasks/${projectId}/`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(tasks => {
                console.log('Received tasks:', tasks);
                const tasksTableBody = tasksTable.querySelector('tbody');
                tasksTableBody.innerHTML = '';
                if (tasks.length === 0) {
                    tasksTableBody.innerHTML = '<tr><td colspan="5">No tasks found for this project.</td></tr>';
                } else {
                    tasks.forEach(task => {
                        const row = `
                            <tr class="expandable-row">
                                <td>${task.name}</td>
                                <td>${task.description || 'N/A'}</td>
                                <td>${task.steps ? JSON.stringify(task.steps) : 'N/A'}</td>
                                <td>${task.success_rate !== null ? task.success_rate + '%' : 'N/A'}</td>
                                <td>
                                    <button class="run-btn">Run</button>
                                    <button class="edit-btn">Edit</button>
                                    <button class="delete-btn">Delete</button>
                                </td>
                            </tr>
                        `;
                        tasksTableBody.insertAdjacentHTML('beforeend', row);
                    });
                }
                addExpandableRowListeners();
            })
            .catch(error => {
                console.error('Error fetching tasks:', error);
                const tasksTableBody = tasksTable.querySelector('tbody');
                tasksTableBody.innerHTML = '<tr><td colspan="5">Error loading tasks. Please try again.</td></tr>';
            });
    }

    function showProjects() {
        projectsTable.style.display = 'table';
        tasksTable.style.display = 'none';
        tableTitle.textContent = 'Projects';
        tableTitle.classList.remove('clickable-title');
        tableTitle.removeEventListener('click', showProjects);
    }

    function handleEditClick(event) {
        const projectName = event.target.closest('tr').querySelector('.project-name').textContent;
        console.log(`Edit clicked for project: ${projectName}`);
        // Implement edit functionality
    }

    function handleDeleteClick(event) {
        const projectName = event.target.closest('tr').querySelector('.project-name').textContent;
        console.log(`Delete clicked for project: ${projectName}`);
        // Implement delete functionality
    }

    function handleRunClick(event) {
        const taskName = event.target.closest('tr').querySelector('td:first-child').textContent;
        console.log(`Run clicked for task: ${taskName}`);
        incrementExecutionCount(taskName);
        alert(`Running task: ${taskName}`);
    }

    async function handleButton1Click() {
        console.log('Button 1 clicked, redirecting to the home page...');
        window.location.href = `${window.location.origin}/home/`;
    }

    async function handleButton2Click() {
        console.log('Button 2 clicked, redirecting to the projects page...');
        window.location.href = `${window.location.origin}/projects/`;
    }

    async function handleButton3Click() {
        console.log('Button 3 clicked, redirecting to the discover page...');
        window.location.href = 'http://127.0.0.1:8000/discover/`; 
    }

    async function handleButton4Click() {
        console.log('Button 4 clicked, redirecting to the settings page...');
        window.location.href = 'http://127.0.0.1:8000/settings/'; 
    }

    function addExpandableRowListeners() {
        const expandableRows = document.querySelectorAll('.expandable-row');
        expandableRows.forEach(row => {
            row.addEventListener('click', function() {
                this.classList.toggle('expanded');
            });
        });
    }
});