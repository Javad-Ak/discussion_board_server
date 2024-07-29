from rest_framework.routers import DefaultRouter
from django.urls import include, path
from . import views

app_name = 'discussions'

router = DefaultRouter()
router.register('topics', views.TopicViewSet, 'discussions')

urlpatterns = [
    path('', include(router.urls)),
    path('topics/<int:pk>/comments/', views.CommentListCreateView.as_view(), name='comments'),
    path('comment/<int:topic_pk>/', views.CommentRetrieveUpdateDestroyView.as_view(), name='comment'),
]
