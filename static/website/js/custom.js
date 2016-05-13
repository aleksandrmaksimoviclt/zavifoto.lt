$(document).ready(function() {

    $("img").on("contextmenu",function(){
       return false;
    }); 

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

    $('.faq-titlea').on('click', function() {
        if (  $( this ).hasClass("collapsed")){
            $(this).removeClass("collapsed");
            $(this).addClass("active");
        } else {
            $(this).addClass("collapsed");
            $(this).removeClass("active");
        }
    }); 
    
});
