window.Datea.Comment = Backbone.Model.extend({
	urlRoot: '/api/v1/comment/'
});


window.Datea.CommentCollection = Backbone.Collection.extend({
	url:'/api/v1/comment',
	model:  Datea.Comment
});