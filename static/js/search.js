async function loadJson() {
  let response = await fetch ("/media.json");
  let json = await response.json();

  return json.map(tmp => (
    {
      "id": tmp.itemBarcode,
      "name": tmp.name,
      "authorFirstName": tmp.authorFirstName,
      "authorLastName": tmp.authorLastName,
      "category": tmp.category,
      "location": tmp.location.replace(" ", "")
    }
  ));
}

function loadSearchData(media) {

  // Create a new Index
  return lunr(function() {
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
      this.add(medium);
    }
  });
}

function doSearch(e, idx, media) {

  // Stop the default action
  e.preventDefault();

  console.log(idx);

  // Find the results from lunr
  let results = idx.search($("#searchField").val());

  for (result of results) {
    let id = result.ref;
    let score = result.score;

    let targetUrl = media[id].location;

    $("#resultList").append("<li><a href=" + targetUrl + "#" + id + ">" + result.name + "</li>");
  }
}

$(document).ready(async function() {
  let media = await loadJson();
  let idx = loadSearchData(media);

  let indexed = {};
  for(let medium of media) {
    indexed[medium.id] = medium;
  }

  // When the search form is submitted
  document.getElementById("searchButton").addEventListener("click", function(event){
    doSearch(event, idx, indexed);
  });

  document.getElementById("searchField").addEventListener("submit", function(event){
    doSearch(event, idx, indexed);
  });
});
