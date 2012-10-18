
window.Datea.MapItem = Backbone.Model.extend({
	urlRoot:"/api/v1/map_item/",
});


window.Datea.MapItemCollection = Backbone.Collection.extend({
	
	model: Datea.MapItem,
	url:"/api/v1/map_item/",
	
	pagination : function(perPage, page) {
       var result = _.rest(this.models, perPage*page);
       return _.first(result, perPage);    
    }
});