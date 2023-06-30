from django.shortcuts import get_object_or_404

from django.db.models import Avg

from rest_framework import viewsets
from rest_framework import serializers


from .permissions import ReviewCommentPermission
from .validators import check_conformity_title_and_review


from .serializers import ReviewSerializer, CommentSerializer

from reviews.models import Review, Comment, Title

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (ReviewCommentPermission,)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        new_queryset = title.reviews.all()
        return new_queryset

    def perform_create(self, serializer):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, id=title_id)
        if Review.objects.filter(
                author=self.request.user, title=title).exists():
            raise serializers.ValidationError(
                "Извините, но Вы уже создали один отзыв к данному произведению"
            )
        serializer.save(author=self.request.user, title=title)
        rating_dict = Review.objects.filter(
            title=title).aggregate(Avg("score"))
        new_rating = rating_dict["score__avg"]
        Title.objects.filter(id=title_id).update(rating=new_rating)

    def perform_update(self, serializer):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)
        rating_dict = Review.objects.filter(
            title=title).aggregate(Avg("score"))
        new_rating = rating_dict["score__avg"]

        Title.objects.filter(id=title_id).update(rating=new_rating)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (ReviewCommentPermission,)

    def get_queryset(self):
        check_conformity_title_and_review(self)
        review = get_object_or_404(Review, id=self.kwargs.get("review_id"))
        new_queryset = review.comments.all()
        return new_queryset

    def perform_create(self, serializer):
        check_conformity_title_and_review(self)
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, review_id=review)
