// refresh live view

setInterval(function() {
    $.get('/question/current_live', function(data) {
        console.log(data);
        if(data.question != null) {
        	var title = data.question.title;
        	var author = data.question.author;
        	var text = data.question.text;

        	$(".title").html(title);
        	$(".context p").html("提問者：" + author);
        	$(".context pre").html(text);
        }
	},
1000);

