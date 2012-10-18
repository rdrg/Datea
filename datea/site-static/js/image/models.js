window.Datea.Image = Backbone.Model.extend({
	urlRoot:"/api/v1/image",
});

window.Datea.ImageCollection = Backbone.Collection.extend({
	model: Datea.Image,
	url: "/api/v1/image",	
});