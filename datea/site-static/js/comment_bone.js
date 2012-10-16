

window.Datea.Comment = Backbone.Model.extend({
	urlRoot: '/api/v1/comment/'
});


window.Datea.CommentCollection = Backbone.Collection.extend({
	url:'/api/v1/comment',
	model:  Datea.Comment
});


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

/* 
 * COMMENT FORM VIEW
 * 
 * init args:
 * 	{
 * 		model: comment model,
 * 		model_col: comment_collection,
 * 		object_type (string): f.e. 'DateaMapItem',
 * 		object_model (int): 12 ,
 *  }
 */
window.Datea.CommentFormView = Backbone.View.extend({
	
	tagName:'div',
	
	attributes: {
		'class': 'comment-form'
	},
	
	events: {
		'click .submit-comment': 'submit'
	},
	
	render: function (ev) {
		// not logged in -> redirect to login
		if (!Datea.is_logged()) {
			this.$el.html( ich.comment_login_tpl({'next': '/'+document.location.hash}));
		}else{
			this.$el.html(ich.comment_form_tpl());
		}
		return this;
	},
	
	submit: function (ev) {
		var comment = this.$el.find('textarea').val();
		if (jQuery.trim(comment) == '') return;
		
		this.$el.find('.ajax-loading').show();
		this.$el.find('.submit-comment').attr('disabled','disabled');
		var self = this;
		this.model.save({
			object_type: this.options.object_type,
			object_id: this.options.object_id,
			comment: comment,
		},{
			'success': function(model, response) {
				if (self.options.model_col) {
					self.options.model_col.add(model);
				}
				self.render();
				self.model = new Datea.Comment();
			},
			'error': function(error) {
				// redirect to login
				console.log(error);
				//document.location.href = document.location.protocol+'//'+document.location.hostname+"/accounts/login/?next="+document.location.hash.replace('#','');
			}
		});
	}
	
});


