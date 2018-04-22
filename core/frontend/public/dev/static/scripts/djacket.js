function setup_static_tabs () {
    jQuery('.static-tabs .tab-links a').on('click', function(e)  {
        var currentAttrValue = jQuery(this).attr('href');

        // Show/Hide Tabs
        jQuery('.static-tabs ' + currentAttrValue).show().siblings().hide();

        // Change/remove current tab to active
        jQuery(this).parent('li').addClass('active').siblings().removeClass('active');

        e.preventDefault();
    });
}

jQuery(function ($) {
    setup_static_tabs();

    $('a[href="#auth"]').on('click', function () {
        $('header#title-bar').css('display', 'none');
        $('section#container').css('display', 'block');
    });

    var url = "" + window.location;
    var id = url.substring(url.lastIndexOf('/#') + 2).trim();
    if (id == 'login-tab') {
        $('header#title-bar').css('display', 'none');
        $('section#container').css('display', 'block');
    } else if (id == 'register-tab') {
        $('header#title-bar').css('display', 'none');
        $('section#container').css('display', 'block');
        $('section#container #login-tab-li').removeClass('active');
        $('section#container #login-tab').removeClass('active');
        $('section#container #register-tab-li').toggleClass('active');
        $('section#container #register-tab').toggleClass('active');
    }
});
