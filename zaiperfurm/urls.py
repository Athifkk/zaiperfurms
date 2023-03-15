from django.urls import path
from .views import *
urlpatterns=[
    path("registration/",shopreg),
    path('',index),
    path('shoplogin/',shoplogin),
    path('shopprofile/',shopprofile),
    path('shopupload/',shopupload),
    path('viewproduct/',viewproduct),
    path('editprofile/<int:id>',shopregedit),
    path('productdelete/<int:id>',deleteproduct),
    path('productedit/<int:id>',editproduct),

    # --------------user--------------
    path("userlogin/",userlogin),
    path("userregister/",userregis),
    path("verify/<auth_token>",verify),
    path("userprofile/",userprofile),

    # -------------addto cart-------
    path('addcart/<int:id>', addcartview),
    path('cart/', cartdisplay),
    # path('cartremove/<int:id>', cartremove),

    path('buyproduct/<int:id>',buyproduct),
    path('END/',end),

]