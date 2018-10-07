$(function () {
    $("#submit").click(function () {
        var u_name = $("#u_name").val();
        var call_phone = $("#call_phone").val();
        var address = $("#address").val();
        var data1 = {
            "u_name": u_name,
            "call_phone": call_phone,
            "address": address
        };
        $.getJSON("/axf/receiver", data1, function (data) {
            if (data["code"] == 200) {
                $("#get_name").html(u_name);
                $("#get_call_phone").html(call_phone);
                $("#get_address").html(address);
            }
        });

    });
    $(".add_cart_num").click(function () {
        var $this = $(this);
        var urlpath = "/axf/add_cart_num";
        var c_goodid = $this.parents("li").attr("c_good_id");
        $.getJSON(urlpath, {"c_goodid": c_goodid}, function (data) {
            if (data["code"] == 200) {
                $this.prev().html(data["num"]);
                $("#sum_count").html("共计" + data["sum_count"] + "件");
                $("#sum_price").html("总价" + data["sum_price"])
            }
        })
    });
    $(".sub_cart_num").click(function () {
        var $this = $(this);
        var urlpath = "/axf/sub_cart_num";
        var c_goodid = $this.parents("li").attr("c_good_id");
        $.getJSON(urlpath, {"c_goodid": c_goodid}, function (data) {
            if (data["code"] == 200) {
                if (data["num"] == 0) {
                    $this.parents("li").remove()
                    $("#sum_count").html("共计" + data["sum_count"] + "件");
                    $("#sum_price").html("总价" + data["sum_price"])
                } else {
                    $this.next().html(data["num"]);
                    $("#sum_count").html("共计" + data["sum_count"] + "件");
                    $("#sum_price").html("总价" + data["sum_price"])
                }
            }
        })
    });
    $(".select").click(function () {
        var $this = $(this);
        var c_goodid = $this.parents("li").attr("c_good_id");
        var is_select = $this.attr("select");// 得到的是一个字符串"False"/"True"
        // console.log(typeof is_select);
        $.getJSON("/axf/change_select", {"is_select": is_select, "c_goodid": c_goodid}, function (data) {
            // console.log(data["is_select"]);
            // console.log(typeof data["is_select"]);
            // 得到的是boolean类型的值,不影响判断
            if (data["is_select"]) {
                $this.children("span").html("√");
                $this.attr("select", "True");
                $("#sum_count").html("共计" + data["sum_count"] + "件");
                $("#sum_price").html("总价" + data["sum_price"])
            } else {
                $this.children("span").html("");
                $this.attr("select", "False");
                $("#sum_count").html("共计" + data["sum_count"] + "件");
                $("#sum_price").html("总价" + data["sum_price"])
            }
            if (data["all_selected"]) {
                $("#allSelectButton").children("span").html("√")
            } else {
                $("#allSelectButton").children("span").html("")
            }
        })
    });

    $("#allSelectButton").click(function () {
        select_array = [];
        not_select_array = [];

        $(".select").each(function () {
            $this = $(this);
            if ($this.attr("select") == "True") {
                select_array.push($this.parents("li").attr("c_good_id"))
            } else {
                not_select_array.push($this.parents("li").attr("c_good_id"))
            }
        });
        // console.log(select_array);
        // console.log(not_select_array);
        if (not_select_array.length == 0 && select_array.length > 0) {
            // 如果所有的商品都被选中(点全选应该取消所有选中)

            var urlpath = "/axf/all_select";
            var data = {"all_select": select_array.join("#")};
            $.getJSON(urlpath, data, function (data) {
                if (data["code"] == 200) {
                    $("#allSelectButton").children("span").html("");
                    $(".select").children("span").html("");
                    $(".select").attr("select", "False");
                    $("#sum_count").html("共计" + data["sum_count"] + "件");
                    $("#sum_price").html("总价" + data["sum_price"])
                }
            })
        } else {
            //存在有至少一个商品未被选中(点全选应该选中它)
            $.getJSON("/axf/all_select", {"not_select_array": not_select_array.join("#")}, function (data) {
                if (data["code"] == 200) {
                    $("#allSelectButton").children("span").html("√");
                    $(".select").children("span").html("√");
                    $(".select").attr("select", "True");
                    $("#sum_count").html("共计" + data["sum_count"] + "件");
                    $("#sum_price").html("总价" + data["sum_price"])
                }
            })

        }
    });
});