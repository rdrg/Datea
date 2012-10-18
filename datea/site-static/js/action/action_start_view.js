
// Start action view -> create new action
window.Datea.ActionStartView = Backbone.View.extend({
	
	tagName: 'div',
	
	render: function(eventName) {
		this.$el.html( ich.content_layout_single_tpl({'dotted_bg': true}));
		this.$el.find('#content').html( ich.action_create_tpl());
		return this;	
	}
	
});
