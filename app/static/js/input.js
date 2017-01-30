function setupTextfields() {
    var inputFields = $('.md-input-field');
    $.each(inputFields, addListenerToTextfield);
}

function addListenerToTextfield() {
    var field = $(this);
    var input = field.find('input');
    field.unbind("focusin");
    field.unbind("focusout");
    field.focusin(function() {
        field.addClass('active');
        field.addClass('filled');
    });

    field.focusout(function(){
        if (!input.val())
            field.removeClass('filled');
        field.removeClass('active');
        verifyInput(field, input);
    });
}

function verifyInput(field, input) {
    var value = input.val();
    var verificationRegex = input.attr('verification');
    var re = new RegExp("^" + verificationRegex + "$");
    var isRequired = input.is(':required');
    if ((verificationRegex && !re.test(value)) || (isRequired && !value)) {    
        field.addClass('error');
    } else {
        field.removeClass('error');
    }
}