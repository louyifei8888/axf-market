import uuid

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.cache import cache_page
from geetest import GeetestLib

from app01.models import Wheel, Nav, MustBuy, ShopModel, MainShow, FoodType, Goods, UserModel, Cart, Receiver, Order, \
    OrderAndGoods


# 展示主页
def home(request):
    wheels = Wheel.objects.all()
    navs = Nav.objects.all()
    mustbuys = MustBuy.objects.all()
    shopmodels_0 = ShopModel.objects.all()[0]
    shopmodels_1_2 = ShopModel.objects.all()[1:3]
    shopmodels_3_6 = ShopModel.objects.all()[3:7]
    shopmodels_7_ = ShopModel.objects.all()[7:]
    mainshows = MainShow.objects.all()
    data = {
        "wheels": wheels,
        "navs": navs,
        "mustbuys": mustbuys,
        "shopmodels_0": shopmodels_0,
        "shopmodels_1_2": shopmodels_1_2,
        "shopmodels_3_6": shopmodels_3_6,
        "shopmodels_7_": shopmodels_7_,
        "mainshows": mainshows,
    }

    return render(request, "home/home.html", data)


# 展示商品页
@cache_page(600)
def market(request, type_id, childid, sortid):
    user_id = request.session.get("use_id")
    try:
        user = UserModel.objects.get(pk=user_id)
    except BaseException:
        user = None
    foodtypes = FoodType.objects.all()
    foodtypes_each = foodtypes.filter(typeid=type_id)

    # 如果无筛选条件,默认全部展示
    if str(childid) == '0':
        goods = Goods.objects.all().filter(categoryid=type_id)
    # 如果有筛选条件,按照筛选条件进行筛选
    else:
        goods = Goods.objects.all().filter(categoryid=type_id).filter(childcid=childid)
    # 根据排序的规则对商品进行排序
    if str(sortid) == '1':
        goods = goods.order_by("productid")
    elif str(sortid) == '2':
        goods = goods.order_by("price")
    elif str(sortid) == '3':
        goods = goods.order_by("-price")
    good_list = []
    for good in goods:
        try:
            carts = Cart.objects.filter(c_goods=good, c_user=user)
        except:
            carts = None
        if carts:
            cart1 = carts.first()
            good.cart = cart1.c_num
        else:
            good.cart = 0
        good_list.append(good)
    goods = good_list

    foodtype_list = []
    for foodtype in foodtypes_each:
        # [全部分类:0,酸奶乳酸菌:103537,牛奶豆浆:103538,面包蛋糕:103540]
        for each in foodtype.childtypenames.split("#"):
            foodtype_list.append(each.split(":"))
    data = {
        "foodtypes": foodtypes,
        "goods": goods,
        "type_id": type_id,
        "childid": childid,
        "foodtype_list": foodtype_list,
    }

    return render(request, "market/market.html", data)


# 展示购物车页面,若未登录则跳转到登录页面
def cart(request):
    use_id = request.session.get("use_id")
    if use_id:
        user = UserModel.objects.get(pk=use_id)
        cart_list = Cart.objects.filter(c_user=user)
        # 用于设定全选按钮的默认状态
        all_select = True
        for each_cart in cart_list:
            if not each_cart.c_isselect:
                all_select = False
                break
        carts = Cart.objects.filter(c_user_id=use_id)
        select_carts = Cart.objects.filter(c_user_id=use_id, c_isselect=True)
        sum_count = 0
        sum_price = 0
        for select_cart in select_carts:
            sum_count += select_cart.c_num
            sum_price += select_cart.c_goods.price * select_cart.c_num
        try:
            receivers = Receiver.objects.get(r_user=user)
        except:
            receivers = Receiver.objects.create(r_name=user.u_name, r_call_phone=0, r_address="未编辑", r_user=user)
        data = {
            "carts": carts,
            "all_select": all_select,
            "sum_count": "{:.1f}".format(sum_count),
            "sum_price": "{:.1f}".format(sum_price),
            "user": user,
            "receivers": receivers
        }
        return render(request, "cart/cart.html", data)
    return redirect(reverse('axf:login'))


# market界面的增加按钮
def add_cart(request):
    use_id = request.session.get("use_id")
    if use_id:
        # 获取登录的用户
        user = UserModel.objects.get(pk=use_id)
        good_id = request.GET.get("good_id")
        good = Goods.objects.get(pk=good_id)
        # 判断该用户有没有创建购物车表数据
        ret = Cart.objects.filter(c_user=user).filter(c_goods=good)
        data = {}
        if ret:
            the_cart = ret.first()
            the_cart.c_num += 1
            the_cart.save()
            data["code"] = 200
            data["msg"] = "加操作成功"
            data["num"] = the_cart.c_num
        else:
            Cart.objects.create(c_user=user, c_goods=good)
            data["code"] = 200
            data["msg"] = "加操作成功"
            data["num"] = 1
        return JsonResponse(data)
    else:
        data = {"href": "/axf/login", "code": 304}
        return JsonResponse(data)


# market界面的减少按钮
def sub_cart(request):
    use_id = request.session.get("use_id")
    if use_id:
        # 获取登录的用户
        user = UserModel.objects.get(pk=use_id)
        good_id = request.GET.get("good_id")
        good = Goods.objects.get(pk=good_id)
        # 判断该用户有没有创建购物车表数据
        the_cart = Cart.objects.get(c_user=user, c_goods=good)
        data = {}
        if the_cart.c_num == 1:
            the_cart.delete()
            data["code"] = 200
            data["msg"] = "减操作成功"
            data["num"] = 0
        elif the_cart.c_num > 1:
            the_cart.c_num -= 1
            the_cart.save()
            data["code"] = 200
            data["msg"] = "减操作成功"
            data["num"] = the_cart.c_num

        return JsonResponse(data)
    else:
        data = {"href": "/axf/login", "code": 304}
        return JsonResponse(data)


# 展示我的页面,如果登录了,则显示登录后的页面
def mine(request):
    user_id = request.session.get("use_id")
    if user_id:
        user = UserModel.objects.get(pk=user_id)
        orders = Order.objects.all()
        wait_pay = orders.filter(o_status=1).count()
        wait_receiver = orders.filter(o_status=2).count()
        wait_calk = orders.filter(o_status=3).count()
        wait_after = orders.filter(o_status=4).count()
        img_path = '/static/upload/' + user.u_img.url
        data = {
            "wait_pay": wait_pay,
            "wait_receiver": wait_receiver,
            "wait_calk": wait_calk,
            "wait_after": wait_after,
            "user": user,
            "img_path": img_path,
        }
        return render(request, "mine/mine.html", data)
    return render(request, "mine/mine.html", {"user": False})


# 展示注册界面
def register(request):
    return render(request, "user/register.html")


# 处理注册相关
def register_check(request):
    if request.method == "GET":
        username = request.GET.get("username")
        user = UserModel.objects.filter(u_name=username)
        if user:
            return JsonResponse({"code": 400, "msg": "该用户名已被使用!"})
        return JsonResponse({"code": 200, "msg": "用户名可用!"})
    elif request.method == "POST":
        # 根据表单内容创建对应的用户
        password = request.POST.get("password")
        username = request.POST.get("username")
        email = request.POST.get("email")
        print(email)
        img_file = request.FILES.get("imgFile")
        UserModel.objects.create(u_name=username, u_passwd=password, u_mail=email, u_img=img_file)
        return redirect(reverse('axf:login'))


# 注销用户
def logout(request):
    request.session.flush()
    return redirect(reverse('axf:mine'))


pc_geetest_id = "b46d1900d0a894591916ea94ea91bd2c"
pc_geetest_key = "36fc3fe98530eea08dfc6ce76e3d24c4"


# 滑动验证码验证
def pcgetcaptcha(request):
    user_id = 'test'
    gt = GeetestLib(pc_geetest_id, pc_geetest_key)
    status = gt.pre_process(user_id)
    request.session[gt.GT_STATUS_SESSION_KEY] = status
    request.session["user_id"] = user_id
    response_str = gt.get_response_str()
    return HttpResponse(response_str)


def login(request):
    # 用于验证ajax请求过来的验证码和帐号密码
    if request.method == 'POST':
        username = request.POST.get("username")
        user = UserModel.objects.filter(u_name=username)
        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        challenge = request.POST.get(gt.FN_CHALLENGE, '')
        validate = request.POST.get(gt.FN_VALIDATE, '')
        seccode = request.POST.get(gt.FN_SECCODE, '')
        status = request.session[gt.GT_STATUS_SESSION_KEY]
        user_id = request.session["user_id"]
        if status:
            result = gt.success_validate(challenge, validate, seccode, user_id)
        else:
            result = gt.failback_validate(challenge, validate, seccode)
        # 如果帐号和验证码验证无误后,验证密码
        if user and result:
            user = user.first()
            # 全部验证通过后返回登录后的页面
            if request.POST.get("password") == user.u_passwd:
                data = {"code": 300, "href": "/axf/mine"}
                response = JsonResponse(data)
                request.session["use_id"] = user.id
                return response
            else:
                data = {"code": 200, "error_msg": "输入的信息有误", "href": "/axf/login"}
                return JsonResponse(data)
        else:
            data = {"code": 200, "error_msg": "输入的信息有误", "href": "/axf/login"}
            return JsonResponse(data)
    # 如果是get请求直接返回登录界面
    return render(request, "user/login.html")


# 在购物车界面增加按钮
def add_cart_num(request):
    user_id = request.session.get("use_id")
    user = UserModel.objects.get(pk=user_id)
    c_good_id = request.GET.get("c_goodid")
    the_cart = Cart.objects.get(c_goods_id=c_good_id)
    the_cart.c_num += 1
    the_cart.save()
    data = {
        "code": 200,
        "msg": "增加成功",
        "num": the_cart.c_num
    }
    sum_tuple = get_count_price(user)
    sum_count = sum_tuple[0]
    sum_price = sum_tuple[1]
    data["sum_count"] = sum_count
    data["sum_price"] = sum_price
    return JsonResponse(data)


# 购物车界面减少按钮
def sub_cart_num(request):
    user_id = request.session.get("use_id")
    user = UserModel.objects.get(pk=user_id)
    c_good_id = request.GET.get("c_goodid")
    the_cart = Cart.objects.get(c_goods_id=c_good_id)
    if the_cart.c_num == 1:
        the_cart.delete()
        data = {
            "code": 200,
            "msg": "减少成功",
            "num": 0
        }
    else:
        the_cart.c_num -= 1
        the_cart.save()
        data = {
            "code": 200,
            "msg": "减少成功",
            "num": the_cart.c_num
        }
    sum_tuple = get_count_price(user)
    sum_count = sum_tuple[0]
    sum_price = sum_tuple[1]
    data["sum_count"] = sum_count
    data["sum_price"] = sum_price
    return JsonResponse(data)


# 购物车商品前的选中状态处理
def change_select(request):
    user_id = request.session.get("use_id")
    user = UserModel.objects.get(pk=user_id)
    carts = Cart.objects.filter(c_user=user)
    # print(all_select)
    # 接受到的是个字符串"True"/"False"
    is_select = request.GET.get("is_select")
    select = eval(is_select)
    c_goodid = request.GET.get("c_goodid")
    the_cart = Cart.objects.get(c_goods_id=c_goodid, c_user=user)
    the_cart.c_isselect = not select
    the_cart.save()
    data = {
        "is_select": the_cart.c_isselect,
    }
    all_selected = True
    for each in carts:
        if not each.c_isselect:
            all_selected = False
            break
    data["all_selected"] = all_selected
    sum_tuple = get_count_price(user)
    sum_count = sum_tuple[0]
    sum_price = sum_tuple[1]
    data["sum_count"] = sum_count
    data["sum_price"] = sum_price
    data["code"] = 200
    return JsonResponse(data)


# 全选按钮处理
def all_select(request):
    user_id = request.session.get("use_id")
    user = UserModel.objects.get(pk=user_id)
    all_selected = request.GET.get("all_select")
    if not all_selected:
        all_selected = request.GET.get("not_select_array")
    # 选中的,将要改变状态的列表
    select_list = all_selected.split("#")
    for select in select_list:
        the_cart = Cart.objects.get(c_goods_id=select, c_user_id=user_id)
        the_cart.c_isselect = not the_cart.c_isselect
        the_cart.save()
    sum_tuple = get_count_price(user)
    sum_count = sum_tuple[0]
    sum_price = sum_tuple[1]
    data = {
        "code": 200,
        "sum_count": sum_count,
        "sum_price": sum_price,
    }
    return JsonResponse(data)


# 定义一个获取数量和价格的函数
def get_count_price(user):
    carts = Cart.objects.filter(c_user=user).filter(c_isselect=True)
    sum_count = 0
    sum_price = 0
    for each in carts:
        sum_count += each.c_num
        sum_price += each.c_goods.price * each.c_num
    sum_tuple = (sum_count, sum_price)
    return sum_tuple


def receiver(request):
    user_id = request.session.get("use_id")
    user = UserModel.objects.get(pk=user_id)
    u_name = request.GET.get("u_name")
    call_phone = request.GET.get("call_phone")
    address = request.GET.get("address")
    the_receiver = Receiver.objects.filter(r_user=user)
    if the_receiver:
        the_receiver = the_receiver.first()
        # the_receiver = Receiver()
        the_receiver.r_name = u_name
        the_receiver.r_call_phone = call_phone
        the_receiver.r_address = address
        the_receiver.save()
    else:
        Receiver.objects.create(r_name=u_name, r_call_phone=call_phone, r_address=address, r_user=user)
    return JsonResponse({"code": 200})


# 生成订单
def create_order(request):
    user_id = request.session.get("use_id")
    user = UserModel.objects.get(pk=user_id)
    # 筛选出该用户所有购物车记录
    carts = Cart.objects.filter(c_user=user).filter(c_isselect=True)
    order_number = uuid.uuid4()
    # 生成此次的订单
    order = Order.objects.create(o_num=order_number, o_user=user, o_status=1)
    # 为每条购物车记录生成与订单关联的关系表数据
    for each_cart in carts:
        OrderAndGoods.objects.create(og_goods=each_cart.c_goods, og_count=each_cart.c_num, og_num=order.o_num)
    order_and_goods = OrderAndGoods.objects.all().filter(og_num=order.o_num)
    data = {
        "order_and_goods": order_and_goods,
        "order_number": order_number,
    }
    return render(request, "cart/order.html", data)


def submit_order(request):
    user_id = request.session.get("use_id")
    user = UserModel.objects.get(pk=user_id)
    order_number = request.GET.get("order_number")
    order = Order.objects.get(o_num=order_number, o_user=user)
    order.o_status = 2
    order.save()
    orders = Order.objects.all()
    wait_pay = orders.filter(o_status=1).count()
    wait_receiver = orders.filter(o_status=2).count()
    wait_calk = orders.filter(o_status=3).count()
    wait_after = orders.filter(o_status=4).count()
    data = {
        "wait_pay": wait_pay,
        "wait_receiver": wait_receiver,
        "wait_calk": wait_calk,
        "wait_after": wait_after,
    }
    print(data)
    return render(request, "mine/mine.html", data)







