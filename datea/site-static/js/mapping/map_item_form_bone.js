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
   	},
   	
   	events: {
   		'click .open-step': 'open_step',
   		'click .save-map-item': 'save_map_item',
   	},
	
	render: function(eventName) {
		
		var context = this.model.toJSON();
		if (this.model.isNew()) {
			context.action_name = 'Crear';
		}else{
			context.action_name = 'Editar';
		}
		this.$el.html( ich.map_item_form_tpl(context));

		// populate category options with mapping categories
		var $cat_el = this.$el.find('.category-options');
		var self = this;
		
		// populate category options
		_.each(this.mappingModel.get('item_categories'), function( cat ){
			var context = jQuery.extend(true, {}, cat);
			if (self.model.get('category_id') && self.model.get('category_id') ==  cat.id ){
				context['extra_attr'] = 'checked="checked"';
			}
			context['input_name'] = 'category';
			$cat_el.append(ich.free_category_radio_option_tpl(context));
		});
		
		// populate images
		this.images_view = new Datea.ImageInputM2MView({
			model: this.image_col,
			el: this.$el.find('.item-images-view'),
		});
		this.images_view.render();
		
		// Verify Step view
		this.verify_view = new Datea.MapItemFormVerifyView({
			model: this.model,
			el: this.$el.find('.verify-view')
		})
		
		return this;
	},
	
	
	open_step: function(ev) {
		ev.preventDefault();
		step = ev.target.dataset.step;
		
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
			this.verify_view.render();
		}
		
		// if everything ok -> open_step
		$('a[href="#map-item-step-'+step+'"]', this.$el).tab('show');
		
		if (step == 2 && typeof(this.map_view) == 'undefined') this.attach_map();
		
		this.step = step;
	},
	
	
	set_model_data: function () {
		
		// find selected category
		var cat_id = $('[name="category"]:checked', this.$el).val()
		var cat = null;
		var categories = this.options.mappingModel.get('item_categories');
		var cat = _.find(categories,function(c){ return c.id == cat_id});

		var data = {
			category: cat,
			category_id: cat.id,
			category_name: cat.name,
			category_color: cat.color,
			content: $('[name="content"]', this.$el).val(),
			images: this.image_col.toJSON(),
		}
		this.model.set(data, {silent: true});
	},
	
	open_window: function () {
		Datea.modal_view.set_content(this);
		var self = this;
		Datea.modal_view.$el.on('shown',function(){
			if (self.step == 2) {
				if (typeof(self.map_view != 'undefined')) {
					self.map_view.map_and_layer.map.updateSize();
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
			var base_url = window.location.protocol+'//'+window.location.host;
			var full_url = base_url + this.model.get('url');
			var context = {
				'id': this.model.get('id'),
				'success_msg': this.options.mappingModel.get('"report_success_message'),
				'full_url': full_url,
				'url': this.model.get('url'),
			}
			this.$el.html( ich.map_item_form_success_tpl(context));
			Datea.share.init_add_this();
		}else{
			Datea.modal_view.close_modal();
		}
	},
	
	clean_up: function() {
		this.map_view.clean_up();
		this.images_view.clean_up();
		this.verify_view.clean_up();
		this.$el.unbind();
        this.$el.remove();
	}
	
});


window.Datea.MapItemFormVerifyView = Backbone.View.extend({
	
	render: function () {
		this.$el.html(ich.map_item_form_verify_tpl(this.model.toJSON()));
		
		// include images
		var $img_el = this.$el.find('.verify-images');
		_.each(this.model.get('images'), function(image) {
			if (image.thumb){
				$img_el.append( ich.map_item_form_verify_image_tpl(image) );
			}
		});
	},
	
	clean_up: function() {
		this.$el.unbind();
        this.$el.remove();
	}
});



window.Datea.MapItemPointFieldView = Backbone.View.extend({
	
	render: function () {
		this.$el.html( ich.map_edit_point_tpl());
		var boundaryData;
		if (this.options.mappingObject && this.options.mappingObject.attributes.boundary) {
			boundaryData = this.options.mappingObject.get('position');
		}
		this.map_and_layer = Datea.CreateEditablePointMap(
			'map_edit_point', 
			this.model, 
			'position', 
			this.options.mappingModel.get('center'), 
			this.options.mappingModel.get('boundary')
		);
    	return this;
	},
	
	clean_up: function () {
		this.map_and_layer.map.destroy();
		this.map_and_layer.layer.destroy();
        this.$el.unbind();
        this.$el.remove();
    }
});