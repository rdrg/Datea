
window.Datea.Follow = Backbone.Model.extend({
	urlRoot: '/api/v1/follow'
});

window.Datea.FollowCollection = Backbone.Model.extend({
	model: Datea.Follow,
	url: '/api/v1/follow',
});


/* INIT WITH
 * {
 * 	follow_key: <name_of_the_model_in_lowercase>.<instance_pk> 	
 * 	follow_model: <model_instance_to_follow>,
 *  widget_class: <optional class for the widget>
 * }
 */

window.Datea.FollowWidgetView = Backbone.View.extend({
	
	tagName: 'div',
	
	className: 'follow-widget',
	
	initialize: function () {
		this.follow_model = this.attributes.follow_model;
		this.follow_key = this.attributes.follow_key;
	},
	
	events: {
		'click': 'follow',
	},
	
	render: function (ev) {
		this.$el.html( ich.follow_widget_tpl(this.) )
		
		if (this.attributes.follow_model.follow_count > 0) {
			
		}
	},
	
	follow: function(ev) {
		alert("hey");
	}
	
});


