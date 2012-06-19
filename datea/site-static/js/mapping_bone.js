
window.Datea.Mapping = Backbone.Model.extend({
	urlRoot:"/api/v1/mapping",
});

window.Datea.MappingCreateView = Backbone.View.extend({
	
	tagName: 'div',
	
	events: {
		'click .save-mapping': 'save_mapping',
	},
	
	initialize: function() {
		this.model.bind("reset", this.render, this);
        this.model.bind("change", this.render, this);
  	},
	
	render: function(eventName) {
		this.$el.html( ich.fix_base_content_single_tpl());
		this.$el.find('#content').html( ich.mapping_create_tpl({ model: this.model }));
		return this;	
	},
	
	save_mapping: function(eventName) {
		this.model.set($('#new-mapping-form', this.$el).serializeObject());
		this.model.save();
	}
	
	
});