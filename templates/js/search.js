// import tables.js to get information about tables (column-numbers, the sorting algorithm, etc)
var script = document.createElement('script');
script.src = "tables.js";
document.head.appendChild(script);

var firstSearch = true;

$(function() {
    $('#search-button').click(function() {
        var artist = document.getElementById("artist-textfield").value;
        var title  = document.getElementById("title-textfield").value;
        if(artist === "" && title === ""){
            $('#inputError').html("You must give an artist, a title or both.")
        }
        else {
            $('#inputError').html("");
            $('#loadingInformation').html("Results are loading ...");
            clearTable("searchResultsTable");
            var form_data = new FormData();
            form_data.append("artist", artist);
            form_data.append("title", title);
            $.ajax({
                type: 'POST',
                url: '/dbSearch.json',
                data: form_data,
                dataType: 'json',
                contentType: false,
                cache: false,
                processData: false,
                async: false,
                success: function (data, s, j) {
                    console.log("data = " + data.results);
                    if(firstSearch) {
                        $("#searchResultsTable").append("<tr><th>#</th><th>Artist</th><th>Title</th><!-- <th>Listen</th> --></tr>");
                    }
                    $.each(data.results, function (index, result) {
                        $("#searchResultsTable").append("<tr><td>" + (index + 1) + "</td><td>" + result.artist + "</td><td>" + result.title + "</td><!-- <td>" + result.listen + "</td> -->");
                    });
                    sortTable("searchResultsTable", indexColumn, comparators["sort normal"]);
                    $('#loadingInformation').html("Search completed.");
                }
            });
            firstSearch = false;
        }
    });
});