
window.Datea.MapItemResponse = Backbone.Model.extend({
	urlRoot : '/api/v1/map_item_response/',
});

window.Datea.MapItemResponseCollection = Backbone.Collection.extend({
	url: '/api/v1/map_item_response/',
	model: Datea.MapItemResponse,
});