from django.urls import include, path

from rest_framework import routers

from .views import(
    # NameViewSet
)

app_name = 'api'
router_v1 = routers.DefaultRouter()

# router_v1.register(r'', ..., basename='titles')
# router_v1.register(r'', ..., basename='categories')
# router_v1.register(r'', ..., basename='genres')
# router_v1.register(r'', ..., basename='reviews')
# router_v1.register(r'', ..., basename='comments')

# users ???
# auth ???

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
