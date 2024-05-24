from django.urls import path
from .import views

urlpatterns=[
    path('funchat/',views.Myview,name="index"),
    path('chatroom/<str:receiver>/',views.chatroom,name="chat_room"),
    path('signup/',views.signup,name='signup'),
    path('signin/',views.signin,name='signin'),
    path("logout/",views.logout_view,name='logout')

    # path('unread_msg/',views.unread_message,name='unread_msg')
]
