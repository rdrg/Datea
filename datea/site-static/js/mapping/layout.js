

Datea.mapping_resize_layout =  function () {
	$(window).unbind('resize.mapping');
	var $mapping_row = $('#main-content-view .mapping-content');
	if ($mapping_row.size() > 0) {
		var min_height = 600;
		//$('.scroll-area.resize-target').removeAttr('style');
		var doc_height = $('html').height();
		var win_height = $(window).height();
		if (win_height < min_height) win_height = min_height;				
		var delta = win_height - doc_height;
	
		if (delta != 0) {
			$('.scroll-area.resize-target').each(function(){
				var height = 480 + delta;
				$(this).css("height", height+'px');
			});
			$('.data-view-body .resize-target').not('.resized').addClass('resized').each(function(){
				var height = $(this).height() + delta;
				$(this).css("height", height+'px');
			});
		}
		if (typeof(Datea.main_map) != 'undefined') Datea.main_map.updateSize();
		
		$(window).bind('resize.mapping', function () {
			var $map_div = $('.data-view-body .resize-target')
			$map_div.removeClass('resized').css('height', '500px');
			$('.scroll-area.resize-target').removeAttr('style');
			if (typeof(Datea.main_map) != 'undefined') Datea.main_map.updateSize();
		});
	}
}