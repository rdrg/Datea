


window.Datea.MappingDataView = Backbone.View.extend({
	
	initialize: function () {
		this.view_mode = 'map';
		this.mappingModel = this.options.mappingModel;
	},
	
	render: function (eventName) {
		this.$el.html( ich.mapping_data_view_tpl( this.mappingModel.toJSON()));
		
		// add map
		this.mapView = new Datea.MappingDataViewMap({
			model: this.model,
			mapModel: this.mappingModel,
			el: this.$el.find('#map-data-view'),	
		});
		this.mapView.render();
		
		// add categories
		var categories = this.mappingModel.get('item_categories');
		if (categories) {
			var $cat_el = this.$el.find('.data-view-categories');
			_.each(categories, function(cat) {
				$cat_el.append(ich.free_category_leyend_tpl(cat));
			});
			$cat_el.removeClass('hide');
		}
		
	}
	
	
});


window.Datea.MappingDataViewMap = Backbone.View.extend({
	
	
	events: {
		'click .popup-zoom': 'popup_zoom',
	},
	
	initialize: function () {
		this.model.bind('reset', this.redraw, this);
		this.model.bind('add', this.redraw, this);
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
				this.mapModel, this.model,
				{'name': 'Aportes', 'cluster': true}
			);
			
			// BUILD MAP OPTIONS
			var mapOptions = {
				"layers": ['google.streets', 'osm.mapnik'],
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
	
	redraw: function () {
		this.itemLayer.reload();
		if (this.first_draw) {
			this.map.initCenter();
		}
	},
	
	popup_zoom: function(ev) {
		ev.preventDefault();
		var id = parseInt(ev.target.dataset.id);
	},
	
	clean_up: function () {
		this.itemLayer.destroy();
		this.map.destroy();
		this.$el.unbind();
        this.$el.remove();
	}
	
});