async function loadJson() {
  let response = await fetch ("media_search.json");
  let json = await response.json();

  return json.map(tmp => (
    {
      "id": tmp.itemBarcode,
      "name": tmp.name,
      "authorFirstName": tmp.authorFirstName,
      "authorLastName": tmp.authorLastName,
      "location": tmp.location,
      "category": tmp.category
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

    for (let medium of media) {
      this.add(medium);
    }
  });
}

function doSearch(e, idx, media) {
  // Stop the default action
  e.preventDefault();

  let searchText = $("#searchField").val();

  let resultList = document.getElementById("result-list");
  resultList.innerHTML = "";

  // Find the results from lunr
  let results = idx.search(searchText);

  if (results.length === 0) {
    $(".no-results").removeClass("is-hidden")
  }

  for (result of results) {
    let id = result.ref;

    let targetLocation = media[id].location.replace(/ /g, "");
    let targetUrl = `location_${targetLocation}.html#${id}`;

    let targetLink = `<li class="has-hover ${targetLocation}"><span class="medium-title"><a href="${targetUrl}">${media[id].name}</a>`

    if (media[id].authorFirstName !== "") {
      targetLink += ` von ${media[id].authorFirstName} ${media[id].authorLastName}`; // In case the book has an author
    }

    targetLink += ` <span class="category is-size-7 is-italic">${media[id].category}</span></span><span class="location"> am Standort ${media[id].location}</span></li>`;

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

  document.getElementById("search-button").addEventListener("click", function(event) {
    doSearch(event, idx, indexed);
  });

  document.getElementById("searchField").addEventListener("keydown", function(event) {
    if (document.getElementById("searchField").value.length >= 3) {
      document.getElementById("search-button").disabled = false;
      $("searchField").removeClass("is-danger");
      $("#fourCharWarning").addClass("is-hidden");

      if (event.keyCode === 13) {
         doSearch(event, idx, indexed);
      }

    } else {
      document.getElementById("search-button").disabled = true;
      $("searchField").addClass("is-danger");
      $("#fourCharWarning").removeClass("is-hidden");
    }
  });
});
