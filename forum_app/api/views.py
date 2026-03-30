from rest_framework import viewsets, generics, permissions
from rest_framework.throttling import ScopedRateThrottle

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from forum_app.models import Like, Question, Answer
from .serializers import QuestionSerializer, AnswerSerializer, LikeSerializer
from .permissions import IsOwnerOrAdmin, CustomQuestionPermission
from .throttling import QuestionGetThrottle, QuestionPostThrottle, QuestionThrottle


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [CustomQuestionPermission]
    # throttle_classes = [QuestionThrottle]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class AnswerListCreateView(generics.ListCreateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['author__username']
    search_fields = ['content']
    ordering_fields = ['content', 'author__username']
    ordering = ['author__username']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    # def get_queryset(self):
    #     queryset = Answer.objects.all()

    #     content_param = self.request.query_params.get('content', None)
    #     if content_param is not None:
    #         queryset = queryset.filter(content__icontains = content_param)

    #     username_param = self.request.query_params.get('author', None)
    #     if username_param is not None:
    #         queryset = queryset.filter(author__username = username_param)

    #     return queryset


class AnswerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsOwnerOrAdmin]

from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination

class MyPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 10
    page_query_param = 'p'

class CustomLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 10
    limit_query_param = "limit"
    offset_query_param = "offset"
    max_limit = 100
    
class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsOwnerOrAdmin]
    pagination_class = CustomLimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
