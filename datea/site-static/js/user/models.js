//++++++++++++++++++++++
// User model
window.Datea.User = Backbone.Model.extend({
	urlRoot: "/api/v1/user",
});

//++++++++++++++++++++++
// Profile model
window.Datea.Profile = Backbone.Model.extend({
	urlRoot: "/api/v1/profile",
});

//++++++++++++++++++++++
// User Collection
window.Datea.UserCollection = Backbone.Collection.extend({
	model: Datea.User,
	url: "/api/v1/user",
});