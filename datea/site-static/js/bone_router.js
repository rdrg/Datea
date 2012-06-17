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
       
        $('#left-content').html(Datea.my_profile_view.render().el);
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

$(document).ready(function() {
	
	// init myprofile 
	Datea.init_my_profile();
	
	Datea.app = new Datea.AppRouter();
	Backbone.history.start();
});