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


});