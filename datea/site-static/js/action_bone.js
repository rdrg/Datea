


// DateaAction backbone model 
window.Datea.Action = Backbone.Model.extend();

// Action Collection
window.Datea.ActionCollection = Backbone.Collection.extend({
	model: Datea.Action,
	url: '/api/v1/action/',
});

window.Datea.CheckActionStats = function ($el, model) {
	// items
	if (model.get('item_count') == 1) {
		$('.item_count .singular', $el).show();
		$('.item_count .plural', $el).hide();
	}
	// comment
	if (model.get('comment_count') == 1) {
		$('.comment_count .singular', $el).show();
		$('.comment_count .plural', $el).hide();
	}
	// users
	if (model.get('user_count') == 1) {
		$('.user_count .singular', $el).show();
		$('.user_count .plural', $el).hide();
	}
}

// ACtion list item
window.Datea.ActionListItemView = Backbone.View.extend({
  
	tagName: 'div',
  
	className: 'action-item',

	render: function(){
  		this.$el.html(ich.action_list_item_tpl(this.model.toJSON()));
  
  		// follow widget
  		if (!Datea.my_user.isNew()) {
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
      
		Datea.CheckActionStats(this.$el, this.model);
		return this;
  }
                                
});

// Action list view -> of action items
window.Datea.ActionListView = Backbone.View.extend({
 
    tagName:'ul',
    
    attributes: {
    	'class': 'action-list',
    },
 
    initialize:function () {
        this.model.bind("reset", this.render, this);
        this.model.fetch();
    },
 
    render:function (eventName) {
        _.each(this.model.models, function (DateaAction) {
            $(this.el).append(new Datea.ActionListItemView({model:DateaAction}).render().el);
        }, this);
        return this;
    }
});


// Start action view -> create new action
window.Datea.ActionStartView = Backbone.View.extend({
	
	tagName: 'div',
	
	render: function(eventName) {
		this.$el.html( ich.fix_base_content_single_tpl());
		this.$el.find('#content').html( ich.action_create_tpl());
		return this;	
	}
	
});






