from rest_framework.routers import DefaultRouter
from django.urls import path
from . import views

app_name = 'discussions'

router = DefaultRouter()
router.register('topics', views.TopicViewSet, 'topics')

urlpatterns = router.urls + [
    path('topics/<int:topic_id>/comments/',
         views.CommentListCreateView.as_view(), name='comments_list'),
    path('topics/<int:topic_id>/comments/<int:pk>/',
         views.CommentRetrieveUpdateDestroyView.as_view(), name='comments_detail'),
    path('search/<str:query>/', views.SearchView.as_view(), name='search'),
]
