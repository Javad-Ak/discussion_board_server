from rest_framework.routers import DefaultRouter
from django.urls import path
from . import views

app_name = 'discussions'

router = DefaultRouter()
router.register('topics', views.TopicViewSet, 'discussions')

urlpatterns = [
                  path('topics/<int:pk>/comments/', views.CommentListCreateView.as_view(), name='comments'),
                  path('comment/<int:topic_id>/', views.CommentRetrieveUpdateDestroyView.as_view(), name='comment'),
              ] + router.urls
