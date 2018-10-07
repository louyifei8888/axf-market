from django.conf.urls import url
from django.contrib import admin
from app01 import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^home/', views.home, name='home'),
    url(r'^market/(\d+)/(\d+)/(\d+)', views.market, name='market'),
    url(r'^add_cart/', views.add_cart, name='add_cart'),
    url(r'^sub_cart/', views.sub_cart, name='sub_cart'),
    url(r'^cart/', views.cart, name='cart'),
    url(r'^mine/', views.mine, name='mine'),
    url(r'^register/', views.register, name='register'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^login/', views.login, name='login'),
    url(r'^register_check/', views.register_check, name='register_check'),
    url(r'^pcgetcaptcha/', views.pcgetcaptcha, name='pcgetcaptcha'),
    url(r'^add_cart_num/', views.add_cart_num, name='add_cart_num'),
    url(r'^sub_cart_num/', views.sub_cart_num, name='sub_cart_num'),
    url(r'^change_select/', views.change_select, name='change_select'),
    url(r'^all_select/', views.all_select, name='all_select'),
    url(r'^receiver/', views.receiver, name='receiver'),
    url(r'^create_order/', views.create_order, name='create_order'),
    url(r'^submit_order/', views.submit_order, name='submit_order'),
]
