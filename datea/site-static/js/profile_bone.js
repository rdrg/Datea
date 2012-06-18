
//++++++++++++++++++++
// DateaProfile model
window.Datea.Profile = Backbone.Model.extend({
	urlRoot:"/api/v1/profile",
});


//++++++++++++++++++++
// Profiles Collection
window.Datea.Profiles = Backbone.Collection.extend({
	model: Datea.Profile,
	url: '/api/v1/profile/'
});

//++++++++++++++++++++++
// My profile collection
window.Datea.MyProfile = Backbone.Collection.extend({
	model: Datea.Profile,
	url: '/api/v1/profile/?is_own=1',
});


window.Datea.MyProfileView = Backbone.View.extend({
	
	tagName: 'div',
	
	initialize: function () {
        this.model.bind("reset", this.render, this);
        this.model.bind("change", this.render, this);
    },
    
    render: function (eventName) {
    	if (this.model.models.length == 1) {
    		this.$el.html(ich.my_profile_tpl(this.model.models[0].toJSON()));
    	}
        return this;
    },
    
    edit_profile: function (eventName) {
    	if (this.model.models.length == 1) {
    		Datea.my_profile_edit_view.open_window();
    	}
        return this;
    },
});


window.Datea.MyProfileHeadView = Backbone.View.extend({
	
	el: $('#profile_head_view'),
	
	events : {
		'click .myprofile-edit-action': 'edit_profile', 
	},
	
	initialize: function () {
        this.model.bind("reset", this.render, this);
        this.model.bind("change", this.render, this);
    },
	
	render: function (eventName) {
    	if (this.model.models.length == 1) {
    		this.$el.html(ich.my_profile_head_tpl(this.model.models[0].toJSON()));
    	}else{
    		this.$el.html(ich.my_profile_head_login_tpl());
    	}
        return this;
    },
    
    edit_profile: function (eventName) {
    	if (this.model.models.length == 1) {
    		Datea.my_profile_edit_view.open_window();
    	}
        return this;
    },
});


//++++++++++++++++++++++++++
// EDIT PROFILE VIEW
window.Datea.MyProfileEditView = Backbone.View.extend({
	
	tagName: 'div',
	
	events: {
		'click .myprofile-save-action': 'save_profile', 
	},
	
	initialize: function () {
		//this.model.bind("reset", this.render, this);
    	this.model.bind("change", this.render, this);
   	},
	
	render: function (eventName) {
		this.$el.html( ich.my_profile_edit_tpl(this.model.models[0].toJSON()));
		return this;
	},
	
	save_profile: function() {
		this.model.models[0].set({
			'full_name': this.$el.find('#edit-profile-full-name').val(),
		});
		this.model.models[0].save();
	},
	
	open_window: function () {
		Datea.modal_view.set_content(this);
		Datea.modal_view.open_modal();
		
		var img_upload_view = new Datea.ImageUploadView({
				'el': $('#profile-image-upload', this.$el),
				'fetch_model': this.model.models[0]
			});
	},
	
});


// INIT MY PROFILE VIEWS FROM THE START
Datea.init_my_profile = function () {
	Datea.my_profile = new Datea.MyProfile();
	Datea.my_profile.fetch();
	Datea.my_profile_view = new Datea.MyProfileView({ model: Datea.my_profile});
	Datea.my_profile_head_view = new Datea.MyProfileHeadView({ model: Datea.my_profile});
	Datea.my_profile_edit_view = new Datea.MyProfileEditView({ model: Datea.my_profile }); 
}
