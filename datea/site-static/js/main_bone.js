

Datea.ModalWrapView = Backbone.View.extend({
   	
   	render: function (eventName) {
		this.$el.html(this.content.render().el);
		return this;
	},
	
	open_modal: function () {
		this.render();
		this.$el.modal();
		//this.$el.modal();
	},
	
	close_modal: function () {
		this.$el.modal('hide');
	}, 
	
	set_content: function (content) {
		this.content = content;
	}
	
});

