# VideoCollector/content/views.py
import urllib

import more_itertools
from content.models import Category, Video
from django import forms
from django.db.models import Q
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


def add_video_form(request, name):
    category = get_object_or_404(Category, name__iexact=name)
    data = {
        "category": category,
    }

    return render(request, "partials/add_video_form.html", data)


def add_video_link(request, name):
    category = get_object_or_404(Category, name__iexact=name)
    data = {
        "category": category,
    }

    return render(request, "partials/add_video_link.html", data)


def search(request):
    search_text = request.GET.get("search_text", "")
    search_text = urllib.parse.unquote(search_text)
    search_text = search_text.strip()

    videos = None

    if search_text:
        parts = search_text.split()

        q = Q(title__icontains=parts[0]) | Q(author__icontains=parts[0])
        for part in parts[1:]:
            q |= Q(title__icontains=part) | Q(author__icontains=part)

        videos = Video.objects.filter(q)

    data = {
        "search_text": search_text,
        "videos": videos,
    }

    if request.htmx:
        return render(request, "partials/search_results.html", data)

    return render(request, "search.html", data)
