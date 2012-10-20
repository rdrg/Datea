
window.Datea.MapItemAdminView = Backbone.View.extend({
	
	tagName: 'tr',
	className: 'item',
	
	template: 'map_item_admin_list_item_tpl',
	
	events: {
		'click .expand-view': 'expand',
		'click .collapse-view': 'collapse',
		'click .save-item': 'save_item',
		'click .respond-item': 'respond_item',
		'click .delete-map-item-ask': 'delete_map_item_ask',
	},
	
	initialize: function() {
		this.model.bind('change', this.change_event, this);
		this.model.bind('sync', this.sync_event, this);
	},
	
	render: function (ev) {
		var context =  this.model.toJSON();
		if (this.options.mapping_model.get('item_categories').length > 0) {
			context.has_categories = true;
		}else{
			context.has_categories = false;
		}
		context.created = formatDateFromISO(context.created, "dd.mm.yyyy - H:MM");
		context.url = this.options.mapping_model.get('url')+'/admin/item'+this.model.get('id');
		context.content = context.content.replace(/\n/g, '<br />');
		this.$el.html(ich[this.template](context));
		return this;
	},
	
	expand: function () {
		this.$el.addClass('expanded');
		this.template = 'map_item_admin_list_item_full_tpl';
		this.render();
		Datea.CheckStatsPlural(this.$el, this.model);
		
		// map
		if (this.model.get('position')) {
			var itemLayer = new Datea.olwidget.InfoLayer(
					this.options.mapping_model, {'models': [this.model]},
					{'name': 'Aportes', 'cluster': true}
				);
			var mapOptions = {
				"layers": ['google.streets', 'google.hybrid'],
				'defaultZoom': 12,
				'mapDivStyle': {'width': '320px', 'height': '240px'},
			}
			var map = new Datea.olwidget.Map("item-map-"+this.model.get('id'), [itemLayer], mapOptions);
		}
		
		// images
		if (this.model.get('images') && this.model.get('images').length > 0) {
			this.$el.find('.images').html(new Datea.ThumbRow({ model: this.model}).render().el);
		}
		
		// form init
		// populate category options with mapping categories
		if (this.options.mapping_model.get('item_categories').length > 0) {
			var $cat_el = this.$el.find('.category-select');
			var self = this;
			_.each(this.options.mapping_model.get('item_categories'), function( cat ){
				var context = jQuery.extend(true, {}, cat);
				if (self.model.get('category_id') && self.model.get('category_id') ==  cat.id ){
					context['extra_attr'] = 'selected="selected"';
				}
				context['input_name'] = 'category';
				$cat_el.append(ich.free_category_select_option_tpl(context));
			});
		}
		
		var self = this;	
		// category field
		if (this.options.mapping_model.get('item_categories').length > 0) {
			var options = [{value:'', name: gettext('-- none --')}];
			var categories = this.options.mapping_model.get('item_categories');
			_.each(categories, function(cat) {
				if (cat.active == true) {
					options.push({value: cat.id, name: ich.category_name_with_color2_tpl(cat, true)});
				}
			});
			this.category_field = new Datea.DropdownSelect({
				options: options,
				div_class: 'no-bg flat',
				box_text_max_length: 95,
			});
			this.category_field.set_value(this.model.get('category_id'));
			this.$el.find('.category-field').html(this.category_field.render().el);
		}
		
		// status field
		var options = [
			{value: 'new', name: gettext('new')},
			{value: 'reviewed', name: gettext('reviewed')},
			{value: 'solved', name: gettext('solved')},
		];
		this.status_field = new Datea.DropdownSelect({
			options: options,
			div_class: 'no-bg flat',
		});
		this.status_field.set_value(this.model.get('status'));
		this.$el.find('.status-field').html(this.status_field.render().el);
		
		this.render_replies();
		
	},
	
	render_replies: function () {
		// get replies
		var responses = new Datea.MapItemResponseCollection();
		var self = this;
		responses.fetch({
			data: {map_items__in: this.model.get('id'), order_by:'created'},
			success: function (collection, response) {
				if (collection.length > 0) {
					var $replies = self.$el.find('.replies');
					$replies.empty();
					_.each(collection.models, function(model){
						$replies.append(new Datea.MapItemResponseView({model: model}).render().el); 
					});
					$replies.show();
				}
			}
		});
	},
	
	collapse: function () {
		this.$el.removeClass('expanded');
		this.template = 'map_item_admin_list_item_tpl';
		this.render();
	},
	
	delete_map_item_ask: function (ev) {
		ev.preventDefault();
		var id = $(ev.currentTarget).data('id');
		var model = this.collection.get(this.collection.url+id+'/');
		var self = this;
		var delete_view = new Datea.MapItemDeleteView({
			model: model,
			collection: this.collection,
			navigate_to: document.location.hash,
			navigate_replace: false,
		});
		delete_view.open_window();
	},
	
	save_item: function () { 
		
		var set_fields = {};
		if (this.options.mapping_model.get('item_categories').length > 0) {
			var cat_id = this.category_field.value;
			if (cat_id == '') {
				set_fields.category = null;
				set_fields.color = this.options.mapping_model.get('default_color');
				this.model.unset('category_name', {silent: true});
				this.model.unset('category_id', {silent: true});
			}else{
				var cat = null;
				var categories = this.options.mapping_model.get('item_categories');
				var cat = _.find(categories,function(c){ return c.id == cat_id});
				set_fields = {
					category: cat,
					category_id: cat.id,
					category_name: cat.name,
					color: cat.color
				};
			}
		}
		
		set_fields.status = this.status_field.value;
		set_fields.published = $('[name="published"]', this.$el).is(':checked');
		this.model.set(set_fields);
		this.model.save();
	},
	
	respond_item: function () {
		var self = this;
		var respond_items = new Datea.MapItemCollection([this.model]); 
		var response_view = new Datea.MapItemResponseFormView({
			el: this.$el.find('.response'),
			model: new Datea.MapItemResponse(),
			map_items: respond_items,
			sync_callback: function () {
				self.render_replies();
			}
		});
		response_view.render();
	},
	
	sync_event: function () {
		//this.expand();
	},
	
	change_event: function () {
		if (this.model.hasChanged()) {
			//Datea.show_big_loading(this.$el.find('.item-edit-wrap'));
			if (this.options.change_callback) {
				this.options.change_callback();
			}
		}
	}

});