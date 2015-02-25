// refresh want listen count

setInterval(function() {
    $.get('/question/want', function(data) {
        console.log(data);
        for(k in data) {
            $("#que-" + k + " .title b").html("(" + data[k] + "人想聽)")
        }
    }, 'json')
}, 1000);
