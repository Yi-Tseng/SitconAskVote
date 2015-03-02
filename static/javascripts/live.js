// refresh live view

setInterval(function() {
    $.get('/question/current_live', function(data) {
        console.log(data);
        if(data.question != null) {
            var title = data.question.title;
            var author = data.question.author;
            var text = data.question.text;

            $(".title")[0].text(title);
            $(".context p").text("提問者：" + author);
            text_arr = text.split("\n");
            text = "";
            for(var t: text_arr) {
                text += t + "<br>";
            }
            $(".context .text").text(text);
        }
    });
}, 1000);

