


// DateaAction backbone model 
window.Datea.Action = Backbone.Model.extend();

// Action Collection
window.Datea.ActionCollection = Backbone.Collection.extend({
	model: Datea.Action,
	url: '/api/v1/action/',
});


// ACtion list item
window.Datea.ActionListItemView = Backbone.View.extend({
  
	tagName: 'div',
  
	className: 'action-item',

	render: function(){
		var context = this.model.toJSON();
		context.created = formatDateFromISO(context.created, "dd.mm.yyyy");
		
		// end date
		if (this.model.get('end_date') != null) {
			var now = new Date();
			now.setHours(0,0,0,0);
			var end = datedayFromISO(this.model.get('end_date'));
			if (now <= end) {
				var days_left = Math.ceil((end.getTime()-now.getTime())/86400000);
				if (days_left > 0) {
					context.active_message = ich.action_days_left_tpl({days_left: days_left}, true);
				}else{
					context.active_message = ich.action_last_day_tpl({}, true);
				}
			}else{
				context.active_message = ich.action_expired_tpl({}, true);
			}
		}
		
  		this.$el.html(ich.action_list_item_tpl(context));
  
  		// follow widget
  		if (Datea.is_logged() && Datea.my_user.get('resource_uri') != this.model.get('user')) {
			this.follow_widget = new Datea.FollowWidgetView({
				object_type: 'dateaaction',
				object_id: this.model.get('id'),
				object_name: gettext('action'),
				followed_model: this.model,
				type: 'button',
				style: 'button-small', 
			});
			this.$el.find('.follow-button').html(this.follow_widget.render().el);
		}
      
		Datea.CheckStatsPlural(this.$el, this.model);
		return this;
  }
                                
});


// Action list view
window.Datea.MyActionListView = Backbone.View.extend({
 
    tagName:'div',
    
    attributes: {
    	'class': 'actions',
    },
    
    events: {
    	'click .get-page': 'get_page',
    },
 
    initialize: function () {
    	this.model = new Datea.ActionCollection();
    	this.model.bind("reset", this.reset_event, this);
    	this.selected_mode = 'my_actions';
    	this.items_per_page = 8;
    	this.page = 0;
		this.pager_view = new Datea.PaginatorView({
			items_per_page: this.items_per_page,
			adjacent_pages: 1,
		});
    },
 
    render:function (ev) {
    	this.$el.html( ich.action_list_tpl());
    	this.build_filter_options();   	
    	this.fetch_actions();
    	
        return this;
    },
    
    // build filter options according to user
    build_filter_options: function () {
    	this.filter_options = [];
    	if (Datea.is_logged() && typeof(Datea.my_user_follows.find(function (f){ return f.get('object_type') == 'dateaaction'})) != 'undefined') {
    		
    		this.filter_options.push({value: 'my_actions', name: gettext('my actions')});
    		
    		if (this.model.find(function (action){
    				return action.get('user') == Datea.my_user.get('resource_uri');
    			})) {
    			this.filter_options.push({value: 'created_actions', name: gettext('actions created')});
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
    
    render_filter: function() {
    	this.build_filter_options();
    	var self = this;
    	
		this.action_filter = new Datea.DropdownSelect({
			options: this.filter_options,
			div_class: 'no-bg white',
			init_value: this.selected_mode,
			callback: function (val) {
				self.selected_mode = val; 
				self.fetch_actions();
			}
		});
		this.$el.find('.filters').html(this.action_filter.render().el);
    },
    
    fetch_actions: function () {
    	Datea.show_big_loading(this.$el.find('#action-list'));
    	if (this.selected_mode == 'my_actions' || this.selected_mode == 'created_actions') {
    		
    		var follows = Datea.my_user_follows.filter(function(fol){
	        	return fol.get('object_type') == 'dateaaction';
	        });
	        if (typeof(follows) != 'undefined' && follows.length > 0) {
	        	var ids = [];
	        	for (i in follows) {
	        		ids.push(follows[i].get('object_id'));
	        	}
	        	this.model.fetch({
	        		data: {'id__in': ids.join(',')}
	        	})	
	        }
    	
    	}else if (this.selected_mode == 'featured_actions') {
    		this.model.fetch({
    			data: {featured: 1, orderby: '-created'}
    		});
    		
    	}else if (this.selected_mode == 'all_actions'){
    		this.model.fetch({ data: {orderby: '-created'} });
    	}
    },
    
    filter_items: function () {
    	
    	if (this.selected_mode == 'my_actions') {
    		this.render_actions = this.model.models;
        
        }else if (this.selected_mode == 'created_actions') {
        	this.render_actions = this.model.filter(function(action) { return action.get('user') == Datea.my_user.get('resource_uri') });	
        
        }else if (this.selected_mode == 'featured_actions')  {
        	this.render_actions = this.model.filter(function(action) { return action.get('featured')});	
        
        }else if (this.selected_mode == 'all_actions')  {
        	this.render_actions = this.model.models;	
        }
        this.render_actions = _.sortBy(this.render_actions, function(action){
        	if (action.get('is_active') == null) return 0;
        	else if (action.get('is_active')) return 0;
        	else return 1;
        })  
    },
      
    render_page: function(page) {
    	var $list = this.$el.find('#action-list');
    	$list.empty();
    	
    	if (typeof(page) != 'undefined') {
    		this.page = page;
    	}
    	
    	var add_pager = false;
    	if (this.render_actions.length > this.items_per_page) {
    		var items = _.rest(this.render_actions, this.items_per_page*this.page);
       		items = _.first(items, this.items_per_page);
       		add_pager = true;  
    	}else{
    		items = this.render_actions;
    	}
    	
    	_.each(items, function (item) {
            	$list.append(new Datea.ActionListItemView({model:item}).render().el);
        }, this);
        
        var $pager_div = this.$el.find('.action-pager');
		if (add_pager) {
			$pager_div.html( this.pager_view.render_for_page(this.page,this.render_actions.length).el);
			$pager_div.removeClass('hide');
		}else{
			$pager_div.addClass('hide');
		}
    },
    
    get_page: function(ev) {
    	ev.preventDefault();
    	var page = parseInt($(ev.currentTarget).data('page'));
		this.render_page(page);
		this.$el.find('.scroll-area').scrollTop(0);
    },
    
    reset_event: function(ev) {
    	this.render_filter();
    	this.filter_items();
    	this.render_page(0);
    }
    
});


window.Datea.ProfileActionListView = Backbone.View.extend({
	
	tagName:'div',
    
    className: 'actions',
    
    events: {
    	'click .get-page': 'get_page',
    },
    
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
    },
	
	render:function (ev) {
    	this.$el.html( ich.action_list_tpl());
    	this.build_filter_options();   	
    	this.fetch_actions();
    	
        return this;
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
        	self.filter_options.push({value: 'created_actions', name: created_str}); 
        }
    },
    
    render_filter: function() {
    	this.build_filter_options();
    	var self = this;
    	
		this.action_filter = new Datea.DropdownSelect({
			options: this.filter_options,
			div_class: 'no-bg white',
			init_value: this.selected_mode,
			callback: function (val) {
				self.selected_mode = val; 
				self.fetch_actions();
			}
		});
		this.$el.find('.filters').html(this.action_filter.render().el);
    },
    
    fetch_actions: function () {
    	Datea.show_big_loading(this.$el.find('#action-list'));
    	if (this.selected_mode == 'actions') {
	        this.model.fetch({
	        	data: {'following_user': this.user_model.get('id'), orderby: '-created'}
	        })	
	    } else if (this.selected_mode == 'created_actions') {
    		this.model.fetch({
    			data: {user__id: this.user_model.get('id'), orderby: '-created'}
    		});
    	}
    },
    
    filter_items: function () {
    	if (this.selected_mode == 'actions') {
    		this.render_actions = this.model.models;
        }else if (this.selected_mode == 'created_actions') {
        	var self = this;
        	this.render_actions = this.model.filter(function(a) { return a.get('user') == self.user_model.get('resource_uri') });
        }
    },
    
    render_page: function(page) {
    	var $list = this.$el.find('#action-list');
    	$list.empty();
    	
    	if (typeof(page) != 'undefined') {
    		this.page = page;
    	}
    	
    	var add_pager = false;
    	if (this.render_actions.length > this.items_per_page) {
    		var items = _.rest(this.render_actions, this.items_per_page*this.page);
       		items = _.first(items, this.items_per_page);
       		add_pager = true;  
    	}else if (this.render_actions.length > 0){
    		items = this.render_actions;
    	}else{
    		$list.html(ich.user_actions_empty_tpl());
    		return;
    	}
    	
    	_.each(items, function (item) {
            	$list.append(new Datea.ActionListItemView({model:item}).render().el);
        }, this);
        
        var $pager_div = this.$el.find('.action-pager');
		if (add_pager) {
			$pager_div.html( this.pager_view.render_for_page(this.page,this.render_actions.length).el);
			$pager_div.removeClass('hide');
		}else{
			$pager_div.addClass('hide');
		}
    },
    
    get_page: function(ev) {
    	ev.preventDefault();
    	var page = parseInt($(ev.currentTarget).data('page'));
		this.render_page(page);
		this.$el.find('.scroll-area').scrollTop(0);
    },
    
    reset_event: function(ev) {
    	this.render_filter();
    	this.filter_items();
    	this.render_page(0);
    }
	
});


// Start action view -> create new action
window.Datea.ActionStartView = Backbone.View.extend({
	
	tagName: 'div',
	
	render: function(eventName) {
		this.$el.html( ich.fix_base_content_single_tpl({'dotted_bg': true}));
		this.$el.find('#content').html( ich.action_create_tpl());
		return this;	
	}
	
});






