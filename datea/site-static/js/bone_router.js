// Router
Datea.AppRouter = Backbone.Router.extend({
 
    routes:{
        "":"home",
        "_=_": "fb_login_redirect",
        "action/start": "action_start",
        "action/create/:action_type": "action_create",
    },
 
    home:function () {
    	this.my_profile_view = new Datea.MyProfileView({model:Datea.my_profile});
        $('#main-content-view').html(this.my_profile_view.render().el);
    },
    
    fb_login_redirect:function () {
    	alert("hey");
    },
    
    action_start: function () {
    	$('#main-content-view').html(new Datea.ActionStartView().render().el);
    },
    
    action_create: function (action_type) {
    	if (action_type == 'mapping') {
    		this.mapping = new Datea.MappingCreateView({model: new Datea.Mapping()});
    		$('#main-content-view').html(this.mapping.render().el);
    	}
    },
    
 	/*
    wineDetails:function (id) {
        this.wine = this.wineList.get(id);
        this.wineView = new WineView({model:this.wine});
        $('#content').html(this.wineView.render().el);
    }*/
});

$(document).ready(function() {
	
	// main stuff
	Datea.modal_view = new Datea.ModalWrapView({'el': $('#modal-wrap-view')});
	
	// init myprofile 
	Datea.init_my_profile();
	
	Datea.app = new Datea.AppRouter();
	Backbone.history.start();

});