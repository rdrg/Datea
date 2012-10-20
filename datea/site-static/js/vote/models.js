window.Datea.Vote = Backbone.Model.extend({
	urlRoot: '/api/v1/vote'
});

window.Datea.VoteCollection = Backbone.Collection.extend({
	model: Datea.Vote,
	url: '/api/v1/vote',
});