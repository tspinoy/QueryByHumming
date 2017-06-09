/* ------------------------------------------------------------------------------------------------------------------ *
 * ------------------------------------------------- Add a new file ------------------------------------------------- *
 * ------------------------------------------------------------------------------------------------------------------ */
$(function() {
    $('#upload-new-file-button').click(function() {
        var files = document.getElementById("file-to-add").files;
        if (files.length < 1) {
            alert("Please select a file.");
        }
        else {
            $('#uploadInformation').html("Uploading ...");
            var form_data = new FormData();
            var title = window.prompt("Please enter the title of the sound", "No Title");
            var artist = window.prompt("Please enter the artist of the sound", "No Artist");
            form_data.append("uploadFile", files[0]);
            form_data.append("title", title);
            form_data.append("artist", artist);
            $.ajax({
                type: 'POST',
                url: '/dbAdd.json',
                data: form_data,
                contentType: false,
                cache: false,
                processData: false,
                async: false,
                success: function () {
                    $('#uploadInformation').html("Upload succeeded!");
                },
                error: function(xhr, ajaxOptions, thrownError) {
                    $('#uploadInformation').html("Something went wrong, please try again.");
                }
            });
        }
    });
});