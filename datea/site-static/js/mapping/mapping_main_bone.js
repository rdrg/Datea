
window.Datea.Mapping = Backbone.Model.extend({
	urlRoot:"/api/v1/mapping",
});

//++++++++++++++++++++
// Profiles Collection
window.Datea.MappingCollection = Backbone.Collection.extend({
	model: Datea.Mapping,
	url: '/api/v1/mapping/',
});

window.Datea.MappingMainView = Backbone.View.extend({
	
	initialize: function () {
		// get map items
		//this.map_items = new Datea.MapItemCollection();
		this.map_items = this.options.map_items;
		//this.items_fetched = false;
		//this.map_items.bind('reset', this.render, this);
		this.map_items.bind('reset', this.reset_event, this);
		var self = this;
	},
	
	events: {
		'click .create-report': 'create_map_item',
		'click .edit-map-item': 'edit_map_item',
		'click .open-popup': 'open_popup',
	},
	
	render: function (eventName) {
		// include main layout
		this.$el.html(ich.map_base_content_split_tpl({
			'content_id': 'mapping-'+this.model.get('id'),
			'class': 'mapping-content',
		}));
		
		// include sidebar view 
		this.sidebar_view = new Datea.MappingSidebar({
			el: this.$el.find('#left-content'),
			model: this.model,
			map_items: this.map_items,
		});
		//this.sidebar_view.render();
		
		// include data-view
		this.data_view = new Datea.MappingDataView({
			model: this.map_items, // MODEL is MAP_ITEM COLLECTION
			mappingModel: this.model,
			el: this.$el.find('#right-content')
		});
		this.data_view.render();
		
		// mapping setting controls
		if (!Datea.my_user.isNew() &&
			( this.model.get('user').id == Datea.my_user.get('id')
			  || Datea.my_user.get('is_staff')
			)) {
			$('#setting-controls').html( ich.mapping_control_button_tpl(this.model.toJSON()));	
		}
		//this.resize_layout();
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
		
		if (Datea.my_user.isNew()) {
			
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
		var model = this.map_items.get(this.map_items.url+ev.target.dataset.id+'/');
		var create_rep_view = new Datea.MapItemFormView({
			model: model,
			mappingModel: this.model,
		
			success_callback: function(model) {
				self.map_items.trigger('reset');
				self.open_popup(model.get('id'));
			}
		});
		create_rep_view.open_window();
	},
	
	open_popup: function(arg) {
		if (typeof(arg.currentTarget) != 'undefined') {
			arg.preventDefault();
			var id = parseInt(arg.currentTarget.dataset.id)
		}else{
			var id = parseInt(arg);
		}
		var model = this.map_items.get(this.map_items.url+id+'/');
		if (model.get('position') && model.get('position').coordinates) {
			this.data_view.mapView.itemLayer.open_popup( id , true, true);
		}
	},
});


window.Datea.MappingSidebar = Backbone.View.extend({
	
	initialize: function () {
		this.map_items = this.options.map_items;
	},
	
	events: {
		'click .navigate': 'navigate',
	},
	
	render: function (eventName) {

		this.$el.html( ich.mapping_sidebar_main_tpl(this.model.toJSON()));
		
		this.start_tab_view = new Datea.MappingStartTab({
			el: this.$el.find('#mapping-start-view'),
			model: this.model,
		});
		
		this.map_item_tab_view = new Datea.MappingMapItemTab({
			el: this.$el.find('#mapping-reports-view'),
			model: this.map_items,
			mappingModel: this.model,
		});
			
		return this;
	},
	
	render_tab: function (params) {
		console.log('render tab');
		// render everything the first time
		if (!this.start_tab_view) this.render();
		
		// START TAB
		if (!params.tab_id || params.tab_id == 'start') {
			
			this.start_tab_view.render(params);
			$('#mapping-start-tablink').tab('show');
			
		// MAP ITEM TAB
		} else if (params.tab_id && params.tab_id == 'reports') {
			this.map_item_tab_view.mode = 'list';
			this.map_item_tab_view.render();
			$('#mapping-reports-tablink').tab('show');
		}
		Datea.mapping_resize_layout();
	},
	
	render_item: function (params) {
		// render everything the first time
		if (!this.start_tab_view) this.render();
		
		this.map_item_tab_view.render_item(params);
		$('#mapping-reports-tablink').tab('show');
		Datea.mapping_resize_layout();
	},
	
	navigate: function(ev) {
		ev.preventDefault();
		Datea.app.navigate(ev.target.dataset.nav,{trigger: true});
		ev.target.blur();
	}
	
});


window.Datea.MappingStartTab = Backbone.View.extend({
	
	initialize: function () {
		this.model.bind('change', this.render, this);
		this.model.bind('add', this.render, this);
		//this.model.bind('reset', this.render, this);
	}, 
	
	render: function(eventName) {
		this.$el.html( ich.mapping_tab_start_tpl(this.model.toJSON()));
	} 
	
});


window.Datea.MappingMapItemTab = Backbone.View.extend({
	
	events: {
		'click .get-page': 'get_page',
		'click .back-to-list': 'back_to_list',
	},
	
	initialize: function() {
		//this.model.bind('change', this.render, this);
		//this.model.bind('reset', this.render, this);
		this.model.bind('add', this.render, this);
		this.model.bind('sync', this.render,this);

		this.items_per_page = 10;
		this.pager_view = new Datea.PaginatorView({
			model: this.model, 
			items_per_page: this.items_per_page,
			adjacent_pages: 1,
		});
		this.page = 0;
		this.mode = 'list';
		this.last_item = null;
		
		// ORDER BY
		var options = [
			{value: 'created', name: 'last added'},
			{value: 'vote_count', name: 'most supported'},
			{value: 'comment_count', name: 'most commented'},
		];
		var self = this;	
		this.orderby_filter = new Datea.DropdownSelect({
			options: options,
			div_class: 'no-bg',
			callback: function () { self.filter_items(); self.render_item_page(); },
		});
		this.orderby_filter.render();
	},
	
	render: function() {
		if (this.mode == 'list') {
			this.$el.html( ich.mapping_tab_map_items_tpl());
			this.$el.find('.filter-controls').append(this.orderby_filter.el);
			this.orderby_filter.reset_events(); 
			if (!this.filtered_items) this.filter_items();
			this.render_item_page(this.page);
		}else{
			this.render_item(this.last_item);
		}
		return this;
	},
	
	render_item_page: function (page) {
		this.mode = 'list';
		
		if (typeof(page) != 'undefined') {
			this.page = page;	
		}
		var add_pager = false;
		
		if (this.filtered_items.length > this.items_per_page) {
			var items = Datea.paginate(this.filtered_items, this.page, this.items_per_page);
			var add_pager = true;	
		}else{
			var items = this.filtered_items;
		}
		
		var $item_list = this.$el.find('.item-list');
		$item_list.empty();
		_.each(items, function(item) {
			$item_list.append(new Datea.MapItemTeaserView({ model:item }).render().el);
		});
		
		// PAGER
		var $pager_div = this.$el.find('.item-pager');
		if (add_pager) {
			$pager_div.html( this.pager_view.render_for_page(this.page).el);
			$pager_div.removeClass('hide');
		}else{
			$pager_div.addClass('hide');
		}	
	
	},
	
	render_item: function (params) {
		this.mode = 'detail';
		if (params.item_id) this.last_item = params.item_id
		var item_model = this.model.get(this.model.url+this.last_item+'/');
		if (item_model) {
			if (this.item_full_view) this.item_full_view.clean_up();
			this.item_full_view = new Datea.MapItemFullView({
				model: item_model,
				mappingModel: this.options.mappingModel
			}); 
			this.$el.html(this.item_full_view.render().el);
		}
	},
	
	get_page: function (ev) {
		ev.preventDefault();
		this.render_item_page(parseInt(ev.target.dataset.page));
		this.$el.find('.scroll-area').scrollTop(0);
	},
	
	back_to_list:function (ev) {
		ev.preventDefault();
		this.mode == 'list';
		Datea.app.navigate('/mapping/'+this.options.mappingModel.get('id')+'/reports', {trigger: true});
	},
	
	filter_items: function () {

		this.page = 0;
		var orderby = this.orderby_filter.value;
		var items = this.model.models;
		
		if (orderby == 'created') {
			// nothing -> already ordered by
		}
		
		// vote count
		if ( orderby == 'vote_count') {
			items = _.filter(items, function(item) {
				return item.get('vote_count') > 0;
			});
			items = _.sortBy(items, function(item) { return item.get('vote_count')}).reverse();
		}
		
		// comment count 
		if ( orderby == 'comment_count') {
			items = _.filter(items, function(item) {
				return item.get('comment_count') > 0;
			});
			items = _.sortBy(items, function(item) { return item.get('comment_count')}).reverse();
		}
		
		this.filtered_items = items;
	},
	
	
});
