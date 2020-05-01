var purchasejs = {

	selectPlan:function(planId){

			let der = "#plan_div_"+planId;
			let cek = "#plan_check_"+planId;
	
			$(".temdiv").removeClass("border-success");
			$(".temcek").removeClass("kt-badge--success");

			$(der).addClass("border-success");
			$(cek).addClass("kt-badge--success");

			$("#selectedPlan").val(planId); 	

        },

	selectAppContinue:function(){

		let selectedApp = $("#selectedApp").val();
		let selectedPlan = $("#selectedPlan").val();

		if(selectedApp == "0" || selectedPlan == "0"){

				swal.fire('Please select an app and plan to continue!'); 

		}else{
				let url = "https://appseno.com/purchase/signup/"+selectedApp+"/"+selectedPlan;
				window.location.replace(url);
		}
			
	},

	validateEmail: function (email) {
			var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
			return re.test(email);
	},

	signup:function(){

			let signup_name = $("#signup_name").val();
			let signup_surname = $("#signup_surname").val();
			var signup_email = $("#signup_email").val();
			var signup_password = $("#signup_password").val();
	
			let selectedApp = $("#selectedApp").val();
			let selectedPlan = $("#selectedPlan").val();


			var onay = 1;
			var metin = "";
	
			if (signup_name.length < 2) {
				onay = 0;
				metin = "Please enter your name!";
			}
	
			if (this.validateEmail(signup_email) === false) {
				onay = 0;
				metin = metin + "\nPlease enter a valid email address!";
			}
	
			if (signup_password < 8) {
				onay = 0;
				metin = metin + "\nPassword must be at least 8-character lenght!";
			}
	
			
			if (onay == 0) {
					swal.fire(metin); 
				} else {

					$("#signupBtn").addClass('kt-spinner kt-spinner--right kt-spinner--sm kt-spinner--light').attr('disabled', true);
					$.ajax({ type: "POST",
							url: "/purchase/signup/signupCheck",
							data: { signup_name : signup_name, signup_surname : signup_surname, 
									signup_email : signup_email, signup_password : signup_password
										},
							//async: false,
							success : function(response){ 
									console.log(response);
							if(response == "success"){
									let url = "/purchase/payment/"+selectedApp+"/"+selectedPlan
									window.location.replace(url);
							}else{
									setTimeout(function() {
											swal.fire('This email is used by another member. Please choose another email address or try login!'); 
											$("#signupBtn").removeClass('kt-spinner kt-spinner--right kt-spinner--sm kt-spinner--light').attr('disabled', false);
									
									}, 1000);
							}
							

							}
					});

					
				}
		
					
				

	},

	login:function(){

			var loginEmail = $("#loginEmail").val();
			var loginPass = $("#loginPass").val();
	
			let selectedApp = $("#selectedApp").val();
			let selectedPlan = $("#selectedPlan").val();

			var onay = 1;
			var metin = "";
	
			if (loginPass.length < 4) {
				onay = 0;
				metin = "Please enter your password!";
			}
	
			if (this.validateEmail(loginEmail) === false) {
				onay = 0;
				metin = metin + "\nPlease enter a valid email address!";
			}
	
			
			
			if (onay == 0) {
					swal.fire(metin); 
				} else {

					$("#loginBtn").addClass('kt-spinner kt-spinner--right kt-spinner--sm kt-spinner--light').attr('disabled', true);

					$.ajax({ type: "POST",
							url: "/purchase/signup/loginCheck",
							data: { loginEmail : loginEmail, loginPass : loginPass  },
							//async: false,
							success : function(response){ 
									console.log(response);
							if(response == "success"){
									let url = "/purchase/payment/"+selectedApp+"/"+selectedPlan
									window.location.replace(url);
							}else{
									setTimeout(function() {
											swal.fire('Please check your email and password!'); 
											$("#loginBtn").removeClass('kt-spinner kt-spinner--right kt-spinner--sm kt-spinner--light').attr('disabled', false);
									
									}, 1000);
							}
							

							}
					});

					
				}


	},

	paymentCheck:function(){

			var cardName = $("#cardName").val();
			var cardExp = $("#cardExp").val();
			var cardCvc = $("#cardCvc").val();
			var cardNumber = $("#cardNumber").val();

			var billName = $("#billName").val();
			var billSurname = $("#billSurname").val();
			var billCompany = $("#billCompany").val();
			var billAddress = $("#billAddress").val();
			var billCity = $("#billCity").val();
			var billZip = $("#billZip").val();
			var billCounty = $("#billCounty").val();
			var billRegion = $("#billRegion").val();

			let selectedApp = $("#selectedApp").val();
			let selectedPlan = $("#selectedPlan").val();

			cardNumber = cardNumber.replace(/ /g, "");
			cardExp = cardExp.replace(/ /g, "");
			

					$("#purchaseBtn").addClass('kt-spinner kt-spinner--right kt-spinner--sm kt-spinner--light').attr('disabled', true);
					$.ajax({ type: "POST",
							url: "/purchase/payment/purchaseCheck",
							data: { cardName : cardName, cardExp : cardExp, cardCvc : cardCvc, cardNumber : cardNumber, 
									billName : billName, billSurname : billSurname, billCompany : billCompany, billAddress : billAddress,
									billCity : billCity, billZip : billZip, billCounty : billCounty, billRegion : billRegion,
									selectedApp : selectedApp,  selectedPlan : selectedPlan
									},
							//async: false,
							success : function(response){ 
									console.log(response);
							if(response == "success"){
									
									let url = "/dashboard";
									window.location.replace(url);
							}else{
									setTimeout(function() {
											swal.fire('Something went wrong! Please check and try again!'); 
											$("#purchaseBtn").removeClass('kt-spinner kt-spinner--right kt-spinner--sm kt-spinner--light').attr('disabled', false);
									
									}, 1000);
							}
							

							}
					});
			

	},

	checkLuhn:function(value){

			// accept only digits, dashes or spaces
			if (/[^0-9-\s]+/.test(value)) return false;
	
			// The Luhn Algorithm. It's so pretty.
			var nCheck = 0, nDigit = 0, bEven = false;
			value = value.replace(/\D/g, "");
	
			for (var n = value.length - 1; n >= 0; n--) {
			var cDigit = value.charAt(n),
					nDigit = parseInt(cDigit, 10);
	
			if (bEven) {
					if ((nDigit *= 2) > 9) nDigit -= 9;
			}
	
			nCheck += nDigit;
			bEven = !bEven;
			}
	
			return (nCheck % 10) == 0;
				

	},


	iyzi3dSecure:function(){

		let g1 = new Date(); 

		var goon = 1;

		var cardNumber = $("#cardNumber").val();
		var cardName = $("#cardName").val();
		var cardExp = $("#cardExp").val();
		var cardCvc = $("#cardCvc").val();
		
		var billName = $("#billName").val();
		var billSurname = $("#billSurname").val();
		var billCompany = $("#billCompany").val();
		var billAddress = $("#billAddress").val();
		var billCity = $("#billCity").val();
		var billZip = $("#billZip").val();
		var billCounty = $("#billCounty").val();
		var billRegion = $("#billRegion").val();

		let selectedApp = $("#selectedApp").val();
		let selectedPlan = $("#selectedPlan").val();

			

		if(cardName.length <= 3){
				goon = 0;
				swal.fire('Please enter a valid name for your card!');
		}


		if(goon == 1){
			if(cardExp.length <= 3){
				goon = 0;
				swal.fire('Please enter a valid expiration date for your card!');
			}else{
				cardExp = cardExp.replace(/ /g, "");
				let cardExp2 = cardExp.split("/");
				let expDate =  new Date('20'+cardExp2[1] + '-' + cardExp2[0] + '-1'); 
				if(g1>expDate){
						goon = 0;
						swal.fire('Invalid Expiration Date!\nPlease check expiration date!'); 
				}  
			}
		}



		if(goon == 1){
		
			if(cardNumber.length <= 10){
					goon = 0;
					swal.fire('Invalid Card Number!\nPlease check your card number!'); 
				}else{
					cardNumber = cardNumber.replace(/ /g, "");
					let res = this.checkLuhn(cardNumber);
					if(!res){
						goon = 0;
						swal.fire('Invalid Card Number!\nPlease check your card number!'); 
					}
				}
		}


		if(goon == 1){
			if(cardCvc.length <= 2){
				goon = 0;
				swal.fire('Please enter CVC number for your card!'); 
			}
		}

		if(goon == 1){
			if(billName.length <= 1){
				goon = 0;
				swal.fire('Please enter billing name!'); 
			}
		}

		if(goon == 1){
			if(billSurname.length <= 2){
				goon = 0;
				swal.fire('Please enter billing last name!'); 
			}
		}

		if(goon == 1){
			if(billAddress.length <= 2){
				goon = 0;
				swal.fire('Please enter billing address!'); 
			}
		}

		if(goon == 1){
			if(billCity.length <= 2){
				goon = 0;
				swal.fire('Please enter billing city!'); 
			}
		}

		if(goon == 1){
			if(billZip.length <= 2){
				goon = 0;
				swal.fire('Please enter billing zip code!'); 
			}
		}

		if(goon == 1){
			if(billCounty == "0"){
				goon = 0;
				swal.fire('Please select billing country!'); 
			}
		}

		if(goon == 1){
			if(selectedApp == "" || selectedPlan == ""){
				goon = 0;
				window.location.replace("/purchase/selectProduct");
			}
		}

		if(goon == 1){
				
			$.ajax({ type: "POST",
				url: "/purchase/payment/iyzi3dSecure",
				data: { cardName : cardName, cardExp : cardExp, cardCvc : cardCvc, cardNumber : cardNumber, 
						billName : billName, billSurname : billSurname, billCompany : billCompany, billAddress : billAddress,
						billCity : billCity, billZip : billZip, billCounty : billCounty, billRegion : billRegion,
						selectedApp : selectedApp,  selectedPlan : selectedPlan
						},
				dataType : 'json',
				//async: false,
				success : function(response){ 
					

					//console.log(response);
					var myObj = $.parseJSON(JSON.stringify(response));

					//console.log(myObj.status);
					//console.log(myObj.html);
					
					if(myObj.status=="success"){
					//	$("#donen").html(myObj.html);
						var newDoc = document.open("text/html", "replace");
						newDoc.write(myObj.html);
						newDoc.close();
					}else{
					
					//	purchasejs.redirectPost('/purchase/failure', { error_coming :myObj.error, appID : selectedApp, planID : selectedPlan });

					}
				


				}
			});


		}


	},

	iyzi3dSecureComplete:function(){

			var appID = $("#selectedApp").val();
			var planID = $("#selectedPlan").val();
			var conversationId = $("#conversationId").val();
			var conversationData = $("#conversationData").val();
			var paymentId = $("#paymentId").val();
			
			console.log("iyzi3dSecureComplete çalıştı");
					
			$.ajax({ type: "POST",
				url: "/purchase/payment/iyzi3dSecureComplete",
				data: { appID : appID, planID : planID, conversationId : conversationId, conversationData : conversationData, paymentId : paymentId},
				dataType : 'json',
				success : function(response){ 

					console.log("response");
					console.log(response);
					var myObj = $.parseJSON(JSON.stringify(response));
					console.log(myObj.status);
					console.log(myObj.error);
					

					
					if(myObj.status == "success"){
						let url = "/purchase/success";
						window.location.replace(url);
					}else{
						
						purchasejs.redirectPost('/purchase/failure', { error_coming :myObj.error, appID : appID, planID : planID });

					}

				
				},
				error: function(XMLHttpRequest, textStatus, errorThrown) { 
					alert("Status: " + textStatus); 
					alert("Error: " + errorThrown); 
					alert("XMLHttpRequest: " + XMLHttpRequest); 
				}       
			});



	},
	
	redirectPost: function(url, data) {
			var form = document.createElement('form');
			document.body.appendChild(form);
			form.method = 'post';
			form.action = url;
			for (var name in data) {
					var input = document.createElement('input');
					input.type = 'hidden';
					input.name = name;
					input.value = data[name];
					form.appendChild(input);
			}
			form.submit();
	},
	
	



    

};
