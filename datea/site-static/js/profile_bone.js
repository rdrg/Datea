
//++++++++++++++++++++++
// User model
window.Datea.User = Backbone.Model.extend({
	urlRoot: "/api/v1/user",
});

//++++++++++++++++++++++
// User Collection
window.Datea.UserCollection = Backbone.Collection.extend({
	model: Datea.User,
	url: "/api/v1/user",
});


window.Datea.MyUserHeadView = Backbone.View.extend({
	
	el: $('#user_head_view'),
	
	events : {
		'click .myprofile-edit-action': 'edit_profile', 
	},
	
	initialize: function () {
        this.model.bind("change", this.render, this);
    },
	
	render: function (eventName) {

    	if (!this.model.isNew()) {
    		console.log(this.model);
    		this.$el.html(ich.my_user_head_tpl(this.model.toJSON()));
    	}else{
    		this.$el.html(ich.my_user_head_login_tpl());
    	}
        return this;
    },
    
    edit_profile: function (eventName) {
    	if (!this.model.isNew()) {
    		Datea.my_user_edit_view.open_window();
    	}
        return this;
    },
});


//++++++++++++++++++++++++++
// EDIT PROFILE VIEW
window.Datea.MyUserEditView = Backbone.View.extend({
	
	tagName: 'div',
	
	events: {
		'click .myprofile-save-action': 'save_profile', 
	},
	
	initialize: function () {
    	this.model.bind("change", this.render, this);
   	},
	
	render: function (eventName) {
		this.$el.html( ich.my_user_edit_tpl(this.model.toJSON()));
		return this;
	},
	
	save_profile: function() {
		this.model.set({
			'full_name': this.$el.find('#edit-profile-full-name').val(),
		});
		this.model.save();
	},
	
	open_window: function () {
		Datea.modal_view.set_content(this);
		Datea.modal_view.open_modal();
		
		var img_upload_view = new Datea.ImageUploadView({
				'el': $('#profile-image-upload', this.$el),
				'fetch_model': this.model
			});
	},
});


window.Datea.MyProfileBoxView = Backbone.View.extend({
	
	tagName: 'div',
	
	initialize: function () {
        this.model.bind("change", this.render, this);
   },
    
    render: function (eventName) {
    	
    	if (!this.model.isNew()) {
    		this.$el.html(ich.my_profile_tpl(this.model.toJSON()));
    	}
        return this;
    },
    
    edit_profile: function (eventName) {
    	if (!this.model.isNew()) {
    		Datea.my_user_edit_view.open_window();
    	}
        return this;
    },
});


window.Datea.MyProfileHomeView = Backbone.View.extend({
	
	tagName: 'div',
	
	render: function (eventName) {
		// set base template
		this.$el.html( ich.fix_base_content_split_tpl());
		
		this.$el.find('#left-content').html( 
			new Datea.MyProfileBoxView({ model: Datea.my_user }).render().el 
		);
		
		// ACTIONS
		this.actionList = new Datea.ActionCollection();
		this.$el.find('#right-content').html(
			new Datea.ActionListView({ model:this.actionList}).render().el
		);
		return this;
	},	
});



// INIT MY USER MODELS/VIEWS FROM THE START
Datea.init_my_user_views = function () {
	Datea.my_user_head_view = new Datea.MyUserHeadView({ model: Datea.my_user});
	Datea.my_user_edit_view = new Datea.MyUserEditView({ model: Datea.my_user }); 
}
