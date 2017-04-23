/* ------------------------------------------------------------------------------------------------------------------ *
 * ---------------------------------------------- Query with new file ----------------------------------------------- *
 * ------------------------------------------------------------------------------------------------------------------ */
// import tables.js to get information about tables (column-numbers, the sorting algorithm, etc)
var script = document.createElement('script');
script.src = "tables.js";
document.head.appendChild(script);

var queryResultsTableFilled = false;

$(function() {
    $('#upload-query-button').click(function() {
        var files = document.getElementById("upload-query").files;
        if (!queryResultsTableFilled) {
            if (files.length < 1) {
                alert("Please select a file.");
            }
            else {
                var form_data = new FormData();
                form_data.append("queryFile", files[0]);
                $.ajax({
                    type: 'POST',
                    url: '/dbFindByQuery.json',
                    data: form_data,
                    dataType: 'json',
                    contentType: false,
                    cache: false,
                    processData: false,
                    async: false,
                    success: function (response, s, j) {
                        $("#queryResultsTable").append("<tr><th>#</th><th>Title</th><th>Score</th><th>Listen</th></tr>");
                        $.each(response.matches, function (index, result) {
                            $("#queryResultsTable").append("<tr><td>" + (index + 1) + "</td><td>" + result.title + "</td><td>" + result.score + "</td><td>" + result.listen + "</td></tr>");
                        });
                        sortTable("queryResultsTable", scoreColumn, comparators["sort normal"]);
                    }
                });
                queryResultsTableFilled = true;
            }
        }
    });
});

/* ------------------------------------------------------------------------------------------------------------------ *
 * ----------------------------------------------------- Other ------------------------------------------------------ *
 * ------------------------------------------------------------------------------------------------------------------ */

var startbutton = document.getElementById("startRecordButton");
var stopbutton = document.getElementById("startRecordButton");
var stream = "";

function startRecordingAudio() {
    navigator.mediaDevices.getUserMedia({
        audio: true,
        video: false
    }).then(gotStream).catch(logError);
    startbutton.disabled = true;
}

function gotStream(stream) {
    stream.getTracks().forEach(function (track) {
        track.onended = function () {
            startbutton.disabled = stream.active;
        };
    });
    stopbutton.disabled = false;
    stream = this.stream;
    console.log(stream);
}

function logError(error) {
    log(error.name + ": " + error.message);
}

function stopRecordingAudio() {
    navigator.mediaDevices.getUserMedia({
        audio: true,
        video: false
    }).then(gotStream).catch(logError);
    startbutton.disabled = true;
}

var searched = false;
$(function(){
    $("#inputfile").on("change" , function(){
        var fileInput = document.getElementById("inputfile");
        var fileList = fileInput.files;
        if(fileList.length != 1){
            alert("Please insert exactly one file!");
            return false;
        }

        var file = fileList[0];
        console.log("fileInput = " + fileInput);
        console.log("fileList = " + fileList);
        console.log("file = " + fileList[0]);
        console.log("filetype = " + file.type);
        console.log("filetype indexof = " + (file.type.indexOf('.') + 1));

        if(file.type.indexOf("mp3") < 0){
            alert("Please choose a sound!");
        }
    })
});

function search() {
    if(!searched) {
        $.get({
            url: "/match.json",
            dataType: 'json',
            success: function (data, s, j) {
                $.each(data.results, function (index, result) {
                    $("#results").append("<tr><td>" + (index + 1) + "</td><td>" + result.title + "</td><td>" + result.listen + "</td></tr>");
                })
            }
        });
        searched = true;
    }
}

/*
navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia;
var record = document.querySelector("#startRecordButton");
var stop = document.querySelector("#stopRecordButton");
var soundClips = document.querySelector('.sound-clips');
if (navigator.getUserMedia) {
    console.log('getUserMedia supported.');
    navigator.getUserMedia (
        // constraints - only audio needed for this app
        {
            audio: true
        },

        // Success callback
        function(stream) {


        },

        // Error callback
        function(err) {
            console.log('The following gUM error occured: ' + err);
        }
    );
} else {
    console.log('getUserMedia not supported on your browser!');
}

// Capturing the media stream
var mediaRecorder = new MediaRecorder();
record.onclick = function() {
    mediaRecorder.start();
    console.log(mediaRecorder.state);
    console.log("recorder started");
    record.style.background = "red";
    record.style.color = "black";
};

var chunks = [];
mediaRecorder.ondataavailable = function(e) {
    chunks.push(e.data);
};

stop.onclick = function() {
    mediaRecorder.stop();
    console.log(mediaRecorder.state);
    console.log("recorder stopped");
    record.style.background = "";
    record.style.color = "";
};

*/