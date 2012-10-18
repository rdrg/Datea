
window.Datea.MapItemResponseFormView = Backbone.View.extend({
	
	tagName: 'div',	
	className: 'map-item-response-form',
	
	initialize: function () {
		this.map_items = this.options.map_items;
		this.model.bind('sync', this.sync_event, this);
	},
	
	events: {
		'click .save-response': 'save_response',
		'click .cancel': 'cancel',
	},
	
	render: function(ev) {
		this.$el.html(ich.map_item_response_form_tpl(this.model.toJSON()));
		return this;
	},
	
	save_response: function() {
		
		var content = $('[name="content"]',this.$el).val();
		if (jQuery.trim(content) != '') {
			this.model.set({
				'user': Datea.my_user.toJSON(),
				'map_items': this.map_items.toJSON(),
				'content': $('[name="content"]',this.$el).val(), 
			});
			this.model.save();
		}
	},
	
	cancel: function (ev) {
		this.$el.unbind();
        this.$el.empty();
	},
	
	sync_event: function() {
		this.$el.unbind();
        this.$el.empty();
		if (this.options.sync_callback) this.options.sync_callback();
	}
		
});