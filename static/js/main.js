var mainjs = {

    validateEmail: function (email) {
        var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        return re.test(email);
    },

	saveSettings:function(){

        let memberName = $("#memberName").val();
        let memberSurName = $("#memberSurName").val();
        let memberEmail = $("#memberEmail").val();
        let memberPhone = $("#memberPhone").val();
        let memberCompanyName = $("#memberCompanyName").val();

        var onay = 1;
        var metin = "";

    
        if (memberName < 1) {
            onay = 0;
            metin = metin + "\nPlease enter your name!";
        }
        if (memberSurName < 1) {
            onay = 0;
            metin = metin + "\nPlease enter your last name!";
        }
        if (this.validateEmail(memberEmail) === false) {
            onay = 0;
            metin = metin + "\nPlease enter a valid email address!";
        }

        if (onay == 0) {
            swal.fire(metin); 
        }else{
            

            $.ajax({ 
                type: "POST",
                url: "/a/ax/saveSettings",
                data: { memberName : memberName, memberSurName: memberSurName, memberEmail: memberEmail,memberPhone : memberPhone, memberCompanyName: memberCompanyName    },
                //async: false,
                success : function(response){ 
                    
                    if(response == "success"){
                        location.reload();
                    }else{
                        alert("An unknown error occured, please try again!");
                    }
                
                }
            });


        }
       
       
       
			

    },
    
    savePassword: function(){

        let oldPass = $("#oldPass").val();
        let newPass1 = $("#newPass1").val();
        let newPass2 = $("#newPass2").val();

        var onay = 1;
        var metin = "";

    
        if (oldPass < 8) {
            onay = 0;
            metin = metin + "\nPlease enter your current password!";
        }
        if (newPass1 < 8 || newPass2 < 8) {
            onay = 0;
            metin = metin + "\nPassword must be at least 8-characters!";
        }

        if (newPass1 !== newPass2) {
            onay = 0;
            metin = metin + "\nNew passwords must match!";
        }

        if (onay == 0) {
            swal.fire(metin); 
        }else{
            

            $.ajax({ 
                type: "POST",
                url: "/a/ax/savePassword",
                data: { oldPass : oldPass, newPass1: newPass1, newPass2: newPass2   },
                //async: false,
                success : function(response){ 
                   
                    if(response == "success"){
                        swal.fire({
                            title: "Done!",
                            text: "Password changed succesfully.",
                            type: "success",
                            buttonsStyling: false,
                            confirmButtonText: "OK",
                            confirmButtonClass: "btn btn-brand"
                        });
                        
                    }else{
                        alert("Your current password is not correct. Please check it!");
                    }
                
                }
            });


        }
       


    },

    checkUsername:function() {
        let id_username = $("#id_username").val();
        let id_username_ori = $("#id_username_hidden").val();

        if (id_username_ori == id_username) {
            $("#username_check_icon").attr('class', 'kt-font-success flaticon2-check-mark');
        } else {


            $.ajax({
                url: '/ajax/validate_username/',
                data: {
                    'username': id_username
                },
                dataType: 'json',
                success: function (data) {
                    if (data.is_taken) {
                        $("#username_check_icon").attr('class', 'kt-font-danger flaticon2-delete');
                    }else{
                        $("#username_check_icon").attr('class', 'kt-font-success flaticon2-check-mark');
                    }
                }
            });
        }

    }


};

$( document ).ready(function() {

    let id_username = document.getElementById("id_username");

    id_username.addEventListener("keyup", function() {
        mainjs.checkUsername();
    });

});
