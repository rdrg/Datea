
Datea.show_big_loading = function ($over_el) {
	$over_el.css('position', 'relative');
	$over_el.append('<div class="loading-big-bg">&nbsp;</div><div class="loading-big-img">&nbsp;</div>');
}

Datea.hide_big_loading = function ($over_el) {
	$over_el.find('.loading-big-bg, .loading-big-img').remove();
}

Datea.show_small_loading = function ($over_el) {
	$over_el.css('position', 'relative');
	$over_el.append('<div class="loading-small-bg">&nbsp;</div><div class="loading-small-img">&nbsp;</div>');
}

Datea.hide_small_loading = function ($over_el) {
	$over_el.find('.loading-small-bg, .loading-small-img').remove();
	$over_el.css(); 
}
