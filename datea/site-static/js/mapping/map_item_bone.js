/***********************************
 *
 *  MAP ITEM
 *
 **/
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



window.Datea.MapItemFullView = Backbone.View.extend({
	
	initialize: function () {
		this.model.bind('sync', this.render, this);
	},
	
	render: function() {
		
		var context = this.model.toJSON();
		// hydrate context 
		context.created = formatDateFromISO(context.created, "dd.mm.yyyy - H:MM");
		context.content = context.content.replace(/\n/g, '<br />');
		this.$el.html( ich.map_item_full_tpl(context) );
		
		// images
		if (context.images && context.images.length > 0) {
			var image_col = new Datea.ImageCollection(context.images);
			var carousel_view = new Datea.ImageCarousel({
				model: image_col,
				carousel_id: 'map-item-carousel-'+this.model.get('id'),
			});
			this.$el.find('.images').html(carousel_view.render().el);
		}
		
		// can edit?
		if (!Datea.my_user.isNew() && (
			this.options.mappingModel.get('user').id == Datea.my_user.get('id')
			|| Datea.my_user.get('id') == this.model.get('user').id
			|| Datea.my_user.get('is_staff'))){
				this.$el.find('.edit-map-item').removeClass('hide');
		}
		
		// has position?
		if (!this.model.get('position') || !this.model.get('position').coordinates) {
			this.$el.find('.open-popup').hide();
		}
		
		// get replies
		var responses = new Datea.MapItemResponseCollection();
		var self = this;
		responses.fetch({
			data: {map_items__in: this.model.get('id'), order_by:'created'},
			success: function (collection, response) {
				if (collection.length > 0) {
					var $replies = self.$el.find('.replies');
					_.each(collection.models, function(model){
						$replies.append(new Datea.MapItemResponseView({model: model}).render().el); 
					});
					$replies.show();
				}
			}
		})
		
		// comments
		this.comments = new Datea.CommentCollection();
		this.comment_view = new Datea.CommentsView({
			el: this.$el.find('.comments'),
			model: this.comments,
			object_type: 'dateamapitem',
			object_id: this.model.get('id'),
		})
		this.comments.fetch({
			data: {'object_type': 'dateamapitem', 'object_id': this.model.get('id'), order_by: 'created'} 
		});
		
		//***************
		// widgets
		var $widgets = this.$el.find('.datea-widgets');
		
		// FOLLOW WIDGET
		var follow_key = 'dateamapitem.'+this.model.get('id');
		var follow = Datea.my_user_follows.find(function(item){
			return item.get('follow_key') == follow_key;
		});
		if (typeof(follow) == 'undefined') {
			follow = new Datea.Follow({
				follow_key: follow_key,
				object_type: 'dateamapitem',
				object_id: this.model.get('id'),
			});
		}
		this.follow_widget = new Datea.FollowWidgetView({
			model: follow,
			followed_model: this.model,
			size: 'small' 
		});
		$widgets.append(this.follow_widget.render().el);
		
		
		// VOTE WIDGET
		var id = this.model.get('id');
		var vote = Datea.my_user_votes.find(function(item){
			return item.get('object_type') == 'dateamapitem' && item.get('object_id') == id;
		});
		if (typeof(vote) == 'undefined') {
			vote = new Datea.Vote({
				object_type: 'dateamapitem',
				object_id: this.model.get('id'),
			});
		}
		this.vote_widget = new Datea.VoteWidgetView({
			model: vote,
			voted_model: this.model,
			size: 'small' 
		});
		$widgets.append(this.vote_widget.render().el);
		
		return this;
	},
	
	clean_up: function () {
		this.$el.unbind();
        this.$el.remove();
	}
});


window.Datea.MapItemTeaserView = Backbone.View.extend({
	
	tagName: 'div',
	attributes: {
		class : "map-item teaser",
	},
	
	initialize: function () {
		this.model.bind('sync', this.render, this);
		this.model.bind('change', this.render, this);
		this.attributes.id = 'map-item-teaser-'+this.model.get('id');
	},
	
	render: function() {
		
		var context = this.model.toJSON();
		// hydrate context 
		context.created = formatDateFromISO(context.created, "dd.mm.yyyy - H:MM");
		this.$el.html( ich.map_item_teaser_tpl(context) );
		
		// has position?
		if (!this.model.get('position') || !this.model.get('position').coordinates) {
			this.$el.find('.open-popup').hide();
		}
		
		return this;
	},
	
	clean_up: function () {
		this.$el.unbind();
        this.$el.remove();
	}
	
});



window.Datea.MapItemPopupView = Backbone.View.extend({
	
	tagName: 'div',
	
	events: {
		'click .popup-zoom': 'zoom',
	},
	
	initialize: function () {
		this.model.bind('sync', this.render, this);
		this.model.bind('change', this.render, this);
	},
	
	render: function() {
		
		var context = this.model.toJSON();
		// hydrate context 
		context.created = formatDateFromISO(context.created, "dd.mm.yyyy - H:MM");
		this.$el.html( ich.map_item_popup_tpl(context) );
		return this;
	},
	
	zoom: function(ev) {
		ev.preventDefault();
		this.options.mapLayer.open_popup( this.model.get('id') , true, true);
	},
	
	clean_up: function () {
		this.$el.unbind();
        this.$el.remove();
	}
	
});






