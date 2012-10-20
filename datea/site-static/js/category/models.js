
// Free category Model
window.Datea.FreeCategory = Backbone.Model.extend({
	urlRoot:"/api/v1/free_category",
});

// Free Category Collection 
window.Datea.FreeCategoryCollection = Backbone.Collection.extend({
	model: Datea.FreeCategory,
	url: "/api/v1/free_category"
});