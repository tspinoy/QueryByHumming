var indexColumn  = 0;
var artistColumn = 1;
var titleColumn  = 2;
var scoreColumn  = 3;
var reversed = false;

/*  We want to pass a comparator as an argument to sortTable(). This is not possible in JavaScript, so we do it like this.
    The "reversed"-comparator means the table is reversed at the moment, so we need "<" to make it "normal" again.
    The "not reversed"-comparator means the table is not reversed at the moment, so we need ">" to reverse it. */
var comparators = {
    "sort reversed" : function (operand1, operand2) {
        return operand1 < operand2;
    },
    "sort normal" : function (operand1, operand2) {
        return operand1 > operand2;
    }
};

// https://www.w3schools.com/howto/howto_js_sort_table.asp
function sortTable(id, column, comparator) {
  var table, rows, switching, i, x, y, shouldSwitch;
  table = document.getElementById(id);
  switching = true;
  // Make a loop that will continue until no switching has been done
  while (switching) {
    // Start by saying: no switching is done
    switching = false;
    rows = table.getElementsByTagName("tr");
    // Loop through all table rows
    // If there are no table headers, i=0, otherwise i=1
    for (i = 1; i < (rows.length - 1); i++) {
      // Start by saying there should be no switching
      shouldSwitch = false;
      // Get the two elements you want to compare, one from current row and one from the next
      x = rows[i].getElementsByTagName("td")[column];
      y = rows[i + 1].getElementsByTagName("td")[column];
      // Check if the two rows should switch place
      if (column === indexColumn) {
        if (comparator(x.innerHTML, y.innerHTML)) {
        // If so, mark as a switch and break the loop
        shouldSwitch = true;
        break;
        }
      }
      else if (comparator(x.innerHTML.toLowerCase(), y.innerHTML.toLowerCase())) {
        // If so, mark as a switch and break the loop
        shouldSwitch = true;
        break;
      }
    }
    if (shouldSwitch) {
      // If a switch has been marked, make the switch and mark that a switch has been done
      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
      switching = true;
    }
  }
  reversed = !reversed; // Set the boolean to know the table is now sorted in the other order
}

function sortContentTableByIndex() {
    if (reversed) {
        // if the table is reversed we want to make it "normal" again
        sortTable("contentTable", indexColumn, comparators["sort normal"])
    }
    // if the table is not reversed, it will be reversed after sorting
    else sortTable("contentTable", indexColumn, comparators["sort reversed"])

}

function sortContentTableByTitle() {
    if (reversed) {
        // if the table is reversed we want to make it "normal" again
        sortTable("contentTable", titleColumn, comparators["sort normal"])
    }
    // if the table is not reversed, it will be reversed after sorting
    else sortTable("contentTable", titleColumn, comparators["sort reversed"])
}

function sortContentTableByArtist() {
    if (reversed) {
        // if the table is reversed we want to make it "normal" again
        sortTable("contentTable", artistColumn, comparators["sort normal"])
    }
    // if the table is not reversed, it will be reversed after sorting
    else sortTable("contentTable", artistColumn, comparators["sort reversed"])
}