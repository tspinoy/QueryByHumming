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
function goToQueryPage() {
    window.location.href = "query.html";
}
function download() {
    alert("The function to download a sound from the database has to be implemented.");
}