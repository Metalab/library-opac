$(document).ready(function() {
  var backToTopButton = $("#backToTop");

  $(window).scroll(function() {
    if ($(window).scrollTop() > 300) {
      backToTopButton.addClass("show");
    } else {
      backToTopButton.removeClass("show");
    }
  });

  backToTopButton.on("click", function(e) {
    e.preventDefault();
    $("html, body").animate({
      scrollTop: 0
    }, "500");
  });
});
