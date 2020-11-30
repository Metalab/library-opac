$(document).ready(async function() {

  function getRandomColor() {
    function c() {
      return Math.floor(Math.random() * 256).toString(16)
    }
    return "#" + c() + c() + c();
  }

  $("#ebu_KE .title").each(function() {
    random = Math.floor((Math.random() * 10) + 5);
    $(this).css({
      "transform": "rotate(" + random + "deg)"
    });
  });

  $("#ebu_KE .subtitle").each(function() {
    random = Math.floor((Math.random() * 10) + 2);
    $(this).css({
      "transform": "rotate(-" + random + "deg)"
    });
  });

  $("#ebu_KE #mainNav .has-dropdown .navbar-dropdown a").each(function() {
    $(this).css("background", getRandomColor());
  });

  $("#ebu_KE .media-container .list-item").each(function() {
    $(this).css("background", getRandomColor());
  });
});
