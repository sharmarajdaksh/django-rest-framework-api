from django.http import HttpResponse
from rest_framework import status, generics, mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from django.shortcuts import get_object_or_404

from .models import Article
from .serializers import ArticleSerializer


#
# MODAL VIEWSET-BASED VIEWS IMPLEMENTATION
#

class ArticleViewSet(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()


#
# GENERIC VIEWSET-BASED VIEWS IMPLEMENTATION
#

class GenericArticleViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()


#
# VIEWSET-BASED VIEWS IMPLEMENTATION
#

class NonGenericArticleViewSet(viewsets.ViewSet):

    @staticmethod
    def list(request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    @staticmethod
    def create(request):
        serializer = ArticleSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def retrieve(request, pk=None):
        queryset = Article.objects.all()
        article = get_object_or_404(queryset, pk=pk)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    @staticmethod
    def update(request, pk=None):
        article = Article.objects.get(pk=pk)
        serializer = ArticleSerializer(article, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#
# GENERICS-BASED VIEWS IMPLEMENTATION
#

class GenericAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin,
                     mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    lookup_field = 'id'
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id=None):
        if id:
            return self.retrieve(id)
        else:
            return self.list(request)

    def post(self, request):
        return self.create(request)

    def put(self, request, id=None):
        return self.update(request, id)

    def delete(self, request, id):
        return self.destroy(request, id)


#
# CLASS-BASED VIEWS IMPLEMENTATION
#

class ArticleAPIView(APIView):

    @staticmethod
    def get(request):
        # GET all articles
        articles = Article.objects.all()

        # Serialize the articles queryset
        # many=True is required for querysets
        serializer = ArticleSerializer(articles, many=True)

        return Response(serializer.data)

    @staticmethod
    def post(request):
        serializer = ArticleSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleDetails(APIView):

    @staticmethod
    def get_object(id):
        try:
            return Article.objects.get(id=id)
        except Article.DoesNotExist:
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, id):
        serializer = ArticleSerializer(self.get_object(id))
        return Response(serializer.data)

    def put(self, request, id):
        # Update single article
        serializer = ArticleSerializer(self.get_object(id), data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        self.get_object(id).delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


#
# FUNCTION-BASED VIEWS IMPLEMENTATION
#

@api_view(['GET', 'POST'])
def article_list(request):
    if request.method == 'GET':
        # GET all articles
        articles = Article.objects.all()

        # Serialize the articles queryset
        # many=True is required for querysets
        serializer = ArticleSerializer(articles, many=True)

        return Response(serializer.data)

    elif request.method == 'POST':
        # Add a new Article
        # data = JSONParser().parse(request)
        serializer = ArticleSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def article_detail(request, pk):
    try:
        article = Article.objects.get(pk=pk)

    except Article.DoesNotExist:
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        # Get single article
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    elif request.method == 'PUT':
        # Update single article
        serializer = ArticleSerializer(article, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # Delete single article
        article.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
