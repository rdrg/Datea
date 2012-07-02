

window.Datea.LayoutView = Backbone.View.extend({
	
	initialize: function () {
		this.$containers = this.$el.find('.container-target');
		this.$rows = this.$el.find('.row-target');
	},
	
	make_fix: function() {
		this.$containers.addClass('container').removeClass('container-fluid');
		this.$rows.addClass('row').removeClass('row-fluid');
	},
	
	make_fluid: function() {
		this.$containers.addClass('container-fluid').removeClass('container');
		this.$rows.addClass('row-fluid').removeClass('row');
	}
	
});
