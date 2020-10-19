function redirectOrUpdateVisible() {
  // rawHash is the paramater from the URL without #
  rawHash = $(location).attr('hash').replace(/^#/, "");

  if (!rawHash) {
    location.href = '#{{firstLocation | replace(" ", "")}}';
    oldVisible = '{{firstLocation | replace(" ", "")}}';
  } else {
    if (typeof oldVisible == 'undefined') {
      oldVisible = '{{firstLocation | replace(" ", "")}}';
    }

    // Umlauts
    decodedHash = decodeURIComponent(rawHash);

    // Old active button remove the highligh
    oldVisibleMenuItem = '.navbar-start a:contains(' + oldVisible + ')';
    if ($(oldVisibleMenuItem).hasClass('activeMenuItem')) {
      $(oldVisibleMenuItem).removeClass('activeMenuItem');
    }

    // Add highligh
    activeMenuItem = '.navbar-start a:contains(' + decodedHash + ')';
    $(activeMenuItem).addClass('activeMenuItem');

    // Hide datasets in other locations
    oldVisibleItemList = '#' + oldVisible;
    if ($(oldVisibleItemList).hasClass('show')) {
      $(oldVisibleItemList).removeClass('show');
    }

    // Show datasets in current location
    activeItemList = '#' + decodedHash;
    $(activeItemList).addClass('show');

    // Save active location (we need that later if a button in the menu is clicked)
    oldVisible = decodedHash;
    window.scrollTo(0, 0);
  }
}
