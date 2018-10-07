from django.db import models


# 构建父模型
class Home(models.Model):
    img = models.CharField(max_length=200)
    name = models.CharField(max_length=50)
    trackid = models.CharField(max_length=50)

    # 取消继承的副作用
    class Meta:
        abstract = True


# 构建顶部轮播图模型
class Wheel(Home):
    class Meta:
        db_table = 'axf_wheel'


# 构建顶部导航模型
class Nav(Home):
    class Meta:
        db_table = "axf_nav"


# 设计必买数据模型
class MustBuy(Home):
    class Meta:
        db_table = "axf_mustbuy"


# 设计shop商店数据模型
class ShopModel(Home):
    class Meta:
        db_table = "axf_shop"


# 建立商品小样展示数据模型
class MainShow(models.Model):
    # 数据的图片地址
    img = models.CharField(max_length=200)
    # 图片的描述名
    name = models.CharField(max_length=100)
    trackid = models.CharField(max_length=50)
    categoryid = models.CharField(max_length=50)
    brandname = models.CharField(max_length=50)

    img1 = models.CharField(max_length=200)
    childcid1 = models.CharField(max_length=50)
    productid1 = models.CharField(max_length=50)
    longname1 = models.CharField(max_length=200)
    price1 = models.CharField(max_length=50)
    marketprice1 = models.CharField(max_length=50)

    img2 = models.CharField(max_length=200)
    childcid2 = models.CharField(max_length=50)
    productid2 = models.CharField(max_length=50)
    longname2 = models.CharField(max_length=200)
    price2 = models.CharField(max_length=50)
    marketprice2 = models.CharField(max_length=50)

    img3 = models.CharField(max_length=200)
    childcid3 = models.CharField(max_length=50)
    productid3 = models.CharField(max_length=50)
    longname3 = models.CharField(max_length=200)
    price3 = models.CharField(max_length=50)
    marketprice3 = models.CharField(max_length=50)

    class Meta:
        db_table = "axf_mainshow"


class FoodType(models.Model):
    typeid = models.CharField(max_length=20)
    typename = models.CharField(max_length=20)
    childtypenames = models.CharField(max_length=200)
    typesort = models.CharField(max_length=20)

    class Meta:
        db_table = "axf_foodtypes"


class Goods(models.Model):
    productid = models.CharField(max_length=100)
    productimg = models.CharField(max_length=200)
    productname = models.CharField(max_length=50)
    productlongname = models.CharField(max_length=200)
    isxf = models.BooleanField(default=0)
    pmdesc = models.IntegerField(default=0)
    specifics = models.CharField(max_length=50)
    price = models.FloatField(default=0)
    marketprice = models.FloatField(default=0)
    categoryid = models.CharField(max_length=50)
    childcid = models.CharField(max_length=50)
    childcidname = models.CharField(max_length=100)
    dealerid = models.CharField(max_length=50)
    storenums = models.IntegerField(default=0)
    productnum = models.IntegerField(default=0)

    class Meta:
        db_table = "axf_goods"


class UserModel(models.Model):
    # id,  用户名  32位  唯一, 密码  256位  md5加密  不能为空,邮箱  64位  唯一,手机号, 性别..., 头像 图片  imageField
    u_name = models.CharField(max_length=32, unique=True)
    u_passwd = models.CharField(max_length=32, null=False)
    u_mail = models.CharField(max_length=64, unique=True)
    # ....
    u_sex = models.BooleanField(default=1)
    # 头像
    u_img = models.ImageField(upload_to="img")

    class Meta:
        db_table = "axf_user"


class Cart(models.Model):
    c_goods = models.ForeignKey(Goods)
    c_num = models.IntegerField(default=1)
    c_isselect = models.BooleanField(default=1)
    c_user = models.ForeignKey(UserModel)

    class Meta:
        db_table = "axf_cart"


class Receiver(models.Model):
    id = models.AutoField(primary_key=True)
    r_name = models.CharField(max_length=50)
    r_call_phone = models.CharField(max_length=50)
    r_address = models.CharField(max_length=200)
    r_user = models.ForeignKey(UserModel)

    class Meta:
        db_table = "axf_receiver"


# 订单所需字段
# 1.用户
# 2.商品 --- 因为可能一个订单存在多个商品所以商品不在此表
# 3.订单编号 --- 用于确认订单的唯一性
# 4.订单创建时间
# 5.订单的状态  0.无效 1.待付款 2.待收货 3.待评价 4.售后/退款
class Order(models.Model):
    o_user = models.ForeignKey(UserModel)
    o_num = models.CharField(max_length=128)
    o_time = models.DateTimeField(auto_now=True)
    o_status = models.IntegerField(default=0)

    class Meta:
        db_table = "axf_order"


class OrderAndGoods(models.Model):
    og_goods = models.ForeignKey(Goods)
    og_count = models.IntegerField(default=1)
    # 订单的编号
    og_num = models.CharField(max_length=128)

    class Meta:
        db_table = "axf_order_goods"









































