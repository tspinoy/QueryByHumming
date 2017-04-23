// http://blog.teamtreehouse.com/uploading-files-ajax

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
                dataType: 'json',
                contentType: false,
                cache: false,
                processData: false,
                async: false,
                success: function (response, s, j) {

                }
            });
        }
    });
});

/* ------------------------------------------------------------------------------------------------------------------ *
 * ---------------------------------------------------- Redirect ---------------------------------------------------- *
 * ------------------------------------------------------------------------------------------------------------------ */

function goToQueryPage() {
    window.location.href = "query.html";
}

/* ------------------------------------------------------------------------------------------------------------------ *
 * ------------------------------------------------------ Other ----------------------------------------------------- *
 * ------------------------------------------------------------------------------------------------------------------ */

function added() {
    //alert("The function to add a sound has to be implemented.");
    var file = document.getElementById("addNewSound").files[0].name;
    console.log("file = " + file);
    $.get({
        url: "/dbFindByID.json",
        //data: "query:"aaabbbaaa", goal:"aaababaaa",
        dataType: 'json',
        //data: file,
        success: function (data, s, j) {
            console.log(data);
            $("#addFileSuccess").html("Your file is added!");
        },
        error: function(p, s, t){
            console.log("hier een fout");
            console.log("jqXHR = " + p);
            console.log("textStatus = " + s);
            console.log("errorThrown = " + t);
        }
    });
}