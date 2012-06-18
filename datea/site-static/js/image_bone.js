
// create with image form element: new Datea.ImageUploadView({'el':$('#some-form')}) 
window.Datea.ImageUploadView = Backbone.View.extend({
	
	events: {
		'change .input-file': 'upload'
	},	

	upload: function() {
		var self = this;
	    $.ajax('/image/save/', {
	    	type: "POST",
	        data: $(":hidden", this.$el).serializeArray(),
	        files: $(":file", this.$el),
	        iframe: true,
	        processData: false
	    }).complete(function(data) {
	        var response = jQuery.parseJSON(data.responseText);
	        // run callback if present 
	        if (typeof(self.options.callback) != 'undefined') self.options.callback(response);
	        // fetch specified models in "fetch_model"
	        if (typeof(self.options.fetch_model) != 'undefined') self.options.fetch_model.fetch();
	    });
	}
});