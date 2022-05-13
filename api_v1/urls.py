from django.urls import include, path
from rest_framework import routers
from api_v1 import views
from rest_framework.authtoken.views import obtain_auth_token


router = routers.DefaultRouter()
router.register(r'chemicals', views.ChemicalViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path(
        'api-auth/',
        include('rest_framework.urls', namespace='rest_framework')
    ),
    # path('chemical/', views.ChemicalDetail.as_view(), name='chemical')
]