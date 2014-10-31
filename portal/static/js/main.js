$(document).ready(function() {
    $(".hire-me").click(function() {
        return $("html, body").animate({
            scrollTop: $($(this).attr("href")).offset().top
        }, 500), !1
    }), $("ul.nav-pills li a").click(function() {
        $("ul.nav-pills li.active").removeClass("active"), $(this).parent("li").addClass("active")
    }), $(window).load(function() {
        var e = $(".grid-wrapper");
        e.isotope({
            filter: "*",
            animationOptions: {
                duration: 750,
                easing: "linear",
                queue: !1
            }
        }), $(".grid-controls li a").click(function() {
            $(".grid-controls .current").removeClass("current"), $(this).addClass("current");
            var i = $(this).attr("data-filter");
            return e.isotope({
                filter: i,
                animationOptions: {
                    duration: 750,
                    easing: "linear",
                    queue: !1
                }
            }), !1
        })
    }), $(".grid-wrap").magnificPopup({
        delegate: "a",
        type: "image",
        gallery: {
            enabled: !0
        }
    })
    

$( function() {

		var $container = $('#grid').isotope({
			masonry: {
				columnWidth: 50
			}
		});

		$ ("#cart-trigger").on( "click", function() {
			$( "#page-portfolio" ).removeClass( "col-md-12 col-sm-12 col-xs-12" ).addClass( "hide-sm col-md-7 col-sm-7 col-xs-7" );
			$( "#cartpage" ).removeClass( "hidden" );
			if ($('#singleproduct').is(":visible")) {
				$( "#singleproduct" ).addClass( "hidden" );
			}
			console.log($container);
			$container.isotope('reLayout');

		});
		$ ("#cart-close").on( "click", function() {
			$( "#page-portfolio" ).removeClass( "hide-sm col-md-7 col-sm-7 col-xs-7" ).addClass( "col-md-12 col-sm-12 col-xs-12" );
			$( "#cartpage" ).addClass( "hidden" );
						console.log($container);
			$container.isotope('reLayout');

		});
		$ ("#single-trigger").on( "click", function() {
			$( "#page-portfolio" ).removeClass( "col-md-12 col-sm-12 col-xs-12" ).addClass( "hide-sm col-md-7 col-sm-7 col-xs-7" );
			$( "#singleproduct" ).removeClass( "hidden" );
			if ($('#cartpage').is(":visible")) {
				$( "#cartpage" ).addClass( "hidden" );
			}
			$container.isotope('reLayout');
		});
		$ ("#single-close").on( "click", function() {
			$( "#page-portfolio" ).removeClass( "hide-sm col-md-7 col-sm-7 col-xs-7" ).addClass( "col-md-12 col-sm-12 col-xs-12" );
			$( "#singleproduct" ).addClass( "hidden" );
			$container.isotope('reLayout');
		});

	});





});