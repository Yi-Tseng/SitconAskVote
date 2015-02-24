// refresh want listen count

setInterval(function() {
	$.get('/question/want', function(data) {
		console.log(data);
		for(k in data) {
			$("#pop-" + k + " .title b").html("(" + data[k] + "人想聽)")
			$("#new_q-" + k + " .title b").html("(" + data[k] + "人想聽)")
		}
		
	}, 'json')
}, 5000);