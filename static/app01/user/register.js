flag = true;
$(function () {

    $("#username").change(function () {
        var username = $("#username").val();
        $.getJSON("/axf/register_check", {"username": username}, function (data) {
        if(data["code"]==200){
            $("#nameError").addClass("glyphicon glyphicon-ok form-control-feedback").css("color", "green");
            $("#nameError").html("");
            flag = true

        }else if (data["code"]==400){
            $("#nameError").html(data["msg"]).css("color", "red");
            $("#nameError").removeClass();
            flag = false
        }
    })
    });
    $("#password2").change(function () {
        var password2 = $("#password2").val();
        if((password2.length<6)||(password2!=$("#password1").val())){
            $("#errorMsg").html("密码长度不能小于6位/两次密码输入不一致!").css("color", "red");
            $("#errorMsg").removeClass();
            flag = false
        }else {
            $("#errorMsg").addClass("glyphicon glyphicon-ok form-control-feedback").css("color", "green");
            $("#errorMsg").html("");
            flag = true
        }
    })
});
function formsubmit() {
    if (flag){
        ret = md5($("#password2").val());
        $("#password1").val(ret);
        $("#password2").val(ret);
        return true
    } else {
        alert("您的信息有误!");
        return false
    }
}