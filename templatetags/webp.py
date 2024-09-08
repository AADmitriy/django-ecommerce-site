import os

from PIL import Image

from django.conf import settings
from django import template

register = template.Library()

def convert_to_webp(image_path):
    webp_image_path = image_path.split('.', 1)[0] + ".webp"

    if not os.path.exists(webp_image_path):
        try:
            img = Image.open(image_path)

            img.save(webp_image_path, 'WEBP')
            print(f"Converted {webp_image_path} to WEBP")
        except Exception as e:
            print(f"Could not convert {webp_image_path} to WEBP. Error: {e}")


@register.simple_tag(takes_context=True)
def webp(context, img_url):
    try:
        request = context['request']

        if 'image/webp' in request.META.get('HTTP_ACCEPT', ""):
            webp_image_path = img_url.split('.', 1)[0] + ".webp"

            webp_full_path = os.path.normpath("".join((str(settings.BASE_DIR), webp_image_path)))
            img_full_path = os.path.normpath("".join((str(settings.BASE_DIR), img_url)))

            if os.path.exists(webp_full_path):
                return webp_image_path
            else:
                convert_to_webp(img_full_path)
                return webp_image_path

    except KeyError:
        return img_url


