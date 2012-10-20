window.Datea.MyUserHeadView = Backbone.View.extend({
	
	el: $('#user_head_view'),
	
	events : {
		'click .myprofile-edit-action': 'edit_profile', 
	},
	
	initialize: function () {
        this.model.bind("change", this.render, this);
        this.render();
    },
	
	render: function (eventName) {
		
    	if (Datea.is_logged()) {
    		this.$el.html(ich.my_user_head_tpl(this.model.toJSON(), true));
    	}else{
    		this.$el.html(ich.my_user_head_login_tpl());
    	}
        return this;
    },
    
    edit_profile: function (eventName) {
    	if (Datea.is_logged()) {
    		Datea.my_user_edit_view.open_window();
    	}
        return this;
    },
});
