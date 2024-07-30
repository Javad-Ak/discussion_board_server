from django.urls import path
from rest_framework import routers

from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, token_blacklist

app_name = 'accounts'

router = routers.DefaultRouter()
router.register('users', views.UserViewSet, 'users')

urlpatterns = [
                  # flush expired tokens on a daily basis.
                  path('signup/', views.SignupView.as_view(), name='signup'),
                  path('login/', TokenObtainPairView.as_view(), name='login'),
                  path('login/refresh/', TokenRefreshView.as_view(), name='refresh_token'),
                  path('logout/', token_blacklist, name='logout'),
                  path('account-recovery/', views.AccountRecoveryView.as_view(), name='recovery'),
              ] + router.urls
