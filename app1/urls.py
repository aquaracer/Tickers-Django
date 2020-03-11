from django.conf.urls import url
import app1.views

urlpatterns = [
    url(r'^$', app1.views.index, name='index'),
    url(r'^%([a-zA-Z]{3,4})%/$', app1.views.get_tickers_list),
    url(r'^%([a-zA-Z]{3,4})%/insider$', app1.views.get_insiders_list),
    url(r"^%([a-zA-Z]{3,4})%/insider/%([a-zA-Z_'+]{2,35})%/$", app1.views.get_insider_trades),
    url(r'^%([a-zA-Z]{3,4})%/analytic[a-zA-Z0-9/&=?+]/$', app1.views.get_analysis),
    url(r'^%([a-zA-Z]{3,4})%/delt[a-zA-Z0-9()/&=?+]/$', app1.views.delta_func)
]
