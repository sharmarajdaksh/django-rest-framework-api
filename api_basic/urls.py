from django.urls import path, include
from .views import ArticleAPIView, ArticleDetails, GenericAPIView, ArticleViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('article', ArticleViewSet, basename='article')  # Bind route to viewset

urlpatterns = [
    # path('article/', article_list),
    path('article/', ArticleAPIView.as_view()),
    # path('detail/<int:pk>/', article_detail)
    path('detail/<int:id>/', ArticleDetails.as_view()),

    #
    # Same functionality using generics
    #
    path('generic/article/', GenericAPIView.as_view()),
    path('generic/article/<int:id>/', GenericAPIView.as_view()),

    #
    # Same functionality using viewsets
    #
    path('viewset/', include(router.urls)),
    path('viewset/<int:pk>', include(router.urls)),
]
