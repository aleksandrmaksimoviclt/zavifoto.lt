/*global
    $, window, lightGallery
*/

$(document).ready(function () {
    "use strict";

    var brightnessOverValue = "brightness(0.5)";
    var brightnessOutValue = "brightness(1)";

    $('li.grid').mouseover(function () {
        $(this).siblings().css({
          "-webkit-filter": brightnessOverValue,
          "filter": brightnessOverValue
        });
    });
    $('li.grid').mouseout(function () {
        $(this).siblings().css({
          "-webkit-filter": brightnessOutValue,
          "filter": brightnessOutValue
        });
    });``
});