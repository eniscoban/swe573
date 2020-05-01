var photobooth_main = {

	addProject:function(){

        let projectname = $("#project-name").val();
       
        if(projectname.length>=3){
            $.ajax({ 
                type: "POST",
                url: "/a/photobooth/ax/addProject",
                data: { projectname : projectname},
                //async: false,
                success : function(response){ 
                    
                    if(response == "success"){
                        location.reload();
                    }else{
                        alert("An unknown error occured, please try again!");
                    }
                
                }
            });

        }else{
            $("#project-name").addClass("is-invalid");
            $("#project-name-error").removeClass("d-none");
        }

			

	},



    
    saveDesignSettings:function(){

        let background_color = $("#background_color").val();
        let button_color = $("#button_color").val();
        let button_text_color = $("#button_text_color").val();
        let primary_text_color = $("#primary_text_color").val();
        let secondary_text_color = $("#secondary_text_color").val();
        let projectID = $("#projectID").val();
        
        $.ajax({ 
            type: "POST",
            url: "/a/photobooth/ax/saveDesignSettings",
            data: { 
                background_color : background_color,
                button_color : button_color,
                button_text_color : button_text_color,
                primary_text_color : primary_text_color,
                secondary_text_color : secondary_text_color,
                projectID : projectID
            },
            //async: false,
            success : function(response){ 
             
                if(response == "success"){
                    swal.fire("Great!", "Design settings saved successfully!", "success");
                }else{
                    alert("An unknown error occured, please try again!");
                }
            
            }
        });

        
        

    },


    saveTextSettings:function(){

        let start_text = $("#start_text").val();

        let page1_text1 = $("#page1_text1").val();
        let page1_text2 = $("#page1_text2").val();
        let page1_button = $("#page1_button").val();
      
        let page2_text1 = $("#page2_text1").val();
        let page2_text2 = $("#page2_text2").val();
        let page2_button = $("#page2_button").val();

        let projectID = $("#projectID").val();
       
        $.ajax({ 
            type: "POST",
            url: "/a/photobooth/ax/saveTextSettings",
            data: { 
                start_text : start_text,
                page1_text1 : page1_text1,
                page1_text2 : page1_text2,
                page1_button : page1_button,
                page2_text1 : page2_text1,
                page2_text2 : page2_text2,
                page2_button : page2_button,
                projectID : projectID
            },
            success : function(response){ 

                if(response == "success"){
                    swal.fire("Great!", "Text settings saved successfully!", "success");
                }else{
                    alert("An unknown error occured, please try again!");
                }
            
            }
        });

    },

  
    saveProjectName:function(){

        let prjName = $("#prjName").val();
        let projectID = $("#projectID").val();

        $.ajax({ 
            type: "POST",
            url: "/a/photobooth/ax/saveProjectName",
            data: { 
                prjName : prjName,
                projectID : projectID
            },
            success : function(response){ 
             
                if(response == "success"){
                    swal.fire("Great!", "Project name saved successfully!", "success");
                }else{
                    alert("An unknown error occured, please try again!");
                }
            
            }
        });


    },

    saveEmailSettings:function(){
        let email_sender = $("#email_sender").val();
        let email_subject = $("#email_subject").val();
        let email_body = $("#email_body").val();
        let projectID = $("#projectID").val();
       
        $.ajax({ 
            type: "POST",
            url: "/a/photobooth/ax/saveEmailSettings",
            data: { 
                email_sender : email_sender,
                email_subject : email_subject,
                email_body : email_body,
                projectID : projectID
            },
            success : function(response){ 
             
                if(response == "success"){
                    swal.fire("Great!", "Email settings saved successfully!", "success");
                }else{
                    alert("An unknown error occured, please try again!");
                }
            
            }
        });

    },

    
    logoutDevice:function(deviceId,projectId){
        $.ajax({ 
            type: "POST",
            url: "/a/photobooth/ax/logoutDevice",
            data: { 
                deviceId : deviceId,
                projectId: projectId
            },
            success : function(response){ 
             
                if(response == "success"){
                    
                    location.reload();
                }else{
                    alert("An unknown error occured, please try again!");
                }
            
            }
        });

    },

    closeProject:function(projectId){
        $.ajax({ 
            type: "POST",
            url: "/a/photobooth/ax/closeProject",
            data: { 
                projectId: projectId
            },
            success : function(response){ 
             
                if(response == "success"){
                    
                    location.reload();
                }else{
                    alert("An unknown error occured, please try again!");
                }
            
            }
        });

    }



};
