from django.shortcuts import render, get_object_or_404, redirect
from .models import Category,Subcategory
from .forms import CategoryForm, SubcategoryForm
from .serializers import SubcategorySerializer
from django.conf import settings
from django.shortcuts import render, get_object_or_404
import requests
from artify.settings import GEMINI_API_KEY
import os
from requests import post, exceptions

# List all categories
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})

def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)  # Add request.FILES here
        if form.is_valid():
            form.save()
            return redirect('category-list')
    else:
        form = CategoryForm()
    return render(request, 'category_form.html', {'form': form})

def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)  # Add request.FILES here
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
        try:
            generated_subcategories = generate_subcategories(category.name)
            for name in generated_subcategories:
                Subcategory.objects.get_or_create(name=name, category=category)
            subcategories = Subcategory.objects.filter(category=category)  # Refresh
        except exceptions.RequestException as e:
            error_message = f"Error generating subcategories: {str(e)}"
            # Handle error, e.g., display message to user
    error_message = ''
    return render(request, 'subcategory_list.html', {
        'category': category,
        'subcategories': subcategories,
        'error_message': error_message if error_message else None,
    })

def generate_subcategories(category_name):
    url = "https://gemini.googleapis.com/v1/models/gemini-pro:generateContent"  # Endpoint without API key
    headers = {
        "Authorization": f"Bearer {GEMINI_API_KEY}",  # Use API key from settings
        "Content-Type": "application/json"
    }
    payload = {
        "prompt": f"Generate subcategories for the category '{category_name}'.",
        "max_tokens": 50
    }
   

    response = post(url, headers=headers, json=payload)
    print(response)
    response.raise_for_status()

    subcategories = response.json().get('subcategories', [])
    return [subcategory.strip() for subcategory in subcategories]

# List all subcategories for a specific category
def subcategory_list(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    subcategories = Subcategory.objects.filter(category=category)
    return render(request, 'subcategory_list.html', {
        'category': category,
        'subcategories': subcategories,
    })

# Create a new subcategory
def subcategory_create(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        form = SubcategoryForm(request.POST)
        if form.is_valid():
            subcategory = form.save(commit=False)
            subcategory.category = category
            subcategory.save()
            return redirect('subcategory-list', category_id=category.id)
    else:
        form = SubcategoryForm()
    return render(request, 'subcategory_form.html', {'form': form, 'category': category})

# Update a subcategory
def subcategory_update(request, category_id, pk):
    category = get_object_or_404(Category, id=category_id)
    subcategory = get_object_or_404(Subcategory, pk=pk)
    if request.method == 'POST':
        form = SubcategoryForm(request.POST, instance=subcategory)
        if form.is_valid():
            form.save()
            return redirect('subcategory-list', category_id=category.id)
    else:
        form = SubcategoryForm(instance=subcategory)
    return render(request, 'subcategory_form.html', {'form': form, 'category': category})

# Delete a subcategory
def subcategory_delete(request, category_id, pk):
    category = get_object_or_404(Category, id=category_id)
    subcategory = get_object_or_404(Subcategory, pk=pk)
    if request.method == 'POST':
        subcategory.delete()
        return redirect('subcategory-list', category_id=category.id)
    return render(request, 'subcategory_delete.html', {'subcategory': subcategory, 'category': category})