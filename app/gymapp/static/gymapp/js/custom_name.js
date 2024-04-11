$(document).ready(function() {
    // Hide custom_name input and label.
    $('#id_custom_name').addClass('hidden');
    $('label[for="id_custom_name"]').addClass('hidden'); 

    // Visibility of custom_name.
    function toggleCustomNameVisibility() {
        if ($('#id_name').val() == 'OT') {
            // Used fadeIn for animation if 'Other' is selected.
            $('#id_custom_name').hide().removeClass('hidden').fadeIn(300);
            $('label[for="id_custom_name"]').hide().removeClass('hidden').fadeIn(300);
        } 
        else {
            // Hide and clear custom_name if it's not 'Other'.
            $('#id_custom_name').fadeOut(300, function() {
                $(this).addClass('hidden').val('');
            });
            $('label[for="id_custom_name"]').fadeOut(300, function() {
                $(this).addClass('hidden');
            });
        }
    }
    toggleCustomNameVisibility(); 
    $('#id_name').change(toggleCustomNameVisibility);
});
