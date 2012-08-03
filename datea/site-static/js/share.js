
function init_share_buttons() {
	try {
		twttr.widgets.load();
	}
	catch(err) {}
	
	try {
		$('.fb-share').not('.processed').each( function() {
			FB.XFBML.parse( this );
			$(this).addClass('processed');
		});
	}catch (err) {}
}

/*
Datea.share = {};
// DATEO INIT ADDtea.share.THIS
Datea.share.init_add_this = function () {
	
	if (typeof(addthis_share) == 'undefined') return;
	
	var usuario = Datea.my_user.get('username');
	
	addthis_share['email_vars'] = {usuario: usuario};
	
	var $boton_addthis = $('.addthis_toolbox').not('.share-processed');
	$boton_addthis.addClass('.share-processed');
	
	/*
	$boton_addthis.hover(
		function () {
			var $bubble = $('.share-services', $(this));
			$bubble.show();
			var footer_offset = $('#footer').offset();
			var win_h = $(window).height();
			var bubble_offset = $bubble.offset();
			var bubble_height = $bubble.height();
			var extra_offset = 28;
			var original_top = bubble_offset.top + bubble_height + extra_offset;
			if (original_top > footer_offset.top || original_top > win_h) {
				$bubble.addClass('top').removeClass('bottom');
				$bubble.css('top', '-'+(bubble_height+extra_offset)+'px');
				$bubble.css('bottom', 'auto');
			}else{
				$bubble.addClass('bottom').removeClass('top');
				$bubble.css('bottom', '-'+(bubble_height+extra_offset)+'px');
				$bubble.css('top', 'auto');
			} 
		},
		function () {
			$('.share-services', $(this)).hide();
		}
	);
	addthis.init();
	//window.addthis.ost = 0;
    //window.addthis.ready();
}*/