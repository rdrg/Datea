

Datea.ModalWrapView = Backbone.View.extend({
   	
   	events: {
   		'click .close-modal': 'close_modal',
   	},
   	
   	render: function (eventName) {
		this.$el.html(this.content.render().el);
		return this;
	},
	
	open_modal: function (options) {
		if (typeof(options) == 'undefined') {
			var options = {backdrop: true, keyboard: true};
		}
		this.render();
		this.$el.modal(options);
	},
	
	close_modal: function () {
		this.$el.modal('hide');
	}, 
	
	set_content: function (content) {
		this.content = content;
	}
});



/* Bootstrap Form validator */
Datea.control_validate_required = function ($control){
	
	var result = true;
	if ($('input[type="text"]', $control).size() > 0) {
		var $input = $('input[type="text"]', $control);
		if ($.trim($input.val()) == '') {
			$control.addClass('error');
			remove_error_on_change($input);
			return false;
		}
	} else if ($('textarea', $control).size() > 0) {
		var $input = $('textarea', $control);
		if ($.trim($input.val()) == '') {
			$control.addClass('error');
			remove_error_on_change($input);
			return false;
		}
	} else if ($('select', $control).size() > 0) {
		var $input = $('select', $control);
		if ($input.val() == '') {
			$control.addClass('error');
			remove_error_on_change($input);
			return false;
		}
	} else if ($('input[type="radio"]', $control).size() > 0) {
		if ($('input:checked', $control).size() == 0) {
			$control.addClass('error');
			remove_error_on_change_radio($('input[type="radio"]', $control));
			return false;
		}
	}
	return true;
}

Datea.controls_validate = function ($form_chunk) {
	
	var $controls =  $('.required', $form_chunk);
	
	// clear all
	$controls.removeClass('error');
	
	// validate
	var test = true;
	$controls.each(function(e){
		 var valid = Datea.control_validate_required($(this));
		 if (valid == false) test = false;	
	});
	if (test == false) {
		$form_chunk.find('.error-msg').removeClass('hide');
		return false;
	}
	
	return true;
}

Datea.set_select_control = function($select_control, val) {
	$select_control.find('option[value="'+val+'"]').attr('selected',true);
}

function remove_error_on_change($element) {
	$element.bind('change.validation', function(){
		if ($.trim($(this).val()) != "") {
			$(this).closest('.control-group').removeClass('error');
			$(this).unbind('change.validation');
		} 
	});
}

function remove_error_on_change_radio($element) {
	$element.bind('change.validation', function(){
		if ($(this).filter(':checked').size() > 0) {
			$(this).closest('.control-group').removeClass('error');
			$(this).unbind('change.validation');
		} 
	});
}




