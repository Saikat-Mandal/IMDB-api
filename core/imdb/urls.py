from django.urls import path , include
from rest_framework.schemas import get_schema_view

from . import views
from .views import api_root 

from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns

# router = DefaultRouter()

# router.register(r'stream', views.StreamPlatformViewSet, basename='streamplatform')

urlpatterns = [
    # path('reviews/' , views.reviewListView.as_view() , name="Review-list"),
    # path('reviews/<int:pk>', views.reviewListViewDetail.as_view(), name="Review-detail"),
    path('list/' , views.movie_list.as_view() , name="Watchlist-list"),
    path('list/<int:pk>/review' , views.reviewListView.as_view() , name="Review-list"),
    path('list/<int:pk>/review-create/' , views.reviewCreate.as_view() , name='Review-create' ),
    path('list/review/<int:pk>/' , views.reviewDetail.as_view() , name='Review-detail'),
    path('list/<int:pk>', views.movie_detail.as_view(), name="Watchlist-detail"),
    path('stream/', views.stream_list.as_view() , name="StreamPlatform-platform"),
    path('stream/<int:pk>', views.stream_detail.as_view() , name="StreamPlatform-detail"),
    path('', views.api_root),

        # ...
        # Use the `get_schema_view()` helper to add a `SchemaView` to project URLs.
        #   * `title` and `description` parameters are passed to `SchemaGenerator`.
        #   * Provide view name for use with `reverse()`.
        path('openapi', get_schema_view(
            title="imdb",
            description="API for all things …",
            version="1.0.0"
        ), name='openapi-schema'),
        # ...

    # path('', include(router.urls)),
]
