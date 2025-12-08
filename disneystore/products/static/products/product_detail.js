$(document).ready(function() {
    // ----------------------------------------------------
    // 1. STAR RATING
    // ----------------------------------------------------
    console.log("Star rating script loaded");
    
    // Use event delegation for dynamically loaded elements
    $(document).on('click', '.rating-star', function() {
        console.log("Star clicked!");
        
        const star = $(this);
        const value = star.data('value');
        const productId = star.closest('.star-rating').data('product-id');
        const csrfToken = $('[name=csrfmiddlewaretoken]').val();
        
        console.log("Value:", value, "Product ID:", productId);
        
        // Update stars UI
        star.parent().find('.rating-star').each(function() {
            if ($(this).data('value') <= value) {
                $(this).removeClass('far').addClass('fas text-warning');
            } else {
                $(this).removeClass('fas text-warning').addClass('far');
            }
        });
        
        // Show loading
        $('#rating-message').text('Saving...');
        
        // Send rating to server
        $.ajax({
            url: '/rate/',
            method: 'POST',
            data: {
                product_id: productId,
                stars: value,
                csrfmiddlewaretoken: csrfToken
            },
            success: function(data) {
                console.log("AJAX response:", data);
                if (data.success) {
                    $('#avg-rating').text(data.average);
                    $('#rating-message').text('Rating saved!');
                } else {
                    $('#rating-message').text('Error: ' + data.error);
                }
            },
            error: function(xhr, status, error) {
                console.log("AJAX error:", error);
                $('#rating-message').text('Error saving rating');
            }
        });
    });
});
