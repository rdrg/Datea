window.Datea.ImageCarousel = Backbone.View.extend({
	
	tagName: 'div',
	attributes: {
		'class': 'carousel slide images',
	},
	
	initialize: function() {
		this.attributes.id = this.options.carousel_id;
		this.$el.attr('id',this.attributes.id);  
	},
	
	render: function () {
		if (this.model.length == 1) {
			this.$el.html( ich.image_single_tpl({image: this.model.models[0].get('image')}));
		}else{
			var context = {'carousel_id': this.attributes.id, 'images':[] };
			var $inner = this.$el.find('.carousel-inner');
			var i = 0;
			_.each(this.model.models, function(model) {
				var mod= model.toJSON();
				mode.order = i;
				context.images.push(model.toJSON());
				i++;
			});
			this.$el.html(ich.image_carousel_tpl(context));
			this.$el.carousel({'interval': false});
			this.$el.carousel(0);
		}
		return this;
	},
	
	start_carousel: function() {
		this.$el.carousel({'interval': false});
	},
});