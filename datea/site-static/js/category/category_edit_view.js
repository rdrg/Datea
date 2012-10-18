// edit list free category item view (listed item)
window.Datea.FreeCategoryEditListItemView = Backbone.View.extend({
	
	tagName: 'tr',
	
	attributes: {
		'class': 'edit-list-item',
	},
	
	events: {
		'click .edit-category': 'edit_category',
		'click .cancel-category': 'cancel_category',
	},
	
	initialize: function() {
		this.model.bind("change", this.render, this);
		this.model.bind("sync", this.render, this);
	},
	
	render: function(eventName) {
		this.$el.html(ich.free_category_edit_list_item_tpl(this.model.toJSON()));
		if (this.model.isNew()){
			this.edit_category();
		}
		return this;
	},
	
	edit_category: function (ev) {
		if (typeof(ev) != 'undefined') ev.preventDefault();
		this.$el.html( new Datea.FreeCategoryEditView({
			model: this.model,
		}).render().el );
		init_autoresize_textareas();
	},
	
	cancel_category: function(ev) {
		ev.preventDefault();
		if (this.model.isNew()) {
			this.$el.unbind();
			this.model.destroy();
			this.$el.empty();
		}else{
			this.render();
		}
	},
		
});

// free category edit list
window.Datea.FreeCategoryEditListView = Backbone.View.extend({
	
	tagName: 'table',
	
	initialize: function() {
		//this.model.bind("change", this.render, this);
		this.model.bind("add", this.render, this);
	},
	
	events: {
		'click .add-category': 'add_category',
	},
	
	render: function(eventName) {
		this.$el.html(ich.free_category_edit_list_tpl());
		
		var list_el = this.$el.find('.list-item-views');
		_.each(this.model.models, function (category) {
			list_el.append( new Datea.FreeCategoryEditListItemView({model:category}).render().el);
		}, this);
		
		return this;
	},
	
	add_category: function (ev) {
		ev.preventDefault();
		this.model.add({});
	}
	
});