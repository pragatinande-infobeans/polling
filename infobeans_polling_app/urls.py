from django.urls import path
from . import views
from infobeans_polling_app import views

# SET THE NAMESPACE!
app_name = 'infobeans_polling_app'

# Be careful setting the name to just /login use userlogin instead!
urlpatterns=[
    # path('user_register/',views.user_register,name='user_register'),
    path('user_register/', views.user_register, name='user_register'),
    path('user_login/', views.user_login, name='user_login'),
    path('user_logout/', views.user_logout, name='user_logout'),
    path('create/', views.create, name='create'),

]
