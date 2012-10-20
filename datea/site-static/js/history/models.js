
window.Datea.History = Backbone.Model.extend({
	urlRoot: '/api/v1/history'
});

window.Datea.HistoryCollection = Backbone.Collection.extend({
	model: Datea.History,
	url: '/api/v1/history',
});