$( "#product-trigger" ).click(function() {
	$("#column1").attr('class', 'col-md-2 col-sm-2 col-xs-2');
});
<script>
	var cccommerce = {
		animateSpeed: 700,

		showPreview: function () {
			$('#cpage-trigger').one('click', function (e) {
				$('#categorylist').removeClass('col-md-12').addClass('col-md-7');
				$('#categorypage').addClass('categorypage-open');
			}); 
		},
		hidePreview: function () {
			$('body').one('click', function (e) {
				if ($(e.target).closest('#categorypage').length === 0 && $(e.target).closest('.categorypage-open').length === 0) {
					cccommerce.performHidePreview();
				} else {
					cccommerce.hidePreview();
				}
			});
		},
		performHidePreview: function () {
			$('#categorylist').removeClass('col-md-7').addClass('col-md-12');
			$('#categorypage').removeClass('categorypage-open');
			cccommerce.preview = false;
		}
	};

</script>