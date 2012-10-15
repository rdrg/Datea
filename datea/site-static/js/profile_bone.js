
//++++++++++++++++++++++
// User model
window.Datea.User = Backbone.Model.extend({
	urlRoot: "/api/v1/user",
});

//++++++++++++++++++++++
// Profile model
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


//++++++++++++++++++++++++++
// EDIT PROFILE VIEW
window.Datea.MyUserEditView = Backbone.View.extend({
	
	tagName: 'div',
	
	events: {
		'click .save-action': 'save_action',
		'click .nav li a': 'tab_click',
	},
	
	initialize: function () {
    	this.model.bind("change", this.render, this);
    	this.save_mode = 'profile';
   	},
	
	render: function (eventName) {
		context = this.model.toJSON();
		if (Datea.is_logged()) {
			jQuery.extend(context, Datea.my_user_notify_settings.toJSON());
		}
		this.$el.html( ich.my_user_edit_tpl(context));
		if (this.img_upload_view) {
			this.$el.find('.image-input-view').html(this.img_upload_view.render().el);
		}
		return this;
	},
	
	save_action: function() {
		
		var self = this;
		if (this.save_mode == 'profile') {
			if (Datea.controls_validate(this.$el.find('#user-edit-form'))) {
				Datea.show_big_loading(this.$el);
				var profile = new Datea.Profile(this.model.get('profile'));
				profile.set({
					'full_name': $('[name="full_name"]', this.$el).val(),
					'message': $('[name="message"]', this.$el).val(),
				});
				this.model.save({
					'profile': profile.toJSON(),
					'email': $('[name="email"]', this.$el).val()
					}, {
					success: function (model, response) {
						Datea.hide_big_loading(self.$el);
					}
				});
			}
		}else if (this.save_mode == 'notify_settings') {
			Datea.show_big_loading(this.$el);
			var set = {};
			$('#notify-settings-form input[type="checkbox"]').each(function (){
				set[$(this).attr('name')] = $(this).is(':checked');
			});
			Datea.my_user_notify_settings.save(set, {
				success: function (model, response) {
					Datea.hide_big_loading(self.$el);
				}
			})
		}
	},
	
	
	tab_click: function (ev) {
		var id = $(ev.currentTarget).attr('href');
		if (id == '#edit-notifications') {
			this.save_mode = 'notify_settings';
		}else if (id == '#edit-profile') {
			this.save_mode = 'profile';
		}
	},
	
	open_window: function (tab) {
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
		
		if (typeof(tab) != 'unedfined') {
    		$('a[href="#'+tab+'"]').tab('show');
		}
		
	},
});


window.Datea.MyProfileBoxView = Backbone.View.extend({
	
	tagName: 'div',
	
	initialize: function () {
        this.model.bind("change", this.render, this);
   },
    
    render: function (eventName) {
    	
    	if (Datea.is_logged()) {
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
    	if (Datea.is_logged()) {
    		Datea.my_user_edit_view.open_window();
    	}
        return this;
    },
});


window.Datea.MyProfileHomeView = Backbone.View.extend({
	
	tagName: 'div',
	
	render: function (ev) {
		
		// set base template
		this.$el.html( ich.fix_base_content_split_tpl({dotted_bg:true}));
		
		this.$el.find('#left-content').html( 
			new Datea.MyProfileBoxView({ model: Datea.my_user }).render().el 
		);
		Datea.CheckStatsPlural(this.$el, this.model);
		if (Datea.is_logged()) {
			this.$el.find('.history-view-container').html(
				new DateaHistoryView({user_model: Datea.my_user}).render().el
			);
		}
		
		// ACTIONS
		this.$el.find('#right-content').html(
			new Datea.MyActionListView().render().el
		);
		return this;
	},	
});


window.Datea.ProfileView = Backbone.View.extend({
	
	tagName: 'div',
	
	render: function (ev) {
		
		this.$el.html( ich.fix_base_content_split_tpl({dotted_bg:true}));
		
		// profile data -> left
		this.$el.find('#left-content').html(ich.my_profile_tpl(this.model.toJSON()));
		Datea.CheckStatsPlural(this.$el, this.model);
		this.$el.find('.history-view-container').html(
			new DateaHistoryView({user_model:this.model}).render().el
		);
		
		// action data -> right
		// ACTIONS
		this.$el.find('#right-content').html(
			new Datea.ProfileActionListView({user_model: this.model}).render().el
		);
		return this;
	}	
});



// INIT MY USER MODELS/VIEWS FROM THE START
Datea.init_my_user_views = function () {
	Datea.my_user_head_view = new Datea.MyUserHeadView({ model: Datea.my_user});
	Datea.my_user_edit_view = new Datea.MyUserEditView({ model: Datea.my_user});
}

Datea.is_logged = function () {
	if (Datea.my_user.get('id')) return true;
	else return false;
}
