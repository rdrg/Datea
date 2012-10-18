
window.Datea.MappingMapItemTab = Backbone.View.extend({
	
	events: {
		'click .get-page': 'get_page',
		'click .back-to-list': 'back_to_list',
	},
	
	initialize: function() {
		//this.model.bind('change', this.render, this);
		//this.model.bind('reset', this.render, this);
		this.model.bind('add', this.add_event, this);
		this.model.bind('remove', this.render, this);
		this.model.bind('sync', this.render,this);

		this.items_per_page = 10;
		this.pager_view = new Datea.PaginatorView({
			items_per_page: this.items_per_page,
			adjacent_pages: 1,
		});
		this.page = 0;
		this.mode = 'list';
		this.last_item = null;
		
		// ORDER BY
		var options = [
			{value: 'created', name: gettext('last added')},
			{value: 'vote_count', name: gettext('most supported')},
			{value: 'comment_count', name: gettext('most commented')},
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
			this.$el.html( ich.mapping_tab_map_items_tpl(this.context));
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
		
		var $item_list = this.$el.find('.item-list');
		
		if (typeof(page) != 'undefined') {
			this.page = page;	
		}
		var add_pager = false;
		
		
		if (this.filtered_items.length > this.items_per_page) {
			var items = Datea.paginate(this.filtered_items, this.page, this.items_per_page);
			var add_pager = true;	
		}else if (this.filtered_items.length > 0){
			var items = this.filtered_items;
		}else{
			$item_list.html(ich.empty_result_tpl());
			return;
		}
		
		$item_list.empty();
		_.each(items, function(item) {
			$item_list.append(new Datea.MapItemTeaserView({ model:item }).render().el);
		});
		
		// PAGER
		var $pager_div = this.$el.find('.item-pager');
		if (add_pager) {
			$pager_div.html( this.pager_view.render_for_page(this.page,this.filtered_items.length).el);
			$pager_div.removeClass('hide');
		}else{
			$pager_div.addClass('hide');
		}	
	},
	
	add_event: function(ev) {
		this.orderby_filter.set_value('created');		
		this.filter_items();
		this.render_item_page(0);
	},
	
	remove_event: function(ev) {
		this.filter_items();
		this.render_item_page(0);
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
		init_share_buttons();
	},
	
	get_page: function (ev) {
		ev.preventDefault();
		var page = parseInt($(ev.currentTarget).data('page'));
		this.render_item_page(page);
		this.$el.find('.scroll-area').scrollTop(0);
	},
	
	back_to_list:function (ev) {
		ev.preventDefault();
		this.mode == 'list';
		Datea.app.navigate('/'+gettext('mapping')+'/'+this.options.mappingModel.get('id')+'/'+gettext('reports'), {trigger: true});
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
		
		// published filter
		items = _.filter(items, function (item) {
			return item.get('published');
		});
		
		this.filtered_items = items;
	},
	
	
});