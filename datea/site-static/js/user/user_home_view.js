

window.Datea.ProfileHomeView = Backbone.View.extend({
	
	events: {
		'click .navigate': 'navigate',
	},
	
	render: function (ev) {
		
		// set base template
		this.$el.html( ich.content_layout_right_bar_tpl({dotted_bg:true}));
		
		// create tabs on main (left) content
		this.$el.find('#left-content').html(
			ich.profile_main_tabs_tpl(this.model.toJSON())
		);
		
		// render actions view in to actions tab
		// -> choose action view according to user
		if (Datea.is_logged() && this.model.get('id') == Datea.my_user.get('id')) {
			this.$el.find('#profile-actions-view').html(
				new Datea.MyActionListView().render().el
			);
		}else{
			this.$el.find('#profile-actions-view').html(
				new Datea.ProfileActionListView({user_model: this.model}).render().el
			);
		}
		
		// render history view into history tab
		this.$el.find('#profile-history-view').html(
			new Datea.HistoryView({user_model: this.model}).render().el
		);
		
		// render profile info on the right
		this.$el.find('#right-content').html(
			new Datea.UserProfileView({model: this.model}).render().el
		); 
		
		return this;
	},
	
	open_tab: function(tab) {
		switch (tab) {
			case 'actions': 
				$('#profile-actions-tablink').tab('show');
				break;
			case gettext('history'):
				$('#profile-history-tablink').tab('show');
				break;
		}	
	},
	
	navigate: function(ev) {
		ev.preventDefault();
		var nav = $(ev.target).data('nav');
		Datea.app.navigate(nav,{trigger: true});
		$(ev.currentTarget).blur();
	},
	
	reset_events: function() {
		this.undelegateEvents();
    	this.delegateEvents();
	}
		
});

