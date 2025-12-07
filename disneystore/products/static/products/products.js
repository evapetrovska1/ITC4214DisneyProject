$(document).ready(function() {

    // Variable declarations (storing the current selected category, color, min price, and max price)
    let selectedCategory = $('#categoryInput').val() || '';
    let selectedColor = $('#colorInput').val() || '';
    let minPrice = $('#minPriceSlider').val() || 0; // Default to 0 if nothing is selected
    let maxPrice = $('#maxPriceSlider').val() || 100; // Default to 100 if nothing is selected

    // Restore active state when page loads (after applying filters)
    if (selectedCategory) {
        $(`.category-link[data-category="${selectedCategory}"]`).addClass('active');
    }
    if (selectedColor) {
        $(`.color-link[data-color="${selectedColor}"]`).addClass('active');
    }

    // --------------------------------
    // 1. PRICE SILDER FUNCTIONALITY
    // --------------------------------

    $('#minPriceSlider').on('input', function() {
        // Update the value displayed next to minimum price
        $('#minPriceValue').text($(this).val())

        // Store the new value in variable
        minPrice = $(this).val();
    });

    $('#maxPriceSlider').on('input', function() {
        // Update the value displayed next to maximum price
        $('#maxPriceValue').text($(this).val())

        // Store the new value in variable
        maxPrice = $(this).val();
    });


    // --------------------------------
    // 2. CATEGORY SELECTION FUNCTIONALITY
    // --------------------------------

    $('.category-link').click(function(e) {
        // Prevent the default link
        e.preventDefault();

        // Get the category ID from the clicked link
        const categoryId = $(this).data('category').toString();

        // Check if the category is already selected
        if (selectedCategory === categoryId) {

            selectedCategory = ''; // Clear the selection

            $(this).removeClass('active');
        } else {

            // If category is not selected, select it now
            selectedCategory = categoryId;
            $('.category-link').removeClass('active'); // Remove the active class from all categories (ensuring one category can be selected at a time)
            
            // Activate the category
            $(this).addClass('active');
        }
    });


    // --------------------------------
    // 3. COLOR SELECTION FUNCTIONALITY
    // --------------------------------

    $('.color-link').click(function(e) {
        // Prevent the default again
        e.preventDefault();

        // Get the color ID from the clicked link
        const colorId = $(this).data('color').toString();

        // Check if the color is already selected
        if (selectedColor === colorId) {

            selectedColor = ''; // Clear the selection

            $(this).removeClass('active');
        } else {

            // If color is not selected, select it now
            selectedColor = colorId;
            $('.color-link').removeClass('active'); // Remove the active class from all categories (ensuring one category can be selected at a time)
            
            // Activate the color
            $(this).addClass('active');
        }
    });


    // --------------------------------
    // 4. APPLY FILTERS BUTTON
    // --------------------------------

    $('#applyFiltersBtn').on('click', function(e) {
        e.preventDefault();

        // Update the hidden inputs with the current selections
        $('#categoryInput').val(selectedCategory);
        $('#colorInput').val(selectedColor);
        $('#minPriceInput').val(minPrice);
        $('#maxPriceInput').val(maxPrice);

        $('#filterForm')[0].submit(); // Submit everything
    });


    // ----------------------------------------------------
    // 5. REMOVING INDIVIDUAL FILTERS (IN FILTERS DISPLAY)
    // ----------------------------------------------------
    $(document).on('click', '.remove-filter', function(e) {
        // Prevent default
        e.preventDefault();
        
        // Get which type of filter to remove from data-filter attribute
        const filterType = $(this).data('filter');
    
        // If statements for the filter type
        if (filterType === 'category') {
            selectedCategory = '';

            // Remove category filter
            $('#categoryInput').val('');
            $('.category-link').removeClass('active');

        } else if (filterType === 'color') {
            selectedColor = '';

            // Remove color filter
            $('#colorInput').val('');
            $('.color-link').removeClass('active');
            
        } else if (filterType === 'price') {
            minPrice = 0;
            maxPrice = 100;

            // Remove price filters
            $('#minPriceInput').val('');
            $('#maxPriceInput').val('');
            $('#minPriceSlider').val(0);
            $('#maxPriceSlider').val(100);
            $('#minPriceValue').text('0');
            $('#maxPriceValue').text('100');
        }

        // Submit the form to apply changes immediately
        $('#filterForm')[0].submit();
    });


    

    // ----------------------------------------------------
    // 6. ADDING TO/REMOVING FROM WISHLIST
    // ----------------------------------------------------
    $(document).on('click','.wishlist-toggle-heart', function (e) {
        e.preventDefault(); // Prevent the default state

        // Declare the variables for the button, product id, and if it is added already
        const $button = $(this);
        const productId = $button.data('product-id');
        const isAdded = $button.hasClass('btn-danger');

        // Dynamic class switching for the UX
        if (isAdded) {
            $button.removeClass('btn-danger').addClass('btn-outline-danger');
            $button.find('i').removeClass('fas').addClass('far');
        } else {
            $button.removeClass('btn-outline-danger').addClass('btn-danger');
            $button.find('i').removeClass('far').addClass('fas');
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
            ? `/wishlist/remove/${productId}/`  // If already added, call remove URL
            : `/wishlist/add/${productId}/`;    // If not added, call add URL

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
                console.log('Wishlist updated!');
            },
            error: function(error) {
                // If AJAX request fails to go through, revert the button to original state
                if (isAdded) {
                    $button.removeClass('btn-outline-danger').addClass('btn-danger');
                    $button.find('i').removeClass('far').addClass('fas');
                } else {
                    $button.removeClass('btn-danger').addClass('btn-outline-danger');
                    $button.find('i').removeClass('fas').addClass('far');
                }
                // Show error message to user
                alert('Something went wrong. Please try again.');
                console.error('Wishlist AJAX error ', error);
            }
        });
       
    });

    // ----------------------------------------------------
    // 7. ADDING TO/REMOVING FROM SHOPPING CART
    // ----------------------------------------------------
    $(document).on('click', '.add-to-cart-btn', function(e) {
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