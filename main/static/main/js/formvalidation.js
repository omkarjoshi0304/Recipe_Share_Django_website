function validateRecipeForm(event) {
    event.preventDefault();
    clearErrors();
    let isValid = true;

    const fields = [
        { id: 'recipeName', rules: { required: true } },
        { id: 'authorEmail', rules: { required: true, email: true } },
        { id: 'ingredients', rules: { required: true, minLength: 10 } }
    ];

    fields.forEach(({ id, rules }) => {
        const field = document.getElementById(id);
        const value = field.value.trim();
        
        if (rules.required && !value) {
            showError(`${field.labels[0].textContent} is required`, field);
            isValid = false;
        }
        
        if (rules.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
            showError('Invalid email format', field);
            isValid = false;
        }
    });

    if (isValid) {
        const formData = {
            recipeName: document.getElementById('recipeName').value,
            authorEmail: document.getElementById('authorEmail').value,
            ingredients: document.getElementById('ingredients').value,
            timestamp: new Date().toISOString()
        };

        const submissions = JSON.parse(localStorage.getItem('recipeSubmissions')) || [];
        submissions.push(formData);
        localStorage.setItem('recipeSubmissions', JSON.stringify(submissions));
        
        window.location.href = './submissions.html';
    }
}

function showError(message, field) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;
    field.parentNode.appendChild(errorDiv);
}

function clearErrors() {
    document.querySelectorAll('.error-message').forEach(el => el.remove());
}