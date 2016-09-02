$(document).ready(function () {
    var galleryId = 0;    
    $('.sort-gallery').css('opacity', '0');
    lightGallery(document.getElementById('lightgallery-all'));
    var options = {
        animationDuration: 0.25,
        filter: 'all',
        delay: 50,
        delayMode: 'progressive',
        easing: 'ease-out',
        filterOutCss: {
            opacity: 0,
            transform: 'scale(0)'
        },
        filterInCss: {
            opacity: 1,
            transform: 'scale(1)'
        },
        layout: 'sameSize',
        selector: '.filtr-container',
        setupControls: true
    };
    var filterizd = $('.filtr-container').filterizr(options);
    filterizd.filterizr('setOptions', options);

    $('ul.sub-category>li').on('click', function () {
        var check = $(this).attr('data-filter');
        $('.all-gallery').css('display', 'none');
        $('.sort-gallery').css('opacity', '1');
    });

    $('.lightgallery').each(function () {
        galleryId += 1;
        $(this).attr('id', 'galleryid' + galleryId);
        lightGallery(document.getElementById('galleryid' + galleryId), {
            galleryId: galleryId
        });
    });
});