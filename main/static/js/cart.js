// Function to get CSRF token for AJAX
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Check if this cookie string begins with the name we want
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


document.querySelectorAll('.star-rating input').forEach((input) => {
    input.addEventListener('change', function() {
        const foodId = this.name.split('-')[1];  // Extract food ID from the name attribute
        const rating = this.value;

        fetch(`/rate-food/${foodId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),  // Assuming you have a function to get CSRF token
            },
            body: JSON.stringify({ rating: rating }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Rating submitted successfully!');
            } else {
                alert('Error submitting rating: ' + data.error);
            }
        });
    });
});

// Function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Check if this cookie string begins with the name we want
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}