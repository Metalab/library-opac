$(document).ready(function() {
  $("#navbar-burger").click(function() {
    $("#navbar-burger").toggleClass("is-active");
    $("#mainNav").toggleClass("is-block");
  });

  $(".navbar-item.has-dropdown").click(function(e) {
      if ($(".navbar-burger").is(":visible")) {
        $(this).toggleClass("is-active");
      }
  });

  $(".navbar-item > .navbar-link").click(function(e) {
      if ($(".navbar-burger").is(":visible")) {
        e.preventDefault();
      }
  });

  $(window).resize(function(e) {
    if (!$(".navbar-burger").is(":visible") && $(".navbar-item.has-dropdown.is-active").length) {
      $(".navbar-item.has-dropdown.is-active").removeClass("is-active");
    }
  });
});
