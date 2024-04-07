document.addEventListener('DOMContentLoaded', function() {
    var toggleDeleteBtn = document.getElementById('toggle-delete');
    var confirmDeleteBtn = document.getElementById('confirm-delete');
    var checkboxes = document.querySelectorAll('.checkbox-column input[type="checkbox"]');
    var checkboxColumns = document.querySelectorAll('.checkbox-column');

    function updateDelButton() {
        // Checks if any checkbox is checked.
        var isAnyCheckboxChecked = Array.from(checkboxes).some(checkbox => checkbox.checked);

        if (isAnyCheckboxChecked) {
            confirmDeleteBtn.style.display = 'inline-block';
        } 
        
        else {
            confirmDeleteBtn.style.display = 'none';
        }
    }

    toggleDeleteBtn.addEventListener('click', function() {
        // Checks if any checkbox columns are visible by checking none have their display style set to 'none'.
        var isAnyCheckboxVisible = Array.from(checkboxColumns).some(column => 
            column.style.display !== 'none');

        if (isAnyCheckboxVisible) {
            // Hide checkboxes and reset them.
            checkboxColumns.forEach(column => column.style.display = 'none');
            checkboxes.forEach(checkbox => {
                checkbox.checked = false;
                checkbox.closest('tr').classList.remove('selected-row');
            });
            confirmDeleteBtn.style.display = 'none';
        } 
        else {
            // Show the checkoxes.
            checkboxColumns.forEach(column => column.style.display = 'table-cell');
        }
        updateDelButton();
    });
    
    checkboxes.forEach(function(checkbox) {
        checkbox.addEventListener('change', function() {
            var row = checkbox.closest('tr');

            if (checkbox.checked) {
                row.classList.add('selected-row');
            } 
            else {
                row.classList.remove('selected-row');
            }
            updateDelButton();
        });
    });

    confirmDeleteBtn.addEventListener('click', function(event) {
        event.preventDefault(); // Prevents form from submitting immediately.
        if (confirm('Are you sure you want to delete?')) {
            document.getElementById('delete-form').submit();
        }
    });
});
