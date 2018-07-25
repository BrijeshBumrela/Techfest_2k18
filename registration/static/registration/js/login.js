$(document).ready(function() {
  $(".yoke").click(function() {
    if ($(".doorleft").hasClass("moveleft")) {
      $(".doorleft").removeClass("moveleft");
      $(".doorright").removeClass("moveright");
      $(".yoke").removeClass("moveyoke");
      $(".littleleft").removeClass("littleout");
      $(".littleright").removeClass("littleout");
      $(".doorleft").addClass("unmoveleft");
      $(".doorright").addClass("unmoveright");
      $(".yoke").addClass("unmoveyoke");
      $(".littleleft").addClass("littlein");
      $(".littleright").addClass("littlein");
    } else {
      $(".doorleft").removeClass("unmoveleft");
      $(".doorright").removeClass("unmoveright");
      $(".yoke").removeClass("unmoveyoke");
      $(".littleleft").removeClass("littlein");
      $(".littleright").removeClass("littlein");
      $(".doorleft").addClass("moveleft");
      $(".doorright").addClass("moveright");
      $(".yoke").addClass("moveyoke");
      $(".littleleft").addClass("littleout");
      $(".littleright").addClass("littleout");
    }
  });
});