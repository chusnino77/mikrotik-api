from django.urls import path
from . import views

urlpatterns = [
    path('', views.loginRequest, name='login_mikrotik'),
    path('logout', views.logoutRequest, name='logout_mikrotik'),
    path('test', views.test, name='test_mikrotik'),
    path('dashboard', views.dashboard, name='dashboard_mikrotik'),
    path('router-create', views.routerCreate, name='routerCreate_mikrotik'),
    path('router-update/<pk>', views.routerUpdate, name='routerUpdate_mikrotik'),
    path('router-delete/<pk>', views.routerDelete, name='routerDelete_mikrotik'),
    path('test-conn', views.testConnection, name='testConn_mikrotik'),
    path('home-mikrotik/<pk>', views.homePage, name='homePage_mikrotik'),
    path('client-list', views.clientList, name='clientList_mikrotik'),
    path('client-create', views.clientCreate, name='clientCreate_mikrotik'),
    path('client-delete/<pk>', views.clientDelete, name='clientDelete_mikrotik'),
    path('client-update/<pk>', views.clientUpdate, name='clientUpdate_mikrotik'),
    path('client-enable/<pk>', views.clientEnable, name='clientEnable_mikrotik'),
    path('client-remote', views.clientRemote, name='clientRemote_mikrotik'),
    path('client-ping/<pk>', views.clientPing, name='clientPing_mikrotik'),
    path('antena-list', views.antenaList, name='antenaList_mikrotik'),
]