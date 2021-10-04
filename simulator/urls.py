
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('activate/<uidb64>/<token>/',views.activate, name='activate'),
    path('transactions', views.thistory, name='thistory'),
    path('portfolio', views.portfolio, name='portfolio'),
    path('orderbook', views.orderbook, name='orderbook'),
    path('pnl', views.pnl, name='pnl'),
]
