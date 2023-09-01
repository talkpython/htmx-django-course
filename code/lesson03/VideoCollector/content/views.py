# VideoCollector/content/views.py
import more_itertools
from content.models import Category, Video
from django.shortcuts import get_object_or_404, render


def home(request):
    categories = Category.objects.all()
    data = {"rows": more_itertools.chunked(categories, 3)}

    return render(request, "home.html", data)


def category(request, name):
    category = get_object_or_404(Category, name__iexact=name)
    videos = Video.objects.filter(categories=category)
    data = {"category": category, "rows": more_itertools.chunked(videos, 3)}

    return render(request, "category.html", data)


def play_video(request, video_id):
    data = {"video": get_object_or_404(Video, id=video_id)}

    return render(request, "play_video.html", data)


def feed(request):
    data = {
        "videos": Video.objects.all(),
    }

    return render(request, "feed.html", data)
