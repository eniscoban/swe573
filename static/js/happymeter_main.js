var happymeter_main = {

	addProject:function(){

        let projectname = $("#project-name").val();
       
        if(projectname.length>=3){
            $.ajax({ 
                type: "POST",
                url: "/a/happymeter/ax/addProject",
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
            url: "/a/happymeter/ax/saveDesignSettings",
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

        let survey_text = $("#survey_text").val();
        let thankyou_text = $("#thankyou_text").val();
        let projectID = $("#projectID").val();
       
        $.ajax({ 
            type: "POST",
            url: "/a/happymeter/ax/saveTextSettings",
            data: { 
                survey_text : survey_text,
                thankyou_text : thankyou_text,
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
            url: "/a/happymeter/ax/saveProjectName",
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

   
    
    logoutDevice:function(deviceId,projectId){
        $.ajax({ 
            type: "POST",
            url: "/a/happymeter/ax/logoutDevice",
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
            url: "/a/happymeter/ax/closeProject",
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

    },

    tnxDoneOpt1:function(){
        $("#tnxLbl").addClass("kt-checkbox--solid");
        $("#qstLbl").removeClass("kt-checkbox--solid");

        $("#tnxBox").prop('checked', true);
        $("#qstBox").prop('checked', false);
        happymeter_main.hideOpt1();
    },
    qstDoneOpt1:function(){
        $("#qstLbl").addClass("kt-checkbox--solid");
        $("#tnxLbl").removeClass("kt-checkbox--solid");

        $("#qstBox").prop('checked', true);
        $("#tnxBox").prop('checked', false);
        happymeter_main.hideOpt1();
    },
    hideOpt1:function(){

        let projectID = $("#projectID").val();
        var act = "0";
        if ($('#tnxBox').prop('checked')) {
            $("#opss").hide();
            act = "0";
        }else{
            $("#opss").show();
            act = "1";
        }

        $.ajax({ 
            type: "POST",
            url: "/a/happymeter/ax/saveOpt1On",
            data: { 
                optionss : act,
                projectID : projectID
            },
            success : function(response){ 

                console.log(response);

                if(response == "success"){
                    console.log("done");
                }else{
                    console.log("An unknown error occured, please try again!");
                }
            
            }
        });

    },

    saveOpt1:function(){
        let quest = $("#quest").val();
        let op1 = $("#op1").val();
        let op2 = $("#op2").val();
        let op3 = $("#op3").val();
        let projectID = $("#projectID").val();

        $.ajax({ 
            type: "POST",
            url: "/a/happymeter/ax/saveOpt1",
            data: { 
                quest : quest,
                op1 : op1,
                op2 : op2,
                op3 : op3,
                projectID : projectID
            },
            success : function(response){ 

                console.log(response);
             
                if(response == "success"){
                    swal.fire("Great!", "Project name saved successfully!", "success");
                }else{
                    alert("An unknown error occured, please try again!");
                }
            
            }
        });


    },

    tnxDoneOpt2:function(){
        $("#tnxLbl").addClass("kt-checkbox--solid");
        $("#qstLbl").removeClass("kt-checkbox--solid");

        $("#tnxBox").prop('checked', true);
        $("#qstBox").prop('checked', false);
        happymeter_main.hideOpt2();
    },
    qstDoneOpt2:function(){
        $("#qstLbl").addClass("kt-checkbox--solid");
        $("#tnxLbl").removeClass("kt-checkbox--solid");

        $("#qstBox").prop('checked', true);
        $("#tnxBox").prop('checked', false);
        happymeter_main.hideOpt2();
    },
    hideOpt2:function(){

        let projectID = $("#projectID").val();
        var act = "0";
        if ($('#tnxBox').prop('checked')) {
            $("#opss").hide();
            act = "0";
        }else{
            $("#opss").show();
            act = "1";
        }

        $.ajax({ 
            type: "POST",
            url: "/a/happymeter/ax/saveOpt2On",
            data: { 
                optionss : act,
                projectID : projectID
            },
            success : function(response){ 

                console.log(response);

                if(response == "success"){
                    console.log("done");
                }else{
                    console.log("An unknown error occured, please try again!");
                }
            
            }
        });

    },

    saveOpt2:function(){
        let quest = $("#quest").val();
        let op1 = $("#op1").val();
        let op2 = $("#op2").val();
        let op3 = $("#op3").val();
        let projectID = $("#projectID").val();

        $.ajax({ 
            type: "POST",
            url: "/a/happymeter/ax/saveOpt2",
            data: { 
                quest : quest,
                op1 : op1,
                op2 : op2,
                op3 : op3,
                projectID : projectID
            },
            success : function(response){ 

                console.log(response);
             
                if(response == "success"){
                    swal.fire("Great!", "Project name saved successfully!", "success");
                }else{
                    alert("An unknown error occured, please try again!");
                }
            
            }
        });


    },

    tnxDoneOpt3:function(){
        $("#tnxLbl").addClass("kt-checkbox--solid");
        $("#qstLbl").removeClass("kt-checkbox--solid");

        $("#tnxBox").prop('checked', true);
        $("#qstBox").prop('checked', false);
        happymeter_main.hideOpt3();
    },
    qstDoneOpt3:function(){
        $("#qstLbl").addClass("kt-checkbox--solid");
        $("#tnxLbl").removeClass("kt-checkbox--solid");

        $("#qstBox").prop('checked', true);
        $("#tnxBox").prop('checked', false);
        happymeter_main.hideOpt3();
    },
    hideOpt3:function(){

        let projectID = $("#projectID").val();
        var act = "0";
        if ($('#tnxBox').prop('checked')) {
            $("#opss").hide();
            act = "0";
        }else{
            $("#opss").show();
            act = "1";
        }

        $.ajax({ 
            type: "POST",
            url: "/a/happymeter/ax/saveOpt3On",
            data: { 
                optionss : act,
                projectID : projectID
            },
            success : function(response){ 

                console.log(response);

                if(response == "success"){
                    console.log("done");
                }else{
                    console.log("An unknown error occured, please try again!");
                }
            
            }
        });

    },

    saveOpt3:function(){
        let quest = $("#quest").val();
        let op1 = $("#op1").val();
        let op2 = $("#op2").val();
        let op3 = $("#op3").val();
        let projectID = $("#projectID").val();

        $.ajax({ 
            type: "POST",
            url: "/a/happymeter/ax/saveOpt3",
            data: { 
                quest : quest,
                op1 : op1,
                op2 : op2,
                op3 : op3,
                projectID : projectID
            },
            success : function(response){ 

                console.log(response);
             
                if(response == "success"){
                    swal.fire("Great!", "Project name saved successfully!", "success");
                }else{
                    alert("An unknown error occured, please try again!");
                }
            
            }
        });


    }



    




};
