
window.Datea.Mapping = Backbone.Model.extend({
	urlRoot:"/api/v1/mapping",
});

//++++++++++++++++++++
// Profiles Collection
window.Datea.MappingCollection = Backbone.Collection.extend({
	model: Datea.Mapping,
	url: '/api/v1/mapping/',
});