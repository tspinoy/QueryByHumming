// import tables.js to get information about tables (column-numbers, the sorting algorithm, etc)
var script = document.createElement('script');
script.src = "tables.js";
document.head.appendChild(script);

var filledContentTable = false;

function fillContentTable() {
    if(!filledContentTable) {
        $.get({
            url: "/content.json",
            dataType: 'json',
            success: function (data, s, j) {
                console.log(data);
                $("#contentTable").append("<tr><th>#</th><th>Artist</th><th>Title</th><!-- <th>Listen</th> --></tr>");
                $.each(data.content, function (index, result) {
                    $("#contentTable").append("<tr><td>" + (index + 1) + "</td><td>" + result.artist + "</td><td>" + result.title + "</td><!-- <td>" + result.listen + "</td> --></tr>");
                })
            }
        });
        filledContentTable = true; // otherwise you can keep adding the same information
    }
    $("#loadingInformation").html("All content is loaded.");
}