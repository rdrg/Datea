

window.Datea.UserProfileView = Backbone.View.extend({
	
	initialize: function() {
		this.model.bind("change", this.render, this);
	},
	
	render: function(ev) {
		this.$el.html(ich.my_profile_tpl(this.model.toJSON()));
		return this;
	}
	
});
