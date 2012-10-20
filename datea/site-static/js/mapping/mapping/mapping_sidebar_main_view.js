
window.Datea.MappingSidebar = Backbone.View.extend({
	
	initialize: function () {
		this.map_items = this.options.map_items;
	},
	
	events: {
		'click .navigate': 'navigate',
	},
	
	render: function (eventName) {
		
		var context = this.model.toJSON();
		this.$el.html( ich.mapping_sidebar_main_tpl(context));
		
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
		
		// render everything the first time
		if (!this.start_tab_view) this.render();
		
		// START TAB
		if (!params.tab_id || params.tab_id == gettext('start')) {
			
			this.start_tab_view.render(params);
			$('#mapping-start-tablink').tab('show');
			
		// MAP ITEM TAB
		} else if (params.tab_id && params.tab_id == gettext('reports')) {
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
		var nav = $(ev.target).data('nav');
		Datea.app.navigate(nav,{trigger: true});
		$(ev.currentTarget).blur();
	}
	
});