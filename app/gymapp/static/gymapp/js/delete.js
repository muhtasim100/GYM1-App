document.getElementById('toggle-delete').addEventListener('click', function() {
    var checkboxColumns = document.querySelectorAll('.checkbox-column');
    checkboxColumns.forEach(function(column) {
        if (column.style.display === 'none') {
            column.style.display = 'table-cell';
        } 
        else {
            column.style.display = 'none';
        }
    });

    // Add change event listeners to checkboxes only once, not every time the delete button is clicked.
    var checkboxes = document.querySelectorAll('.checkbox-column input[type="checkbox"]');
    checkboxes.forEach(function(checkbox) {
        checkbox.onchange = checkbox.onchange || function() { // Prevent adding multiple listeners to the same checkbox.
            // OR operator used to call function if checkbox.onchange false.
            // When the checkbox state changes, toggle the 'selected-row' class.
            if (checkbox.checked) {
                checkbox.closest('tr').classList.add('selected-row');
            } 
            
            else {
                checkbox.closest('tr').classList.remove('selected-row');
            }
        };
    });
});
