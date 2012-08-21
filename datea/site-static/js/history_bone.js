
window.Datea.History = Backbone.Model.extend({
	urlRoot: '/api/v1/history'
});

window.Datea.HistoryCollection = Backbone.Collection.extend({
	model: Datea.History,
	url: '/api/v1/history',
});

window.Datea.HistoryItemView = Backbone.View.extend({
	
	tagName: 'div',
	
	className: 'history-item',
	
	render: function (ev) {
		
		var stype = this.model.get('sender_type');
		var rtype = this.model.get('receiver_type');
		
		var recv_arr = [];
		var recv_items = this.model.get('receiver_items');
		for (i in recv_items) {
			recv_arr.push(ich[rtype+'_history_receiver'](recv_items[i], true));
		}

		var context = this.model.toJSON();
		context.receiver_html = recv_arr.join(', ');
		context.title_html = ich[stype+'_history_sender'](context, true);
		context.link = context.receiver_items[0].url;
		context.created = formatDateFromISO(context.created, "dd.mm.yyyy - H:MM");
		
		this.$el.html(ich.history_item_tpl(context));
		
		return this;
	},
});


window.DateaHistoryView = Backbone.View.extend({
	
	tagName: 'div',
	
	className: 'history-view',
	
	events: {
    	'click .get-page': 'get_page',
    },
	
	initialize: function () {
		this.user_model = this.options.user_model;
		this.model = new Datea.HistoryCollection();
    	this.model.bind("reset", this.reset_event, this);
    	this.selected_mode = 'combined';
    	this.items_per_page = 4;
    	this.page = 0;
		this.pager_view = new Datea.PaginatorView({
			items_per_page: this.items_per_page,
			adjacent_pages: 1,
		});
	},
	
	render:function (ev) {
    	this.$el.html( ich.history_view_tpl());
    	this.build_filter_options();   	
    	this.fetch_actions();
        return this;
    },
    
    // build filter options according to user
    build_filter_options: function () {
    	if (Datea.is_logged() && this.user_model.get('id') == Datea.my_user.get('id')) {
    		var prefix = gettext('my');
    	}else{
    		var prefix = '';
    	} 
    	
    	this.filter_options = [
    		{value: 'combined', name: gettext('combined view')},
    		{value: 'contributions', name: prefix+' '+gettext('contributions')},
    		{value: 'comments', name: prefix+' '+gettext('comments')},
    		{value: 'votes', name: prefix+' '+gettext('supports')},
		];    		
    },
    
    render_filter: function() {
    	this.build_filter_options();
    	var self = this;
    	
		this.history_filter = new Datea.DropdownSelect({
			options: this.filter_options,
			div_class: 'no-bg',
			init_value: this.selected_mode,
			callback: function (val) {
				self.selected_mode = val; 
				self.fetch_actions();
			}
		});
		this.$el.find('.filter').html(this.history_filter.render().el);
    },
    
    fetch_actions: function () {
    	Datea.show_small_loading(this.$el);
    	if (this.selected_mode == 'combined') {
    		this.model.fetch({
    			data: {following_user: this.user_model.get('id'), orderby: '-created'}
    		});
    		
    	}else if (this.selected_mode == 'contributions') {
    		this.model.fetch({
    			data: {following_user: this.user_model.get('id'), sender_type: 'map_item', orderby: '-created'}
    		});
    	}else if (this.selected_mode == 'comments') {
    		this.model.fetch({
    			data: {following_user: this.user_model.get('id'), sender_type: 'comment', orderby: '-created'}
    		});
    	}else if (this.selected_mode == 'votes') {
    		this.model.fetch({
    			data: {following_user: this.user_model.get('id'), sender_type: 'vote', orderby: '-created'}
    		});
    	}	
    },
    
    filter_items: function () {
    	this.render_items = this.model.models;  
    },
    
    render_page: function(page) {
    	Datea.hide_small_loading(this.$el);
    	
    	var $list = this.$el.find('.item-list');
    	$list.empty();
    	
    	if (typeof(page) != 'undefined') {
    		this.page = page;
    	}
    	
    	var add_pager = false;
    	if (this.render_items.length > this.items_per_page) {
    		var items = _.rest(this.render_items, this.items_per_page*this.page);
       		items = _.first(items, this.items_per_page);
       		add_pager = true;  
    	}else if (this.render_items.length > 0){
    		items = this.render_items;
    	}else{
    		if (Datea.is_logged() && this.user_model.get('id') == Datea.my_user.get('id')) {
    			this.$el.html(ich.datea_logged_intro_tpl());
    		}else{
    			$list.html(ich.empty_result_tpl());
    		}
    		return;
    	}
    	
    	_.each(items, function (item) {
            	$list.append(new Datea.HistoryItemView({model:item}).render().el);
        }, this);
        
        var $pager_div = this.$el.find('.item-pager');
		if (add_pager) {
			$pager_div.html( this.pager_view.render_for_page(this.page, this.render_items.length).el);
			$pager_div.removeClass('hide');
		}else{
			$pager_div.addClass('hide');
		}
    },
    
   get_page: function(ev) {
    	ev.preventDefault();
		this.render_page(parseInt(ev.target.dataset.page));
		this.$el.find('.scroll-area').scrollTop(0);
    },
    
    reset_event: function(ev) {
    	this.render_filter();
    	this.filter_items();
    	this.render_page(0);
    } 
	
})







