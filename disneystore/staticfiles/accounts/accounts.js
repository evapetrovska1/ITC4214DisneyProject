$(document).ready(function() {

    // Profile Save Confirmation Pop-Up
    $('#confirmSaveBtn').on('click', function(e) {
        e.preventDefault();  // Prevent immediate submit

        // Create the pop up (used some formatting from midterm assignment)
        const popup = `
            <div class="profile-popup-overlay">
                <div class="profile-popup">
                    <div class="profile-popup-header">
                        <h3>Confirm Changes</h3>
                        <button class="popup-close button-general">&times;</button>
                    </div>
                    <div class="profile-popup-content">
                        <div class="popup-details">
                            <p>Are you sure you want to save your profile changes?</p>
                            <p class="text-muted">This will update your first name and/or last name permanently.</p>
                        </div>
                        <p class="popup-thankyou">Thanks for keeping your account up to date!</p>
                    </div>
                    <div class="profile-popup-footer">
                        <button class="btn button-general popup-cancel">Cancel</button>
                        <button class="btn button-general popup-ok">Yes, Save Changes</button>
                    </div>
                </div>
            </div>
        `;

        // Append the pop-up to the body
        $('body').append(popup);

        // Close pop-up events
        $('.popup-close, .popup-cancel, .profile-popup-overlay').on('click', function() {
            $('.profile-popup-overlay').remove();
        });

        // Prevent closing when clicking inside pop-up
        $('.profile-popup').on('click', function(e) {
            e.stopPropagation();
        });

        // When user clicks the "Yes, Save Changes" button
        $('.popup-ok').on('click', function() {
            $('#profileForm').submit();  // Submit the form
            $('.profile-popup-overlay').remove();  // Remove pop-up
        });
    });
});