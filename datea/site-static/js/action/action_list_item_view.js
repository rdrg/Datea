
// ACtion list item
window.Datea.ActionListItemView = Backbone.View.extend({
  
	tagName: 'div',
  
	className: 'action-item',

	render: function(){
		var context = this.model.toJSON();
		context.created = formatDateFromISO(context.created, "dd.mm.yyyy");
		
		// end date
		if (this.model.get('end_date') != null) {
			var now = new Date();
			now.setHours(0,0,0,0);
			var end = datedayFromISO(this.model.get('end_date'));
			if (now <= end) {
				var days_left = Math.ceil((end.getTime()-now.getTime())/86400000);
				if (days_left > 0) {
					context.active_message = ich.action_days_left_tpl({days_left: days_left}, true);
				}else{
					context.active_message = ich.action_last_day_tpl({}, true);
				}
			}else{
				context.active_message = ich.action_expired_tpl({}, true);
			}
		}
		context.unpublished = !context.published;
		
  		this.$el.html(ich.action_list_item_tpl(context));
  
  		// follow widget
  		if (Datea.is_logged() && Datea.my_user.get('resource_uri') != this.model.get('user')) {
			this.follow_widget = new Datea.FollowWidgetView({
				object_type: 'dateaaction',
				object_id: this.model.get('id'),
				object_name: gettext('action'),
				followed_model: this.model,
				type: 'button',
				style: 'button-small',
				callback: this.options.follow_callback 
			});
			this.$el.find('.follow-button').html(this.follow_widget.render().el);
		}
      
		Datea.CheckStatsPlural(this.$el, this.model);
		return this;
  }
                                
});