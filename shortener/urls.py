from django.urls import path

from . import views

app_name = "shortener"

urlpatterns = [
    path("api/shorturls/", views.URLMapView.as_view(), name="create"),
    path("api/shorturls/<str:hash>/", views.URLMapView.as_view(), name="details"),
    path("<str:hash>/", views.RedirectToURLView.as_view(), name="redirect"),
]
