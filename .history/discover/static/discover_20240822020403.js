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

    // Add event listeners for project names
    const projectNames = document.querySelectorAll('.project-name');
    projectNames.forEach(projectName => {
        projectName.addEventListener('click', handleProjectClick);
    });

    // Add event listeners for edit and delete buttons
    const editButtons = document.querySelectorAll('.edit-btn');
    const deleteButtons = document.querySelectorAll('.delete-btn');
    editButtons.forEach(button => button.addEventListener('click', handleEditClick));
    deleteButtons.forEach(button => button.addEventListener('click', handleDeleteClick));

    function handleProjectClick(event) {
        event.preventDefault();
        const projectId = event.target.getAttribute('data-project-id');
        console.log(`Project ${projectId} clicked. Showing tasks.`);
        projectsTable.style.display = 'none';
        tasksTable.style.display = 'table';
        tableTitle.textContent = 'Tasks';
        tableTitle.classList.add('clickable-title');
        tableTitle.addEventListener('click', showProjects);
        // Here you would typically load tasks for the selected project
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
        window.location.href = 'http://127.0.0.1:8000/discover/; 
    }

    async function handleButton4Click() {
        console.log('Button 4 clicked, redirecting to the settings page...');
        window.location.href = 'http://127.0.0.1:8000/settings/'; 
    }
});