
window.Datea.Image = Backbone.Model.extend({
	urlRoot:"/api/v1/image",
});


window.Datea.ImageCollection = Backbone.Collection.extend({
	model: Datea.Image,
	url: "/api/v1/image",	
});


// create with image form element: new Datea.ImageUploadView({'el':$('#some-form')}) 
window.Datea.ImageUploadView = Backbone.View.extend({
	
	events: {
		'change .input-file': 'upload'
	},	

	upload: function() {
		var self = this;
	    $.ajax('/image/save/', {
	    	type: "POST",
	        data: $(":hidden", this.$el).serializeArray(),
	        files: $(":file", this.$el),
	        iframe: true,
	        processData: false
	    }).complete(function(data) {
	        var response = jQuery.parseJSON(data.responseText);
	        // run callback if present 
	        if (typeof(self.options.callback) != 'undefined') self.options.callback(response);
	        // fetch specified models in "fetch_model"
	        if (typeof(self.options.fetch_model) != 'undefined') self.options.fetch_model.fetch();
	    });
	}
});


/*
 * Create with following data:
 * 
 * var image_view = new Datea.ImageFormView({
 * 		model = image_model,
 * 		img_data: {
 * 			object_type: 'type_of_object' // some model - optional
 * 			object_id: pk_of_object // optional
 * 			object_field: field_name (PK OR M2M) // optional
 * 			thumb_preset: easythumbnail preset name for extra thumbnail
 * 		}
 * 		callback: an_upload_callback
 * 		
 * });
 */
window.Datea.ImageInputView = Backbone.View.extend({
	
	tagName: 'div',
	
	template: 'image_input_tpl',
	
	attributes: {
		'class': "image-input-item",
	},
	
	
	initialize: function() {
		if (typeof(this.options.img_data) == 'undefined') this.options.img_data = {};
		this.options.img_data['csrfmiddlewaretoken'] = $('#crsf-form [name="csrfmiddlewaretoken"]').val();
		if (this.options.template) {
			this.template = this.options.template;
		}
		if (this.options.placeholder){
			this.$el.addClass('has-placeholder');
		}
	},
	
	events: {
		'change .input-file': 'upload',
		'click .delete-image': 'delete_image',
	},
	
	render: function (eventName) {
		var context = this.model.toJSON();
		if (this.model.isNew() && this.options.placeholder) {
			context.thumb = this.options.placeholder;
		}
		this.$el.html( ich[this.template](context));
		if (!this.model.isNew()) {
			this.$el.removeClass('is-empty').addClass('is-full');
			$('.delete-image', this.$el).removeClass('hide');
		}else{
			this.$el.removeClass('is-full').addClass('is-empty');
		}
		
		if (this.options.no_delete) {
			this.$el.find('.delete-image').hide();
		}
		
		return this
	},	

	upload: function() {
		
		if(!this.options.hide_loading) {
			this.$el.find('.ajax-loading').removeClass('hide');
		}
		
		if (this.options.callfirst) this.options.callfirst();
		
		var self = this;
	    $.ajax('/image/save/', {
	    	type: "POST",
	        data: this.options.img_data,
	        files: $(":file", this.$el),
	        iframe: true,
	        processData: false
	    
	    }).complete(function(data) {
	 
	        var response = jQuery.parseJSON(data.responseText);
	        if (response.ok) {
	        	
		        self.model.set(response.resource);
		        
		        // run callback if present 
		        if (typeof(self.options.callback) != 'undefined') self.options.callback(response);
		        
		        self.render();
		    }
		    self.$el.find('.ajax-loading').addClass('hide');
		    
	    });
	},
	
	delete_image: function (ev) {
		ev.preventDefault();
		this.$el.find('.ajax-loading').removeClass('hide');
		var self = this;
		this.model.destroy({success:function(model, response) { 
				if (typeof(self.options.destroy_callback) != 'undefined') self.options.destroy_callback(model, response);
				self.model.unset();
				self.render();
				self.$el.find('.ajax-loading').addClass('hide');
		}});
	},
	
	clean_up: function () {
		this.$el.unbind();
        this.$el.remove();	
	}
	
});



window.Datea.ImageInputM2MView = Backbone.View.extend({
	
	tagName: 'div',
	
	events: {
		'click .add-image': 'add_image',
	},
	
	inititalize: function () {
		this.model.bind("add", this.render, this);
		this.model.bind("change", this.render, this);
		if (!this.options.img_data) this.options.img_data = {};
	},
	
	render: function(eventName) {

		this.$el.html(ich.image_input_m2m_tpl());
		
		this.check_add_button();
		
		if (this.model.length == 0){
			this.model.add( new Datea.Image({order:0}, {silent:true}));
		}
		
		var $img_el = this.$el.find('.images');
		var self = this;
		_.each(this.model.models, function(image) {
			$img_el.append( new Datea.ImageInputView({ 
				model:image, 
				img_data: self.options.img_data,
				callback: function(){
					self.check_add_button();
				},
				destroy_callback: function(single_model, response) {
					self.model.remove(single_model);
					self.render();
				}
			}).render().el);
		});
		
		return this;
	},

	add_image: function (ev) {
		ev.preventDefault();
		this.model.add(new Datea.Image({order: (this.model.length -1)}), {silent:true});
		this.render();
		console.log(this.model);
	},
	
	check_add_button: function(ev) {
		if (this.model.length == 0 || 
			(this.options.max_num && this.model.length >= this.options.max_num)) {
			$('.add-button', this.$el).addClass('hide');
		}else{
			$('.add-button', this.$el).removeClass('hide');
		}
	},
	
	clean_up: function () {
		this.$el.unbind();
        this.$el.remove();	
	}
});



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
			this.$el.html(ich.image_carousel_tpl({'carousel_id': this.attributes.id }));
			var $inner = this.$el.find('.carousel-inner');
			var i = 0;
			_.each(this.model.models, function(model) {
				var context = model.toJSON();
				if (i == 0) {
					context.active_class = 'active';
				}
				$inner.append(ich.image_carousel_item_tpl(context));
				i++;
			});
			this.$el.carousel({'interval': false});
		}
		return this;
	},
	
	start_carousel: function() {
		this.$el.carousel({'interval': false});
	},
	
}); 
