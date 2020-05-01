var datamasterjs = {


    init:function(){

        $("#kt_sortable_portlets").sortable({
            connectWith: ".dragarea",
            items: ".dragitems",
            opacity: 0.8,
            handle : '.dragarea',
            coneHelperSize: true,
            placeholder: 'kt-portlet--sortable-placeholder',
            forcePlaceholderSize: true,
            tolerance: "pointer",
            helper: "clone",
            tolerance: "pointer",
            forcePlaceholderSize: !0,
            helper: "clone",
            cancel: ".kt-portlet--sortable-empty", // cancel dragging if portlet is in fullscreen mode
            revert: 250, // animation in milliseconds
            update: function(b, c) {
                if (c.item.prev().hasClass("kt-portlet--sortable-empty")) {
                    c.item.prev().before(c.item);
                }
                
                datamasterjs.orderForm();
                
            }
        });


    },

    orderForm:function(){
        i=1;
        $('#kt_sortable_portlets > .dragitems > .hidden_order').each(function(){
            var itemId = $(this).attr("id");
            
            $.ajax({ 
                type: "POST",
                url: "/a/datamaster/ax/orderForm",  
                data: { 
                    itemId : itemId,
                    itemOrder : i
                }, 
               // async: false,
                success : function(text){  response= text;  }
            });

            $(this).val(i);
            i++;
        });
    },

    //singleline form

    addSingleLineForm:function(projectID){

        var response;
        $.ajax({ 
            type: "POST",
            url: "/a/datamaster/ax/addSingleLineForm",  
            data: { 
                projectID : projectID
            }, 
            async: false,
            success : function(text){  response= text; }
        });
        $('#kt_sortable_portlets').append(response);

    },

    deleteItem:function(itemId){
        
        $.ajax({ 
            type: "POST",
            url: "/a/datamaster/ax/deleteItem",  
            data: { 
                itemId : itemId
            }, 
           // async: false,
            success : function(text){  response= text;  }
        });

        var hel="#" + itemId+"_main";
        $(hel).remove();
    },

    editLineFormAx:function(itemId){

        $.ajax({
            url: '/a/datamaster/ax/editLineFormAx',
            type: 'post',
            data: {itemId: itemId},
            success: function(response){ 
                $('.modal-body').html(response);
            }
        });

    },

    saveLineFormAx:function(){
        let itemname_edited = $("#itemname_edited").val();
        let itemid_edited = $("#itemid_edited").val();

        $.ajax({
            url: '/a/datamaster/ax/saveLineFormAx',
            type: 'post',
            data: {itemid_edited: itemid_edited, itemname_edited: itemname_edited},
            success: function(response){ 
                if(response == "success"){
                    location.reload();
                }
            }
        });

        
    },

    //multiline form

    addMultiLineForm:function(projectID){

        var response;
        $.ajax({ 
            type: "POST",
            url: "/a/datamaster/ax/addMultiLineForm",  
            data: { 
                projectID : projectID
            }, 
            async: false,
            success : function(text){  response= text; }
        });
        $('#kt_sortable_portlets').append(response);

    },

    //dropdown
    addDropdownForm:function(projectID){

        var response;
        $.ajax({ 
            type: "POST",
            url: "/a/datamaster/ax/addDropdownForm",  
            data: { 
                projectID : projectID
            }, 
            async: false,
            success : function(text){  response= text; }
        });
        $('#kt_sortable_portlets').append(response);

    },

    editDropdownFormAx:function(itemId){
        $.ajax({
            url: '/a/datamaster/ax/editDropdownFormAx',
            type: 'post',
            data: {itemId: itemId},
            success: function(response){ 
                $('.modaldropbody').html(response);
            }
        });
    },

    deleteOptionDropbox:function(opid){
        let itemId = $("#itemid_idi").val();
        let dv = "#opt"+opid;
        $(dv).remove();
        $.ajax({
            url: '/a/datamaster/ax/deleteOptionDropbox',
            type: 'post',
            data: {itemId: itemId,opid: opid},
            success: function(response){ }
        });
    },

    addOptionDropbox:function(){
        
        let itemid_idi = $("#itemid_idi").val();
        let optionName = $("#optionBox").val();
       
        resp="";
        $.ajax({
            url: '/a/datamaster/ax/addOptionDropbox',
            type: 'post',
            data: {itemId: itemid_idi, optionName: optionName},
            success: function(response){ 
                resp= response 
                $("#optionsDiv").append(resp);
                $("#optionBox").val('');
            }
        });

        
    },

    orderDropdownOptions:function(){

        var firstOptionId = "";

        i=1;
        $('#optionsDiv > .dragitems > .hidden_order').each(function(){
            var optionId = $(this).attr("id");
            
            if(i == 1){
                firstOptionId = optionId;
            }

            $.ajax({ 
                type: "POST",
                url: "/a/datamaster/ax/orderDropdownOptions",  
                data: { 
                    optionId : optionId,
                    optionOrder : i
                }, 
               // async: false,
                success : function(text){  response= text;  }
            });

            $(this).val(i);
            i++;
        });

        datamasterjs.dropdownUpdateDefault(firstOptionId);

    },

    dropdownUpdateDefault:function(firstOptionId){
        $.ajax({ 
            type: "POST",
            url: "/a/datamaster/ax/dropdownUpdateDefault",  
            data: { 
                firstOptionId : firstOptionId
            }, 
            success : function(text){  response= text;  }
        });
    },

    //agreement

    addCheckboxForm:function(projectID){

        var response;
        $.ajax({ 
            type: "POST",
            url: "/a/datamaster/ax/addCheckboxForm",  
            data: { 
                projectID : projectID
            }, 
            async: false,
            success : function(text){  response= text; }
        });
        $('#kt_sortable_portlets').append(response);

    },

    editCheckboxContent:function(itemId){
        $.ajax({
            url: '/a/datamaster/ax/editCheckboxContent',
            type: 'post',
            data: {itemId: itemId},
            success: function(response){ 
                $('.modalAgreement').html(response);
            }
        });
    },

    saveCheckboxContent:function(){
        let itemcontent_edited = $("#itemcontent_edited").val();
        let itemid_edited = $("#itemid_edited").val();

        $.ajax({
            url: '/a/datamaster/ax/saveCheckboxContent',
            type: 'post',
            data: {itemid_edited: itemid_edited, itemcontent_edited: itemcontent_edited},
            success: function(response){ 
                if(response == "success"){
                    location.reload();
                }
            }
        });
    },


    //manatory

    manatoryclicked:function(itemId){
        let vel = "#man"+itemId;
       
        var durum = "";
        if($(vel).is(':checked')){
            durum="checked";
        }else{
            durum="unchecked";
        }

        $.ajax({ 
            type: "POST",
            url: "/a/datamaster/ax/manatoryclicked",  
            data: { 
                itemId : itemId,
                durum : durum
            }, 
           // async: false,
            success : function(text){  response= text;  }
        });
        

    },
    
    defaultclicked:function(itemId){
        let vel = "#def"+itemId;
       
        var durum = "";
        if($(vel).is(':checked')){
            durum="checked";
        }else{
            durum="unchecked";
        }

        $.ajax({ 
            type: "POST",
            url: "/a/datamaster/ax/defaultclicked",  
            data: { 
                itemId : itemId,
                durum : durum
            }, 
           // async: false,
            success : function(text){  response= text;  }
        });
        

    }


    
}

jQuery(document).ready(function() {
    datamasterjs.init();
});