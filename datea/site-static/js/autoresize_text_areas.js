

// start autosize on all textareas with the autoresize class 
$(document).ready(function() {
	$(document).on('focus', '.autoresize',{},function(){
		if (!$(this).hasClass('autoresize-processed')) {
			$(this).addClass('autoresize-processed');
			$(this).autosize();	
		}
	});
	
});
