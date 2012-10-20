
window.Datea.MapItemResponseView = Backbone.View.extend({
	
	tagName: 'div',
	className: 'map-item-reply',
	
	initialize: function() {
		this.model.bind('sync',this.render, this);
	},
	
	events :{
		'click .edit-response': 'edit',
		'click .save-response': 'save',
		'click .cancel': 'render',
	},
	
	render: function() {
		var context = this.model.toJSON();
		context.created = formatDateFromISO(context.created, "dd.mm.yyyy - H:MM");
		context.content = context.content.replace(/\n/g, '<br />');
		this.$el.html( ich.map_item_response_tpl(context));
		if (Datea.is_logged() && (
			this.model.get('user').id == Datea.my_user.get('id')
			|| Datea.my_user.get('is_staff')
			)){
				this.$el.find('.edit').show();
			}
		return this;
	},
	
	edit: function(){
		var context = this.model.toJSON();
		context.created = formatDateFromISO(context.created, "dd.mm.yyyy - H:MM");
		this.$el.html( ich.map_item_response_edit_tpl(context));
		this.$el.find('[name="content"]').focus();
	},
	
	save: function() {
		this.model.set({
			content: $('[name="content"]', this.$el).val(),
		});
		this.model.save();
	},
	
});