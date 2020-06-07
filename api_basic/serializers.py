from rest_framework import serializers
from .models import Article


# Generally, you would use the Serializer for CUSTOM implementations
# For using created Models without modifications, the ModelSerializer is a better option
# class ArticleSerializer(serializers.Serializer):
#     # A class to Serialize our Article model to and from JSON
#     title = serializers.CharField(max_length=100)
#     author = serializers.CharField(max_length=100)
#     email = serializers.EmailField(max_length=50)
#     date = serializers.DateTimeField()
#
#     def create(self, validated_data):
#         # Create new Article based on input validated_data
#         return Article.objects.create(validated_data)
#
#     def update(self, instance, validated_data):
#         # Update an existing Article
#         instance.title = validated_data.get('title', instance.title)
#         instance.author = validated_data.get('author', instance.author)
#         instance.email = validated_data.get('email', instance.email)
#         instance.date = validated_data.get('date', instance.date)
#         instance.save()

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        # fields = ['id', 'title', 'author']
        fields = '__all__'
