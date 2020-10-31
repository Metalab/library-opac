async function loadJson() {
  let response = await fetch ("/media.json");
  let json = await response.json();

  toReturn = [];
  for (let tmp of json) {
    toReturn.push({
      "id": tmp.itemBarcode,
      "name": tmp.name,
      "authorFirstName": tmp.authorFirstName,
      "authorLastName": tmp.authorLastName,
      "category": tmp.category
    });
  }

  return toReturn;
}

async function loadSearchData() {
  let media = await loadJson();

  // Create a new Index
  idx = lunr(function() {
    this.ref("id");
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

    for (let medium of media) {
      this.add({
        "id": medium.itemBarcode,
        "name": medium.name,
        "authorFirstName": medium.authorFirstName,
        "authorLastName": medium.authorLastName,
        "category": medium.category
      });
    }
  });
}

async function doSearch(e) {
  let media = await loadJson();

  // Stop the default action
  e.preventDefault();

  // Find the results from lunr
  results = idx.search($("#searchField").val());

  for (result of results) {
    id = result.ref;

    // console.log(media[id]);
    // $("#resultList").append("<li><a href=" + result.name + ">" + result.authorFirstName + "</li>");
  }

  // Loop through results
  // $.each(results, function(index, result) {
  //   // Get the entry from the window global
  //   entry = window.searchData[result.ref];
  // });
}

$(document).ready(function() {
  loadSearchData();

  // When the search form is submitted
  document.getElementById("searchButton").addEventListener("click", function(event){
    doSearch(event);
  });
  document.getElementById("searchField").addEventListener("submit", function(event){
    doSearch(event);
  });
});
