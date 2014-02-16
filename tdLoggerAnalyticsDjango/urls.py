from django.conf.urls import patterns, include, url

from django.contrib import admin
from messages import views

admin.autodiscover()

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'messages_old', views.MessageViewSet)


urlpatterns = patterns('',

    url(r'^$', views.message_log, name='message_gallery'),

    url(r'^api/', include(router.urls)),
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
    #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/messages/$', 'messages.views.messages', name='messages'),

    url(r'^admin/', include(admin.site.urls)),
)
