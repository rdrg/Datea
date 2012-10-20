window.Datea.HistoryItemView = Backbone.View.extend({
	
	tagName: 'div',
	
	className: 'history-item',
	
	render: function (ev) {
		
		var stype = this.model.get('sender_type');
		var rtype = this.model.get('receiver_type');
		
		var recv_arr = [];
		var recv_items = this.model.get('receiver_items');
		for (i in recv_items) {
			recv_arr.push(ich[rtype+'_history_receiver'](recv_items[i], true));
		}

		var context = this.model.toJSON();
		context.receiver_html = recv_arr.join(', ');
		console.log(stype);
		context.title_html = ich[stype+'_history_sender'](context, true);
		context.link = context.receiver_items[0].url;
		context.created = formatDateFromISO(context.created, "dd.mm.yyyy - H:MM");
		
		this.$el.html(ich.history_item_tpl(context));
		
		return this;
	},
});