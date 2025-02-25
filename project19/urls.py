"""
URL configuration for project19 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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


from django.shortcuts import redirect

from django.contrib import admin
from django.urls import include, path
from home import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
admin.site.site_header = "clothify Admin"
admin.site.site_title = "clothify Admin Portal"
admin.site.index_title = "Welcome to clothify Researcher Portal"
#from django.views.generic import RedirectView
urlpatterns = [
    #path('', RedirectView.as_view(url='/home/', permanent=True)),
    
    path("admin/", admin.site.urls),
    path('', lambda request: redirect('home'), name='root'),
    path('', include("home.urls")),
    path('contact/', views.contact, name='contact'),
    path('faqs/', views.faqs, name='faqs'),
    path('register/',views.register_page,name='register_page'),
    path('',include("django.contrib.auth.urls")),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if settings.DEBUG:
#     urlpatterns +=static(settings.MEDIA_URL,
#                     document_root = settings.MEDIA_ROOT)

# urlpatterns += staticfiles_urlpatterns()

