$(function () {


       // 验证开始需要向网站主后台获取id，challenge，success（是否启用failback）
    $.ajax({
        url: "/axf/pcgetcaptcha/?t=" + (new Date()).getTime(), // 加随机数防止缓存
        type: "get",
        dataType: "json",
        success: function (data) {
            // 使用initGeetest接口
            // 参数1：配置参数
            // 参数2：回调，回调的第一个参数验证码对象，之后可以使用它做appendTo之类的事件
            initGeetest({
                gt: data.gt,
                challenge: data.challenge,
                product: "popup", // 产品形式，包括：float，embed，popup。注意只对PC版验证码有效
                offline: !data.success // 表示用户后台检测极验服务器是否宕机，一般不需要关注
                // 更多配置参数请参见：http://www.geetest.com/install/sections/idx-client-sdk.html#config
            }, handlerPopup);
        }
    });
    var handlerPopup = function (captchaObj) {
        // 成功的回调
        captchaObj.onSuccess(function () {
            console.log("success");
            var validate = captchaObj.getValidate();
            var username = $('#username').val();
            var password = $('#password').val();
            var csrftoken = $("[name='csrfmiddlewaretoken']").val();
            $.ajax({
                url: "/axf/login/", // 进行二次验证
                type: "post",

                data: {
                    username: username,
                    password: password,
                    csrfmiddlewaretoken: csrftoken,
                    geetest_challenge: validate.geetest_challenge,
                    geetest_validate: validate.geetest_validate,
                    geetest_seccode: validate.geetest_seccode
                },
                success: function (data) {
                    if (data["code"]==300) {
                        location.href = data["href"];
                    } else {
                        alert(data["error_msg"]);
                        location.href = data["href"];
                        $("#error_msg").html(data["error_msg"])
                    }
                }
            });
        });
        $("#login_button").click(function () {
            // alert(111);
            captchaObj.show();
        });
        // 将验证码加到id为captcha的元素里
        captchaObj.appendTo("#popup-captcha");
        // 更多接口参考：http://www.geetest.com/install/sections/idx-client-sdk.html
    };






$("#make_md5").click(function() {
    var password = $("#password").val();
    ret = md5(password);
    $("#password").val(ret);
    return true
});
});