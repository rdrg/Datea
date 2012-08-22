


window.Datea.MappingDataView = Backbone.View.extend({
	
	initialize: function () {
		this.model.bind('reset', this.render, this);
		this.model.bind('add', this.add_event, this);
		this.view_mode = 'map';
		this.mappingModel = this.options.mappingModel;
	},
	
	add_event: function(model) {
		this.filter_items();
		this.mapView.redraw(this.render_items);
	},
	
	render: function (eventName) {
		
		this.$el.html( ich.mapping_data_view_tpl( this.mappingModel.toJSON()));
		
		this.filter_items();
		
		// add map
		this.mapView = new Datea.MappingDataViewMap({
			model: this.model,
			render_items: this.render_items,
			mapModel: this.mappingModel,
			el: this.$el.find('#map-data-view'),	
		});
		this.mapView.render();
		
		// add categories
		var categories = this.mappingModel.get('item_categories');
		
		if (typeof(categories) != 'undefined' && categories.length > 0) {
			var per_row = 4;
			var $cat_el = this.$el.find('.data-view-category-leyend');
			var rows = Math.ceil(categories.length / per_row);
			for (var i=0; i<rows; i++) {
				var cat_row = _.rest(categories, i*per_row);
				cat_row =  _.first(cat_row, per_row);
				var row = [];
				for (var j in cat_row) {
					var cat = {name: cat_row[j]['name'], color: cat_row[j]['color']};
					if (cat.name.length > 36) {
						cat.title = cat.name;
						cat.name = cat.name.substr(0,36)+'...';
					}
					row.push(cat);
				}
				$cat_el.append( ich.free_category_leyend__group_tpl({categories: row}));
			}
			$cat_el.removeClass('hide');
		}
		
		var self = this;
		
		// category filter
		if (typeof(categories) != 'undefined' && categories.length > 0) {

			var options = [{value:'all', name: gettext('All categories')}];
			_.each(categories, function(cat) {
				if (cat.active == true) {
					options.push({value: cat.id, name: ich.category_name_with_color2_tpl(cat, true)});
				}
			});
			this.category_filter = new Datea.DropdownSelect({
				options: options,
				div_class: 'dropup no-bg',
				callback: function () { self.filter_items(); self.mapView.redraw(self.render_items); },
				box_text_max_length: 90,
			});
			this.$el.find('.category-filter').html(this.category_filter.render().el);
		}
		
		
		// status filter
		var options = [
			{value: 'new', name: gettext('new')},
			{value: 'reviewed', name: gettext('reviewed')},
			{value: 'solved', name: gettext('solved')},
			{value: 'all', name: gettext('any state')},
		];
		this.status_filter = new Datea.DropdownSelect({
			options: options,
			div_class: 'dropup no-bg',
			callback: function () { self.filter_items(); self.mapView.redraw(self.render_items);}
		});
		this.$el.find('.status-filter').html(this.status_filter.render().el);
		
		
		// time filter
		var options = [
			{value: 'all', name: gettext('since start') },
			{value: 'last_week', name: gettext('last week') },
			{value: 'last_month', name: gettext('last month') }
		];
		this.time_filter = new Datea.DropdownSelect({
			options: options,
			div_class: 'dropup no-bg',
			callback: function () { self.filter_items(); self.mapView.redraw(self.render_items); }
		});
		this.$el.find('.time-filter').html(this.time_filter.render().el);
				
	},
	
	filter_items: function () {
		
		var self = this;
		var render_items = this.model.models;
		
		// category filter
		if (this.category_filter && this.category_filter.value != 'all') {
			render_items = _.filter(render_items, function (item) { 
				return item.get('category_id') == self.category_filter.value;
			});
		}
		
		// status filter
		if (this.status_filter && this.status_filter.value != 'all') {
			render_items = _.filter(render_items, function (item) { 
				return item.get('status') == self.status_filter.value;
			});
		}
		
		// Time filter
		if (this.time_filter && this.time_filter.value != 'all') {
			var d = new Date();
			if (this.time_filter.value == 'last_month') {
				d.setMonth(d.getMonth()-1,d.getDate());  
			} else if (this.time_filter.value == 'last_week') {
				d.setDate(d.getDate()-7); 
			}
			render_items = _.filter(render_items, function (item) {
				var item_created = dateFromISO(item.get('created')); 
				return item_created >= d;
			});
		}
		
		// published filter
		render_items = _.filter(render_items, function (item) {
			return item.get('published');
		});
		
		this.render_items = new Datea.MapItemCollection(render_items);
	},
	
});


window.Datea.MappingDataViewMap = Backbone.View.extend({
	
	
	events: {
		'click .popup-zoom': 'popup_zoom',
	},
	
	initialize: function () {
		//this.model.bind('add', this.redraw, this);
		this.model.bind('sync', this.redraw, this);
		this.mapModel = this.options.mapModel;
		this.first_draw = true;
	},
	
	render: function (eventName) {
		this.draw();
		return this;
	},
	
	draw: function () {
		if (typeof(this.map) != 'undefined') {
			this.itemLayer.reload();
			this.map.updateSize();
			this.map.initCenter();
		}else{
			this.itemLayer = new olwidget.DateaMainMapItemLayer(
				this.mapModel, this.options.render_items,
				{'name': 'Aportes', 'cluster': true}
			);
			
			// BUILD MAP OPTIONS
			var mapOptions = {
				"layers": ['google.streets'],
				'defaultZoom': 12,
			}
			if (this.mapModel.get('center') && this.mapModel.get('center').coordinates) {
				mapOptions.defaultLon = this.mapModel.get('center').coordinates[0];
				mapOptions.defaultLat =  this.mapModel.get('center').coordinates[1];
			}
			if (this.mapModel.get('boundary') && this.mapModel.get('boundary').coordinates) {
				mapOptions.defaultBoundary = this.mapModel.get('boundary');
			}
			
			this.map = new olwidget.DateaMainMap("map-data-view", [this.itemLayer], mapOptions);
		}
	},
	
	redraw: function (render_items) {
		
		if (typeof(render_items) != 'undefined') {
			this.itemLayer.mapItems = render_items;
		}
		this.itemLayer.reload();
		if (this.first_draw) {
			this.map.initCenter();
		}
	},
	
	popup_zoom: function(ev) {
		ev.preventDefault();
	},
	
	clean_up: function () {
		this.itemLayer.destroy();
		this.map.destroy();
		this.$el.unbind();
        this.$el.remove();
	}
});

