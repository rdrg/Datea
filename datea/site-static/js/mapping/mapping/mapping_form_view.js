
window.Datea.MappingFormView = Backbone.View.extend({
	
	tagName: 'div',
	
	events: {
		'click .save-mapping': 'save_mapping',
		'shown [data-toggle="tab"]': 'attach_map',
		'click .delete-mapping-ask': 'delete_ask',
	},

	initialize: function() {
		//this.model.bind("reset", this.render, this);
        //this.model.bind("sync", this.sync_event, this);
        if (this.model.attributes.item_categories) {
        	this.item_cat_col = new Datea.FreeCategoryCollection(this.model.attributes.item_categories);
        }else{
        	this.item_cat_col = new Datea.FreeCategoryCollection();
        }
  	},
	
	render: function(eventName) {
		
		var context = this.model.toJSON();
		if (this.model.isNew()) {
			context.action_name = gettext('Create');
		}else{
			context.action_name = gettext('Edit');
		}
		if (context.end_date != null) {
			if (Datea.lang == 'en') {
				context.end_date_date = formatDateFromISO(context.end_date, "mm/dd/yyyy");
			}else{
				context.end_date_date = formatDateFromISO(context.end_date, "dd/mm/yyyy");
			}
			context.end_date_time = formatDateFromISO(context.end_date, "HH:MM");
		}
		if (this.model.isNew()) context.published = true;
		
		var page_title = context.action_name+' '+gettext('mapping');
		if (context.name && context.name != '') page_title= page_title+': '+context.name;
		this.$el.html(ich.mapping_admin_zone_head_tpl({page_title: page_title}));
		this.$el.append(ich.content_layout_single_tpl());
		this.$el.find('#content').html( ich.mapping_form_tpl(context));
		
		// select category if set
		if (this.model.get('category')) {
			var $sel = this.$el.find('#id_category');
			Datea.set_select_control($sel, this.model.get('category').id);
		}
		
		// Item Categories
		var cat_items = [];
		
		var cat_view = new Datea.FreeCategoryEditListView({
			el: this.$el.find('#edit-mapping-categories'),
			model: this.item_cat_col,
		})
		cat_view.render();
		
		// MAPPING IMAGE
		var img = new Datea.Image();
		if (this.model.get('image')) img.set(this.model.get('image'));
		
		var self = this;
		var img_view = new Datea.ImageInputView({
			model: img, 
			callback: function(data){
				if (data.ok) {
					self.model.set({image: data.resource }, {silent: true});
				}
			},
			destroy_callback: function(response) {
				self.model.set('image', null,{ silent: true });
			} 
		});
		this.$el.find('#mapping-image-input-view').html(img_view.render().el);
		
		return this;	
	},
	
	save_mapping: function(ev) {
		ev.preventDefault();
		var self = this;
		if (Datea.controls_validate(this.$el, function(){
			$('.edit-mapping-settings', self.$el).tab('show');
		})){
			
			// validate position (needs position or boundary!)
			if (!this.model.get('center') && !this.model.get('boundary')) {
				$('.map-settings-label',this.$el).css('color', 'red');
				$('.edit-mapping-boundary',this.$el).tab('show');
				$(window).scrollTop(0);
				return;
			}
			
			// proceed to save
			Datea.show_big_loading(this.$el);
			
			var hashtag = $('[name="hashtag"]', this.$el).val().replace('#','');
			var set_data = {
				name: $('[name="name"]', this.$el).val(),
				short_description: $('[name="short_description"]', this.$el).val(),
				published: $('[name="published"]', this.$el).is(':checked'),
				mission: $('[name="mission"]', this.$el).val(),
				information_destiny: $('[name="information_destiny"]', this.$el).val(),
				category: $('[name="category"]', this.$el).val(),
				item_categories: this.item_cat_col.toJSON(),
				color: $('[name="color"]', this.$el).val(),
				hashtag: hashtag,
			}
			if (set_data['category'] == '') set_data['category'] = null;
			
			var end_date = $('[name="end_date_date"]').val();
			if (end_date != '') {
				var edate = end_date.split('/');
				
				//var end_time = $('[name="end_date_time"]').val();
				//if (end_time == '') end_time = '00:00';
				var end_time = '00:00';
				if (Datea.lang == 'en') {
					var isodate = edate[2]+'-'+edate[0]+'-'+edate[1]+'T'+end_time+':00';
				}else{
					var isodate = edate[2]+'-'+edate[1]+'-'+edate[0]+'T'+end_time+':00';
				}
				set_data.end_date = isodate;
			}
			
			var is_new = this.model.isNew();
			var self = this;
			
			this.model.set(set_data,{ silent: true});
			this.model.save({},
				  {
					success: function(model, response){
						self.model.fetch({'success': function(){
							// add follow object to my follows
							if (is_new) {
								var follow = new Datea.Follow();
								follow.save({
									follow_key: 'dateaaction.'+model.get('id'),
									object_type: 'dateaaction',
									object_id: model.get('id'),
								}, {
									success: function (model, response) {
										Datea.my_user_follows.add(model);
									}
								})
							}
							Datea.app.navigate('/'+gettext('mapping')+'/'+model.attributes.id, {trigger: true});
						}});
					},
					error: function(model,response) {
						console.log("error");	
					}
			});
		}
	},
	
	attach_map: function (e) {
		
		if (typeof(e) != 'undefined' && e.currentTarget.hash == '#mapping-boundary' && !this.map_view) {
			this.map_view = new Datea.MapEditMultiLayerView({
				el: this.$el.find('#edit-mapping-position'),
				mapModel: this.model,
			});
			this.map_view.render();
		}
	},
	
	delete_ask: function(ev) {
		var delete_view = new Datea.MappingDeleteView({
			model: this.model,
		});
		delete_view.open_window();
	}
	
});


window.Datea.MapEditMultiLayerView = Backbone.View.extend({
	
	render: function(){
		this.$el.html( ich.mapping_edit_boundary_tpl());
		
		var map = new Datea.olwidget.Map('map_edit_boundary', [
        	new Datea.olwidget.EditableLayer( this.options.mapModel, 'center', 
        		{
        		 'name': gettext("Center"), 'geometry': 'point', 
        		 'overlayStyle': {'fillColor': "#ff0000", 'strokeColor': "#ff0000"},  
        		}
        	),
        	new Datea.olwidget.EditableLayer( this.options.mapModel, 'boundary', 
        		{'name': gettext("Boundary"), 'geometry': 'polygon',
        		 'overlayStyle': {'fillColor': "#ecff00", 'strokeColor': "#ecff00"},  
  				}
        	),
    	], { 
    		'overlayStyle': { 'fillColor': "#ff0000" }, 
    		'layers': ['google.streets', 'google.hybrid'],
    		'mapDivStyle': {
                'width': '100%',
                'height': '550px'
            	}
    		}
    	);
    	return this;
	}
});


window.Datea.MappingDeleteView = Backbone.View.extend({
	
	tagName: 'div',
	
	events: {
		'click .delete-mapping': 'delete_mapping',
	},
	
	render: function (ev) {
		this.$el.html(ich.mapping_delete_dialog_tpl());
		return this;
	},
	
	open_window: function () {
		this.render();
		Datea.modal_view.set_content(this);
		Datea.modal_view.open_modal();
	},
	
	delete_mapping: function(ev) {
		ev.preventDefault();
		Datea.show_big_loading(this.$el);
		var self = this;
		this.model.destroy({
			success: function (model, response) {
				Datea.app.navigate('/', {trigger: true, replace: true});
				Datea.modal_view.close_modal();
			}
		});
	},
});

