
function dateFromISO(isostr) {
 var parts = isostr.match(/\d+/g);
 return new Date(parts[0], parts[1] - 1, parts[2], parts[3], parts[4], parts[5]);
}

function datedayFromISO(isostr) {
	var parts = isostr.match(/\d+/g);
 	return new Date(parts[0], parts[1] - 1, parts[2], 0, 0, 0);
}

function formatDateFromISO(isostr, format) {
	return  dateFromISO(isostr).format(format);
}

function get_base_url() {
	return window.location.protocol+'//'+window.location.host;
}

if(!String.linkify) {
    String.prototype.linkify = function() {

        // http://, https://, ftp://
        var urlPattern = /\b(?:https?|ftp):\/\/[a-z0-9-+&@#\/%?=~_|!:,.;]*[a-z0-9-+&@#\/%=~_|]/gim;

        // www. sans http:// or https://
        var pseudoUrlPattern = /(^|[^\/])(www\.[\S]+(\b|$))/gim;

        // Email addresses
        var emailAddressPattern = /\w+@[a-zA-Z_]+?(?:\.[a-zA-Z]{2,6})+/gim;

        return this
            .replace(urlPattern, '<a href="$&">$&</a>')
            .replace(pseudoUrlPattern, '$1<a href="http://$2">$2</a>')
            .replace(emailAddressPattern, '<a href="mailto:$&">$&</a>');
    };
}





