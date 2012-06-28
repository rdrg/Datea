/***********************************
 *
 *  MAP ITEM
 *
 * */
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
		this.model.bind('sync', this.render, this)
	},
	
	render: function() {
		
		var context = this.model.toJSON();
		// hydrate context 
		context.created = formatDateFromISO(context.created, "dd.mm.yyyy - H:M");
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
		this.attributes.id = 'map-item-teaser-'+this.model.get('id');
	},
	
	render: function() {
		
		var context = this.model.toJSON();
		// hydrate context 
		context.created = formatDateFromISO(context.created, "dd.mm.yyyy - H:M");
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
	
	initialize: function () {
		this.model.bind('sync', this.render, this);
	},
	
	render: function() {
		
		var context = this.model.toJSON();
		// hydrate context 
		context.created = formatDateFromISO(context.created, "dd.mm.yyyy - H:M");
		this.$el.html( ich.map_item_popup_tpl(context) );
		return this;
	},
	
	clean_up: function () {
		this.$el.unbind();
        this.$el.remove();
	}
	
});




