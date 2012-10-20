
window.Datea.BlogFeedView = Backbone.View.extend({
	
	className: 'blog-feed-block dotted-inner',
	
	render: function () {
		this.$el.html(ich.blog_feed_block_tpl());
		return this;
	}

});
	
