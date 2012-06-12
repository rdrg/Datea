window.Datea = {};

//++++++++++++++++++++
// DateaProfile model
window.Datea.Profile = Backbone.Model.extend();

window.Datea.Profiles = Backbone.Collection.extend({
	model: Datea.Profile,
	url: '/api/v1/profile/'
});

window.Datea.MyProfile = Backbone.Collection.extend({
	model: Datea.Profile,
	url: '/api/v1/profile/?is_own=1',
});

window.Datea.MyProfileView = Backbone.View.extend({
	
	tagName: 'div',
	
	initialize:function () {
        this.model.bind("reset", this.render, this);
    },
    
    render:function (eventName) {
    	if (this.model.models.length == 1) {
    		this.$el.html(ich.my_profile(this.model.models[0].toJSON()));
    	}
        return this;
    }
}); 

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
      $(this.el).html(ich.action_list_item(this.model.toJSON()));
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


// Router
Datea.AppRouter = Backbone.Router.extend({
 
    routes:{
        "":"home",
        "_=_": "fb_login_redirect",
        "actions/:id":"action_detail",
    },
 
    home:function () {
        this.actionList = new Datea.ActionCollection();
        this.actionListView = new Datea.ActionListView({ model:this.actionList});
        this.actionList.fetch();
        $('#right-content').html(this.actionListView.render().el);
        
        this.myProfile = new Datea.MyProfile();
        this.myProfileView = new Datea.MyProfileView({ model: this.myProfile});
        this.myProfile.fetch();
        $('#left-content').html(this.myProfileView.render().el);
    },
    fb_login_redirect:function () {
    	alert("hey");
    }
 	/*
    wineDetails:function (id) {
        this.wine = this.wineList.get(id);
        this.wineView = new WineView({model:this.wine});
        $('#content').html(this.wineView.render().el);
    }*/
});

Datea.app = new Datea.AppRouter();
Backbone.history.start();





