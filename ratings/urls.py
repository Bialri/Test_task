from django.urls import path
from ratings.views import RatingView, ComicView


urlpatterns = [
    path('ratings/', RatingView.as_view()),
    path('comics/<int:comic_id>/rating/', ComicView.as_view())
]