// refresh want listen count

setInterval(function() {
	$.get('/question/want', function(data) {
		console.log(data);
	}, 'json')
}, 5000);