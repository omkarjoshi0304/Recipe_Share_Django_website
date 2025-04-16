document.getElementById('contactForm').addEventListener('submit', async function (e) {
    e.preventDefault();
    
    // Show loading message
    document.getElementById('responseMessage').innerText = 'Sending...';
    document.getElementById('responseMessage').style.color = 'blue';
    
    const form = e.target;
    const formData = new FormData(form);
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
    try {
        const response = await fetch("/contact/ajax/", {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'X-Requested-With': 'XMLHttpRequest',  // Indicate AJAX request
                'Accept': 'application/json'          // Request JSON response
            },
            body: formData
        });
        
        if (response.headers.get('content-type')?.includes('application/json')) {
            const data = await response.json();
            const msgDiv = document.getElementById('responseMessage');
            msgDiv.innerText = data.message || 'Message sent successfully';
            msgDiv.style.color = data.success ? 'green' : 'red';
            if (data.success) {
                form.reset();
            }
        } else {
            // Not JSON response
            const responseText = await response.text();
            console.log("Non-JSON response:", responseText);
            document.getElementById('responseMessage').innerText = 'Server returned an invalid response format';
            document.getElementById('responseMessage').style.color = 'red';
        }
    } catch (error) {
        console.error('Error submitting contact form:', error);
        document.getElementById('responseMessage').innerText = 'An error occurred. Try again later.';
        document.getElementById('responseMessage').style.color = 'red';
    }
});