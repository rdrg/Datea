

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
    },
 
    render:function (eventName) {
        _.each(this.model.models, function (DateaAction) {
            $(this.el).append(new Datea.ActionListItemView({model:DateaAction}).render().el);
        }, this);
        return this;
    }
});







