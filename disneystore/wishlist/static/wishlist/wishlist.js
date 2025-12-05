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
    // 3. HELPER FOR UPDATING COUNT + TOTAL
    // -----------------------------------------
    function updateWishlistStats() {
        const count = $('.wishlist-item').length;
        $('.text-muted.mb-3').html(`<i class="fas fa-gift me-1"></i> ${count} item${count !== 1 ? 's' : ''}`);
    }

    // -----------------------------------------
    // 4. IF NO ITEMS, SHOW PLACEHOLDER MESSAGE
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

});