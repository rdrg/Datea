

window.Datea.BaseActionListView = Backbone.View.extend({
	
	tagName:'div',
    
    attributes: {
    	'class': 'actions',
    },
    
    events: {
    	'click .get-page': 'get_page',
    	'submit .action-search-form': 'search'
    },
    
    initialize: function () {
    	this.model = new Datea.ActionCollection();
    	this.model.bind("reset", this.reset_event, this);
    	this.items_per_page = 8;
    	this.page = 0;
		this.pager_view = new Datea.PaginatorView({
			items_per_page: this.items_per_page,
			adjacent_pages: 1,
		});
		this.search_str = '';
		if (this.options.add_class) this.$el.addClass(this.options.add_class);
    },
    
    render:function (ev) {
    	this.$el.html( ich.action_list_tpl());
    	this.build_filter_options();   	
    	this.fetch_actions();
    	
        return this;
    },
    
    render_filter: function() {
    	this.build_filter_options();
    	var self = this;
    	
    	var div_class = 'no-bg';
    	if (this.options.add_class == 'unlogged') div_cass = div_class +" white"; 
    	
		this.action_filter = new Datea.DropdownSelect({
			options: this.filter_options,
			div_class: 'no-bg white',
			init_value: this.selected_mode,
			callback: function (val) {
				if (self.selected_mode != val) {
					self.selected_mode = val;
					self.page = 0;
				} 
				self.fetch_actions();
			}
		});
		this.$el.find('.filters').html(this.action_filter.render().el);
    },
	
	render_page: function(page) {
    	var $list = this.$el.find('#action-list');
    	$list.empty();
    	
    	if (typeof(page) != 'undefined') {
    		this.page = page;
    	}
    	
    	var add_pager = false;
    	if (this.model.meta.total_count > this.model.meta.limit) {
       		add_pager = true;  
    	}
    	var self = this;
    	this.model.each(function (item) {
    			var opts = {
    				model: item,
    				follow_callback: function() { self.render_filter(); }
    			}
            	$list.append(new Datea.ActionListItemView(opts).render().el);
        }, this);
        
        var $pager_div = this.$el.find('.action-pager');
		if (add_pager) {
			$pager_div.html( this.pager_view.render_for_page(this.page, this.models.meta.total_count).el);
			$pager_div.removeClass('hide');
		}else{
			$pager_div.addClass('hide');
		}
    },
    
    get_page: function(ev) {
    	ev.preventDefault();
    	if (typeof(ev) != 'undefined') this.page = parseInt($(ev.currentTarget).data('page'));
    	this.fetch_actions();
		this.$el.find('.scroll-area').scrollTop(0);
    },
    
    search: function (ev) {
    	ev.preventDefault();
    	var q = jQuery.trim($('#search-action-input', this.$el).val());
    	if (this.search_str != q) {
    		this.page = 0;
    		this.search_str = q;
    	}
    	this.fetch_actions();
		this.$el.find('.scroll-area').scrollTop(0);
    },
    
    reset_event: function(ev) {
    	this.render_filter();
    	this.render_page();
    }
});


// Action list view
window.Datea.MyActionListView = Datea.BaseActionListView.extend({
    
    selected_mode: 'my_actions',
    
    // build filter options according to user
    build_filter_options: function () {
    	this.filter_options = [];
    	if (Datea.is_logged() && typeof(Datea.my_user_follows.find(function (f){ return f.get('object_type') == 'dateaaction'})) != 'undefined') {
    		
    		this.filter_options.push({value: 'my_actions', name: gettext('my actions')});
    		
    		if (this.model.find(function (action){
    				return action.get('user') == Datea.my_user.get('resource_uri');
    			})) {
    			this.filter_options.push({value: 'own_actions', name: gettext('own actions')});
    		}
    	}
        this.filter_options.push({value: 'featured_actions', name: gettext('featured actions')});
        this.filter_options.push({value: 'all_actions', name: gettext('all actions')});
        
        // check availability of
        var self = this; 
        if (typeof(_.find(this.filter_options, function (op) {
        		return op.value == self.selected_mode;
        		})) == 'undefined') {
        	this.selected_mode = this.filter_options[0].value;
        }
    },
    
    fetch_actions: function (page) {
    	
    	if (typeof(page) != 'undefined') this.page = page; 
    	
    	Datea.show_big_loading(this.$el.find('#action-list'));
    	
    	var params = {
    		limit: this.items_per_page, 
    		offset: this.page * this.items_per_page
    		};
    	if (this.search_str!= '') {
    		params['q'] = this.search_str;
    	}
    	
    	switch(this.selected_mode) {
    		case 'my_actions':
    			params['following_user'] = Datea.my_user.get('id');
    			break;
    		case 'own_actions':
    			params['user_id'] = Datea.my_user.get('id');
    			break;
    		case 'featured_actions':
    			params['featured'] = 1;
    			break;
    		case 'all_actions':
    			break;
    	}

    	this.model.fetch({ data: params});
    },
    
});


window.Datea.ProfileActionListView = Datea.BaseActionListView.extend({
    
    selected_mode: 'actions',
    
    initialize: function () {
    	this.user_model = this.options.user_model;
    	this.model = new Datea.ActionCollection();
    	this.model.bind("reset", this.reset_event, this);
    	this.selected_mode = 'actions';
    	this.items_per_page = 8;
    	this.page = 0;
		this.pager_view = new Datea.PaginatorView({
			items_per_page: this.items_per_page,
			adjacent_pages: 1,
		});
		this.search_str = '';
    },
    
    // build filter options according to user
    build_filter_options: function () {
    	var format = gettext("%(uname)s's actions");
    	var action_str = interpolate(format, {'uname': this.user_model.get('username')}, true);   
    	this.filter_options = [
    		{value: 'actions', name: action_str},
        ];
        var self = this;
        if (this.model.find(function(a){ return a.get('user_url') == self.user_model.get('url')})) {
        	var format = gettext("actions created by %(uname)s");
        	var created_str = interpolate(format, {'uname': self.user_model.get('username')}, true);
        	self.filter_options.push({value: 'user_actions', name: created_str}); 
        }
    },

    fetch_actions: function (page) {
    	
    	if (typeof(page) != 'undefined') this.page = page; 
    	
    	Datea.show_big_loading(this.$el.find('#action-list'));
    	
    	var params = {
    		limit: this.items_per_page, 
    		offset: this.page * this.items_per_page
    	};
    	if (this.search_str != '') {
    		params['q'] = this.search_str;
    	}
    	
    	switch(this.selected_mode) {
    		case 'actions':
    			params['following_user'] = Datea.my_user.get('id');
    			break;
    		case 'user_actions':
    			params['user_id'] = Datea.my_user.get('id');
    			break;
    	}
    	
    	this.model.fetch({ data: params});
    },
	
});








