"""Effort URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.i18n import JavaScriptCatalog
from lists import urls as listsUrls
from django.conf import settings

js_info_dict = {
    'packages': ('recurrence', ),
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('lists/', include('lists.urls')),
    path('notes/', include('notes.urls')),
    path('accounts/', include('allauth.urls')),
    path('accounts/', include("allauth_ui.urls")),
    path('markdownx/', include('markdownx.urls'))
]

urlpatterns += [
    re_path(r'^jsi18n/$', JavaScriptCatalog.as_view(), js_info_dict),
]
urlpatterns += [
    path('jsi18n.js', JavaScriptCatalog.as_view(packages=['recurrence']), name='jsi18n'),
]

if settings.DEBUG:
    urlpatterns = [
        re_path(r'^herald/', include('herald.urls')),
] + urlpatterns