# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url, include
import realtime_ticket.views as views


urlpatterns = patterns('',
                       url(r'^ticket/$', views.RealtimeTicketView.as_view(),
                           name="realtime_ticket"),
                       )
