window.Datea.ThumbRow = Backbone.View.extend({
	tagName: 'div',
	
	events: {
		'click .start-lightbox': 'start_lightbox',
	},
	
	render: function (ev) {
		var context = this.model.toJSON();
		for (var i in context.images) {
			context.images[i].lightbox_id = this.model.get('id');
			context.images[i].order = i;
		}
				
		this.$el.html(ich.thumb_row_tpl(context));
		
		if (context.images.length == 1) {
			this.$el.find('.lightbox-content').html(ich.image_single_tpl(context.images[0]));
		}else{
			context.carousel_id = 'carousel-'+this.model.get('id');
			context.images[0].active_class = 'active';
			this.$el.find('.lightbox-content').html(ich.image_carousel2_tpl(context));
		}
		return this;
	},
	
	start_lightbox: function(ev) {
		ev.preventDefault();
		var self = this;
		var img = parseInt($(ev.currentTarget).data('order'));
		$('#image-lightbox-'+this.model.get('id')).on('show',function(){
			if (self.model.get('images').length > 1) {
				var $carousel = self.$el.find('.carousel');
				$carousel.carousel({interval: false});
				self.$el.find('.carousel').carousel(img); 
			}
		});
		$('#image-lightbox-'+this.model.get('id')).lightbox();
	}
	
});