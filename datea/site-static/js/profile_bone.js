
//++++++++++++++++++++++
// User model
window.Datea.User = Backbone.Model.extend({
	urlRoot: "/api/v1/user",
});

//++++++++++++++++++++++
// User model
window.Datea.Profile = Backbone.Model.extend({
	urlRoot: "/api/v1/profile",
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
		if (this.img_upload_view) {
			this.$el.find('.image-input-view').html(this.img_upload_view.render().el);
		}
		return this;
	},
	
	save_profile: function() {
		
		var profile = new Datea.Profile(this.model.get('profile'));
		profile.set({
			'full_name': this.$el.find('#edit-profile-full-name').val(),
		});
		
		this.model.set({
			'profile': profile.toJSON(),
		});
		Datea.show_big_loading(this.$el);
		var self = this;
		this.model.save({
			success: function (model, response) {
				Datea.hide_big_loading(self.$el);
			}
		});
	},
	
	open_window: function () {
		Datea.modal_view.set_content(this);
		Datea.modal_view.open_modal();
		
		var img = new Datea.Image();
		var self = this;
		this.img_upload_view = new Datea.ImageInputView({
			model: img,
			placeholder: this.model.get('profile').image_large,
			no_delete: true,
			hide_loading: true,
			img_data: {
				object_type: 'DateaProfile',
				object_id: this.model.get('profile').id,
				object_field: 'image',
				thumb_preset: 'profile_image_large',
			},
			callfirst:function() {
				Datea.show_big_loading(self.$el);
			},
			callback: function (response) {
				if (response.ok) {
					self.model.fetch({
						success: function () {
							Datea.hide_big_loading(self.$el);
						}
					});
				}
			}, 
		});
		this.$el.find('.image-input-view').html(this.img_upload_view.render().el);
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
    	}else{
    		var title = gettext('Datea, a platform to activate and channel community engagements.');
    		context = {
    			title: title,
    			hashtag: 'datea',
    			tweet_text: title,
    			full_url: get_base_url()
    		}
    		this.$el.html(ich.datea_presentation_tpl(context));
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
		this.$el.html( ich.fix_base_content_split_tpl({'class':'dotted-bg'}));
		
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
