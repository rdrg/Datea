

/***
 * Init with:
 * 
 * {
 * 	options: [{value: "foo", name: "bar"}, {value: "foo2", name: "bar2"}],
 *  div_class: 'dropup' // optional
 *  callback: <fn when changed>
 *  init_value: default value // optional
 * }
 * 
 */
window.Datea.DropdownSelect = Backbone.View.extend({
	
	tagName: 'div',
	className: 'btn-group dropdown-select',
	
	initialize: function () {
		if (this.options.init_value) {
			this.value = this.options.init_value; 
		}else{
			this.value = this.options.options[0].value;
		}
		if (this.options.div_class) {
			this.$el.addClass(this.options.div_class);
		}
	},
	
	events: {
		'click li a': 'select_option',
	},
	
	render: function (ev) {
		var context = {
			options: this.options.options,
		};
		
		this.$el.html( ich.dropdown_select_tpl(context));
		this.set_value(this.value);
		return this;
	},
	
	set_value: function (value) {
		var opt = _.find(this.options.options, function (o) { return o.value == value });
		if (typeof(opt) == 'undefined') {
			opt = this.options.options[0];
		}
		this.value = opt.value;
		var name = opt.name;
		if (this.options.box_text_max_length && name.length > this.options.box_text_max_length) {
			name = name.substr(0, this.options.box_text_max_length)+'...';
		}
		this.$el.find('.name').html(name);
	},
	
	select_option: function (ev) {
		ev.preventDefault();
		this.set_value(ev.target.dataset.value);
		if (this.options.callback) this.options.callback(this.value);
	},
	
	reset_events: function () {
		this.undelegateEvents();
		this.delegateEvents();
	},
	
});
