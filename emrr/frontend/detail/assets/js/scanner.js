$(document).ready(function() {
    $('#uploadForm').submit(function(e) {
        e.preventDefault();  // Prevent the default form submission that leads to a page reload

        var formData = new FormData(this); // Collect all data from the form

        $.ajax({
            url: "{{ url_for('scanner') }}", // Endpoint on the server that processes the POST request
            type: 'POST',
            data: formData,
            contentType: false,  // This must be set to false to send a FormData object
            processData: false,  // This must also be set to false to send a FormData object
            success: function(response) {
                // This function processes the response received from the server
                if (response.url) {
                    $('#blah').attr('src', response.url);  // Update the image preview
                } else if (response.error) {
                    alert('Error: ' + response.error);  // Show an error message
                }
            },
            error: function(xhr, status, error) {
                // This function handles any errors that occur during the HTTP request
                alert('An error occurred: ' + error);
            }
        });
    });
});


    // Optional: Function to show the final image and update form fields (if applicable)
    function showFinalImage() {
        $('#loading').show();
        $('#finalImageDiv').hide();

        var randomDelay = Math.floor(Math.random() * (9000 - 3000 + 1)) + 3000;
        
        setTimeout(function() {
            $('#loading').hide();
            $('#finalImageDiv').show();
            // Example: Update form fields or handle other UI updates
        }, randomDelay);
    }
});