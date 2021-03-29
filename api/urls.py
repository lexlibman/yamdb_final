from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitlesViewSet, UserViewSet,
                    send_confirm_code, send_token)

v1_router = DefaultRouter()
v1_router.register('users', UserViewSet, basename='user_detail')
v1_router.register('titles', TitlesViewSet, basename='Title')
v1_router.register('genres', GenreViewSet, basename='Genre')
v1_router.register('categories', CategoryViewSet, basename='Category')
v1_router.register(
    r'titles/(?P<title_id>[0-9]+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
v1_router.register(
    r'titles/(?P<title_id>[0-9]+)/reviews/(?P<review_id>[0-9]+)/comments',
    CommentViewSet,
    basename='comments'
)

auth_patterns = [
    path('token/', send_token, name='get_token'),
    path('email/', send_confirm_code, name='send_confirm_code'),
]

urlpatterns = [
    path('v1/auth/', include(auth_patterns)),
    path('v1/', include(v1_router.urls)),
]
