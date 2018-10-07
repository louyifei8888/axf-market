$(function () {
    $("#type_container").hide();
    $("#sort_container").hide();
    $("#alltype").click(function () {
        $("#type_container").show();
        $("#arrow1").removeClass("glyphicon-chevron-down").addClass("glyphicon-chevron-up");
        $("#sort_container").hide();
        $("#arrow2").removeClass("glyphicon-chevron-up").addClass("glyphicon-chevron-down")
    });
    $("#allsort").click(function () {
        $("#type_container").hide();
        $("#arrow1").removeClass("glyphicon-chevron-up").addClass("glyphicon-chevron-down");
        $("#sort_container").show();
        $("#arrow2").removeClass("glyphicon-chevron-down").addClass("glyphicon-chevron-up")
    });
    $("#type_container").click(function () {
        $("#type_container").hide();
        $("#arrow1").removeClass("glyphicon-chevron-up").addClass("glyphicon-chevron-down");
        // $("#arrow2").removeClass("glyphicon-chevron-up").addClass("glyphicon-chevron-down")
    });
    $("#sort_container").click(function () {
        $(this).hide();
        $("#arrow2").removeClass("glyphicon-chevron-down").addClass("glyphicon-chevron-up")
    });
    $(".add_cart").click(function () {
        var $this = $(this);
        var urlpath = "/axf/add_cart";
        var good_id = $this.parent().attr("good_id");
        var data = {"good_id": good_id};
        $.getJSON(urlpath, data, function (data) {
            if (data["code"] == 304) {
                location.href = data["href"]
            } else if (data["code"] == 200) {
                $this.prev().html(data["num"])
            }
        })
    });
    $(".sub_cart").click(function () {
        var $this = $(this);
        var urlpath = "/axf/sub_cart";
        var good_id = $this.parent().attr("good_id");
        var data = {"good_id": good_id};
        $.getJSON(urlpath, data, function (data) {
            if (data["code"] == 304) {
                location.href = data["href"]
            } else if (data["code"] == 200) {
                $this.next().html(data["num"])
            }
        })
    })
});





