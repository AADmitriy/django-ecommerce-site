from django.db import models
from datetime import date
from django.conf import settings
import os

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128, default="", null=False, unique=True)

    def __str__(self):
        return self.slug
    
class Image(models.Model):
    image = models.ImageField(default="fallback.png", blank=True, upload_to="uploads")

    def __str__(self):
        return self.image.url

class Product(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField(max_length=4096)
    price = models.DecimalField(max_digits=64, decimal_places=2)
    date = models.DateField(default=date.today)
    times_ordered = models.IntegerField(default=0)
    left_in_storage = models.IntegerField(default=1)
    image = models.ManyToManyField(Image)
    categories = models.ManyToManyField(Category)

    @property
    def main_img_url(self):
        all_images = self.image.all()

        if all_images:
            return str(all_images[0])
        else:
            return ''
        
    @property
    def main_img_webp_url(self):
        main_img = self.main_img_url

        if not main_img: return ''

        main_img_webp = main_img.rsplit('.', 1)[0] + '.webp'

        full_img_path = os.path.normpath("".join((str(settings.BASE_DIR), main_img)))
        full_webp_path = os.path.normpath("".join((str(settings.BASE_DIR), main_img_webp)))

        if not os.path.exists(full_webp_path):
            try:
                img = Image.open(full_img_path)
                img.save(main_img_webp, 'WEBP')
                print(f"Converted {main_img} to WEBP")
            except Exception as e:
                print(f"Could not convert {main_img} to WEBP. Error: {e}")
                return ''
        
        return main_img_webp
        
    @property
    def categories_list(self):
        all_categories = self.categories.all()

        if all_categories:
            return [str(category) for category in all_categories]
        else:
            return []

    def __str__(self):
        return self.title
    