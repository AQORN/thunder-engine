//Show the loading image while loading the page.
$(window).load(function() {
    $(".pre-load").fadeOut( 1000 );
});

//$(function() {
//    //To show and hide the password 
//    $(".show-password").parent().find('input').attr("type", "password");
//
//    //Hiding the password while doing the mouse up
//    $(".show-password").mouseup(function() {
//        $(this).parent().find('input').attr("type", "password");
//    });
//    
//    //Showing the password while doing the mouse down
//    $(".show-password").mousedown(function() {
//        $(this).parent().find('input').attr("type", "text");
//    });
//});

// Function to make the displayed left menu active
$(function() {
    
  //Function to make the displayed top menu active
    $('.nodeCheckbox').prop('checked', false);
    
    //this will get the full URL at the address bar
    var url = window.location.href;

    // passes on every "a" tag 
    $(".nav-menu a").each(function() {
        
        // checks if its the same on the address bar
        if (url == (this.href)) {
            $(this).closest("div").addClass("menu_active");
        }
    });
    
    //To show and hide the password 
    $(".show-password").parent().find("input").attr("type", "password");
    $(".show-password").on("click", function() {
        if ( $(this).hasClass( "hidden-password" )) {
            $(this).removeClass("hidden-password");
            $(this).parent().find('input').attr("type", "password");
            $(this).removeClass("glyphicon-eye-open");
            $(this).addClass("glyphicon-eye-close");
        }
        else {
            $(this).parent().find('input').attr("type", "text");
            $(this).addClass("hidden-password");
            $(this).removeClass("glyphicon-eye-close");
            $(this).addClass("glyphicon-eye-open");
        }
    });
    
    // passes on every "a" tag 
    $(".sidebar-panel a").each(function() {
        // checks if its the same on the address bar
        if (url == (this.href)) {
            $(this).closest("div").addClass("active-sidebar");
        }
    });
});

//Sidebar toggler for mobile resolutions
function toggler() {
    var txt = $(".toggle-sidebar").is(':visible') ? '+' : '-';
    $(".sb-toggle-btn").text(txt);
    $('.toggle-sidebar').toggle("slow");
}

// function to verify network
function verifyNetwork() {
	$('#form-modal-body').load('/clouds/verifyNetwork/', function() {
        $('#form-modal').modal('toggle');
        $('.modal-dialog').css('width', '900px');
        $('.modal-title').html("Verify Network");
    });
}

//Loading js after document ready
$( document ).ready(function() {

    // To call the function to check whether any new alert is found
    timeout = setInterval(function() {
                $.ajax({
                    type: 'GET',
                    url: "/hasNewAlerts",
                    success: function (xhr, ajaxOptions, thrownError) {
                        status = xhr.hasNewAlerts;
                        
                        // Executes if new alerts are available
                        if (status == 'true') {
                            
                            // Sets the image to no-bell for alert
                            $("#alert-notify > img").attr("src", "/site_media/images/icon-bell.png");
                        }
                    }
                });
            }, 45000);
    
    //Ajax form submit
    var formAjaxSubmit = function(form, modal) {
        $(form).submit(function (e) {
            e.preventDefault();
            $.ajax({
                type: $(this).attr('method'),
                url: $(this).attr('action'),
                data: $(this).serialize(),
                success: function (xhr, ajaxOptions, thrownError) {
                    if ( $(xhr).find('.has-error').length > 0 ) {
                        $(modal).find('.modal-body').html(xhr);
                        formAjaxSubmit(form, modal);
                    } else {
                    	location.reload(); 
                    	$(modal).modal('toggle');
                    }
                },
                error: function (xhr, ajaxOptions, thrownError) {
                }
            });
        });
    }
   
	// to verify the network settings using the network values
	$(document).on("click", "#verify_network", function(e) {
		$('#load-image').show();
		$('#check_conection_msg').load('/clouds/checkConnection/', function () {
			$('#load-image').hide();
        });
    });
	
    //For the role configure
    $('#roles').click(function() {
        $('#form-modal-body').load('/tabs/', function () {
            $('#form-modal').modal('toggle');
            $('.modal-dialog').css('width', '90%');
            //formAjaxSubmit('#form-modal-body form', '#form-modal');
            $('.modal-title').html("Role-Based Access Control (RBAC)");
            $("#form-modal-body").addClass('rm-pad-value role-base');
            $("#form-modal-body > div.row").addClass('rm-pad-value');
            $("#form-modal-body > ul.roleUl").addClass('rm-pad-value');
        });
    });
    
    //For the support menu
    $('#support-options').click(function() {
    	$('#form-modal-body').load('/support/', function () {
            $('#form-modal').modal('toggle');
            $('.modal-dialog').css('width', '90%');
            formAjaxSubmit('#form-modal-body form', '#form-modal');
            $('.modal-title').html("Support Options");
        });    	 
	});
    
    //For the monitor-process
    $('#monitor-process').click(function() {
        $('#form-modal-body').load('/monitor/', function () {
            $('#form-modal').modal('toggle');
            $('.modal-dialog').css('width', '900px');
            formAjaxSubmit('#form-modal-body form', '#form-modal');
            $('.modal-title').html("Monitor process");
        });      
    });
    
    //For the log details
    $('#logs').click(function() {
    	$('#form-modal-body').load('/log/', function () {
            $('#form-modal').modal('toggle');
            $('.modal-dialog').css('width', '90%');
            formAjaxSubmit('#form-modal-body form', '#form-modal');
            $('.modal-title').html("Log Viewer"); 
            
            // Sets the height for the log display container
            eleCount = $(".log-cont").length;
            heightVal = eleCount * 50;
            if (heightVal > 250) {
                $("#logContainer").css({height : 250 + 'px'});
                
                // Checks whether the scroll need to be displayed
                // if (heightVal > 250) {
                //    $("#logContainer").css({overflowX : 'auto'});
                // }
            } else {
                $("#logContainer").css({'min-height' : heightVal + 'px'});
                $("#logContainer").css({overflow : 'hidden'});
            }
            
            // Displays empty list
            if (eleCount == 0) {
                $("#logContainer").css({height : '50px'});
                $("#logContainer").css({overflow : 'hidden'});
                $("#logContainer").html("<p class='log-cont'>No logs available</p>");
            }
        });   
	});
         
    //For the role assignment
    $('#addNodes').click(function() {
    	$('#form-modal-body').load('/roleAssign/', function () {
            $('#form-modal').modal('toggle');
            $('.modal-dialog').css('width', '950px');
            formAjaxSubmit('#form-modal-body form', '#form-modal');
            $('.modal-title').html("Add & Assign Roles");
        });
    });
    
    //For the node configure
    $('#configureNode').click(function() {
        if($("#confignodeId").val() != 'test') {
            $('#form-modal-body').load('/nodeConfig/'+$("#confignodeId").val(), function () {
                $('#form-modal').modal('toggle');
                $('.modal-dialog').css('width', '1000px');
                formAjaxSubmit('#form-modal-body form', '#form-modal');
                $('.modal-title').html("Configure Node");
            });
        }
    });
    
    //For the configuration
    $(".nodeCheckbox").on("click", function(e) {
        if($('.nodeCheckbox:checked').size() != 1) {
            $('#configureNode').css('pointer-events', 'none');
            $("#confignodeId").val('test')
        } else {
            $('#configureNode').css('pointer-events', 'auto');
            ids = $('.nodeCheckbox:checked').val().split('-');
            $("#confignodeId").val(ids[1])
        }
    });
    
    //manage addons
    $('#manage-add-ons').click(function() {
        $('#form-modal-body').load('/manageAddons/', function () {
            $('#form-modal').modal('toggle');
            $('.modal-dialog').css('width', '80%');
            formAjaxSubmit('#form-modal-body form', '#form-modal');
            $('.modal-title').html("Manage Add-ons");
        });
    }); 
    
    // To display the alert list as popup
    $(document).on("click", "#all-alert", function(e) {
        $('#form-modal-body').load('/thunderalert?view-all=true', function () {
            $('#form-modal').modal('toggle');
            $('.modal-dialog').css('width', '90%');
            $('.modal-title').html("Alerts");
            
            // Sets the height for the log display container
            eleCount = $(".alert-content").length;
            heightVal = eleCount * 50;
            if (heightVal > 250) {
                $(".bdr-pop").css({height : 250 + 'px'});
            } else {
                $(".bdr-pop").css({'min-height' : heightVal + 'px'});
                $(".bdr-pop").css({overflow : 'hidden'});
            }
            
            // Displays empty list
            if (eleCount == 0) {
                $(".bdr-pop").css({height : '50px'});
                $(".bdr-pop").css({overflow : 'hidden'});
                $(".bdr-pop").html("<p class='log-cont'>No alerts found</p>");
            }
        });
    });
    
    //For the remove nodes
    $('#removeNodes').click(function() {
    	
    	var checkedValues = $('input[name="do_delete"]:checked').map(function() {
    	    return this.value;
    	}).get();  
    	
    	jsonData = JSON.stringify(checkedValues);
    	$.ajax({
    		beforeSend: function(xhr)  {
		     	xhr.setRequestHeader('X-CSRFToken', window.csrf_val);  
		    },
    		type: 'POST',  
    		url: "/removeRole/",
            data: { 'datepost' : jsonData },
            success: function (xhr, ajaxOptions, thrownError) {
               if ( $(xhr).find('.has-error').length > 0 ) {    
            	   location.reload(); 
               }
               else {
            	   location.reload();
               }
            },
            error: function (xhr, ajaxOptions, thrownError) {
            }                
        });
        
    });
    
    //For the search functionlity of the logs
    $(document).on("click", "#searchLog", function(e) {
        $.ajax({
            type: 'GET', 
            url: "/searchLogs/",
            data: {cloudlist: $("#cloud-list").val(), nodelist: $("#node-list").val(), rolelist: $("#role-list").val()},
            success: function (xhr, ajaxOptions, thrownError) {
               if ( $(xhr).find('.has-error').length > 0 ) {
                   alert('error');
               }
               else {
                   logs = '';
                   // Empty the table
                   $('#log-details-tab').html("");
                   $.each(xhr, function(key, server) {
                       // Append the log entry
                       logs = logs + "<p class='log-cont'>" + server.log_details + "</p>";
                   });
                   $("#log-details-tab").html(logs);
                   
                   // Sets the height for the log display container
                   eleCount = $(".log-cont").length;
                   heightVal = eleCount * 50;
                   if (heightVal > 250) {
                       $("#logContainer").css({height : 250 + 'px'});
                       
                       // Checks whether the scroll need to be displayed
                       // if (heightVal > 250) {
                       //    $("#logContainer").css({overflowX : 'auto'});
                       // }
                   } else {
                       $("#logContainer").css({'height' : '0'});
                       $("#logContainer").css({'min-height' : heightVal + 'px'});
                       $("#logContainer").css({overflow : 'hidden'});
                   }
                   
                   // Displays empty list
                   if (eleCount == 0) {
                       $("#logContainer").css({height : '50px'});
                       $("#logContainer").css({overflow : 'hidden'});
                       $("#logContainer").html("<p class='log-cont'>No logs available</p>");
                   }
               }
            },
            error: function (xhr, ajaxOptions, thrownError) {
            }
        });
    });
    
    //To add more fields into the public network
    $(".add-public").click(function() {
    	$(".public-network-container:hidden").last().show();
    });
    
    // To check whether the public multi fields in network tab have values or not
    // If found, display them
    $(".public-network-container").each(function() {
        var fieldValue = $(this).find('div.public-ip-from > input').val();
        
        
        fieldValue = fieldValue.trim();
        // Sets the element id
        var id = $(this).attr('id');
       
        // Checks whether value is assigned or not
        if (fieldValue.length > 0) {
            $("#" + id).show();
        } else {        
            $("#" + id).hide();   
        }
    });
    
    // To check whether the public cidr multi fields in network tab have values or not
    // If found, display them
    $(".public-net-cidr-list").each(function() {
    	
    	var fieldValue = $(this).find('div.public-net-cidr > input').val();
        fieldValue = fieldValue.trim();
        
        // Sets the element id
        var id = $(this).attr('id');
        
        // Checks whether value is assigned or not
        if (fieldValue.length > 0) {
            $("#" + id).show();
        } else {        
            $("#" + id).hide();   
        }
    });
    
    // To check whether the floating ip multi fields in network tab have values or not
    // If found, display them
    $(".float-network-ips").each(function() {
        
        var fieldValue = $(this).find('div.float-ip-from > input').val();
        fieldValue = fieldValue.trim();
       
        // Sets the element id
        var id = $(this).attr('id');
       
        // Checks whether value is assigned or not
        if (fieldValue.length > 0) {
            $("#" + id).show();
        } else {        
            $("#" + id).hide();   
        }
    });
    
    // To check whether the dns server multi fields in network tab have values or not
    // If found, display them
    $(".dns-server").each(function() {
        var fieldValue = $(this).find('div.dns-server-from > input').val();
        fieldValue = fieldValue.trim();
       
        // Sets the element id
        var id = $(this).attr('id');
       
        // Checks whether value is assigned or not
        if (fieldValue.length > 0) {
            $("#" + id).show();
        } else {        
            $("#" + id).hide();   
        }
    });
    
    // To check whether the private multi fields in network tab have values or not
    // If found, display them
    $(".private-network").each(function() {
        var fieldValue = $(this).find('div#pg-network-input > input').val();
        fieldValue = fieldValue.trim();
       
        // Sets the element id
        var id = $(this).attr('id');
       
        // Checks whether value is assigned or not
        if (fieldValue.length > 0) {
            $("#" + id).show();
        } else {        
            $("#" + id).hide();   
        }
    });
    
    // To hide all the fields other than the first one 
    $("#public-1").show();
    $("#public-cidr-1").show();
    $("#float-1").show();
    $("#dns-1").show();
    $("#private-1").show();
    
    //To remove the fields from the public network
    $(".remove-public").click(function() {
        $(".public-network-container:visible").last().find("div > input").val("");
    	$(".public-network-container:visible").last().hide();
    });
    
    // To add more fields into the public network cidr
    $(".add-public-cidr").click(function() {
    	$(".public-net-cidr-list:hidden").last().show();
    });
    
    //To remove the fields from the public network cidr
    $(".remove-public-cidr").click(function() {
        $(".public-net-cidr-list:visible").last().find("div > input").val("");
    	$(".public-net-cidr-list:visible").last().hide();
    });
    
    //To add more fields into the public network
    $(".add-float").click(function() {
    	$(".float-network-ips:hidden").last().show();
    });
    
    //To remove the fields from the public network
    $(".remove-float").click(function() {
        $(".float-network-ips:visible").last().find("div > input").val("");
    	$(".float-network-ips:visible").last().hide();
    });
    
    //To add more fields into the public network
    $(".add-dns").click(function() {
    	$(".dns-server:hidden").last().show();
    });
    
    //To remove the fields from the public network
    $(".remove-dns").click(function() {
        $(".dns-server:visible").last().find("div > input").val("");
    	$(".dns-server:visible").last().hide();
    }); 
    
    //To add more fields into the private network section
    $(".add-private-network").click(function() {
        $(".private-network:hidden").last().show();
    });
    
    //To remove the fields from the private network section
    $(".remove-private-network").click(function() {
        $(".private-network:visible").last().find("div > input").val("");
        $(".private-network:visible").last().hide();
    }); 
    
    // To set the public n/w vlan value
    var publicVlan = $("#id_public_vlan").val();
    $("#id_public_use_vlan").click(function() {
        /* Checks whether the checkbox is ticked Sets the default value, else resets */
        if ($(this).prop('checked')) {
            if (publicVlan == "") {
                publicVlan = 1;
            }
            $("#id_public_vlan").val(publicVlan);
        } else {
            $("#id_public_vlan").val('');
        }
    }); 
    
    //Saving the vlan values, this is to show afterwards
    var vlanValue = $("#id_in_vlan").val();
    var stVlan = $("#id_st_vlan").val();
    // To set the management n/w vlan value
    $("#id_in_use_vlan").click(function() {
        /* Checks whether the checkbox is ticked Sets the default value, else resets */
        if ($(this).prop('checked')) {
            if (vlanValue == "") {
                vlanValue = 1;
            }
            $("#id_in_vlan").val(vlanValue);
        } else {
            $("#id_in_vlan").val('');
        }
    }); 
    
    // To set the management n/w vlan value
    $("#id_st_use_vlan").click(function() {
        /* Checks whether the checkbox is ticked Sets the default value, else resets */
        if ($(this).prop('checked')) {
            if (stVlan == "") {
                stVlan = 1;
            }
            $("#id_st_vlan").val(stVlan);
        } else {
            $("#id_st_vlan").val('');
        }
    });
    
    //For the Network verification
//    $('#networkverify').click(function() {
//    	$('#form-modal-body').load(base_url + 'clouds/verifyNetwork/', function () {
//            $('#form-modal').modal('toggle');
//            $('.modal-dialog').css('width', '900px');
//            formAjaxSubmit('#form-modal-body form', '#form-modal');
//            $('.modal-title').html("Network Verification");
//        });    	 
//	});
    
    //To select all check boxes
    $(document).on("click", "#selecctall", function(e) {
        $('input:checkbox').prop('checked', this.checked);
    });
    
    
    //For the search functionality of the logs
    /******************oLD ALERT SECTION*****************************************
    $(document).on("click", "#alert-notify", function(e) {                      *
    	$.ajax({                                                                *
    		type: 'GET',                                                        *
    		url: "/cloud/alert",                                                *
            data: {},                                                           *
            success: function (xhr, ajaxOptions, thrownError) {                 *
               if ( $(xhr).find('.has-error').length > 0 ) {                    *
            	   alert('error');                                              *
               }                                                                *
               else {                                                           *
            	   $("#alert-id").html(xhr);                                    *
               }                                                                *
            },                                                                  *
            error: function (xhr, ajaxOptions, thrownError) {                   *
            }                                                                   *
        });                                                                     *
    });                                                                         *
    ****************************************************************************/
    
/**********************************ALERT SECTION *******************************/
    $(document).on("click", "#alert-notify", function(e) {
        
        // Gets the class for clicked item and unsets the bottom border value
        classVal = $("#alert-notify").parent().attr('class');
        if (classVal.indexOf(" open") > -1) {
            $("#alert-notify").parent().parent().parent().css("border-bottom", "0px none")
        }
        
        // Sets the image to no-bell for alert
        $("#alert-notify > img").attr("src", "/site_media/images/no-icon-bell.png");
        
        $.ajax({
            type: 'GET',
            url: "/thunderalert",
            data: {},
            success: function (xhr, ajaxOptions, thrownError) {
               if ( $(xhr).find('.has-error').length > 0 ) {
                   alert('error');
               }
               else {
                   $("#alert-id").html(xhr);
                   
                   // Display text for no-alert
                   if ($(".view_alert_log").length == 0) {
                       $("#alert-id").html("<li class='no-entries'>No alerts found.</li>");
                   }
                   
                   // Calls the fn to update alert visited status
                   $.ajax({
                       type: 'GET',
                       url: "/updateAlerts",
                       success: function (xhr, ajaxOptions, thrownError) {
                           status = xhr.status;
                       }
                   });
               }
            },
            error: function (xhr, ajaxOptions, thrownError) {
            }
        });
    });    
    
    // To display the alert log popup
    /*$(document).on("click", ".view_alert_log", function(e) {
        
        // Set the log id selected
        var logId = $(this).attr('id');
        // Making the ajax call to get the log details
        $.ajax({
            beforeSend: function(xhr)  {
                xhr.setRequestHeader('X-CSRFToken', window.csrf_val);
            },
            type: 'POST',
            url: "/alertView",
            data: { 'datapost' : logId },
            success: function (xhr, ajaxOptions, thrownError) {
                
               // Checks the response data
               if ($(xhr).find('.has-error').length > 0) {
                   location.reload(); 
               } else {
                   
                   // Display the details in popup
                   $("#alert_log_details").html('<a href="javascript:void(0)" id="alert_close">Close</a>' + xhr);
                   $("#black_overlay").show();
                   $("#alert_log_details").show();
                   $(".backlist").hide();
               }
            },
            error: function (xhr, ajaxOptions, thrownError) {
            }
        });
    });*/
    
    // To close the alert log popup
    $(document).on("click", "#alert_close", function(e) {
        $("#black_overlay").hide();
        $("#alert_log_details").hide();
    });
    
    
    //To reschedule the job
    $(document).on("click", ".view-more", function(e) {
        viewId = $(this).attr('id');  
        $.ajax({
            beforeSend: function(xhr)  {
                xhr.setRequestHeader('X-CSRFToken', window.csrf_val);
            },
            type: 'POST',  
            url: "/alertView",
            data: { 'datapost' : viewId },
            success: function (xhr, ajaxOptions, thrownError) {
               if ( $(xhr).find('.has-error').length > 0 ) {
                   location.reload(); 
               }
               else {
                   $(".allalerts").hide();
                   $("#alert-view").html(xhr);
                   $("#alert-view").show();
               }
            },
            error: function (xhr, ajaxOptions, thrownError) {
            }                
        });
    });
/**********************************ALERT SECTION *******************************/

    
    //To reschedule the job
    $('.reshedule' ).click(function() {
    	rescheduleId = $(this).attr('id'); // table row ID 
    	$.ajax({
    		beforeSend: function(xhr)  {
		     	xhr.setRequestHeader('X-CSRFToken', window.csrf_val);
		    },
    		type: 'POST',  
    		url: "/cloud/resheduleJob",
            data: { 'datapost' : rescheduleId },
            success: function (xhr, ajaxOptions, thrownError) {
               if ( $(xhr).find('.has-error').length > 0 ) {
            	   location.reload(); 
               }
               else {
            	   if (xhr.jobStatus == true) {
            		   successMsg('Job created successfully.');
            	   } else {
            		   errorMsg('Job already exists.');
            	   }
               }
            },
            error: function (xhr, ajaxOptions, thrownError) {
            }                
        });
   	});
    
    /************************************************************************************
    //To reschedule the job                                                             *
    $(document).on("click", ".view-more", function(e) {                                 *
    	viewId = $(this).attr('id');                                                    *
    	$.ajax({                                                                        *
    		beforeSend: function(xhr)  {                                                *
		     	xhr.setRequestHeader('X-CSRFToken', window.csrf_val);                   *
		    },                                                                          *
    		type: 'POST',                                                               *
    		url: "/cloud/jobView",                                                      *
            data: { 'datapost' : viewId },                                              *
            success: function (xhr, ajaxOptions, thrownError) {                         *
               if ( $(xhr).find('.has-error').length > 0 ) {                            *
            	   location.reload();                                                   *
               }                                                                        *
               else {                                                                   *
            	   $(".allalerts").hide();                                              *
            	   $("#alert-view").html(xhr);                                          *
            	   $("#alert-view").show();                                             *
               }                                                                        *
            },                                                                          *
            error: function (xhr, ajaxOptions, thrownError) {                           *
            }                                                                           *
        });                                                                             *
   	});                                                                                 *
    /***********************************************************************************/
    //To show the list back
    $(document).on("click", ".backlist", function(e) {
 	   	$(".allalerts").show();
 	   	$("#alert-view").hide();
    });
    
    //To disable and enable the assign role button
    $(document).on("click", ".serverassign", function(e) {
        $("#configure-role").attr('disabled',true);
        if (($('input.serverassign:checked').length > 0) && ($('input.roleAssign:checked').size() > 0)) {
            $("#configure-role").attr('disabled',false);
        }
    });
    
    //To disable and enable the assign role button
    $(document).on("click", ".roleAssign", function(e) {
        $("#configure-role").attr('disabled',true);
        if (($('input.serverassign:checked').length > 0) && ($('input.roleAssign:checked').size() > 0)) {
            $("#configure-role").attr('disabled',false);
        }
    });
    
    //Removing the select role functionality once we click on the nodes
    //To select the check box for the selected role
//    $(document).on("click", ".serverassign", function(e) {
//        $('input:checkbox').prop('checked', false);
//    	$(this).prop('checked', true);
//    	viewId = $(this).val();
//        $.ajax({
//            beforeSend: function(xhr)  {
//    	        xhr.setRequestHeader('X-CSRFToken', window.csrf_val);
//    	    },
//            type: 'POST',  
//            url: "/clouds/getroleId",
//            data: {viewId: viewId},
//            success: function (xhr, ajaxOptions, thrownError) {
//            	if ( $(xhr).find('.has-error').length > 0 ) {
//                    alert('error');
//                } 
//                else {
//            	   logs = '';
//            	   $("input.roleAssign").attr("disabled", false);
//            	   $.each(xhr, function(key, role) {
//            		   $("input.roleAssign[value="+role.roleId+"]").prop("checked", true);
//            		   $("input.roleAssign[value="+role.roleId+"]").attr("disabled", true);
//            	   });
//                }
//            },
//            error: function (xhr, ajaxOptions, thrownError) {
//            }                
//        }); 
//    });
    
    // To add domain
    $(document).on("click", "#domain_add", function(e) {
    	var cloudList = $('select[name=scope_list]').val();
    	var domainName = $("#domain_name").val();
    	var cloudListValues = "";
    	
    	// Clears the error messages
		$('#domainErr').hide();
		$('#scopeErr').hide();
    	
    	// Check the cloudList
    	if (cloudList) {
    		cloudListValues = cloudList.toString();
    	}
    	
    	// Makes the ajax call to add domain
    	$.ajax({
    	    beforeSend: function(xhr)  {
    	    	xhr.setRequestHeader('X-CSRFToken', window.csrf_val);
    	    },
    		type: 'POST',  
    		url: "/addCloudDomain",
            data: {'cloudList' : cloudListValues, 'domainName' : domainName},
            success: function (xhr, ajaxOptions, thrownError) {
                if (xhr.status == true) {
                    var domainName = xhr.domainName;
                    var cloudNameStr = xhr.cloudNameStr;
                    var domainId = xhr.domainId;
                    $('#cloudDomainList').append('<div class="col-sm-12">' +
                                                    '<div class="patch-releases-left new-entry">' +
                                                        '<div class="col-sm-6 textBold">' + domainName + '</div>' +
                                                        '<div class="col-sm-6">' + cloudNameStr + '</div>' +
                                                    '</div>' +
                                                    '<a class="domain-delete-icon" id="domain-' + domainId + '" onclick="javascript:void(0)" href="#">' +
                                                    '<div class="col-sm-1 patch-releases-btn">X</div></a></div>');
                    
                    $('#domain_name').val('');
                    /*$("#scope_list").multiSelect("clearSelection");
                    $("#scope_list").multiSelect("refresh");*/
                    $('#scope_list').children(':selected').removeProp('selected');
                    $("#scope_list option:selected").removeAttr("selected");
                    return false;
                } else {
                	$('#domainErr').show();
                	$('#scopeErr').show();
                	$('#domainErrText').html(xhr.message_domain);
                	$('#scopeErrText').html(xhr.message_scope);
                }
            },
            error: function (xhr, ajaxOptions, thrownError) {
            }                
        });
    	
    });
    
    // To add new role
    $(document).on("click", "#role_add", function(e) {
    	
    	var permissionText = $('#permission_list option:selected').text();
    	var domainText = $('#domain_list option:selected').text();
    	var data = $('#role_add_form').serialize();
    	
    	// Clears the error messages
		$('#cloudDomainErr').hide();
		$('#permissionErr').hide();
		$('#roleErr').hide();
    	
    	// Makes the ajax call to add domain
    	$.ajax({
    		beforeSend: function(xhr)  {
                    xhr.setRequestHeader('X-CSRFToken', window.csrf_val);
    		},
    		type: 'POST',
    		url: "/addDomainRole",
    		data: data + "&permissionText=" + permissionText + "&domainText=" + domainText,
    		success: function (xhr, ajaxOptions, thrownError) {
                if (xhr.status == true) {
                    var domainName = xhr.domainName;
                    var permissionName = xhr.permissionName;
                    var roleName = xhr.roleName;
                    var roleId = xhr.roleId;
                    $('#domainRoleList').append('<div class="col-sm-12">' +
                                                    '<div class="patch-releases-left new-entry">' +
                                                        '<div class="col-sm-4 textBold">' + roleName +'</div>' +
                                                        '<div class="col-sm-4">' + domainName + '</div>' +
                                                        '<div class="col-sm-3">' + permissionName + '</div>' +
                                                    '</div>' +
                                                    '<a class="role-delete-icon" id="role-' + roleId + '" onclick="javascript:void(0)" href="#roles_tab">' +
                                                        '<div class="col-sm-1 patch-releases-btn">X</div>' +
                                                    '</a>' +
                                                '</div>');
                    
                    $('#role_name').val('');
                    $('#domain_list').children(':selected').removeProp('selected');
                    $("#domain_list option:selected").removeAttr("selected");
                    $('#permission_list').children(':selected').removeProp('selected');
                    $("#permission_list option:selected").removeAttr("selected");
//	            		return false;
                } else {
                    $('#roleErr').show();
                    $('#cloudDomainErr').show();
                    $('#permissionErr').show();
                    $('#cloudDomainErrText').html(xhr.message_domain);
                    $('#permissionErrText').html(xhr.message_permission);
                    $('#roleErrText').html(xhr.message_role);
                }
            },
            error: function (xhr, ajaxOptions, thrownError) {
            } 
        });
    });
    
    // To add new user
    $(document).on("click", "#user_add", function(e) {
    	
        var roleText = $('#role_list option:selected').text();
        var data = $('#user_add_form').serialize();
    	
        // Clears the error messages
        $('#accountErr').hide();
        $('#userErr').hide();
        $('#passwordErr').hide();
        $('#emailErr').hide();
        $('#userRoleErr').hide();
    	
        // Makes the ajax call to add domain
        $.ajax({
            beforeSend: function(xhr)  {
                xhr.setRequestHeader('X-CSRFToken', window.csrf_val);
            },
            type: 'POST',
            url: "/addUser",
            data: data + "&roleText=" + roleText,
            success: function (xhr, ajaxOptions, thrownError) {
                if (xhr.status == true) {
                    var userName = xhr.userName;
                    var roleName = xhr.roleName;
                    var userId = xhr.userId;
                    $('#userRoleList').append('<div class="col-sm-12">' +
                                                   '<div class="patch-releases-left new-entry">' +
                                                       '<div class="col-sm-6 textBold">' + roleName +'</div>' +
                                                       '<div class="col-sm-6">' + userName + '</div>' +
                                                   '</div>' +
                                                   '<a class="user-delete-icon" id="user-' + userId + '" onclick="javascript:void(0)" href="#users_tab">' +
                                                       '<div class="col-sm-1 patch-releases-btn">X</div>' +
                                                   '</a>' +
                                               '</div>');
                        
                    $('#account_name').val('');
                    $('#user_name').val('');
                    $('#password').val('');
                    $('#email').val('');
                    $('#role_list').children(':selected').removeProp('selected');
                    $("#role_list option:selected").removeAttr("selected");
                } else {
                    $('#userRoleErr').show();
                    $('#accountErr').show();
                    $('#passwordErr').show();
                    $('#userErr').show();
                    $('#emailErr').show();
                    $('#userRoleErrText').html(xhr.message_role);
                    $('#accountErrText').html(xhr.message_account);
                    $('#passwordErrText').html(xhr.message_password);
                    $('#userErrText').html(xhr.message_user);
                    $('#emailErrText').html(xhr.message_email);
                }
            },
            error: function (xhr, ajaxOptions, thrownError) {
            } 
        }); 
    });
    
    // To handle domain list data display
    $(document).on("click", ".tabViews a", function(e) {
    	var href = (this.href).toString();
    	hrefArr = href.split("#");
    	
    	// href checking
    	if (hrefArr[1] == 'roles_tab') {
        	
            // Makes the ajax call to load domain
            $.ajax({
                beforeSend: function(xhr) {
                    xhr.setRequestHeader('X-CSRFToken', window.csrf_val);
                },
                type: 'GET',
                url: "/getDomainList",
                data: "",
                success: function (xhr, ajaxOptions, thrownError) {
                	
                    // Removes the options from drop down and appends default
                    $('#domain_list').empty().append("<option>Select Domain</option>");
                	
                    // If the request status is true 
                    if (xhr.status == true) {
                    	
                        // Sets count
                        var count = 0;
                        
                        // Populate the domain data 
                        $.each(xhr.domainList, function(key, domain) {
                            $('#domain_list').append("<option value='" + domain.id + "'>" + domain.name + "</option>");
                        });
                        $('#domainRoleList').html("");
                        
                        // Populate the role data
                        $.each(xhr.roleList, function(key, roles) {
                            
                            // Sets default value
                            var display_del = "";
                            
                            // Checks if it is the root user role
                            if (roles.domain_id == 1) {
                                display_del = "";
                            } else {
                                display_del = "<a href='#roles_tab' onclick='javascript:void(0)' id='role-" + roles.role_id + 
                                                "' class=role-delete-icon><div class='col-sm-1 patch-releases-btn'>X</div></a>";
                            }
                            
                            // Sets and appends to the div to display
                            $('#domainRoleList').append("<div class='col-sm-12'><div class='patch-releases-left'>" + 
                                                        "<div class='col-sm-4 textBold'>" + roles.role + "</div>" + 
                                                        "<div class='col-sm-4'>" + roles.domain + "</div>" + 
                                                        "<div class='col-sm-3'>" + roles.permission + "</div>" + 
                                                        "</div>" + display_del + "</div>");
                            
                            // counter update
                            count++;
                        }); 
                    }
                },
                error: function (xhr, ajaxOptions, thrownError) {
                }
            });
    		
    	} else if (hrefArr[1] == 'users_tab') {
        	
            // Makes the ajax call to load domain
            $.ajax({
                beforeSend: function(xhr) {
                    xhr.setRequestHeader('X-CSRFToken', window.csrf_val);
                },
                type: 'GET',  
                url: "/getRoleList",
                data: "",
                success: function (xhr, ajaxOptions, thrownError) {
                	
                    // Removes the options from drop down and appends the default
                    $('#role_list').empty().append("<option>Select Scope</option>");
                    $('#userRoleList').html("");
                	
                    // If the request status is true
                    if (xhr.status == true) {
                        
                        // Sets count
                        var count = 0;
                	
                        // Populate the data 
                        $.each(xhr.roleList, function(key, role) {
                            if (role.domain_id != 1) {
                                $('#role_list').append("<option value='" + role.role_id + "'>" + role.role + "</option>");
                            }
                        });
                        
                        // Populate the role data
                        $.each(xhr.userList, function(key, user) {
                            
                            // Sets default value
                            var display_del = "";
                            
                            // Checks if it is the root user
                            if (user.user_id == 1) {
                                display_del = "";
                            } else {
                                display_del = "<a  href='#users_tab' onclick='javascript:void(0)' id='user-" + user.user_id + 
                                "' class=user-delete-icon><div class='col-sm-1 patch-releases-btn'>X</div></a>";
                            }
                            
                            // Sets and appends to the div to display
                            $('#userRoleList').append("<div class='col-sm-12'><div class='patch-releases-left'>" + 
                                                        "<div class='col-sm-6 textBold'>" + user.role + "</div>" + 
                                                        "<div class='col-sm-6'>" + user.user + "</div>" + 
                                                        "</div>" + display_del + "</div>");
                            
                            // counter update
                            count++;
                        });
                    }
                },
                error: function (xhr, ajaxOptions, thrownError) {
                }
            });
            
    	}
    });
    
  //For the remove nodes
    $('#deploy').click(function() {
        $.ajax({
            beforeSend: function(xhr)  {
                xhr.setRequestHeader('X-CSRFToken', window.csrf_val);  
            },
            type: 'POST',
            url: "/deploythunder/",
            data: { 'datepost' : '' },
            success: function (xhr, ajaxOptions, thrownError) {
               if ( $(xhr).find('.has-error').length > 0 ) {    
               }
               else {
                   if (xhr.status == true) {
                       successMsg(xhr.text);
                   } else {
                       errorMsg(xhr.text);
                   }
               }
            },
            error: function (xhr, ajaxOptions, thrownError) {
            }
        });
    });
    
    /****************************************************************************************************************    
    // To display the alert log popup                                                                               *
    $(document).on("click", ".view_alert_log", function(e) {                                                        *
        
        // Set the log id selected                                                                                  *
        var logId = $(this).attr('id');                                                                             *
                                                                                                                    *
        // Making the ajax call to get the log details                                                              *
        $.ajax({                                                                                                    *
            beforeSend: function(xhr)  {                                                                            *
                xhr.setRequestHeader('X-CSRFToken', window.csrf_val);                                               *
            },                                                                                                      *
            type: 'POST',                                                                                           *
            url: "/cloud/jobView",                                                                                  *
            data: { 'datapost' : logId },                                                                           *
            success: function (xhr, ajaxOptions, thrownError) {                                                     *
                                                                                                                    *
               // Checks the response data                                                                          *
               if ($(xhr).find('.has-error').length > 0) {                                                          *
                   location.reload();                                                                               *
               } else {                                                                                             *
                                                                                                                    *
                   // Display the details in popup                                                                  *
                   $("#alert_log_details").html('<a href="javascript:void(0)" id="alert_close">Close</a>' + xhr);   *
                   $("#black_overlay").show();                                                                      *
                   $("#alert_log_details").show();                                                                  *
                   $(".backlist").hide();                                                                           *
               }                                                                                                    *
            },                                                                                                      *
            error: function (xhr, ajaxOptions, thrownError) {                                                       *
            }                                                                                                       *
        });                                                                                                         *
    });                                                                                                             *
                                                                                                                    *
/*********************************************************************************************************************/    
    // To handle the rbac attributes' delete request
    $(document).on("click", ".domain-delete-icon", function(e) {
        
        // Asks for confirmation        
        if (confirm("Do you want to delete the entry?")) {
            
            // Setting the data variables
            var elementId = $(this).attr('id');
            var splitStr = elementId.toString().split('-');
            var domainId = splitStr[1];
            var data = {"domainId" : domainId};
            var status;
            
            // Calls the ajax call
            status = makeAjaxPostRequest('/deleteCloudDomain', data, elementId);
        }
    });
    
    // To handle the rbac attributes' delete request
    $(document).on("click", ".role-delete-icon", function(e) {
        
        // Asks for confirmation        
        if (confirm("Do you want to delete the entry?")) {
        
            // Setting the data variables
            var elementId = $(this).attr('id');
            var splitStr = elementId.toString().split('-');
            var roleId = splitStr[1];
            var data = {"roleId" : roleId};
            var status;
            
            // Calls the ajax call
            status = makeAjaxPostRequest('/deleteDomainRole', data, elementId);
            
        }
    });
    
    // To handle the rbac attributes' delete request
    $(document).on("click", ".user-delete-icon", function(e) {
        
        // Asks for confirmation
        if (confirm("Do you want to delete the entry?")) {
        
            // Setting the data variables
            var elementId = $(this).attr('id');
            var splitStr = elementId.toString().split('-');
            var userId = splitStr[1];
            var data = {"userId" : userId};
            var status;
            
            // Calls the ajax call
            status = makeAjaxPostRequest('/deleteRoleUser', data, elementId);
        }
        
    });
    
    function makeAjaxPostRequest(ajaxUrl, postData, elementId) {
        
        var status = false;
        
        // Making the ajax call to get the log details
        $.ajax({
            beforeSend: function(xhr)  {
                xhr.setRequestHeader('X-CSRFToken', window.csrf_val);
            },
            type: 'POST',
            url: ajaxUrl,
            data: postData,
            async: false,
            success: function (xhr, ajaxOptions, thrownError) {
                status = xhr.status;
                $("#" + elementId).parent().remove();
            },
            error: function (xhr, ajaxOptions, thrownError) {
                status = false;
            }
        });
        return status;
    }
    
    // To close the alert log popup
    $(document).on("click", "#alert_close", function(e) {
        $("#black_overlay").hide();
        $("#alert_log_details").hide();
    });
    
    // To check the access and display the error message if not
    var notAuthenticated = getUrlVars()['notAuthenticated'];
    if (notAuthenticated != null) {
        errorMsg('You are not authorized!');
    }
    
    // To handle the alert delete request
    $(document).on("click", "#delete-alert", function(e) {
        var data = $('#alert_del_form').serialize();
        $.ajax({
            beforeSend: function(xhr)  {
                xhr.setRequestHeader('X-CSRFToken', window.csrf_val);
            },
            type: 'POST',
            url: "/thunderalert",
            data: data + '&view-all=true',
            success: function (xhr, ajaxOptions, thrownError) {
               if ( $(xhr).find('.has-error').length > 0 ) {
                   alert('error');
               }
               else {
                   $("#form-modal-body").html(xhr);
                   
                   // Sets the height for the log display container
                   eleCount = $(".alert-content").length;
                   heightVal = eleCount * 50;
                   if (heightVal > 250) {
                       $(".bdr-pop").css({height : 250 + 'px'});
                   } else {
                       $(".bdr-pop").css({'min-height' : heightVal + 'px'});
                       $(".bdr-pop").css({overflow : 'hidden'});
                   }
                   
                   // Displays empty list
                   if (eleCount == 0) {
                       $(".bdr-pop").css({height : '50px'});
                       $(".bdr-pop").css({overflow : 'hidden'});
                       $(".bdr-pop").html("<p class='log-cont'>No alerts found</p>");
                   }
               }
            },
            error: function (xhr, ajaxOptions, thrownError) {
            }
        });
    });
    
    /* To handle the modal close button */
    $("button.close").click(function(e) {
        $("#form-modal-body").removeClass('rm-pad-value role-base');
        $("#form-modal-body > div.row").removeClass('rm-pad-value');
        $("#form-modal-body > ul.roleUl").removeClass('rm-pad-value');
    });
    
    // To handle the normal click action
    $("body").click(function() {
        aEle = $("a[aria-expanded='true']");
        $.each(aEle, function() {
            borderWidth = $(this).parent().parent().parent().css("border-bottom-width");
            if (borderWidth == "0px") {
                $(this).parent().parent().parent().css("border-bottom", "1px solid #d6d6d6");
            }
        });
    });
    
    // To handle tasks click
    $("#tasks-menu").click(function() {
        $("#tasks-menu").css("border-bottom", "0px none");
    });
    
    //To update the disk values in the box
    $(document).on("click", ".system-space-config", function(e) {
        system = $(this).prev().prev().find('input').val()
        data = $(this).parent().next().find('input[type="text"]').val()
        total = $(this).parent().next().find('input[type="hidden"]').val();
        systemNew = total - data;
        $(this).prev().prev().find('input').val(total);
        $(this).parent().next().find('input[type="text"]').val(0);       
        
    });

    //To update the disk values in the box
    $(document).on("click", ".data-space-config", function(e) {
        data = $(this).prev().prev().find('input[type="text"]').val();
        system = $(this).parent().prev().find('input[type="text"]').val()
        total = $(this).prev().prev().find('input[type="hidden"]').val();
        dataNew = total - system_space;
        $(this).parent().prev().find('input[type="text"]').val(system_space);
        $(this).prev().prev().find('input[type="text"]').val(dataNew);
    });
    
    //To update the disk values in the box
    $(document).on("click", ".data-space-config2", function(e) {
        data = $(this).prev().prev().find('input[type="text"]').val();
        system = $(this).parent().prev().find('input[type="text"]').val()
        total = $(this).prev().prev().find('input[type="hidden"]').val();
       
        $(this).prev().prev().find('input[type="text"]').val(total);
        $(this).parent().prev().find('input[type="text"]').val(0)
    });
});

function chkDiskField() {
    var $inputs = $('#disk-Form :input[type="text"]');
    var sub = 1;
    $inputs.each(function() {
        if ($.isNumeric($(this).val()) == false) {
            sub = 0;
        }
    });
    
    //To show the error if disk drives exceeds the total
    var $fields = $('.calc-disk');
    counter = 0;
    $fields.each(function() {
        storageData = parseFloat($("#id_form-"+counter+"-storage_space").val());
        totalData = parseFloat($("#id_form-"+counter+"-total_space").val());
        systemData = parseFloat($("#id_form-"+counter+"-system_space").val());
        calcData = parseFloat(storageData) + parseFloat(systemData);
        $("#id_form-"+counter+"-storage_space").css('border', '1px solid #d3d3d3');
        if(totalData < calcData) {
            $("#id_form-"+counter+"-storage_space").css('border', '1px solid #FF0000');
            sub = 2;
        }
        counter = counter + 1;
    });
    
    //If sub is 1 no error,0 means values are not integers, 2 means values exceeds the total
    if (sub == 1) {
        $("#disk-Form").submit();
    } else if (sub == 0){
        errorMsg('Only integer values are accepted.');
    } else{
        errorMsg('Disk values exceeds total space.');
    }
}
// To show the success message in the header for server actions
function successMsg(text){
	$('.status').removeClass('errorStatus');
	$('.statusText').html(text).show();
	$('.status').addClass('successStatus');
	$('.status').show().delay(4000).fadeOut();
}

//To show the error message in the header for server actions
function errorMsg(text){
	if (text != '') {
		$('.status').removeClass('successStatus');
		$('.status').addClass('errorStatus');
		$('.statusText').html(text).show();
		$('.status').show().delay(4000).fadeOut();
	}
}

/*
 * Function to get the get params from URL @returns get params
 */
function getUrlVars() {
    var vars = {};
    var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi,
            function(m, key, value) {
                vars[key] = value;
            });
    return vars;
}

//To delete the cloud from the list
function confirmUpdate(text) {
    if(confirm(text)) {
      return true
    }
    else {
      return false
    }
}
