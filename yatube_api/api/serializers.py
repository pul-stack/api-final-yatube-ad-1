from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from posts.models import Comment, Follow, Group, Post

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'author', 'text', 'pub_date', 'image', 'group')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        model = Comment
        fields = ('id', 'author', 'text', 'created', 'post')
        read_only_fields = ('post',)


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description')


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
    )

    class Meta:
        model = Follow
        fields = ('user', 'following')

    def validate(self, attrs):
        request = self.context.get('request')
        user = getattr(request, 'user', None)
        following = attrs.get('following')
        if user == following:
            raise serializers.ValidationError(
                {'following': ['Нельзя подписаться на самого себя!']}
            )
        if Follow.objects.filter(user=user, following=following).exists():
            raise serializers.ValidationError(
                {'following': ['Вы уже подписаны на этого автора.']}
            )
        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        return Follow.objects.create(user=user, **validated_data)
