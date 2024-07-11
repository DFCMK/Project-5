document.addEventListener('DOMContentLoaded', function() {
    const stars = document.querySelectorAll('.rating-stars input[type="radio"]');
    const modalStars = document.querySelectorAll('.modal .rating-stars input[type="radio"]');
    const ratingValue = document.getElementById('modal-rating-value');
    const reviewForm = document.getElementById('reviewForm');
    const customerReviews = document.getElementById('customerReviews');

    function setSelectedRating(stars, value) {
        stars.forEach(star => {
            star.checked = (star.value === value);
        });
    }

    stars.forEach(star => {
        star.addEventListener('click', function() {
            const value = this.value;
            ratingValue.value = value;
            setSelectedRating(modalStars, value);
            $('#reviewModal').modal('show');
        });
    });

    reviewForm.addEventListener('submit', function(event) {
        event.preventDefault();
        console.log("Form submitted");

        var formData = new FormData(reviewForm);
        $.ajax({
            type: 'POST',
            url: reviewForm.action,
            data: formData,
            contentType: false,
            processData: false,
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
                console.log("Before send:", xhr, settings);
                // If using Django, add the CSRF token
                xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
            },
            success: function(response) {
                console.log("Success:", response);

                if (response.reviews_html) {
                    customerReviews.innerHTML = response.reviews_html;
                } else {
                    console.error("Unexpected response format:", response);
                }

                $('#reviewModal').modal('hide');
            },
            error: function(xhr, status, error) {
                console.error('AJAX Error:', error);
            }
        });
    });

    function loadReviews(productId) {
        $.ajax({
            type: 'GET',
            url: '/path/to/review_list/' + productId + '/',
            success: function(data) {
                $('#reviewsContainer').html(data);
            },
            error: function(xhr, status, error) {
                console.error('Error loading reviews:', error);
            }
        });
    }

    // Function to get CSRF token if using Django
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
});