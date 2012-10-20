
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
