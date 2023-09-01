# VideoCollector/content/views.py
import more_itertools
from content.models import Category, Video
from django import forms
from django.shortcuts import get_object_or_404, render

VideoForm = forms.modelform_factory(
    Video, fields=["youtube_id", "title", "author", "view_count"]
)


def home(request):
    categories = Category.objects.all()
    data = {"rows": more_itertools.chunked(categories, 3)}

    return render(request, "home.html", data)


def category(request, name):
    category = get_object_or_404(Category, name__iexact=name)
    if request.method == "GET":
        form = VideoForm()
    else:
        # POST
        form = VideoForm(request.POST)
        if form.is_valid():
            video = form.save()
            video.categories.add(category)

    videos = Video.objects.filter(categories=category)
    data = {
        "category": category,
        "rows": more_itertools.chunked(videos, 3),
        "form": form,
    }

    return render(request, "category.html", data)


def play_video(request, video_id):
    data = {"video": get_object_or_404(Video, id=video_id)}

    return render(request, "play_video.html", data)


def feed(request):
    data = {
        "videos": Video.objects.all(),
    }

    return render(request, "feed.html", data)
