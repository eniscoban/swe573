var mainjs = {

    validateEmail: function (email) {
        var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        return re.test(email);
    },

    login:function(){
        let id_email = $("#id_email").val();
        let id_password = $("#id_password").val();

        let csrftoken = Cookies.get('csrftoken');

        var onay = 1;
        var metin = "";

        if (this.validateEmail(id_email) === false) {
            onay = 0;
            metin = metin + "\nPlease enter a valid email address!";
        }

        if (id_password.length < 8) {
            onay = 0;
            metin = "Password must be at least 8 character!";
        }

        if (onay == 0) {
            toastr.warning(metin);
        } else {

            $.ajax({
                url: '/login/',
                type: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                data: {
                    'email': id_email,
                    'password': id_password
                },

                success: function (data) {

                    if(data.authenticated == true){
                        window.location.href = "/";
                    }else{
                        toastr.warning("Please check your email address or password.");
                    }

                }
            });



        }





    },

    register:function(){
        let id_email = $("#id_email").val();
        let id_password = $("#id_password").val();
        let id_username = $("#id_username").val();

        var onay = 1;
        var metin = "";

        if (id_username.length < 6) {
            onay = 0;
            metin = "Username must be at least 6 character!";
        }

        if (this.validateEmail(id_email) === false) {
            onay = 0;
            metin = metin + "\nPlease enter a valid email address!";
        }

        if (id_password.length < 8) {
            onay = 0;
            metin = "Password must be at least 8 character!";
        }

        if (onay == 0) {
            toastr.warning(metin);
        } else {

            let csrftoken = Cookies.get('csrftoken');

            $.ajax({
            url: '/signup/',
            type: 'POST',
            headers: { 'X-CSRFToken': csrftoken },
            data: {
                'email': id_email,
                'password': id_password,
                'username': id_username
            },
            success: function (data) {

               if(data.authenticated == true){
                   window.location.href = "/";
               }else{
                    toastr.warning("Please change your email and username. Such a user exists!");
               }
            }
            });


        }

    },

    change_avatar: function(){
         $.ajax({
            url: '/ajax/change_avatar/',
            data: {},
            dataType: 'json',
            success: function (data) {
                console.log(data);
                location.reload();
            }
         });
    },

    create_recipe_ajax:function() {
         let csrftoken = Cookies.get('csrftoken');

         let recipe_name = $("#recipe_name").val();
         let recipe_description = $("#recipe_description").val();
         let recipe_category = $("#recipe_category").val();
         let recipe_cuisine = $("#recipe_cuisine").val();
         let ingredients_ready = window.ingredients_ready;
         let recipe_serving = $("#recipe_serving").val();

         $.ajax({
            url: '/ajax/create_recipe_ajax/',
            type: 'POST',
            headers: {'X-CSRFToken': csrftoken},
            data: {
                'recipe_name': recipe_name,
                'recipe_description': recipe_description,
                'recipe_category': recipe_category,
                'recipe_cuisine': recipe_cuisine,
                'recipe_serving': recipe_serving,
                'ingredients_ready': ingredients_ready
            },
            dataType: 'json',
            success: function (data) {
                console.log(data);
            }
         });

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

    },

    addComment:function(token,recipe_id){

       let comment = $("#comment").val();
       let token_g = "Token " + token;
       let csrftoken = Cookies.get('csrftoken');

       if(comment.length >= 3){

            $.ajax({
            url: 'http://127.0.0.1:8000/api/add_comment/',
            type: 'POST',
            headers: { 'X-CSRFToken': csrftoken,  'Authorization': token_g  },
            data: {
                'comment': comment,
                'recipe_id': recipe_id
            },
            success: function (data) {

               location.reload();
            }
            });
       }

    },

    follow_user:function (token, target_username) {

        let token_g = "Token " + token;
        let csrftoken = Cookies.get('csrftoken');

        $.ajax({
        url: 'http://127.0.0.1:8000/api/follow_user/',
        type: 'POST',
        headers: { 'X-CSRFToken': csrftoken,  'Authorization': token_g  },
        data: {
            'target_username': target_username
        },
        success: function (data) {

           location.reload();
        }
        });
    },
    unfollow_user:function (token, target_username) {

        let token_g = "Token " + token;
        let csrftoken = Cookies.get('csrftoken');

        $.ajax({
            url: 'http://127.0.0.1:8000/api/unfollow_user/',
            type: 'POST',
            headers: { 'X-CSRFToken': csrftoken,  'Authorization': token_g  },
            data: {
                'target_username': target_username
            },
            success: function (data) {

               location.reload();
            }
        });
    },



    like_recipe:function(token,recipe_id){
       let token_g = "Token " + token;
       let csrftoken = Cookies.get('csrftoken');

       $.ajax({
            url: 'http://127.0.0.1:8000/api/like_recipe/',
            type: 'POST',
            headers: { 'X-CSRFToken': csrftoken,  'Authorization': token_g  },
            data: {
                'recipe_id': recipe_id
            },
            success: function (data) {

               location.reload();
            }
       });
    },

    unlike_recipe:function(token,recipe_id){
       let token_g = "Token " + token;
       let csrftoken = Cookies.get('csrftoken');

       $.ajax({
            url: 'http://127.0.0.1:8000/api/unlike_recipe/',
            type: 'POST',
            headers: { 'X-CSRFToken': csrftoken,  'Authorization': token_g  },
            data: {
                'recipe_id': recipe_id
            },
            success: function (data) {

               location.reload();
            }
       });
    },




    follow_provider:function (token, target_provider) {

        let token_g = "Token " + token;
        let csrftoken = Cookies.get('csrftoken');

        $.ajax({
        url: 'http://127.0.0.1:8000/api/follow_provider/',
        type: 'POST',
        headers: { 'X-CSRFToken': csrftoken,  'Authorization': token_g  },
        data: {
            'target_provider': target_provider
        },
        success: function (data) {

           location.reload();
        }
        });
    },
    unfollow_provider:function (token, target_provider) {

        let token_g = "Token " + token;
        let csrftoken = Cookies.get('csrftoken');

        $.ajax({
            url: 'http://127.0.0.1:8000/api/unfollow_provider/',
            type: 'POST',
            headers: { 'X-CSRFToken': csrftoken,  'Authorization': token_g  },
            data: {
                'target_provider': target_provider
            },
            success: function (data) {

               location.reload();
            }
        });
    },








};

$( document ).ready(function() {

    let id_username = document.getElementById("id_username");

    id_username.addEventListener("keyup", function() {
        mainjs.checkUsername();
    });

});
