function loadJson() {
  toReturn = [];

  $.getJSON("/media.json", function(data) {
    toReturn.push(data);
  });

  return toReturn;

}
function loadSearch(json) {
  media = loadJson();

  // Create a new Index
  idx = lunr(function() {
    this.ref("itemBarcode");
    this.field("name", {
      boost: 10
    });
    this.field("authorFirstName", {
      boost: 5
    });
    this.field("authorLastName", {
      boost: 5
    });
    this.field("category");

    // Loop through each entry and add it to the index
    media.forEach(function (medium) {
      console.log(medium);
      this.add(medium);
    }, this);
  });

  // When the search form is submitted
  $("#searchButton").on("submit", function(e) {
    // Stop the default action
    e.preventDefault();

    // Find the results from lunr
    results = idx.search($("#searchField").val());

    $("#searchResults").append("<ul id=" + searchResults + "></ul>");

    // Loop through results
    $.each(results, function(index, result) {
      // Get the entry from the window global
      entry = window.searchData[result.ref];

      // Append the entry to the list.
      $("#searchResults").append("<li><a href=" + entry.url + ">" + entry.name + "</li>");
    })
  })
}

$(document).ready(function() {
  loadSearch();
});
