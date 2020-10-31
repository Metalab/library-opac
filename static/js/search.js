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
      "location": tmp.location
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

  let resultList = document.getElementById("resultList");
  resultList.innerHTML = "";

  let searchText = $("#searchField").val();

  if (searchText == "") {
    alert("Bitte einen Suchbegriff eingeben!");
    return;
  }

  if(searchText.length < 4) {
    alert("Bitte mehr als vier Zeichen eingeben!");
    return;
  }

  // Find the results from lunr
  let results = idx.search(searchText);

  for (result of results) {
    let id = result.ref;
    let score = result.score;

    let targetLocationUrl = media[id].location.replaceAll(" ", "");
    let targetUrl = "location_" + targetLocationUrl + ".html#" + id;
    let targetLink = '<li><a href="' + targetUrl + '">' + media[id].name + '</a> von ' + media[id].authorFirstName + ', ' + media[id].authorLastName +  ' am Standort ' + media[id].location + '</li>';

    resultList.innerHTML += targetLink;
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
