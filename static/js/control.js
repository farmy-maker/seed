$(document).ready(function() {
    var csrf_token = "{{ csrf_token() }}";
    $('.control-btn').click(function (event){
        $.ajax({
           url: "/control/",
           type: "POST",
           contentType: "application/json",
           headers: {
              "X-CSRFToken": csrf_token
           },
           data: JSON.stringify({
             "controller_type": $(this).data("type"),
             "action_type": $(this).data("action-type"),
             "token": $(this).data("token")
           }),
        })
    });
});
