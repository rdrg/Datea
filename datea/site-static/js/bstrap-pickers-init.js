
// start autosize on all textareas with the autoresize class 
$(document).ready(function() {
	
	$(document).on('focus', '.colorfield',{},function(){
		if (!$(this).hasClass('processed')) {
			$(this).addClass('processed');
			$(this).colorpicker().on('changeColor', function(ev){
				$(this).css("background-color", ev.color.toHex());
			});
		}
	});
	
	$(document).on('mouseenter', '.datefield',{},function(){
		if (!$(this).hasClass('processed')) {
			$(this).addClass('processed');
			var opts = {
				language: Datea.lang,
			}
			if (Datea.lang == 'en') {
				opts.format = 'mm/dd/yyyy';
			}else{
				opts.format = 'dd/mm/yyyy';
			}
			$(this).datepicker(opts);
		}
	});
	
	$(document).on('mouseenter', '.timefield',{},function(){
		if (!$(this).hasClass('processed')) {
			$(this).addClass('processed');
			$(this).find('input[type="text"]').timepicker({
				defaultTime: false,
				showMeridian: false,
			});
		}
	});
	
});