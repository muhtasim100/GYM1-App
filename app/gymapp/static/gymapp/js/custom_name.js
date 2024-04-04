// JS for exercise form. Handling name and custom name.
$(document).ready(function(){
     // Hide custom name input and label to start with.
    $('#id_custom_name').hide();
    $('label[for="id_custom_name"]').hide();

    // change is the event listener that looks for the dropdown change.
    $('#id_name').change(function(){
        // Checks if other is selected from dropdown list.
        if($(this).val() == 'OT'){
            $('#id_custom_name').show(); // Show custom name input field and label.
            $('label[for="id_custom_name"]').show();

        } else {
            $('#id_custom_name').hide().val(''); // Hide custom name input and makes the input an empty string.
            $('label[for="id_custom_name"]').hide(); // Hides the label.

        }
    });
});
