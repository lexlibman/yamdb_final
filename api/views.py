from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from api_yamdb.settings import DEFAULT_FROM_EMAIL

from .filters import TitleFilter
from .models import Category, Genre, Review, Title
from .permissions import (IsAdmin, IsAdminOrReadOnly, IsOwner,
                          IsOwnerAdminModeratorOrReadOnly)
from .serializers import (CategorySerializer, CommentSerializer,
                          CustomUserSerializer, EmailSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitleCreateSerializer, TitleListSerializer)


class CreateListDestroyViewSet(ListModelMixin,
                               CreateModelMixin,
                               DestroyModelMixin,
                               viewsets.GenericViewSet):
    pass


User = get_user_model()


@api_view(['POST'])
@permission_classes([AllowAny])
def send_confirm_code(request):
    serializer = EmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data.get('email')
    username = serializer.data.get('username')
    if username == "":
        username = email.split('@')[0]

    user = User.objects.get_or_create(
        email=email,
        username=username,
    )
    token = default_token_generator.make_token(user)

    user.confirmation_code = token
    user.save()

    send_mail(
        subject='Confirmation your email',
        message=f'Please confirm your email \
                by reply this confirmation_code {token}\
                to link: https://domain.ru/v1/auth/token/',
        from_email=DEFAULT_FROM_EMAIL,
        recipient_list=(email, )
    )

    return Response(
        {'email': email},
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def send_token(request):
    serializer = CustomUserSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.data.get('email')
        confirm_code = serializer.data.get('confirmation_code')

        user = User.objects.get(
            User,
            email=email,
            confirmation_code=confirm_code
        )

        token = AccessToken().for_user(user)
        return Response(
            {'token': str(token)},
            status=status.HTTP_200_OK
        )
    return Response(
        {"field_name": [serializer.error_messages]},
        status=status.HTTP_400_BAD_REQUEST
    )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (IsAdmin, )
    filter_backends = [SearchFilter]
    search_fields = ['username']
    lookup_field = 'username'

    @action(methods=('get', 'patch'), detail=False, permission_classes=(IsOwner,))
    def me(self, request):
        if request.GET == 'GET':
            return User.objects.filter(request.user)
        serializer = self.get_serializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role)
        return Response(serializer.data, status.HTTP_200_OK)


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    filter_backends = (DjangoFilterBackend, SearchFilter)
    permission_classes = (IsAdminOrReadOnly, )
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action not in ('list', 'retrieve'):
            return TitleCreateSerializer
        return TitleListSerializer


class CategoryViewSet(CreateListDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly, )
    search_fields = ['name']
    lookup_field = 'slug'


class GenreViewSet(CreateListDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly, )
    search_fields = ['name']
    lookup_field = 'slug'


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerAdminModeratorOrReadOnly)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerAdminModeratorOrReadOnly)

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title__pk=self.kwargs.get('title_id')
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title__pk=self.kwargs.get('title_id')
        )
        serializer.save(author=self.request.user, review=review)
