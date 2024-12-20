document.addEventListener("DOMContentLoaded", function() {
    const addToCartButtons = document.querySelectorAll('.add-to-cart-btn');

    addToCartButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault(); // Prevent the default form submission
            const form = this.closest('form');
            const foodId = form.action.split('/').slice(-2, -1)[0]; // Get food ID from the URL
            const foodName = form.querySelector('input[name="food_name"]').value; // Get food name from hidden input

            console.log("Adding to cart:", foodName); // Debugging line

            fetch(form.action, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken') // Get CSRF token
                },
                body: new URLSearchParams(new FormData(form))
            })
            .then(response => {
                if (response.ok) {
                    alertify.notify(foodName + " has been added to your cart!", "success", 5);
                    updateCartCount(); // Call function to update cart count
                } else {
                    alert('Failed to add item to cart.');
                }
            });
        });
    });

    // Function to get CSRF token for AJAX
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Function to update the cart count
    function updateCartCount() {
        fetch('/cart/count/')
            .then(response => response.json())
            .then(data => {
                document.getElementById('cart-item-count').innerText = data.count; // Update cart count
            });
    }
});