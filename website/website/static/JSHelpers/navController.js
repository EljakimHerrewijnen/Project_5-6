$(document).ready(function() {
    if (!localStorage.getItem("user")) {
        $('#logout-button').remove();
    } else {
        $('#logout-button').html("<li class='nav-item nav-right'>LOGOUT</li>");
    }
});