

window.Datea.UserProfileView = Backbone.View.extend({
	
	events: {
		'click .edit-profile': 'edit_profile', 
	},
	
	initialize: function() {
		this.model.bind("change", this.render, this);
	},
	
	render: function(ev) {
		var context = this.model.toJSON();
		context.show_user_actions = Datea.is_logged() && this.model.get('id') == Datea.my_user.get('id');
		context.action_create_link = gettext('action/start');
		this.$el.html(ich.my_profile_tpl(context));
		return this;
	},
	
	edit_profile: function (eventName) {
    	Datea.my_user_edit_view.open_window();
    },
	
});
