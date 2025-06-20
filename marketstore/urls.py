from django.urls import path
from . import views

urlpatterns = [

    path("homepage/", views.homepage_view, name="homepage"),
    path("item/list/", views.item_list_view, name="item_list"),
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("item/<int:pk>/", views.item_detail_view, name="item_detail"),
    path("item/<int:pk>/contact/", views.contact_seller_view, name="contact_seller"),
    path("item/<int:pk>/purchase/", views.purchase_item_view, name="purchase_item"),
    path("sell/", views.create_item_view, name="create_item"),
    path("dashboard/seller/", views.seller_dashboard_view, name="seller_dashboard"),
    path("messages/seller/", views.seller_messages_view, name="seller_messages"),
    path("purchases/", views.buyer_purchases_view, name="buyer_purchases"),
    path("about/", views.about_view, name="about"),
    path("contact/", views.contact_view, name="contact"),
]