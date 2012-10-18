


window.Datea.MyProfileHomeView = Backbone.View.extend({
	
	tagName: 'div',
	
	render: function (ev) {
		
		// set base template
		this.$el.html( ich.content_layout_right_bar_tpl({dotted_bg:true}));
		
		this.$el.find('#left-content').html( 
			new Datea.MyProfileBoxView({ model: Datea.my_user }).render().el 
		);
		
		Datea.CheckStatsPlural(this.$el, this.model);
		if (Datea.is_logged()) {
			this.$el.find('.history-view-container').html(
				new DateaHistoryView({user_model: Datea.my_user}).render().el
			);
		}
		
		// ACTIONS
		this.$el.find('#right-content').html(
			new Datea.MyActionListView().render().el
		);
		return this;
	},	
});


window.Datea.ProfileView = Backbone.View.extend({
	
	tagName: 'div',
	
	render: function (ev) {
		
		this.$el.html( ich.content_layout_split_tpl({dotted_bg:true}));
		
		// profile data -> left
		this.$el.find('#left-content').html(ich.my_profile_tpl(this.model.toJSON()));
		Datea.CheckStatsPlural(this.$el, this.model);
		this.$el.find('.history-view-container').html(
			new DateaHistoryView({user_model:this.model}).render().el
		);
		
		// action data -> right
		// ACTIONS
		this.$el.find('#right-content').html(
			new Datea.ProfileActionListView({user_model: this.model}).render().el
		);
		return this;
	}	
});