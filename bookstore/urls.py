from django.urls import path
from . import views    

from django.contrib.auth import views as authViews

urlpatterns = [
    path('' ,views.home , name="home"),
    path('books/' ,views.books , name="books"),
    path('books/<str:pk>' ,views.books_detail , name="book_detail"),

  # path('customer/' ,views.customer),
    path('customer/<str:pk>' ,views.customer, name="customer"),
  #  path('create/' ,views.create, name="create"),
    path('create/<str:pk>' ,views.create, name="create"),
    path('update/<str:pk>' ,views.update, name="update"),
    path('delete/<str:pk>' ,views.delete, name="delete"),
    path('register/' ,views.register, name="register"),
    path('login/' ,views.userLogin, name="login"),
    path('logout/' ,views.userLogout, name="logout"),
    path('user/' ,views.userProfile, name="user_profile"),
    path('profile/' ,views.profileInfo, name="profile_info"),
    path('payment/', views.payment, name="payment"),

    path('add_to_cart', views.add_to_cart, name='add_to_cart'),
    path('cart', views.cart, name='cart'),
    path('<int:orderdetails_id>',views.remove_from_cart, name='remove_from_cart'),
    path('add_qty/<int:orderdetails_id>', views.add_qty, name='add_qty'),
    path('sub_qty/<int:orderdetails_id>', views.sub_qty, name='sub_qty'),

     path('reset_password/' ,authViews.PasswordResetView.as_view(template_name= "bookstore/password_reset.html") , name="reset_password"),
     path('reset_password_sent/' ,authViews.PasswordResetDoneView.as_view(template_name= "bookstore/password_reset_sent.html") , name="password_reset_done"),
     path('reset/<uidb64>/<token>/' ,authViews.PasswordResetConfirmView.as_view(template_name= "bookstore/password_reset_form.html") , name="password_reset_confirm"),
     path('reset_password_complete/' ,authViews.PasswordResetCompleteView.as_view(template_name= "bookstore/password_reset_done.html") , name="password_reset_complete"),

]