$(document).ready(function() {
    $('.del-ex').click(function() {
        var exerciseId = $(this).data('exercise-id');
        $.ajax({
            url: '/delete_exercise/', 
            type: 'POST',
            data: {
                'exercise_id': exerciseId,
                'csrfmiddlewaretoken': '{{ csrf_token }}'
            },
            success: function(response) {
                if(response.success) {
                    window.location.reload(); 
                }
            }
        });
    });
});
