$(".nav-bar-btn").click(function(e) {
    var style = $(".nav-bar").attr("style");

    if(style === "display: block;") {
        $(".nav-bar").attr("style", "")
    } else {
        $(".nav-bar").attr("style", "display: block;")
    }
});


$(".btn-want-this-question").click(function(e) {
    console.log(e.target.id);
    var sel = "#" + e.target.id;

    if($(sel).hasClass("wanted")) {
        $(sel).removeClass("wanted");
        $(sel).html("想聽");
        // TODO: change database
    } else {
        $(sel).addClass("wanted");
        $(sel).html("已列入想聽名單");
        // TODO: change database
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


$(".btn-send-register").click(function(e) {
    $("#reg_form").submit();
});

$(".btn-login").click(function(e) {
    $("#login_form").submit();
});