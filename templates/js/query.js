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