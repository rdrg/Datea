/* 
 * INIT WITH
 * {
 * 	model: <voted model instance> 	
 * 	voted_model: <model_instance_to_vote_on>,
 * }
 */

window.Datea.VoteWidgetView = Backbone.View.extend({
	
	tagName: 'div',
	
	className: 'vote-widget',
	
	initialize: function () {
		this.voted_model = this.options.voted_model;
		//this.model.bind('sync', this.sync, this);
		var id = this.options.object_id;
		if (Datea.my_user_votes) {
			this.model = Datea.my_user_votes.find(function(item){
				return item.get('object_type') == 'dateamapitem' && item.get('object_id') == id;
			});
		}
		if (typeof(this.model) == 'undefined') {
			this.model = new Datea.Vote({
				object_type: this.options.object_type,
				object_id: this.options.object_id,
			});
		}
		this.$el.addClass(this.options.style);
	},
	
	events: {
		'click': 'vote',
		'mouseleave': 'mouseleave',
	},
	
	render: function (ev) {
		var context = this.model.toJSON();
		context.vote_count = this.voted_model.get('vote_count');
		
		if (this.model.isNew()) {
			context.msg = gettext("support!");
		}else{
			context.msg = gettext("already supporting");
		}
		this.$el.html( ich.vote_widget_tpl(context));

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
		// for the moment, votes cannot be deleted
		if (this.model.isNew()) {
			Datea.show_small_loading(this.$el);
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