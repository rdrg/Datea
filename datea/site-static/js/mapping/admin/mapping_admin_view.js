
window.Datea.MappingAdminView = Backbone.View.extend({
	
	tagName: 'div',
	
	events: {
		'click .get-page': 'get_page',
	},
	
	initialize: function () {
		this.map_items = this.options.map_items,
		this.map_items.bind('reset', this.render, this);
		this.map_items.bind('remove', this.remove_event, this);
		this.page = 0;
		this.items_per_page = 25;
		this.pager_view = new Datea.PaginatorView({
			items_per_page: this.items_per_page,
			adjacent_pages: 2
		});
		this.$el.addClass("mapping-items-admin");
	},
	
	render: function(ev) {
		
		var context = this.model.toJSON();
		
		if (this.model.get('item_categories').length > 0) {
			this.has_categories = true;
		}else{
			this.has_categories = false;
		}
		context.has_categories = this.has_categories;
		
		var page_title = gettext('Admin Panel')+': '+context.name;
		this.$el.html(ich.mapping_admin_zone_head_tpl({page_title: page_title}));
		this.$el.append(ich.content_layout_single_tpl());
		this.$el.find('#content').html( ich.mapping_admin_list_tpl(context));
			
		var self = this;	
		// category filter
		if (context.has_categories) {
			var categories = this.model.get('item_categories');
			var options = [{value:'all', name: gettext('All categories')}];
			_.each(categories, function(cat) {
				if (cat.active == true) {
					options.push({value: cat.id, name: ich.category_name_with_color2_tpl(cat, true)});
				}
			});
			this.category_filter = new Datea.DropdownSelect({
				options: options,
				div_class: 'no-bg',
				callback: function () { self.filter_items(); self.render_page(0); },
				box_text_max_length: 95,
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
			div_class: 'no-bg',
			callback: function () { self.filter_items(); self.render_page(0);}
		});
		this.$el.find('.status-filter').html(this.status_filter.render().el);
		
		
		// published filter
		var options = [
			{value: 1, name: gettext('published')},
			{value: 0, name: gettext('un-published')},
		];
		this.published_filter = new Datea.DropdownSelect({
			options: options,
			div_class: 'no-bg',
			callback: function () { self.filter_items(); self.render_page(0);}
		});
		this.$el.find('.published-filter').html(this.published_filter.render().el);
		
		this.filter_items();
		this.render_page();
		 
		return this;
	},
	
	render_page:function (page) {
		
		if (typeof(page) != 'undefined') {
			this.page = page;	
		}
		
		var add_pager = false;
		
		if (this.filtered_items.length > this.items_per_page) {
			var items = _.rest(this.filtered_items, this.items_per_page*this.page);
       		items = _.first(items, this.items_per_page);
			var add_pager = true;
		}else{
			var items = this.filtered_items;
		}
		
		var $item_list = this.$el.find('.item-list');
		$item_list.empty();
		
		if (items.length == 0) {
			$('.no-results-msg', this.$el).show();
			$('.map-item-admin-table').hide();
			
		} else {
			$('.no-results-msg', this.$el).hide();
			$('.map-item-admin-table').show();
			
			var self = this;
			_.each(items, function(item) {
				$item_list.append(new Datea.MapItemAdminView({ 
					model:item, 
					mapping_model: self.model,
					collection: self.map_items,
					change_callback: function () {
						self.filter_items();
						self.render_page();
					} 
				}).render().el);
			});
		}
		// PAGER
		var $pager_div = this.$el.find('.item-pager');
		if (add_pager) {
			$pager_div.html( this.pager_view.render_for_page(this.page, this.filtered_items.length).el);
			$pager_div.removeClass('hide');
		}else{
			$pager_div.addClass('hide');
		}

	},
	
	get_page: function (ev) {
		ev.preventDefault();
		var page = parseInt($(ev.currentTarget).data('page')); 
		this.render_page(page);
		$(document).scrollTop(0);
	},
	
	filter_items: function() {
		
		var self = this;
		var fitems = this.map_items.models;
		
		// category filter
		if (this.category_filter && this.category_filter.value != 'all') {
			fitems = _.filter(fitems, function (item){ 
				return item.get('category_id') == self.category_filter.value;
			});
		}
		
		// status filter
		if (this.status_filter && this.status_filter.value != 'all') {
			fitems = _.filter(fitems, function (item){ 
				return item.get('status') == self.status_filter.value;
			});
		}
		
		// published filter
		if (this.published_filter && this.published_filter.value != 'all') {
			fitems = _.filter(fitems, function (item){ 
				return item.get('published') == self.published_filter.value;
			});
		}
		
		this.filtered_items = fitems;
	},
	
	remove_event: function(ev) {
		this.filter_items();
		this.render_page();
	}
	
});




