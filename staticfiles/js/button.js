
$(document).ready(function() {
    $('form').submit(function() {
        $(this).find(':button[type=submit]').prop('disabled', true);
        // For this example, don't actually submit the form
        event.preventDefault();
    });
});