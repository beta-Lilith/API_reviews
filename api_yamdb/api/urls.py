from django.urls import include, path
from rest_framework.routers import SimpleRouter
from rest_framework import routers

from .views import CommentViewSet,  ReviewViewSet

# from .views import(
#     NameViewSet
# )
router = SimpleRouter()
app_name = 'api'
router_v1 = routers.DefaultRouter()

# router_v1.register(r'', ..., basename='titles')
# router_v1.register(r'', ..., basename='categories')
# router_v1.register(r'', ..., basename='genres')
router.register(
    'titles/(?P<title_id>\\d+)/reviews',
    ReviewViewSet,
    basename="reviews",
)
router.register(
    'titles/(?P<title_id>\\d+)/reviews/(?P<review_id>\\d+)/comments',
    CommentViewSet,
    basename="comments",
)

# users ???
# auth ???

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
