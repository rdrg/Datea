// Comment list ITEM VIEW
window.Datea.CommentItemView = Backbone.View.extend({
	
	tagName: 'div',
	
	attributes: {
		'class' : 'comment-item',
	},
	
	initialize: function () {
		this.model.bind('sync', this.render, this);
		this.model.bind('change', this.render, this);
	},
	
	render: function(eventName) {
		var context = this.model.toJSON()
		context.created = formatDateFromISO(context.created, "dd.mm.yyyy - H:MM");
		context.comment = context.comment.replace(/\n/g, '<br />');
		this.$el.html(ich.comment_item_tpl(context));
		return this;
	}
});