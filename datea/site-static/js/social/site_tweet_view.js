

window.Datea.SiteTweetView = Backbone.View.extend({
	
	className: 'tweet-block dotted-inner',
	
	render: function() {
		this.$el.html(ich.tweet_block_tpl());
		this.$el.find('.tweet-list').tweet({
			username: 'somosdateros',
			avatar_size: 32,
			count: 5,
			join_text: 'auto',
			auto_join_text_default: '',
			auto_join_text_ed: gettext('we'),
			auto_join_text_ing: gettext('we were'),
			auto_join_text_reply: gettext('replied to'),
			auto_join_text_url: gettext('checking out'),
			loading_text: gettext('loading tweets...'),
			// this replaces twitter_search.html
			// query: '{{ object.query }}'
		});
		return this;
	}
	
});
