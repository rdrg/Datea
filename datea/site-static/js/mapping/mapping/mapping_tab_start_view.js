

window.Datea.MappingStartTab = Backbone.View.extend({
	
	initialize: function () {
		this.model.bind('change', this.render, this);
		this.model.bind('add', this.render, this);
		this.model.bind('remove', this.render, this);
		//this.model.bind('reset', this.render, this);
	}, 
	
	render: function(eventName) {
		var context = this.model.toJSON();
		context.full_url = get_base_url() + this.model.get('url');
		context.tweet_text = this.model.get('short_description');
		context.unpublished = !context.published;
		
		this.$el.html( ich.mapping_tab_start_tpl(context));
		Datea.CheckStatsPlural(this.$el, this.model);
		
		// follow widget
  		if (Datea.is_logged()) {
  			var data = {
  				object_type: 'dateaaction',
				object_id: this.model.get('id'),
				object_name: gettext('action'),
				followed_model: this.model,
				silent: true,
				type: 'full',
				style: 'full-large', 
  			}
  			if (Datea.my_user.get('id') == this.model.get('user').id) {
  				data.read_only = true;
  				data.is_own = true;
  			}
			this.follow_widget = new Datea.FollowWidgetView(data);
			this.$el.find('.follow-button').html(this.follow_widget.render().el);
		}
		
		init_share_buttons();
	} 
	
});
