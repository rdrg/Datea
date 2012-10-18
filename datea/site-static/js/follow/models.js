
window.Datea.Follow = Backbone.Model.extend({
	urlRoot: '/api/v1/follow'
});

window.Datea.FollowCollection = Backbone.Collection.extend({
	model: Datea.Follow,
	url: '/api/v1/follow',
});

window.Datea.NotifySettings = Backbone.Model.extend({
	urlRoot: '/api/v1/notify_settings'
});