# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url, include
from django.conf import settings
from rest_framework_bulk.routes import BulkRouter
from rest_framework_nested import routers as nested_routers

from . import views


# Register /sites as a top-level resource
router = BulkRouter(trailing_slash=settings.APPEND_SLASH)
router.register(r'sites', views.SiteViewSet)

# Nested router for resources under /sites
sites_router = nested_routers.NestedSimpleRouter(
    router, r'sites', lookup='site', trailing_slash=settings.APPEND_SLASH
)

# Map nested router to bulk put/patch operations
sites_router.routes[0].mapping.update({
    'put': 'bulk_update',
    'patch': 'partial_bulk_update',
    'delete': 'bulk_destroy',
})

# Resources that are nested under /sites
sites_router.register(r'attributes', views.AttributeViewSet)
sites_router.register(r'changes', views.ChangeViewSet)
sites_router.register(r'devices', views.DeviceViewSet)
sites_router.register(r'interfaces', views.InterfaceViewSet)
sites_router.register(r'networks', views.NetworkViewSet)
sites_router.register(r'values', views.ValueViewSet)

# Resources pinned to API index at /
router.register(r'attributes', views.AttributeViewSet)
router.register(r'changes', views.ChangeViewSet)
router.register(r'devices', views.DeviceViewSet)
router.register(r'interfaces', views.InterfaceViewSet)
router.register(r'networks', views.NetworkViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'values', views.ValueViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    # API routes
    url(r'^', include(router.urls)),
    url(r'^', include(sites_router.urls)),

    # Browsable API auth login
    url(r'^api-auth/', include('rest_framework.urls',
        namespace='rest_framework')),

    # API auth_token login/verify (email/secret_key)
    url(r'^authenticate/', views.AuthTokenLoginView.as_view(),
        name='authenticate'),
    url(r'^verify_token/', views.AuthTokenVerifyView.as_view(),
        name='verify_token'),
]
