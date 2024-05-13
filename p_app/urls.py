from django.urls import path
from . import views
from .views import *
from .views import forgot_password, reset_password
urlpatterns = [

    path('admin_view',views.admin_view,name='admin_view'),
    path('admin_add',views.admin_lense_add,name='admin_add'),
    path('admin_update/<int:pk>/',views.update_lens,name='admin_update'),
    path('admin_delete/<int:pk>/',views.admin_lense_delete,name='admin_delete'),
    path('register',register,name='register'),
    path('login',userLogin,name='login'),
    path('',home_page,name='homepage'),
    path('logout/', user_logout, name='logout'),
    path('allproducts',allProducts,name='allProducts'),
    path('view-product/<int:id>',view_product),
    path('add-to-cart/<int:id>',views.addtocart),

    path('remove_from_wishlist/<int:product_id>/', views.remove_from_wishlist,name='remove_from_wishlist'),
    path('add_to_wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/', views.wishlist, name='wishlist'),

    path('search/', views.searchresult, name='search'),

    path('my-cart',views.mycart, name='my-cart'),

    path('managecart/<int:id>/',views.managecart,name="managecart"),

    path("empty-cart/",views.emptycart),

    path("checkout",views.checkout),
    path('my-orders',my_orders,name='my-orders'),
    path('display_orders', views.display_orders, name='display_orders'),
    path('update-order-status/<int:order_id>/', views.update_order_status, name='update_order_status'),
    path('download-invoice/<int:order_id>/', views.generate_pdf, name='download_invoice'),
    path('forgot_password/', forgot_password, name='forgot_password'),
    path('reset_password/<str:uidb64>/<str:token>/', reset_password, name='reset_password'),
    path('low_quantity/', views.low_quantity_products, name='low_quantity_products'),
 
]
