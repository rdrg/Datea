/* INIT WITH
 * {
 * 	object_type: <string: follow model type>
 *  object_id: <int: follow model pk>
 *  object_name: <string: follow model verbose name>  	
 * 	followed_model: <model_instance_to_follow>,
 *  type: <'full' or 'button'>
 *  style: <'full-small' or 'button-small'>
 * }
 */

window.Datea.FollowWidgetView = Backbone.View.extend({
	
	tagName: 'div',
	
	className: 'follow-widget',
	
	initialize: function () {
		var follow_key = this.options.object_type+'.'+this.options.object_id;
		
		if (Datea.my_user_follows) {
			this.model = Datea.my_user_follows.find(function(item){
				return item.get('follow_key') == follow_key;
			});
		}
		if (typeof(this.model) == 'undefined') {
			this.model = new Datea.Follow({
				follow_key: follow_key,
				object_type: this.options.object_type,
				object_id: this.options.object_id,
			});
		}
		
		this.followed_model = this.options.followed_model;
		//this.model.bind('sync', this.sync, this);
		this.$el.addClass(this.options.style);
		if (this.options.read_only) this.$el.addClass('read-only');
	},
	
	events: {
		'click': 'follow',
		'mouseleave': 'mouseleave',
	},
	
	render: function (ev) {
		var context = this.model.toJSON();
		context.follow_count = this.followed_model.get('follow_count');
		if (this.model.isNew()) {
			$.extend(context, {
				msg: gettext('follow!'),
				label: gettext('follow'),
			});
		}else if (this.options.read_only) {
			$.extend(context, {
				msg: gettext('follow'),
				label: gettext('follow'),
			});
		}else{
			$.extend(context, {
				msg: gettext('stop following'),
				label: gettext('following'),
			});
			context.msg = gettext('stop following');
		}
		if (this.options.is_own) {
			context.follow_count--;
			if (context.follow_count < 0) context.follow_count = 0;
		}
		 
		this.$el.html( ich['follow_widget_'+this.options.type+'_tpl'](context));

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
		ev.preventDefault();
		
		if (this.options.read_only) return;
		
		Datea.show_small_loading(this.$el);
		
		var set_options = {};
		if (this.options.silent) set_options.silent = true; 
		
		if (this.model.isNew()) {
			var self = this;
			this.model.save({},{
				success: function (model, response) {
					self.render();
					if (self.options.callback) self.options.callback();
				}
			});
			Datea.my_user_follows.add(this.model);
			this.followed_model.set('follow_count', this.followed_model.get('follow_count') + 1, set_options);
		}else {
			Datea.my_user_follows.remove(this.model);
			this.model.destroy();
			this.model = new Datea.Follow({
				object_type: this.model.get('object_type'),
				object_id: this.model.get('object_id'),
				follow_key: this.model.get('follow_key'),
			});
			this.followed_model.set('follow_count', this.followed_model.get('follow_count') - 1, set_options);
			this.render();
			if (this.options.callback) this.options.callback();
		}
		this.$el.addClass('after-click');
	},
	
	mouseleave: function (ev) {
		this.$el.removeClass('after-click');
	}
	
});