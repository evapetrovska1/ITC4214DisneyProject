$(document).ready(function() {
    // Call the function upon every page load to load placeholder message (if no items are added)
    checkIfEmpty();

    // -----------------------------------------
    // 1. REMOVE SINGLE ITEM FROM WISHLIST
    // -----------------------------------------
    $(document).on('click', '.wishlist-remove-btn', function(e) {
        e.preventDefault(); // Prevent default state

        // Declare the variables
        const $button = $(this);
        const productId = $button.data('product-id');
        const $card = $button.closest('.wishlist-item');

        // Animate the removal of the product card
        $card.fadeOut(300, function() {
            $(this).remove();
            updateWishlistStats();
            checkIfEmpty();
        });

        // Actually remove the product from the wishlist
        $.ajax({
            url: `/wishlist/remove/${productId}/`,
            method: 'POST',
            data: {
                csrfmiddlewaretoken: window.csrfToken || '{{ csrf_token }}'
            }
        });
    });



    // -----------------------------------------
    // 2. CLEAR ALL — SHOW MODAL MESSAGE
    // -----------------------------------------
    $('#clearWishlistBtn').on('click', function() {
        // Show the modal message
        $('#clearWishlistModal').modal('show');

    });



    // -----------------------------------------
    // 3. ACTUAL MODAL MESSAGE FUNCTIONALITY
    // -----------------------------------------
    $('#confirmClearBtn').on('click', function() {
        
        // Animate the removal of the items
        $('.wishlist-item').fadeOut(400, function() {
            $(this).remove();
            updateWishlistStats();
            checkIfEmpty();
        });

        // Actually remove all of the items with the ajax request
        $('.wishlist-item').each(function() {
            const productId = $(this).data('product-id');

            $.ajax({
                url: `/wishlist/remove/${productId}/`,
                method: 'POST',
                data: {
                    csrfmiddlewaretoken: window.csrfToken
                }
            });
        });

        // Hide the message
        $('#clearWishlistModal').modal('hide');
    });


    // -----------------------------------------
    // 4. HELPER FOR UPDATING COUNT + TOTAL
    // -----------------------------------------
    function updateWishlistStats() {
        const count = $('.wishlist-item').length;
        $('.text-muted.mb-3').html(`<i class="fas fa-gift me-1"></i> ${count} item${count !== 1 ? 's' : ''}`);
    }

    // -----------------------------------------
    // 5. IF NO ITEMS, SHOW PLACEHOLDER MESSAGE
    // -----------------------------------------
    function checkIfEmpty() {
        if ($('.wishlist-item').length === 0) {
            $('#wishlistContainer').html(`
                <div class="card shadow-sm border-0 p-3">
                    <div class="card-body text-center py-5">
                        <div class="empty-wishlist-icon mb-4">
                            <i class="far fa-heart fa-5x"></i>
                        </div>
                        <h4 class="mb-3">Your wishlist is empty</h4>
                        <p class="text-muted mb-4">Start adding items you love!</p>
                        <a href="/" class="btn button-general px-5">
                            <i class="fas fa-search me-2"></i>Browse Products
                        </a>
                    </div>
                </div>
            `);
        }
    }

    // -----------------------------------------------
    // 6. ADD TO CART BUTTON (SAME LIKE PRODUCT_LIST)
    // ------------------------------------------------
    $(document).on('click', '.add-to-cart-wishlist-btn', function(e) {
        e.preventDefault();

        // Declare the variables for the button, product id, and if it is added
        const $button = $(this);
        const productId = $button.data('product-id');
        const isAdded = $button.hasClass('btn-success');

        // Dynamic class switching for the UX
        if (isAdded) {
            $button.removeClass('btn-success').addClass('btn-primary');
            $button.html('<i class="fas fa-cart-plus me-1"></i> Add to Cart');
        } else {
            $button.removeClass('btn-primary').addClass('btn-success');
            $button.html('<i class="fas fa-check me-1"></i> Added!');
        }

        // CSRF Token Function
        function getCookie(name) {
            let cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                // Split the cookie into individual cookies
                const cookies = document.cookie.split(';');
                
                // Loop through the array of cookies
                for (let i = 0; i < cookies.length; i++) {
                    const cookie = cookies[i].trim();
                    
                    // Find the CSRF token cookie
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        // Decode and return the token value
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }

        // Get the csrf token from the cookie
        const csrfToken = getCookie('csrftoken');
        console.log('CSRF Token found:', csrfToken ? 'Yes' : 'No');


        // Determine which URL to call (if item is already added or not)
        const url = isAdded
            ? `/cart/remove/${productId}/`  // If already added, call remove URL
            : `/cart/add/${productId}/`;    // If not added, call add URL

        
        // Send the AJAX request without page reload
        $.ajax({
            url: url,
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken  // Include CSRF token in headers of POST request
            },
            data: {
                csrfmiddlewaretoken: csrfToken  // Also include in data for compatibility
            },
            success: function() {
                console.log('Cart updated!');
            },
            error: function(error) {
                // If AJAX request fails to go through, revert the button to original state
                if (isAdded) {
                    // Was removing but failed - show as still added
                    $button.removeClass('btn-primary').addClass('btn-success');
                    $button.html('<i class="fas fa-check me-1"></i> Added!');
                } else {
                    // Was adding but failed - show as not added
                    $button.removeClass('btn-success').addClass('btn-primary');
                    $button.html('<i class="fas fa-cart-plus me-1"></i> Add to Cart');
                }
                // Show error message to user
                alert('Something went wrong. Please try again.');
                console.error('Cart AJAX error ', error);
            }
        });

    });

});