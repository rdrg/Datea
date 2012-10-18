
// DateaAction backbone model 
window.Datea.Action = Backbone.Model.extend();

// Action Collection
window.Datea.ActionCollection = Backbone.Collection.extend({
	model: Datea.Action,
	url: '/api/v1/action/search',
});