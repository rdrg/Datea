

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
		if (typeof(this.content.render) != 'undefined') {
			this.content.undelegateEvents();
		}
	}, 
	
	set_content: function (content) {
		this.content = content;
	}
});








