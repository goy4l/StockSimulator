
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
    path('news', views.News, name='news'),
    path('lauth', views.Lauth , name='lauth'),
    path('news/<newsid>/',views.News_v, name='news_v'),  
    path('transact',views.equity_transactions, name='transact'),  
    path('transfer',views.transfers, name='transfers'),  
    path('transfer/requests',views.trequests, name='trequests'),  
    path('transfer/requests/delete/<stockid>/',views.trd, name='trd'),  
    path('transfer/requests/decline/<stockid>/',views.trr, name='trr'),  
    path('transfer/requests/accept/<stockid>/',views.tra, name='tra'),  

    

]
