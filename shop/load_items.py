from .models import Category, Product, Image
from django.core import files
from io import BytesIO
import urllib.request
import requests
import json


def load_categories():
    url = "https://dummyjson.com/products/categories"

    with urllib.request.urlopen(url) as response:
        body_json = response.read()

    body_dict = json.loads(body_json)

    for category_info in body_dict:
        Category.objects.create(name=category_info['name'], slug=category_info['slug'])
    

def load_images(urls):
    imgs = []
    for url in urls:
        resp = requests.get(url)
        if resp.status_code != requests.codes.ok:
            continue
        
        fp = BytesIO()
        fp.write(resp.content)
        file_name = url.split("/images/")[-1]
        file_name = file_name.replace('/', '_')
        image_instance = Image()
        image_instance.image.save(file_name, files.File(fp))
        image_instance.save()
        imgs.append(image_instance)

    return imgs


def load_products():
    url = "https://dummyjson.com/products?select=title,description,category,price,stock,images,thumbnail&limit=30"

    with urllib.request.urlopen(url) as response:
        body_json = response.read()

    body_dict = json.loads(body_json)

    for product_info in body_dict['products']:
        print(product_info['id'])
        product = Product(
            title=product_info['title'],
            description=product_info['description'],
            price=product_info['price'],
            left_in_storage=product_info['stock'],
        )
        product.save()

        product_category = Category.objects.get(slug=product_info['category'])
        product.categories.add(product_category)

        img_urls = [product_info['thumbnail']] + product_info['images']
        print(img_urls)
        image_objs = load_images(img_urls)

        for image_obj in image_objs:
            product.image.add(image_obj)

        
