$(document).ready(function() {
	$.event.special.widthChanged = {
        remove: function() {
            $(this).children('iframe.width-changed').remove();
        },
        add: function () {
            var elm = $(this);
            var iframe = elm.children('iframe.width-changed');
            if (!iframe.length) {
                iframe = $('<iframe/>').addClass('width-changed').prependTo(this);
            }
            var oldWidth = elm.width();
            function elmResized() {
                var width = elm.width();
                if (oldWidth != width) {
                    elm.trigger('widthChanged', [width, oldWidth]);
                    oldWidth = width;
                }
            }

            var timer = 0;
            var ielm = iframe[0];
            (ielm.contentWindow || ielm).onresize = function() {
                clearTimeout(timer);
                timer = setTimeout(elmResized, 500);
            };
        }
    }

    

    $('#myContainer').on('widthChanged',function(){

    	
        slider.destroy();

        if (!slider.lightSlider) {
            $('#imageGallery').lightSlider({
		        gallery:true,
		        item:1,
		        loop:true,
		        thumbItem:9,
		        slideMargin:0,
		        enableDrag: false,
		        currentPagerPosition:'left',
		        onSliderLoad: function(el) {
		            el.lightGallery({
		                selector: '#imageGallery .lslide'
		            });
		        }   
    		});  
        }
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

});

// 		$('#sidebar-wrapper').css("margin-left", "-100%");
// 	    $('#sidebar-wrapper').css("left", "100%");
// 	    $('#sidebar-wrapper').css("width", "100%");
//    .sidebar-nav {
//     width: 100%;
// }