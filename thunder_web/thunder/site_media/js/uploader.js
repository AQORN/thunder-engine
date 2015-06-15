/**
* File to handle the ajax file uploading. 
*/

$( document ).ready(function() {
    
    // Variable to store your files
    var files;

    // Add events
    $('input[type=file]').on('change', prepareUpload);

    // Grab the files and set them to our variable
    function prepareUpload(event) {
        files = event.target.files;
    }
    
    // Handle the file upload
    $('#uploadPatchFileForm').on('submit', uploadFiles);

    // Catch the form submit and upload the files
    function uploadFiles(event) {
        
        event.stopPropagation(); // Stop stuff happening
        event.preventDefault(); // Totally stop stuff happening

        // START A LOADING SPINNER HERE
        // Create a formdata object and add the files
        var data = new FormData();
        $.each(files, function(key, value) {
            data.append(key, value);
        });

        // Making the ajax call
        $.ajax({
            beforeSend: function(xhr)  {
                xhr.setRequestHeader('X-CSRFToken', window.csrf_val);  
            },
            url: '/updatePatch/',
            type: 'POST',
            data: data,
            cache: false,
            dataType: 'json',
            processData: false, // Don't process the files
            contentType: false, // Set content type to false as jQuery will tell the server its a query string request
            success: function(data, textStatus, jqXHR) {
                
                // Style changes for message display
                $('#update_status_display').css({color : data.status ? 'green' : 'red'}).html(data.message).show();
                $('#update_status_display').show().delay(4000).fadeOut();
                
                // Reset the form
                if (data.status == true) {
                    $('#uploadPatchFileForm')[0].reset();
                    
                    // Refresh the contents
                    makeAjaxGETRequest('/updateThunder/', {'refresh' : true}, 'installed-patch-version-content');
                }
            },
            error: function(jqXHR, textStatus, errorThrown) {

                 // Handle errors here
                 console.log('ERRORS: ' + textStatus);
                 // STOP LOADING SPINNER
            },
            complete: function() {
                // STOP LOADING SPINNER
            }
        });
    }
    
    // Handling the form submission
    function submitForm(event, data) {
        
        // Create a jQuery object from the form
        $form = $(event.target);

        // Serialize the form data
        var formData = $form.serialize();

        // You should serialise the file names
        $.each(data.files, function(key, value) {
            formData = formData + '&filenames[]=' + value;
        });

        // Making the ajax call
        $.ajax({
            beforeSend: function(xhr)  {
                xhr.setRequestHeader('X-CSRFToken', window.csrf_val);  
            },
            url: '/updatePatch/',
            type: 'POST',
            data: formData,
            cache: false,
            dataType: 'json',
            success: function(data, textStatus, jqXHR) {
            },
            error: function(jqXHR, textStatus, errorThrown) {
                
                console.log('ERRORS: ' + textStatus);
            },
            complete: function() {
                
                // STOP LOADING SPINNER
            }
        });
    }
    
    // Handles the upload file button action
    $("#upload-patch").click(function(e) {
        
        // Checks if a file is selected for upload
        if (($("#patch_file").val()).length == 0) {
            
            // Style changes for message display
            $('#update_status_display').css({color : 'red'}).html('Please select a patch file of .micro / .macro format').show();
            $('#update_status_display').show().delay(4000).fadeOut();
            return false;
        }
        
        // Submits the form
        $("#uploadPatchFileForm").submit();
    });    

    // Function to make ajax get calls
    function makeAjaxGETRequest(ajaxUrl, getData, elementId) {
        
        var status = false;
        
        // Making the ajax call to get the log details
        $.ajax({
            type: 'GET',
            url: ajaxUrl,
            data: getData,
            async: false,
            success: function (xhr, ajaxOptions, thrownError) {
                
                // Initialise the data variable
                status = xhr.status;
                displayStr = "";
                
                // Empties the content
                $('#' + elementId).html("");
                
                // Display the installed patch versions
                $.each(xhr.updatedVersions, function(key, patchVersion) {
                    
                    // Assigns refreshed entry list
                    displayStr += '<div class="col-sm-12">' +
                                  '<div class="patch-releases-left col-sm-11">' + patchVersion.version + '</div>';
                    
                    // Checks if rollback is applicable
                    if (patchVersion.can_rollback) {
                        displayStr += '<div class="col-sm-1 patch-releases-btn"><a href="#" id="patchVersion-' + patchVersion.id + '" class="rollback-version">x</a></div>';
                    }
                    
                    // Assigns refreshed entry list    
                    displayStr += '</div>';
                });
                
                // Assigns the content
                $('#' + elementId).html(displayStr);
            },
            error: function (xhr, ajaxOptions, thrownError) {
                status = false;
            }
        });
        return status;
    }
    
    // Handles the patch rollback request
    $(document).on("click", ".rollback-version", function(e) {
        
        // Sets the version id
        var elementId = $(this).attr('id');
        var splitStr = elementId.toString().split('-');
        var versionId = splitStr[1];
        var data = {"versionId" : versionId};
        
        // Making the ajax call to get the log details
        $.ajax({
            type: 'GET',
            url: '/rollBackPatch/',
            data: data,
            async: false,
            success: function (data, ajaxOptions, thrownError) {
                
                // Style changes for message display
                $('#update_status_display').css({color : data.status ? 'green' : 'red'}).html(data.message).show();
                $('#update_status_display').show().delay(4000).fadeOut();
                
                // Refresh the contents
                if (data.status == true) {
                    makeAjaxGETRequest('/updateThunder/', {'refresh' : true}, 'installed-patch-version-content');
                }
            },
            error: function (xhr, ajaxOptions, thrownError) {
            }
        });
    });
});