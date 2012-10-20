
/* Comment LIST VIEW
 * init args:
 * 	{
 * 		model: comment_collection,
 * 		object_type (string): 'DateaMapItem',
 * 		object_id (int): 12, 
 *  }
 */
window.Datea.CommentsView = Backbone.View.extend({
	
	tagName: 'div',
	
	attributes: {
		'class': 'comments'
	},
	
	
	initialize: function() {
		this.model.bind("add", this.add_comment, this);
		this.model.bind("reset", this.render, this);
	},
	
	
	render: function (ev) {
		// base template
		this.$el.html(ich.comments_tpl());
		
		// render_comments 
		if (this.model.length == 0) {
			this.$el.find('.comment-list').addClass('hide');
		}else{
			var $list_el = this.$el.find('.comment-list');
			_.each(this.model.models, function(comment) {
				$list_el.append(new Datea.CommentItemView({model:comment}).render().el);
			});
		}
		
		// render comment form
		this.comment_form = new Datea.CommentFormView({
			el: this.$el.find('.comment-form'),
			model: new Datea.Comment(),
			model_col: this.model,
			object_type: this.options.object_type,
			object_id: this.options.object_id,
		});
		this.comment_form.render()

		return this;
	},
	
	add_comment: function (model) {
		var $com_list = this.$el.find('.comment-list');
		$com_list.removeClass('hide');
		var new_comment = new Datea.CommentItemView({model: model});
		new_comment.render();
		new_comment.$el.hide();
		$com_list.append(new_comment.el);
		new_comment.$el.slideDown('normal');
		if (this.options.callback) this.options.callback(model);
	}
	
});