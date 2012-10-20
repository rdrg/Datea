
window.Datea.HistoryView = Backbone.View.extend({
	
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
    	this.items_per_page = 10;
    	this.page = 0;
		this.pager_view = new Datea.PaginatorView({
			items_per_page: this.items_per_page,
			adjacent_pages: 2,
		});
	},
	
	render:function (ev) {
    	this.$el.html( ich.history_view_tpl());
    	this.build_filter_options();   	
    	this.fetch_models();
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
				if (self.selected_mode != val) {
					self.selected_mode = val;
					self.page = 0;
				}
				self.fetch_actions();
			}
		});
		this.$el.find('.filter').html(this.history_filter.render().el);
    },
    
    fetch_models: function () {
    	
    	Datea.show_small_loading(this.$el);
    	
    	var params = {
    		limit: this.items_per_page, 
    		offset: this.page * this.items_per_page
    	};
    	
    	switch(this.selected_mode) {
    	
    		case 'combined':
    			$.extend(params, {
    				following_user: this.user_model.get('id')
    			});
    			break;
    		case 'contributions':
    			$.extend(params, {
    				following_user: this.user_model.get('id'), 
    				sender_type: 'map_item'
    			});
    			break;
    		case 'comments':
    			$.extend(params,{
    				following_user: this.user_model.get('id'), 
    				sender_type: 'comment'
    			});
    			break;
    		case 'votes':
    			$.extend(params,{
    				following_user: this.user_model.get('id'), 
    				sender_type: 'vote'
    			});
    			break;
    	}
    	this.model.fetch({ data: params});
    },
    
    render_page: function(page) {
    	Datea.hide_small_loading(this.$el);
    	
    	var $list = this.$el.find('.item-list');
    	$list.empty();
    	
    	if (typeof(page) != 'undefined') {
    		this.page = page;
    	}
    	
    	var add_pager = false;
    	if (this.model.meta.total_count > this.model.meta.limit) {
       		add_pager = true;  
    	}
    	
    	if (this.model.size() > 0) {
	    	var self = this;
	    	this.model.each(function (item) {
	    			var opts = {model: item}
	            	$list.append(new Datea.HistoryItemView(opts).render().el);
	        }, this);
	    }else{
	    	$list.html(ich.empty_result_tpl());	
	    }
        
        var $pager_div = this.$el.find('.item-pager');
		if (add_pager) {
			$pager_div.html( this.pager_view.render_for_page(this.page, this.model.meta.total_count).el);
			$pager_div.removeClass('hide');
		}else{
			$pager_div.addClass('hide');
		}
    },
    
    get_page: function(ev) {
    	ev.preventDefault();
    	if (typeof(ev) != 'undefined') this.page = parseInt($(ev.currentTarget).data('page'));
    	this.fetch_models();
		$(document).scrollTop(0);
    },
    
    reset_event: function(ev) {
    	this.render_filter();
    	this.render_page();
    } 
	
});