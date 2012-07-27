
window.Datea.MappingAdminView = Backbone.View.extend({
	
	tagName: 'div',
	
	events: {
		'click .get-page': 'get_page',
		//'click .back-to-list': 'back_to_list',
		'change .filter-status select': 'filter_status',
	},
	
	initialize: function () {
		this.map_items = this.options.map_items,
		this.map_items.bind('reset', this.render, this);
		this.page = 0;
		this.items_per_page = 25;
		this.pager_view = new Datea.PaginatorView({
			model: this.map_items, 
			items_per_page: this.items_per_page
		});
		this.$el.addClass("mapping-items-admin");
	},
	
	render: function(ev) {
		this.$el.html( ich.mapping_admin_main_tpl());
		var context = this.model.toJSON();
		if (this.model.get('item_categories').length > 0) {
			context.has_categories = true;
		}else{
			context.has_categories = false;
		}
		this.$el.find('#right-content').html( ich.mapping_admin_list_tpl(context));
		if (!this.filtered_items) {
			this.filtered_items = this.map_items.filter(function(item) {
  				return item.get("status") == 'new';
  			});
		}
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
		var self = this;
		_.each(items, function(item) {
			$item_list.append(new Datea.MapItemAdminView({ 
				model:item, 
				mapping_model: self.model,
				status_changed_callback: function () {
					self.render_page();
				} 
			}).render().el);
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
	
	get_page: function (ev) {
		ev.preventDefault();
		this.render_page(parseInt(ev.target.dataset.page));
		$(document).scrollTop(0);
	},
	
	filter_status: function() {
		var status = $('.filter-status select').val();
		this.filtered_items = this.map_items.filter(function(item) {
  			return item.get("status") == status;
		});
		this.render_page(0);
	}
	
});


window.Datea.MapItemAdminView = Backbone.View.extend({
	
	tagName: 'tr',
	className: 'item',
	
	template: 'map_item_admin_list_item_tpl',
	
	events: {
		'click .expand-view': 'expand',
		'click .collapse-view': 'collapse',
		'click .save-item': 'save_item',
		'click .respond-item': 'respond_item',
	},
	
	initialize: function() {
		this.model.bind('change', this.change_event, this);
		this.model.bind('sync', this.sync_event, this);
	},
	
	render: function (ev) {
		var context =  this.model.toJSON();
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
		Datea.CheckMapItemStats(this.$el, this.model);
		
		// map
		if (this.model.get('position')) {
			var itemLayer = new olwidget.DateaMainMapItemLayer(
					this.options.mapping_model, {'models': [this.model]},
					{'name': 'Aportes', 'cluster': true}
				);
			var mapOptions = {
				"layers": ['google.streets', 'google.hybrid'],
				'defaultZoom': 12,
				'mapDivStyle': {'width': '280px', 'height': '220px'},
			}
			var map = new olwidget.DateaMainMap("item-map-"+this.model.get('id'), [itemLayer], mapOptions);
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
		
		// set status
		$('[name="status"]', this.$el).val(this.model.get('status'));
		
		// get replies
		var responses = new Datea.MapItemResponseCollection();
		var self = this;
		responses.fetch({
			data: {map_items__in: this.model.get('id'), order_by:'created'},
			success: function (collection, response) {
				if (collection.length > 0) {
					var $replies = self.$el.find('.replies');
					_.each(collection.models, function(model){
						$replies.append(new Datea.MapItemResponseView({model: model}).render().el); 
					});
					$replies.show();
				}
			}
		})
	},
	
	collapse: function () {
		this.$el.removeClass('expanded');
		this.template = 'map_item_admin_list_item_tpl';
		this.render();
	},
	
	save_item: function () { 
		Datea.show_big_loading(this.$el.find('.item-edit-wrap'));
		
		if (this.options.mapping_model.get('item_categories').length > 0) {
			var cat_id = $('[name="category"]', this.$el).val();
			var cat = null;
			var categories = this.options.mapping_model.get('item_categories');
			var cat = _.find(categories,function(c){ return c.id == cat_id});
			this.model.set({
				category: cat,
				category_id: cat.id,
				category_name: cat.name,
				color: cat.color
			}, {silent: true});
		}
		
		this.model.set({
			status: $('[name="status"]', this.$el).val(), 
		});
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
				self.model.fetch({
					'success': self.expand(),
				});
			}
		});
		response_view.render();
	},
	
	sync_event: function () {
		this.expand();
	},
	
	change_event: function () {
		if (this.model.hasChanged('status')) {
			if (this.options.status_changed_callback) {
				this.options.status_changed_callback();
			}
		}
	}

});


window.Datea.MapItemResponse = Backbone.Model.extend({
	urlRoot : '/api/v1/map_item_response/',
});

window.Datea.MapItemResponseCollection = Backbone.Collection.extend({
	url: '/api/v1/map_item_response/',
	model: Datea.MapItemResponse,
});

window.Datea.MapItemResponseFormView = Backbone.View.extend({
	
	tagName: 'div',	
	className: 'map-item-response-form',
	
	initialize: function () {
		this.map_items = this.options.map_items;
		this.model.bind('sync', this.sync_event, this);
	},
	
	events: {
		'click .save-response': 'save_response'
	},
	
	render: function(ev) {
		this.$el.html(ich.map_item_response_form_tpl(this.model.toJSON()));
		return this;
	},
	
	save_response: function() {
		
		var items = [];
		this.model.set({
			'user': Datea.my_user.toJSON(),
			'map_items': this.map_items.toJSON(),
			'content': $('[name="content"]',this.$el).val(), 
		});
		this.model.save();
	},
	
	sync_event: function() {
		this.$el.unbind();
        this.$el.empty();
		if (this.options.sync_callback) this.options.sync_callback();
	}
		
});

window.Datea.MapItemResponseView = Backbone.View.extend({
	
	tagName: 'div',
	className: 'map-item-reply',
	
	initialize: function() {
		this.model.bind('sync',this.render, this);
	},
	
	events :{
		'click .edit-response': 'edit',
		'click .save-response': 'save',
		'click .cancel': 'render',
	},
	
	render: function() {
		var context = this.model.toJSON();
		context.created = formatDateFromISO(context.created, "dd.mm.yyyy - H:MM");
		context.content = context.content.replace(/\n/g, '<br />');
		this.$el.html( ich.map_item_response_tpl(context));
		if (!Datea.my_user.isNew() && (
			this.model.get('user').id == Datea.my_user.get('id')
			|| Datea.my_user.get('is_staff')
			)){
				this.$el.find('.edit').show();
			}
		return this;
	},
	
	edit: function(){
		var context = this.model.toJSON();
		context.created = formatDateFromISO(context.created, "dd.mm.yyyy - H:MM");
		this.$el.html( ich.map_item_response_edit_tpl(context));
		this.$el.find('[name="content"]').focus();
	},
	
	save: function() {
		this.model.set({
			content: $('[name="content"]', this.$el).val(),
		});
		this.model.save();
	},
	
});


