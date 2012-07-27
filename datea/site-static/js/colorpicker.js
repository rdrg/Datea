
// start autosize on all textareas with the autoresize class 
$(document).ready(function() {
	
	$(document).on('focus', '.colorfield',{},function(){
		if (!$(this).hasClass('processed')) {
			$(this).addClass('processed');
			$(this).colorpicker().on('changeColor', function(ev){
				$(this).css("background-color", ev.color.toHex());
			});;
		}
	});
});