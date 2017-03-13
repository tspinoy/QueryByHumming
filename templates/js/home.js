function add() {
    //alert("The function to add a sound has to be implemented.");
    $.get({
        url: "/match.json",
        //data: "query:"aaabbbaaa", goal:"aaababaaa",
        dataType: 'json',
        success: function (data, s, j) {
            $("#test").html(data.results[1].title);
            //console.log("data" + data.result.test);
        },
        error: function(p, s, t){
            console.log("hier een fout");
            console.log("jqXHR = " + p);
            console.log("textStatus = " + s);
            console.log("errorThrown = " + t);
        }
    });
}
function gotoQueryPage() {
    window.location.href = "query.html";
}
function download() {
    alert("The function to download a sound from the database has to be implemented.");
}