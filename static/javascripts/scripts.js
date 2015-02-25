$(".nav-bar-btn").click(function(e) {
    var style = $(".nav-bar").attr("style");

    if(style === "display: block;") {
        $(".nav-bar").attr("style", "")
    } else {
        $(".nav-bar").attr("style", "display: block;")
    }
});


$(".btn-want-this-question").click(function(e) {
    
    var sel = "#" + e.target.id;

    var qid = e.target.id.split('-')[2];
    $.get('/question/want?qid=' + qid);

    if($(sel).hasClass("wanted")) {
        $('#btn-pop-' + qid).removeClass("wanted");
        $('#btn-pop-' + qid).html("想聽");

        $('#btn-new_q-' + qid).removeClass("wanted");
        $('#btn-new_q-' + qid).html("想聽");
    } else {
        $('#btn-pop-' + qid).addClass("wanted");
        $('#btn-pop-' + qid).html("已列入想聽名單");

        $('#btn-new_q-' + qid).addClass("wanted");
        $('#btn-new_q-' + qid).html("已列入想聽名單");
    }

    
});


$(".btn-collapse").click(function(e) {

    if(e.target.innerHTML === "▼") {
        var href = e.target.href;
        var target = href.split("#")[1];
        $("#" + target).hide();
        e.target.innerHTML = "►";
    } else {
        var href = e.target.href;
        var target = href.split("#")[1];
        $("#" + target).show();
        e.target.innerHTML = "▼";
    }
});
