from django.shortcuts import render, get_object_or_404, redirect
from .models import Category,Subcategory
from .forms import CategoryForm
from .serializers import SubcategorySerializer
from django.conf import settings
from django.shortcuts import render, get_object_or_404
import requests



# List all categories
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})

# Create a new category
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category-list')
    else:
        form = CategoryForm()
    return render(request, 'category_form.html', {'form': form})

# Update a category
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category-list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'category_form.html', {'form': form})

# Delete a category
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('category-list')
    return render(request, 'category_delete.html', {'category': category})

def subcategory_list(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    subcategories = Subcategory.objects.filter(category=category)

    if request.method == 'POST':
        generated_subcategories = generate_subcategories(category.name)
        for name in generated_subcategories:
            Subcategory.objects.get_or_create(name=name, category=category)

        subcategories = Subcategory.objects.filter(category=category)  # Refresh subcategories

    return render(request, 'subcategory/subcategory_list.html', {
        'category': category,
        'subcategories': subcategories,
    })

def generate_subcategories(category_name):
    url = "https://api.gemini.com/v1/generate_subcategories"  # Replace with the actual endpoint
    headers = {
        "Authorization": f"Bearer {settings.GEMINI_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "prompt": f"Generate subcategories for the category '{category_name}'.",
        "max_tokens": 50
    }
    
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()  # Raise an error for bad responses

    subcategories = response.json().get('subcategories', [])
    return [subcategory.strip() for subcategory in subcategories]