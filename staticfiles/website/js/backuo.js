$(document).ready(function() {

    function sliderInit () {
        $('#carousel').flexslider({
            animation: "slide",
            touch: true,
            keyboard: true,
            multipleKeyboard: true,
            controlNav: false,
            directionNav: false,
            animationLoop: false,
            slideshow: false,
            itemWidth: 210,
            minItems: 6,
            maxItems: 6,
            asNavFor: '#slider'
        });
 
    $('#slider').flexslider({
            animation: "slide",
            touch: true,
            keyboard: true,
            multipleKeyboard: true,
            controlNav: false,
            directionNav: false,
            animationLoop: false,
            slideshow: false,
            sync: "#carousel"
        });
    }

    sliderInit();

    var slider1 = $('#carousel').data('flexslider');
    var slider2 = $('#slider').data('flexslider');

  // Div resize tracking

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
                timer = setTimeout(elmResized, 1);
            };
        }
    }

    // end

    $('#page-content-wrapper').on('widthChanged',function(){
        slider1.resize();
        slider2.resize();
    });
});