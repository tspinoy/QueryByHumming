var filledContentTable = false;

function fillContentTable() {
    if(!filledContentTable) {
        $.get({
            url: "/content.json",
            dataType: 'json',
            success: function (data, s, j) {
                console.log(data);
                $.each(data.content, function (index, result) {
                    $("#contentTable").append("<tr><td>" + (index + 1) + "</td><td>" + result.title + "</td><td>" + result.listen + "</td></tr>");
                })
            }
        });
        filledContentTable = true; // otherwise you can keep adding the same information
    }
    $("#loadingInformation").html("All content is loaded.");
}