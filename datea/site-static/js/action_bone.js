

//+++++++++++++++++++++++++
// DateaAction backbone model 
window.Datea.Action = Backbone.Model.extend();

window.Datea.ActionCollection = Backbone.Collection.extend({
	model: Datea.Action,
	url: '/api/v1/action/',
});

window.Datea.ActionListItemView = Backbone.View.extend({
  
  tagName: 'li',
 
  render: function(){
      $(this.el).html(ich.action_list_item_tpl(this.model.toJSON()));
      return this;
  }
                                          
});

window.Datea.ActionListView = Backbone.View.extend({
 
    tagName:'ul',
 
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


window.Datea.ActionStartView = Backbone.View.extend({
	
	tagName: 'div',
	
	render: function(eventName) {
		this.$el.html( ich.fix_base_content_single_tpl());
		this.$el.find('#content').html( ich.action_create_tpl());
		return this;	
	}
	
});







