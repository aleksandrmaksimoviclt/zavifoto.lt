$( document ).ready(function() {
	var ww = window.innerWidth;

	if (ww > 768) {
	    console.log('true');
	} else {
	    console.log('false');
	    $('#wrapper').toggleClass("toggled");
	    $('#hambrger').removeClass("is-active");

	    
	}

	var $hamburger = $(".hamburger");
  	$hamburger.on("click", function(e) {
    	$hamburger.toggleClass("is-active");
    	e.preventDefault();
        $("#wrapper").toggleClass("toggled");
  });
});

// 		$('#sidebar-wrapper').css("margin-left", "-100%");
// 	    $('#sidebar-wrapper').css("left", "100%");
// 	    $('#sidebar-wrapper').css("width", "100%");
//    .sidebar-nav {
//     width: 100%;
// }