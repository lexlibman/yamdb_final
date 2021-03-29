from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from .models import Category, Comment, Genre, MyUser, Review, Title


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = MyUser
        fields = (
            'first_name',
            'last_name',
            'username',
            'bio',
            'email',
            'role'
        )

        ordering = ('username',)


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(
        max_length=100,
        allow_blank=True,
        required=True
    )


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='username'
    )

    def validate(self, data):
        request = self.context.get('request')

        if request.method == 'POST':
            title = get_object_or_404(
                Title,
                id=request.parser_context["kwargs"]["title_id"]
            )
            review_existed = Review.objects.filter(
                author=request.user,
                title=title
            ).exists()

            if review_existed:
                raise serializers.ValidationError('Review from that user '
                                                  'has already been created')

        return data

    class Meta:
        model = Review
        exclude = ['title']
        read_only_fields = ['pub_date']


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        exclude = ['review']
        read_only_fields = ['pub_date']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleListSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title


class TitleCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all()
    )

    class Meta:
        fields = '__all__'
        model = Title
