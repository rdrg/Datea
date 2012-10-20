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