

// start autosize on all textareas with the autoresize class 
$(document).ready(function() {
	$(document).on('focus', '.autoresize',{},function(){
		if (!$(this).hasClass('autoresize-processed')) {
			$(this).addClass('autoresize-processed');
			$(this).autosize();	
		}
	});
});

function init_autoresize_textareas() {
	$('.autoresize').not('.autoresize-processed').each(function(e){
		$(this).addClass('autoresize-processed');
		$(this).autosize();
	});
}
