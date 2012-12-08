


window.Datea.MappingMainView = Backbone.View.extend({
	
	initialize: function () {
		// get map items
		//this.map_items = new Datea.MapItemCollection();
		this.map_items = this.options.map_items;
		//this.items_fetched = false;
		//this.map_items.bind('reset', this.render, this);
		//this.map_items.bind('reset', this.reset_event, this);
		var self = this;
	},
	
	events: {
		'click .create-report': 'create_map_item',
		'click .edit-map-item': 'edit_map_item',
		'click .delete-map-item-ask': 'delete_map_item_ask',
		'click .open-popup': 'open_popup',
	},
	
	render: function (eventName) {
		
		// end date
		if (this.model.get('end_date') != null) {
			var now = new Date();
			now.setHours(0,0,0,0);
			var end = datedayFromISO(this.model.get('end_date'));
			if (now <= end) {
				var days_left = Math.ceil((end.getTime()-now.getTime())/86400000);
				if (days_left > 0) {
					this.model.set('active_message', ich.action_days_left_tpl({days_left: days_left}, true));
				}else{
					this.model.set('active_message', ich.action_last_day_tpl({days_left: days_left}, true));
				}
			}else{
				this.model.set('active_message', ich.action_expired_tpl({}, true));
			}
		}
		
		// include main layout
		this.$el.html(ich.content_layout_map_tpl({
			'content_id': 'mapping-'+this.model.get('id'),
			'class': 'mapping-content',
		}));
		
		// include data-view
		this.data_view = new Datea.MappingDataView({
			model: this.map_items, // MODEL is MAP_ITEM COLLECTION
			mappingModel: this.model,
			el: this.$el.find('#right-content')
		});
		this.data_view.render();
		
		// include sidebar view 
		this.sidebar_view = new Datea.MappingSidebar({
			el: this.$el.find('#left-content'),
			model: this.model,
			map_items: this.map_items,
		});
		//this.sidebar_view.render();
				
		return this;
	},
	
	render_tab: function(params) {
		this.sidebar_view.render_tab(params);
	},
	
	render_item: function (params) {
		this.sidebar_view.render_item(params);
		this.open_popup(params.item_id);
	},
	
	create_map_item: function (ev) {
		
		ev.preventDefault();
		
		if (!Datea.is_logged()) {
			
			var path = document.location.hash.replace('#', '/');
			document.location.href = '/accounts/login/?next='+path;
			return
		}
		
		var self = this;
		var create_rep_view = new Datea.MapItemFormView({
			model: new Datea.MapItem({
				action: this.model.get('resource_uri'),
			}),
			mappingModel: this.model,
		
			success_callback: function(model) {
				self.map_items.unshift(model);
				self.open_popup(model.get('id'));
				self.model.fetch();
			}
		});
		create_rep_view.open_window();
	},
	
	edit_map_item: function(ev) {
		ev.preventDefault();
		var self = this;
		var id = $(ev.currentTarget).data('id');
		var model = this.map_items.get(this.map_items.url+id+'/');
		var create_rep_view = new Datea.MapItemFormView({
			model: model,
			mappingModel: this.model,
			success_callback: function(model) {
				//self.map_items.trigger('reset');
				self.open_popup(model.get('id'));
				self.model.fetch();
			}
		});
		create_rep_view.open_window();
	},
	
	delete_map_item_ask: function (ev) {
		ev.preventDefault();
		var id = $(ev.currentTarget).data('id');
		var model = this.map_items.get(this.map_items.url+id+'/');
		var self = this;
		var delete_view = new Datea.MapItemDeleteView({
			model: model,
			collection: this.map_items,
			navigate_to: this.model.get('url'),
			success_callback: function () {
				self.model.fetch();
			}
		});
		delete_view.open_window();
	},
	
	open_popup: function(arg) {
		if (typeof(arg.currentTarget) != 'undefined') {
			arg.preventDefault();
			var id = $(arg.currentTarget).data('id');
		}else{
			var id = parseInt(arg);
		}
		
		// find model
		var model = this.map_items.get(this.map_items.url+id+'/');
		
		if (model.get('position') && model.get('position').coordinates) {
			// check data view filters
			// time filter
			if (this.data_view.time_filter.value != 'all') {
				var d = new Date();
				if (this.time_filter.value == 'last_month') {
					d.setMonth(d.getMonth()-1,d.getDate());  
				} else if (this.time_filter.value == 'last_week') {
					d.setDate(d.getDate()-7); 
				}
				var item_created = dateFromISO(model.get('created')); 
				if (item_created < d) {
					this.data_view.time_filter.set_value('all');
					this.data_view.filter_items();
					this.data_view.mapView.redraw(this.data_view.render_items);
				};
			}
			// status filter
			if (this.data_view.status_filter.value != 'all'
				&& this.data_view.status_filter.value != model.get('status')) {
				this.data_view.status_filter.set_value('all');
				this.data_view.filter_items();
				this.data_view.mapView.redraw(this.data_view.render_items);
			}
			// category filter
			if (this.data_view.category_filter
				&& this.data_view.category_filter.value != 'all'
				&& this.data_view.category_filter.value != model.get('category').id) {
				this.data_view.category_filter.set_value('all');
				this.data_view.filter_items();
				this.data_view.mapView.redraw(this.data_view.render_items);	
			}
		
			this.data_view.mapView.itemLayer.open_popup( id , true, true);
		}
	},
});

