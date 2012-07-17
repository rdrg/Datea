
window.Datea.Follow = Backbone.Model.extend({
	urlRoot: '/api/v1/follow'
});

window.Datea.FollowCollection = Backbone.Collection.extend({
	model: Datea.Follow,
	url: '/api/v1/follow',
});

window.Datea.NotifySettings = Backbone.Model.extend({
	urlRoot: '/api/v1/notify_settings'
});


/* INIT WITH
 * {
 * 	model: <follow model instance> 	
 * 	followed_model: <model_instance_to_follow>,
 * }
 */

window.Datea.FollowWidgetView = Backbone.View.extend({
	
	tagName: 'div',
	
	className: 'follow-widget',
	
	initialize: function () {
		this.followed_model = this.options.followed_model;
		//this.model.bind('sync', this.sync, this);
		this.$el.addClass(this.options.size);
	},
	
	events: {
		'click': 'follow',
		'mouseleave': 'mouseleave',
	},
	
	render: function (ev) {
		var context = this.model.toJSON();
		context.follow_count = this.followed_model.get('follow_count');
		this.$el.html( ich.follow_widget_tpl(context));
		
		if (this.model.isNew()) {
			this.$el.find('.hover-msg').html( ich.follow_hover_msg_tpl({object_name: 'report'}) );
		}else{
			this.$el.find('.hover-msg').html( ich.unfollow_hover_msg_tpl() );
		}

		if (!this.model.isNew()) {
			this.$el.addClass('active');
		}else{
			this.$el.removeClass('active');
		}
		
		if (this.followed_model.get('follow_count') > 0) {
			this.$el.removeClass('force-hover');
		}else{
			this.$el.addClass('force-hover');
		}
		
		return this;
	},
	
	follow: function(ev) {
		Datea.show_small_loading(this.$el);
		
		if (this.model.isNew()) {
			var self = this;
			this.model.save({},{
				success: function (model, response) {
					self.render();
				}
			});
			Datea.my_user_follows.add(this.model);
			this.followed_model.set('follow_count', this.followed_model.get('follow_count') + 1);
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
		this.$el.addClass('after-click');
	},
	
	mouseleave: function (ev) {
		this.$el.removeClass('after-click');
	}
	
});


