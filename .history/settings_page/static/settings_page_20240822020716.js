document.addEventListener('DOMContentLoaded', function() {
    const editButtons = document.querySelectorAll('.edit-button');
    const logoutButton = document.querySelector('.settings-button:not(.danger)');
    const deleteAccountButton = document.querySelector('.settings-button.danger');
    const faqItems = document.querySelectorAll('.faq-item');
    const button1 = document.getElementById('button1');
    const button2 = document.getElementById('button2');
    const button3 = document.getElementById('button3');
    const button4 = document.getElementById('button4');

    // Add click event listeners to edit buttons
    editButtons.forEach(button => {
        button.addEventListener('click', handleEdit);
    });

    // Add click event listeners to logout and delete account buttons
    logoutButton.addEventListener('click', handleLogout);
    deleteAccountButton.addEventListener('click', handleDeleteAccount);

    // Add click event listeners to FAQ items
    faqItems.forEach(item => {
        item.addEventListener('click', toggleFAQ);
    });

    // Add click event listeners to sidebar buttons
    button1.addEventListener('click', handleButton1Click);
    button2.addEventListener('click', handleButton2Click);
    button3.addEventListener('click', handleButton3Click);
    button4.addEventListener('click', handleButton4Click);

    function handleEdit(event) {
        const field = event.target.previousElementSibling;
        const currentValue = field.textContent;
        const newValue = prompt(`Edit ${field.id}:`, currentValue);
        if (newValue !== null && newValue !== "") {
            field.textContent = newValue;
            // Here you would typically send an update request to your server
            console.log(`Updated ${field.id} to: ${newValue}`);
        }
    }

    function handleLogout() {
        console.log('Logout clicked');
        // Implement logout logic here
    }

    function handleDeleteAccount() {
        if (confirm('Are you sure you want to delete your account? This action cannot be undone.')) {
            console.log('Delete account confirmed');
            // Implement account deletion logic here
        }
    }

    function toggleFAQ(event) {
        const item = event.currentTarget;
        const answer = item.querySelector('.faq-answer');
        const icon = item.querySelector('.faq-icon');

        answer.classList.toggle('show');
        icon.textContent = answer.classList.contains('show') ? '−' : '+';
    }

    function handleButton1Click() {
        console.log('Button 1 clicked, redirecting to the projects page...');
        window.location.href = `${window.location.origin}/home/`;
    }
    function handleButton2Click() {
        console.log('Button 2 clicked, redirecting to the projects page...');
        window.location.href = 'http://127.0.0.1:8000/projects/`;
    }

    function handleButton3Click() {
        console.log('Button 3 clicked, redirecting to another page...');
        window.location.href = 'http://127.0.0.1:8000/discover/';
    }
    function handleButton4Click() {
        console.log('Button 4 clicked, redirecting to another page...');
        window.location.href = 'http://127.0.0.1:8000/settings/';
    }
});