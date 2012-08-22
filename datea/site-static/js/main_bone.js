

Datea.ModalWrapView = Backbone.View.extend({
   	
   	initialize: function () {
   		this.$el.on('shown',function(){
   			init_autoresize_textareas();
   		});
   	},
   	
   	events: {
   		'click .close-modal': 'close_modal',
   	},
   	
   	render: function (eventName) {
   		if (typeof(this.content.render) != 'undefined') {
			this.$el.html(this.content.render().el);
		}else{
			this.$el.html(this.content);
		}
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
		if ($input.hasClass('validate-email')) {
			var reg = /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/;
			if (!reg.test($.trim($input.val()))) {
				$control.addClass('error');
				remove_error_on_change($input);
				var error_msg = gettext('Please enter a valid email address.');
				$control.find('.controls').append('<div class="error-block">'+error_msg+'</div>');
				return {valid: false, msg: error_msg};
			}
		} else if ($.trim($input.val()) == '') {
			$control.addClass('error');
			remove_error_on_change($input);
			return {valid:false};
		}
	} else if ($('textarea', $control).size() > 0) {
		var $input = $('textarea', $control);
		if ($.trim($input.val()) == '') {
			$control.addClass('error');
			remove_error_on_change($input);
			return {valid: false};
		}
	} else if ($('select', $control).size() > 0) {
		var $input = $('select', $control);
		if ($input.val() == '') {
			$control.addClass('error');
			remove_error_on_change($input);
			return {valid: false};
		}
	} else if ($('input[type="radio"]', $control).size() > 0) {
		if ($('input:checked', $control).size() == 0) {
			$control.addClass('error');
			remove_error_on_change_radio($('input[type="radio"]', $control));
			return {valid: false};
		}
	}
	return true;
}

Datea.controls_validate = function ($form_chunk, invalid_callback) {
	
	var $controls =  $('.required', $form_chunk);
	
	// clear all
	$controls.removeClass('error');
	
	// validate
	var is_valid = true;
	$controls.each(function(e){
		 var test = Datea.control_validate_required($(this));
		 if (test.valid == false) is_valid = false;	
	});
	if (is_valid == false) {
		$form_chunk.find('.error-msg').removeClass('hide');
		if (typeof(invalid_callback) != 'undefined') invalid_callback();
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
			$(this).find('.error-block').remove();
		} 
	});
}

function remove_error_on_change_radio($element) {
	$element.bind('change.validation', function(){
		if ($(this).filter(':checked').size() > 0) {
			$(this).closest('.control-group').removeClass('error');
			$(this).unbind('change.validation');
			$(this).find('.error-block').remove();
		} 
	});
}




