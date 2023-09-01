# VideoCollector/content/management/commands/load.py
import json
from pathlib import Path

from content.models import Category, Video
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError


class Command(BaseCommand):
    help = "Imports videos and categories from a JSON file"

    def add_arguments(self, parser):
        parser.add_argument("filename", help="JSON file to use for importing")

    def handle(self, *args, **options):
        path = Path(options["filename"]).resolve()

        sections = json.loads(path.read_text())
        for section in sections:
            category, _ = Category.objects.get_or_create(
                name=section["category"], image_name=section["image"]
            )

            for item in section["videos"]:
                video = Video.objects.filter(youtube_id=item["id"]).first()
                if video is None:
                    video = Video.objects.create(
                        youtube_id=item["id"],
                        title=item["title"],
                        author=item["author"],
                        view_count=item["views"],
                    )

                video.categories.add(category)
