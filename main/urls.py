from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("",index,name="index"),
    path("about/",about,name='about'),
    path("contact/",contact,name='contact'),
    path("menu/",menu,name='menu'),
    path("services/",services,name='services'),
    path("Register/",Register,name="Register"),
    path("login/",log_in,name="login"),
    path('logout/',log_out,name="logout"),
    path('change_password/',change_password,name="change_password"),
    path('add-to-cart/<int:food_id>/', add_to_cart, name='add_to_cart'),
    path('cart/count/', get_cart_count, name='get_cart_count'),
    path('food_details/<int:id>/',food_details,name='food_details'),
    
     
    #  change_password 
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # cart_system
    path('cart/', cart_view, name='cart'),  # View the cart
    path('cart/update/<int:cart_item_id>/', update_cart, name='update_cart'),  # Update cart item quantity
    path('cart/remove/<int:cart_item_id>/', remove_from_cart, name='remove_from_cart'),  # Remove item from cart
    path('rate-food/<int:food_id>/', rate_food, name='rate_food'),  # Rate a food item
    path('cart/proceed-to-payment/', proceed_to_payment, name='proceed_to_payment'),  # Proceed to payment
]

