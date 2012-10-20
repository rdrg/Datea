
Datea.CheckStatsPlural = function ($el, model) {
	// votes
	if (model.get('vote_count') && model.get('vote_count') == 1) {
		$('.vote_count .singular', $el).show();
		$('.vote_count .plural', $el).hide();
	}
	// comment
	if (model.get('comment_count') && model.get('comment_count') == 1) {
		$('.comment_count .singular', $el).show();
		$('.comment_count .plural', $el).hide();
	}
	// items (contributions / dateos)
	if (model.get('item_count') && model.get('item_count') == 1) {
		$('.item_count .singular', $el).show();
		$('.item_count .plural', $el).hide();
	}
	// followers
	if (model.get('follow_count') && model.get('follow_count') == 1) {
		$('.follow_count .singular', $el).show();
		$('.follow_count .plural', $el).hide();
	}
	// followers
	if (model.get('user_count') && model.get('user_count') == 1) {
		$('.user_count .singular', $el).show();
		$('.user_count .plural', $el).hide();
	}
}