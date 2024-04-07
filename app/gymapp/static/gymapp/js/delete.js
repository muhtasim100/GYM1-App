document.getElementById('toggle-delete').addEventListener('click', function() {
    
    var checkboxes = document.querySelectorAll('.checkbox-column');
    function toggleVisibility(element) {
        if (element.style.display === 'none') {
            element.style.display = 'table-cell';
        } else {
            element.style.display = 'none';
        }
    }
    
    document.getElementById('toggle-delete').addEventListener('click', function() {
        var checkboxes = document.querySelectorAll('.checkbox-column');
        checkboxes.forEach(toggleVisibility);
    });
    
});


