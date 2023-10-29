from django.urls import include, re_path

from ncaacards import views
from ncaacards.feeds import RecentCardTradesFeed, RecentStockTradesFeed

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = [
    re_path(r'^api/', include('ncaacards.api.urls')),
    re_path(r'^$', views.home),
    re_path(r'^game/([0-9]+)/$', views.game_home),
    re_path(r'^game/([0-9]+)/rss/cards/$', RecentCardTradesFeed()),
    re_path(r'^game/([0-9]+)/rss/stocks/$', RecentStockTradesFeed()),
    re_path(r'^game/([0-9]+)/scoring_settings/$', views.scoring_settings),
    re_path(r'^game/([0-9]+)/save_settings/$', views.save_settings),
    re_path(r'^game/([0-9]+)/lock_settings/$', views.lock_settings),
    re_path(r'^game/([0-9]+)/marketplace/$', views.marketplace),
    re_path(r'^game/([0-9]+)/team_list/$', views.team_list),
    re_path(r'^game/([0-9]+)/market_maker/$', views.market_maker),
    re_path(r'^game/([0-9]+)/make_market/$', views.do_make_market),
    re_path(r'^game/([0-9]+)/leaderboard/$', views.leaderboard),
    re_path(r'^game/([0-9]+)/entry/([0-9]+)/$', views.entry_view),
    re_path(r'^game/([0-9]+)/team/([0-9]+)/$', views.game_team_view),
    re_path(r'^game/([0-9]+)/team/([a-zA-Z]+)/$', views.game_team_view),
    re_path(r'^game/([0-9]+)/create_offer/$', views.create_offer),
    re_path(r'^game/([0-9]+)/make_offer/$', views.make_offer),
    re_path(r'^game/([0-9]+)/place_order/$', views.do_place_order),
    re_path(r'^game/([0-9]+)/cancel_order/$', views.cancel_order),
    re_path(r'^game/([0-9]+)/change_order/$', views.change_order),
    re_path(r'^game/([0-9]+)/offer/([0-9]+)/$', views.offer_view),
    re_path(r'^game/([0-9]+)/offer/([0-9]+)/accept/$', views.accept_offer),
    re_path(r'^game/([0-9]+)/offer/([0-9]+)/cancel/$', views.cancel_offer),
    re_path(r'^create_game/$', views.create_game),
    re_path(r'^game_list/$', views.game_list),
    re_path(r'^do_create_game/$', views.do_create_game),
    re_path(r'^join_game/$', views.join_game),
]
