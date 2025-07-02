from django.core.management.base import BaseCommand
from django.utils.text import slugify
from store.models import Category, Product
from django.core.files.base import ContentFile
import requests
from decimal import Decimal
import random

class Command(BaseCommand):
    help = 'Setup demo data for the store'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating categories...')
        
        # Create categories
        categories = [
            {
                'name': 'Tech',
                'icon': 'fa-laptop-code',
                'products': [
                    {
                        'name': 'Premium Laptop',
                        'price': '1299.99',
                        'description': 'High-performance laptop with the latest technology.',
                        'image_url': 'https://images.pexels.com/photos/18105/pexels-photo.jpg',
                        'discount': 10,
                    },
                    {
                        'name': 'Wireless Earbuds',
                        'price': '199.99',
                        'description': 'Premium wireless earbuds with noise cancellation.',
                        'image_url': 'https://images.pexels.com/photos/3780681/pexels-photo-3780681.jpeg',
                        'discount': 0,
                    },
                ]
            },
            {
                'name': 'Clothes',
                'icon': 'fa-tshirt',
                'products': [
                    {
                        'name': 'Designer Jacket',
                        'price': '299.99',
                        'description': 'Luxury designer jacket made with premium materials.',
                        'image_url': 'https://images.pexels.com/photos/1124468/pexels-photo-1124468.jpeg',
                        'discount': 15,
                    },
                    {
                        'name': 'Premium Jeans',
                        'price': '149.99',
                        'description': 'High-quality denim jeans with perfect fit.',
                        'image_url': 'https://images.pexels.com/photos/1082529/pexels-photo-1082529.jpeg',
                        'discount': 0,
                    },
                ]
            },
            {
                'name': 'Cosmetics',
                'icon': 'fa-spa',
                'products': [
                    {
                        'name': 'Luxury Perfume',
                        'price': '199.99',
                        'description': 'Exclusive fragrance for the sophisticated.',
                        'image_url': 'https://images.pexels.com/photos/965989/pexels-photo-965989.jpeg',
                        'discount': 5,
                    },
                    {
                        'name': 'Premium Skincare Set',
                        'price': '299.99',
                        'description': 'Complete skincare routine with natural ingredients.',
                        'image_url': 'https://images.pexels.com/photos/3321416/pexels-photo-3321416.jpeg',
                        'discount': 0,
                    },
                ]
            },
            {
                'name': 'Others',
                'icon': 'fa-ellipsis-h',
                'products': [
                    {
                        'name': 'Luxury Watch',
                        'price': '999.99',
                        'description': 'Premium timepiece with elegant design.',
                        'image_url': 'https://images.pexels.com/photos/190819/pexels-photo-190819.jpeg',
                        'discount': 20,
                    },
                    {
                        'name': 'Designer Sunglasses',
                        'price': '249.99',
                        'description': 'Stylish sunglasses with UV protection.',
                        'image_url': 'https://images.pexels.com/photos/701877/pexels-photo-701877.jpeg',
                        'discount': 0,
                    },
                ]
            },
        ]

        for cat_data in categories:
            category = Category.objects.create(
                name=cat_data['name'],
                slug=slugify(cat_data['name']),
                icon=cat_data['icon']
            )
            
            self.stdout.write(f'Created category: {category.name}')
            
            # Create products for this category
            for prod_data in cat_data['products']:
                try:
                    # Download image from URL
                    response = requests.get(prod_data['image_url'])
                    if response.status_code == 200:
                        # Create product
                        product = Product.objects.create(
                            category=category,
                            name=prod_data['name'],
                            slug=slugify(prod_data['name']),
                            description=prod_data['description'],
                            price=Decimal(prod_data['price']),
                            discount=prod_data['discount'],
                            stock=random.randint(5, 50),
                            is_featured=random.choice([True, False])
                        )
                        
                        # Save image
                        image_name = f"{slugify(prod_data['name'])}.jpg"
                        product.image.save(image_name, ContentFile(response.content), save=True)
                        
                        self.stdout.write(f'Created product: {product.name}')
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error creating product {prod_data["name"]}: {str(e)}'))

        self.stdout.write(self.style.SUCCESS('Successfully created demo data'))
