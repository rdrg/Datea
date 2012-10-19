
window.Datea.HomeView = Backbone.View.extend({
	
	
	render: function () {
		
		// presentation block
		var title = gettext('Datea, a platform to activate and channel community engagements.');
		context = {
			title: title,
			hashtag: 'datea',
			tweet_text: title,
			full_url: get_base_url()
		}
		this.$el.html(ich.datea_presentation_tpl(context));
		
		// add right bar layout below presentation block
		this.$el.append(ich.content_layout_right_bar_tpl({dotted_bg: true}));
		
		// ACTIONS
		this.$el.find('#left-content').html(
			new Datea.MyActionListView({add_class:'unlogged'}).render().el
		);
		
		var $right_content = this.$el.find('#right-content');
		// BLOG
		$right_content.append(new Datea.BlogFeedView().render().el);
		// TWEETS
		$right_content.append(new Datea.SiteTweetView().render().el);
		
		return this;
	}
	
	
});
