from django.urls import path
from rest_framework import routers

from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, token_blacklist

app_name = 'accounts'

router = routers.DefaultRouter()
router.register('users', views.UserViewSet, 'users')

urlpatterns = [
                  # Run 'python manage.py flushexpiredtokens' on a daily basis.
                  path('login/', TokenObtainPairView.as_view(), name='login'),
                  path('login/refresh/', TokenRefreshView.as_view(), name='refresh_token'),
                  path('logout/', token_blacklist, name='logout'),
              ] + router.urls
