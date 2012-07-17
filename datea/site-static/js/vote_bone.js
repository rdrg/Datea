window.Datea.Vote = Backbone.Model.extend({
	urlRoot: '/api/v1/vote'
});

window.Datea.VoteCollection = Backbone.Collection.extend({
	model: Datea.Vote,
	url: '/api/v1/vote',
});


/* INIT WITH
 * {
 * 	model: <follow model instance> 	
 * 	followed_model: <model_instance_to_follow>,
 * }
 */

window.Datea.VoteWidgetView = Backbone.View.extend({
	
	tagName: 'div',
	
	className: 'vote-widget',
	
	initialize: function () {
		this.voted_model = this.options.voted_model;
		//this.model.bind('sync', this.sync, this);
		this.$el.addClass(this.options.size);
	},
	
	events: {
		'click': 'vote',
		'mouseleave': 'mouseleave',
	},
	
	render: function (ev) {
		var context = this.model.toJSON();
		context.vote_count = this.voted_model.get('vote_count');
		this.$el.html( ich.vote_widget_tpl(context));
		
		if (this.model.isNew()) {
			this.$el.find('.hover-msg').html( ich.vote_hover_msg_tpl({object_name: 'report'}) );
		}else{
			this.$el.find('.hover-msg').html( ich.unvote_hover_msg_tpl() );
		}

		if (!this.model.isNew()) {
			this.$el.addClass('active');
		}else{
			this.$el.removeClass('active');
		}
		
		if (this.voted_model.get('vote_count') > 0) {
			this.$el.removeClass('force-hover');
		}else{
			this.$el.addClass('force-hover');
		}
		return this;
	},

	
	vote: function(ev) {
		Datea.show_small_loading(this.$el);
		
		// for the moment, votes cannot be deleted
		if (this.model.isNew()) {
			var self = this;
			this.model.save({},{
				success: function (model, response) {
					self.render();
				}
			});
			Datea.my_user_votes.add(this.model);
			this.voted_model.set('vote_count', this.voted_model.get('vote_count') + 1);
		}
		/*
		}else {
			Datea.my_user_follows.remove(this.model);
			this.model.destroy();
			this.model = new Datea.Follow({
				object_type: this.model.get('object_type'),
				object_id: this.model.get('object_id'),
				follow_key: this.model.get('follow_key'),
			});
			this.followed_model.set('follow_count', this.followed_model.get('follow_count') - 1);
			this.render();
		}
		*/
		this.$el.addClass('after-click');
	},
	
	mouseleave: function (ev) {
		this.$el.removeClass('after-click');
	}
	
});