
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





