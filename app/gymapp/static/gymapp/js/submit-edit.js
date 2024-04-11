document.getElementById('btn').addEventListener('click', function(event) {
    event.preventDefault(); // StopS the form from submitting immediately which was a reoccuring problem.
    var button = this;
    
    button.classList.add('start-spin');

    // Waits for the animation to finish before submitting the form.
    setTimeout(function() {
        document.getElementById('DetailsForm').submit();
    }, 2600); 
});