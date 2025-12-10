$(document).ready(function() {

    // ----------------------------------------------------
    // 1. GET THE CSRF TOKEN FROM THE COOKIE (SAME AS PRODUCTS.JS)
    // ----------------------------------------------------
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

    const csrfToken = getCookie('csrftoken');
    console.log('CSRF TOken: ', csrfToken ? 'Found' : 'NOT FOUND');

    // ----------------------------------------------------
    // 2. SELECT ONE OF SAVED ADDRESSES
    // ----------------------------------------------------
    $(document).on('click', '.address-card', function(e) {
        e.preventDefault();

        console.log('=== ADDRESS CARD CLICKED ===');

        const $card = $(this);
        const addressId = $card.data('address-id');
        
        console.log("Address selected!");

        // Visual highlight
        $('.address-card').removeClass('selected');
        $('.check-icon').css('opacity', '0');
        $card.addClass('selected');
        $card.find('.check-icon').css('opacity', '1');

        // Send an AJAX request to the view
        $.ajax({
            url: '/cart/select_address/',
            method: 'POST',
            data: {
                address_id: addressId,  // Send as POST data
                csrfmiddlewaretoken: csrfToken
            },
            success: function(response) {
                if (response.success) {
                    console.log('Address selected:', response);
                    $('#continueToPayment').show();
                } else {
                    alert('Error: ' + response.message);
                    $card.removeClass('selected');
                    $card.find('.check-icon').css('opacity', '0');
                }
            },
            error: function() {
                alert('Error selecting address');
                $card.removeClass('selected');
                $card.find('.check-icon').css('opacity', '0');
            }
        });
    });

    // ----------------------------------------------------
    // 3. SUBMIT A NEW ADDRESS
    // ----------------------------------------------------
    $('#newAddressForm').on('submit', function(e) {
        e.preventDefault();

        // Send AJAX request
        $.ajax({
            url: $(this).attr('action'),
            method: 'POST',
            data: $(this).serialize(),
            headers: { 'X-CSRFToken': csrfToken },
            success: function(response) {
                if (response.success) {
                    const addr = response.address || response.address_data;

                    // Append the new card at the top of the page (for logged in users)
                    const newCard = `
                        <div class="card mb-3 address-card selected cursor-pointer" data-address-id="${addr.id || 'temp'}">
                            <div class="card-body d-flex justify-content-between align-items-center">
                                <div>
                                    <strong>${addr.full_name || addr.full_name}</strong>
                                    <p class="mb-0">${addr.street_address || addr.street_address}</p>
                                    <p class="mb-0">${addr.city || addr.city}, ${addr.state || addr.state || ''} ${addr.zip_code || addr.zip_code}</p>
                                    <p class="mb-0">${addr.country || addr.country}</p>
                                    <small class="text-muted">${addr.phone || addr.phone || 'No phone'}</small>
                                </div>
                                <i class="fas fa-check fa-2x text-success check-icon" style="opacity:1;"></i>
                            </div>
                        </div>`;

                    if ($('#saved-addresses').length === 0) {
                        $('.express-checkout').after('<h5 class="mt-4">Saved Addresses</h5><div id="saved-addresses"></div>');
                    }
                    $('#saved-addresses').prepend(newCard);
                    $('#newAddressForm')[0].reset();
                    $('#continueToPayment').show();
                }
            },
            error: function() {
                alert('Please fill all required fields');
            }
        });
    });

    // Show continue button if address already selected
    if ($('.address-card.selected').length > 0 || $('.address-card').length === 0 && $('#newAddressForm').length > 0) {
        $('#continueToPayment').show();
    }
});