$( document ).ready(function() {


	$('.dropdown-button').dropdown({
		inDuration: 300,
		outDuration: 225,
		constrain_width: false, // Does not change width of dropdown to that of the activator
		hover: true, // Activate on hover
		gutter: 0, // Spacing from edge
		belowOrigin: true, // Displays dropdown below the button
		alignment: 'left' // Displays dropdown with edge aligned to the left of button
		}
	);

	$('.select-language-button').dropdown({
		inDuration: 300,
		outDuration: 225,
		constrain_width: true, // Does not change width of dropdown to that of the activator
		hover: true, // Activate on hover
		gutter: 0, // Spacing from edge
		belowOrigin: true, // Displays dropdown below the button
		alignment: 'right' // Displays dropdown with edge aligned to the left of button
		}
	);

	
	var ww = window.innerWidth;
	var menuWidth = 300;
	$(".button-collapse").sideNav();

	// if (ww > 992) {
	// 	$(".button-collapse").sideNav({
	// 		menuWidth: 300,
	// 	});
	//     console.log('true');
	//     var menuWidth = 300;
	//     console.log(menuWidth);
	// } else {
	// 	$(".button-collapse").sideNav({
	// 		menuWidth: ww,

	// 	});
	// 	$(".long-text-handler").css('width',ww-24)
	//     console.log('false');
	//     var menuWidth = ww;
	//     console.log(menuWidth);
	// }

	$(".close").click(function(){
		$('.button-collapse').click();
	});

    setNavigation();

	var goLeft = $('#textback').width();

	$("#back-icon").css('left', menuWidth - goLeft);

	function setNavigation() {
	    var path = window.location.pathname;
	    path = path.replace(/\/$/, "");
	    path = decodeURIComponent(path);

	    $("a").each(function () {
	        var href = $(this).attr('href');
	        if (path.substring(0, href.length) === href) {
	            $(this).addClass('active');
	        }
	    });
	}
	
    window.getWindowSpecs = function(){
    	var w = window.outerWidth;
    };

    $(".scroll-on-hover").mouseover(function() {
		$(this).removeClass("ellipsis");
		var maxscroll = $(this).width();
		var speed = maxscroll * 20;
			$(this).animate({
			scrollLeft: maxscroll
		}, speed, "linear");
	});

	$(".scroll-on-hover").mouseout(function() {
	    $(this).stop();
	    $(this).addClass("ellipsis");
	    $(this).animate({
	        scrollLeft: 0
	    }, 'slow');
	});


	// getProjectPhotoWidth = $('.project-photo').width();

	// $('.project-photo').css('height', getProjectPhotoWidth);
	$('.single-item').slick();
});

window.createCookie = function(name,value,days) {
	if (days) {
	    var date = new Date();
	    date.setTime(date.getTime()+(days*24*60*60*1000));
	    var expires = "; expires="+date.toGMTString();
	}
	else var expires = "";
	document.cookie = name+"="+value+expires+"; path=/";
	}

window.readCookie = function(name) {
	var nameEQ = name + "=";
	var ca = document.cookie.split(';');
	for(var i=0;i < ca.length;i++) {
	    var c = ca[i];
	    while (c.charAt(0)==' ') c = c.substring(1,c.length);
	    if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
	}
	return null;
	}

function getAbsolutePath() {
    var loc = window.location;
    var pathName = loc.pathname.substring(0, loc.pathname.lastIndexOf('/') + 1);
    return loc.href.substring(0, loc.href.length - ((loc.pathname + loc.search + loc.hash).length - pathName.length));
}

