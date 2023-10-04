from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", include("core.urls", namespace="core"))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
