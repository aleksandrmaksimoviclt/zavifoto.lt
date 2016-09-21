/*global
    $, window, lightGallery
*/

$(document).ready(function () {
    "use strict";

    var aspectratio = 1.77;
    var gridWidth = $('.grid:first').width();
    var gridHeight = Math.round(gridWidth / aspectratio);

    function setaspectratio() {
        gridWidth = $('.grid:first').width();
        gridHeight = Math.round(gridWidth / aspectratio);

        $('.grid').each(function () {
            $(this).css('height', gridHeight);
        });
    }

    function setNavigation() {
        var path = window.location.pathname;
        path = path.replace(/\/$/, "");
        path = decodeURIComponent(path);

        $("a").each(function () {
            var href = $(this).attr('href');
            if (typeof href === "undefined"){
            } else if (path.substring(0, href.length) === href) {
                $(this).addClass('active');
            }
        });
    }

    // $("img").on("contextmenu", function () {
    //     return false;
    // });

    var ww = window.innerWidth;

    if (!(ww > 992)) {
        $('#wrapper').toggleClass("toggled");
        $('#hambrger').removeClass("is-active");
    }


    var $hamburger = $(".hamburger");
    $hamburger.on("click", function (e) {
        $hamburger.toggleClass("is-active");
        e.preventDefault();
        $("#wrapper").toggleClass("toggled");

        if (ww < 992) {
            $('body').toggleClass("noscroll");
            $('.overlay').toggleClass("activated");
        }

    });

    $('.faq-titlea').on('click', function () {
        if ($(this).hasClass("collapsed")) {
            $(this).removeClass("collapsed");
            $(this).addClass("active");
        } else {
            $(this).addClass("collapsed");
            $(this).removeClass("active");
        }
    });

    var rtime;
    var timeout = false;
    var delta = 200;

    function resizeend() {
        if (new Date() - rtime < delta) {
            setTimeout(resizeend, delta);
        } else {
            timeout = false;
            ww = window.innerWidth;
            setaspectratio();
        }
    }

    $(window).resize(function () {
        rtime = new Date();
        if (timeout === false) {
            timeout = true;
            setTimeout(resizeend, delta);
        }
    });
    setNavigation();
    setaspectratio();
});