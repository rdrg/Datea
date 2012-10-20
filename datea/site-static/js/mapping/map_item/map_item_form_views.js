/*********************************
 * MAP ITEM FORM VIEWS
 */
window.Datea.MapItemFormView = Backbone.View.extend({
	
	tagName: 'div',
	attributes: {
		'class': 'map-item-form', 
	},
	
	initialize: function () {
    	this.model.bind("sync", this.sync_event, this);
    	this.step = 1;
    	if (this.model.get('images')) {
    		this.image_col = new Datea.ImageCollection(this.model.get('images'));
    	}else{
    		this.image_col = new Datea.ImageCollection();
    	}
    	this.mappingModel = this.options.mappingModel;
    	
    	this.geocoder = geocoder = new google.maps.Geocoder();
    	if (this.mappingModel.get('boundary')) {
    		this.geocoder_bounds = new google.maps.LatLngBounds();
    		var points = this.mappingModel.get('boundary').coordinates[0]
    		for (var i in points) {
    			this.geocoder_bounds.extend(new google.maps.LatLng(points[i][1],points[i][0]));
    		}
    	}
   	},
   	
   	events: {
   		'click .open-step': 'open_step',
   		'click .save-map-item': 'save_map_item',
   		'submit #search-location-form': 'search_location',
   	},
	
	render: function(eventName) {
		
		var context = this.model.toJSON();
		if (this.model.isNew()) {
			context.action_name = gettext('Create');
		}else{
			context.action_name = gettext('Edit');
		}
		this.$el.html( ich.map_item_form_tpl(context));

		// populate category options with mapping categories
		var self = this;
		
		// populate category options
		var categories = []; 
		_.each(this.mappingModel.get('item_categories'), function( cat ){
			var cat_row = jQuery.extend(true, {}, cat);
			if (self.model.get('category_id') && self.model.get('category_id') ==  cat.id ){
				cat_row['extra_attr'] = 'checked="checked"';
			}
			cat_row['input_name'] = 'category';
			categories.push(cat_row);
			//$cat_el.append(ich.free_category_radio_option_tpl(context));
		});
		if (categories.length > 0) {
			context.has_categories = true;
			context.categories = categories;
		}else{
			context.has_categories = false;
		}
		// render base template
		this.$el.html( ich.map_item_form_tpl(context) );
		
		// populate images
		this.images_view = new Datea.ImageInputM2MView({
			model: this.image_col,
			el: this.$el.find('.item-images-view'),
		});
		this.images_view.render();
		
		return this;
	},
	
	
	open_step: function(ev) {
		ev.preventDefault();
		step = $(ev.currentTarget).data('step');
		
		// run validation of previous steps
		if (step > this.step) {
			for (var s=1; s<step; s++) {
				var step_valid = Datea.controls_validate(this.$el.find('#map-item-step-'+s));
				if (!step_valid) {
					$('a[href="#map-item-step-'+s+'"]', this.$el).tab('show');
					return;
				}
			}
		}
		
		// if step == 3 -> set data to model to trigger verify view
		if (step == 3) {
			this.set_model_data();
			this.$el.find('.verify-view').html(ich.map_item_form_verify_tpl(this.model.toJSON()));
		}
		
		// if everything ok -> open_step
		$('a[href="#map-item-step-'+step+'"]', this.$el).tab('show');
		
		if (step == 2 && typeof(this.map_view) == 'undefined') this.attach_map();
		
		this.step = step;
	},
	
	
	set_model_data: function () {
		
		var data = {
			content: $('[name="content"]', this.$el).val(),
			images: this.image_col.toJSON(),
		}
		
		// find selected category, if any
		if (this.mappingModel.get('item_categories').length > 0) {
			var cat_id = $('[name="category"]:checked', this.$el).val();
			var cat = null;
			var categories = this.options.mappingModel.get('item_categories');
			var cat = _.find(categories,function(c){ return c.id == cat_id});
			this.model.set({
				category: cat,
				category_id: cat.id,
				category_name: cat.name,
				color: cat.color
			},{silent: true});
		}
		this.model.set(data, {silent: true});
	},
	
	open_window: function () {
		Datea.modal_view.set_content(this);
		var self = this;
		Datea.modal_view.$el.on('shown',function(){
			if (self.step == 2) {
				if (typeof(self.map_view != 'undefined')) {
					self.map_view.map.updateSize();
				}
			}
		});
		Datea.modal_view.open_modal({backdrop: 'static', keyboard: false});
	},
	
	attach_map: function () {
		this.map_view = new Datea.MapItemPointFieldView({
			el: this.$el.find('.enter-position-view'),
			model: this.model,
			mappingModel: this.mappingModel,
		});
		this.map_view.render();
	},
	
	save_map_item: function (ev) {
		ev.preventDefault();
		Datea.show_big_loading(this.$el);
		this.was_new = this.model.isNew();
		this.model.save();
	},
	
	sync_event: function (){
		this.model.trigger('change');
		Datea.hide_big_loading(this.$el);
		if (this.options.success_callback ) {
			this.options.success_callback(this.model);
		}
		if (this.was_new) {
			var full_url = get_base_url() + this.model.get('url');
			var context = {
				'id': this.model.get('id'),
				'success_msg': this.options.mappingModel.get('report_success_message'),
				'full_url': full_url,
				'hashtag': this.options.mappingModel.get('hashtag'),
				'tweet_text': this.model.get('extract'),
				'url': this.model.get('url'),
			}
			this.$el.html( ich.map_item_form_success_tpl(context));
			init_share_buttons();
		}else{
			Datea.modal_view.close_modal();
		}
	},
	
	search_location: function (ev) {
		ev.preventDefault();
		var address = $('.search-address', this.$el).val();
		if (address == '') return;
		var search_data = { 'address': address};
		if (this.geocoder_bounds){
			search_data.bounds = this.geocoder_bounds;
		}
		var self = this;
    	this.geocoder.geocode( search_data, function(results, status) {
      		if (status == google.maps.GeocoderStatus.OK) {
        		var lat = results[0].geometry.location.lat();
        		var lng = results[0].geometry.location.lng();
        		self.model.set('position', {coordinates: [lng, lat], type: 'Point'}, {silent: true});
        	
        		var zoom_bounds = [
        			{coordinates: [results[0].geometry.viewport.getNorthEast().lng(), results[0].geometry.viewport.getNorthEast().lat()], type: "Point"},
        			{coordinates: [results[0].geometry.viewport.getSouthWest().lng(), results[0].geometry.viewport.getSouthWest().lat()], type: "Point"},
        		];
        		self.map_view.set_model(self.model, zoom_bounds);
        	
      		} else {
        		var input = $('.search-address', self.$el);
        		input.val( gettext("no location found") );
        		input.addClass('error-text');
        		setTimeout(function(){
        			input.val('');
        			input.removeClass('error-text');
        		}, 1500)
      		}
    	});
	},
	
	clean_up: function() {
		this.map_view.clean_up();
		this.images_view.clean_up();
		this.verify_view.clean_up();
		this.$el.unbind();
        this.$el.remove();
	}
	
});


window.Datea.MapItemPointFieldView = Backbone.View.extend({
	
	render: function () {
		this.$el.html( ich.map_edit_point_tpl());
	    
	    this.pointLayer = new Datea.olwidget.EditableLayer(
			this.model, 
			'position', 
			{"name": gettext("Position")}, 
			this.options.mappingModel.get('center'), 
			this.options.mappingModel.get('boundary')
		);
	    
	    var $mapDiv = $('#map_edit_point'); 
	    this.map = new Datea.olwidget.Map('map_edit_point', [this.pointLayer], 
		    { "layers": ['google.streets', 'google.hybrid'],
		      "mapDivStyle": {'width': $mapDiv.css('width'), 'height': $mapDiv.css('height')},
		      "overlayStyle": {
		      	"externalGraphic": "/static/js/libs/datea_openlayers/img/marker.png", 
		      	"graphicHeight": 21, 
		      	"graphicWidth": 16, 
		      	"graphicOpacity": 1
		      },
		      'mapOptions': {
		      	"controls" : ['LayerSwitcher', 'Navigation', 'PanZoom', 'Attribution'],
		      	'numZoomLevels': 20,
		      }
		    }
		);
		this.pointLayer.initCenter();
		this.pointLayer.setEditOn();
		
    	return this;
	},
	
	set_model: function(model, zoom_bounds) {
		this.pointLayer.layer.mapModel = model;
		this.pointLayer.layer.destroyFeatures();
		this.pointLayer.readModel(zoom_bounds);
	},
	
	clean_up: function () {
		this.map.destroy();
		this.pointLayer.destroy();
        this.$el.unbind();
        this.$el.remove();
    }
});

window.Datea.MapItemDeleteView = Backbone.View.extend({
	
	tagName: 'div',
	
	events: {
		'click .delete-map-item': 'delete_map_item',
	},
	
	initialize: function () {
		if (!this.options.navigate_replace) {
			this.options.navigate_replace = true;
		}
	},
	
	render: function (ev) {
		this.$el.html(ich.map_item_delete_dialog_tpl());
		return this;
	},
	
	open_window: function () {
		this.render();
		Datea.modal_view.set_content(this);
		Datea.modal_view.open_modal();
	},
	
	delete_map_item: function(ev) {
		ev.preventDefault();
		Datea.show_big_loading(this.$el);
		var self = this;
		this.model.destroy({
			success: function (model, response) {
				self.collection.remove(model);
				Datea.app.navigate(self.options.navigate_to, {trigger: true, replace: self.options.navigate_replace});
				Datea.modal_view.close_modal();
				if (typeof(self.options.success_callback) != 'undefined') self.options.success_callback();
			}
		});
	},
	
});
