"use strict";

// Class Definition
var KTLoginGeneral = function() {

    var login = $('#kt_login');

    var showErrorMsg = function(form, type, msg) {
        var alert = $('<div class="kt-alert kt-alert--outline alert alert-' + type + ' alert-dismissible" role="alert">\
			<button type="button" class="close" data-dismiss="alert" aria-label="Close"></button>\
			<span></span>\
		</div>');

        form.find('.alert').remove();
        alert.prependTo(form);
        //alert.animateClass('fadeIn animated');
        KTUtil.animateClass(alert[0], 'fadeIn animated');
        alert.find('span').html(msg);
    }


    var handleSignInFormSubmit = function() {
        $('#kt_login_signin_submit').click(function(e) {
            e.preventDefault();
            var btn = $(this);
            var form = $(this).closest('form');           

            form.validate({
                rules: {
                    email: {
                        required: true,
                        email: true
                    },
                    password: {
                        required: true
                    }
                }
            });

            if (!form.valid()) {
                return;
            }

            btn.addClass('kt-spinner kt-spinner--right kt-spinner--sm kt-spinner--light').attr('disabled', true);

            var email_f = $("#email_f").val();
            var password_f = $("#password_f").val();

           
            $.ajax({ type: "POST",
				url: "/login/loginCheck",
				data: { email_f : email_f, password_f : password_f },
				//async: false,
				success : function(response){ 
                   
                    if(response == "success"){
                        window.location.replace("/a/dashboard");
                    }else{
                        setTimeout(function() {
                            btn.removeClass('kt-spinner kt-spinner--right kt-spinner--sm kt-spinner--light').attr('disabled', false);
                            showErrorMsg(form, 'danger', 'Incorrect username or password. Please try again.');
                        }, 1000);
                    }
                  

                }
			});
           

        });
    }



    return {
    
        init: function() {

            handleSignInFormSubmit();

        }
    };
}();

// Class Initialization
jQuery(document).ready(function() {
   // KTLoginGeneral.init();
});