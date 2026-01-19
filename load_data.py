import os
import django
import requests

# Django സെറ്റിംഗ്‌സ് ലോഡ് ചെയ്യുന്നു
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from store.models import Product, Category

def fetch_and_save_products():
    url = "https://fakestoreapi.com/products"
    response = requests.get(url)
    
    if response.status_code == 200:
        products_data = response.json()
        
        for item in products_data:
            # കാറ്റഗറി ഉണ്ടോ എന്ന് നോക്കുന്നു, ഇല്ലെങ്കിൽ പുതിയത് ഉണ്ടാക്കുന്നു
            category_obj, created = Category.objects.get_or_create(
                name=item['category'],
                defaults={'slug': item['category'].lower().replace(" ", "-")}
            )
            
            # പ്രോഡക്റ്റ് ഡാറ്റാബേസിലേക്ക് സേവ് ചെയ്യുന്നു
            Product.objects.create(
                category=category_obj,
                name=item['title'],
                description=item['description'],
                price=item['price'],
                stock=50, # ഡിഫോൾട്ട് ആയി 50 എണ്ണം കൊടുക്കുന്നു
                image_url=item['image']
            )
        print("Success: All products loaded to your database!")
    else:
        print("Failed to fetch data from API")

if __name__ == "__main__":
    fetch_and_save_products()