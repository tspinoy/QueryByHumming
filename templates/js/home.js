// http://blog.teamtreehouse.com/uploading-files-ajax

/* ------------------------------------------------------------------------------------------------------------------ *
 * ------------------------------------------------- Add a new file ------------------------------------------------- *
 * ------------------------------------------------------------------------------------------------------------------ */
var addNewFileForm = document.getElementById("add-new-file-form");
var fileSelect = document.getElementById("select-file-to-add");
var uploadButton = document.getElementById("upload-new-file-button");

addNewFileForm.onsubmit = function(event) {
  event.preventDefault();

  // Update button text.
  uploadButton.innerHTML = 'Uploading...';

  // Get the selected files from the input.
  var files = fileSelect.files;

  // Create a new FormData object.
  var formData = new FormData();

  // Loop through each of the selected files. (for in case you decide to allow the user to select multiple files at once)
  for (var i = 0; i < files.length; i++) {
      var file = files[i];

      // Check the file type.
      if (!file.type.match('audio.*')) {
          continue;
      }

      // Add the file to the request.
      console.log(file.name);
      formData.append('uploadFile', file, file.name);
  }

  // Set up the request.
  var xhr = new XMLHttpRequest();

  // Open the connection.
  xhr.open('POST', 'server.py', true);

  // Set up a handler for when the request finishes.
  xhr.onload = function () {
      if (xhr.status === 200) {
          // File(s) uploaded.
          uploadButton.innerHTML = 'Upload';
          alert('Your file has successfully been uploaded!')
      } else {
          alert('An error occurred!');
      }
  };

  // Send the Data.
  xhr.send(formData);
};

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

var searchForm = document.getElementById("search-form");
searchForm.onsubmit = function(event){
    var radioresult = {};
};

function enableUploadButton(){
    uploadButton.disabled = false;
}

function download() {
    alert("The function to download a sound from the database has to be implemented.");
}