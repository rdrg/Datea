
window.Datea.paginate = function (list, page, items_per_page) {
	var result = _.rest(list, items_per_page*page);
    return _.first(result, items_per_page);
}


window.Datea.PaginatorView = Backbone.View.extend({
	
	tagName: 'ul',
	
	attributes: {
		'class': 'paginator nav',
	},
	
	initialize: function( ) {
		this.page = 0;
		this.adjacent_pages = 2;
		this.items_per_page = 5;
		if (this.options.adjacent_pages) {
			this.adjacent_pages = this.options.adjacent_pages;
		}
		if (this.options.items_per_page) {
			this.items_per_page= this.options.items_per_page;
		}
		this.num_pages = Math.ceil(this.model.length / this.items_per_page);
	},
	
	render_for_page: function(active_page) {
		this.num_pages = Math.ceil(this.model.length / this.items_per_page);
		this.page = parseInt(active_page);
		this.render();
		return this;
	},
	
	render: function () {
		
		this.$el.empty();
		var p_range = this.get_page_range();
		if (this.num_pages == 1) return;
		
		if (this.has_first()) {
			this.$el.append( ich.paginator_first());
			//this.$el.append(ich.paginator_separator());
		}
		if (this.has_prev()) {
			var ctx = {'page': this.page -1, 'page_name': this.page}
			this.$el.append( ich.paginator_prev(ctx));
		}
		if (p_range[0] > 0) {
			this.$el.append(ich.paginator_dots());
		}else if (this.has_prev()){
			this.$el.append(ich.paginator_separator());
		}
		
		for (var i=0; i< p_range.length; i++) {
			var p = p_range[i];
			var ctx = {'page': p, 'page_name': (parseInt(p) + 1)};
			if (p == this.page) ctx.li_attr = 'class="active"';
			this.$el.append(ich.paginator_page(ctx));
			if (i < p_range.length -1) {
				this.$el.append(ich.paginator_separator());
			}
		}
		if (p_range[p_range.length -1] != this.num_pages -1) {
			this.$el.append(ich.paginator_dots());
		}else{
			this.$el.append(ich.paginator_separator());
		}
		
		if (this.has_next()) {
			var ctx = {'page': (this.page + 1)}
			this.$el.append( ich.paginator_next(ctx));
		}
		if (this.has_last()) {
			//this.$el.append(ich.paginator_separator());
			var ctx = {'page': this.num_pages-1, 'page_name': this.num_pages}
			this.$el.append( ich.paginator_last(ctx));
		}
		return this;
	},
	
	get_page_range: function () {
		var page_range = [];
		// start range
		for (var i=this.page-this.adjacent_pages; i < this.page; i++) {
			if (i>=0) page_range.push(i);
		}
		page_range.push(this.page);
		for (var i=this.page+1; i < this.page + 1 + this.adjacent_pages; i++) {
			if (i < this.num_pages) page_range.push(i);
		} 	
		return page_range;
	},
	
	has_prev: function () {
		if (this.page != 0) return true;
		return false
	},
	
	has_next: function () {
		if ( (this.page + 1) < this.num_pages) return true;
		return false
	},
	
	has_first:function () {
		if (this.page - this.adjacent_pages > 0) return true;
		return false
	},
	
	has_last:function () {
		if (this.page + this.adjacent_pages < this.num_pages) return true;
		return false
	}
	
});
