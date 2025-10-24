from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from tasks.views import TaskViewSet, health_check
from django.http import HttpResponse

router = routers.DefaultRouter()
router.register(r"tasks", TaskViewSet)


def root_ok(request):
    return HttpResponse("OK", content_type="text/plain")


urlpatterns = [
    path("", root_ok),
    path("", include("django_prometheus.urls")),
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("health", health_check),
]
