from django.shortcuts import render, get_object_or_404, redirect
from .models import Artwork, ArtCollection
from .forms import ArtworkForm, ArtCollectionForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages 

def artwork_list(request):
    search_query = request.GET.get('search', '') 
    artworks = Artwork.objects.filter(user=request.user) 
    if search_query:  
        artworks = artworks.filter(tags__icontains=search_query)  

    context = {
        'artworks': artworks,
        'search_query': search_query,
    }
    return render(request, 'artwork/artwork_list.html', {'artworks': artworks})

def artwork_detail(request, pk):
    artwork = get_object_or_404(Artwork, pk=pk)
    return render(request, 'artwork/artwork_detail.html', {'artwork': artwork})

@login_required 
def artwork_create(request):
    if request.method == 'POST':
        form = ArtworkForm(request.POST, request.FILES)
        if form.is_valid():
            artwork = form.save(commit=False) 
            artwork.user = request.user  
            artwork.save()  
            
            messages.success(request, "Nouvelle œuvre ajoutée avec succès!")
            
            return redirect('artwork_list')
    else:
        form = ArtworkForm()
    return render(request, 'artwork/artwork_form.html', {'form': form})

@login_required  
def artwork_update(request, pk):
    artwork = get_object_or_404(Artwork, pk=pk)

    if artwork.user != request.user:
        return redirect('artwork_list')

    if request.method == 'POST':
        form = ArtworkForm(request.POST, request.FILES, instance=artwork)
        if form.is_valid(): 
            form.save()  
            messages.success(request, 'L\'œuvre a été modifiée avec succès.')  
            return redirect('artwork_list')  
    else:
        form = ArtworkForm(instance=artwork)

    return render(request, 'artwork/artwork_form.html', {'form': form})

@login_required 
def artwork_delete(request, pk):
    artwork = get_object_or_404(Artwork, pk=pk)

    if artwork.user != request.user:
        return redirect('artwork_list')
    if request.method == 'POST':
        artwork.delete() 
        messages.success(request, 'L\'œuvre a été supprimée avec succès.')  
        return redirect('artwork_list')  

    return render(request, 'artwork/artwork_confirm_delete.html', {'artwork': artwork})

def all_artworks(request):
    search_query = request.GET.get('search', '')  
    artworks = Artwork.objects.all() 

    if search_query: 
        artworks = artworks.filter(tags__icontains=search_query) 

    return render(request, 'artwork/all_artworks.html', {
        'artworks': artworks,
        'search_query': search_query,  
    })
def artwork_public_detail(request, pk):
    artwork = get_object_or_404(Artwork, pk=pk)
    return render(request, 'artwork/artwork_public_detail.html', {'artwork': artwork})

def add_to_gallery(request, artwork_id):
    artwork = get_object_or_404(Artwork, id=artwork_id)
    galleries = ArtCollection.objects.filter(user=request.user)

    if request.method == 'POST':
        if request.POST.get('action') == 'create_gallery':
            form = ArtCollectionForm(request.POST)
            if form.is_valid():
                new_collection = form.save(commit=False)
                new_collection.user = request.user
                new_collection.save()
                new_collection.artworks.add(artwork)
                messages.success(request, "L'œuvre a été ajoutée à la galerie avec succès !")
                return redirect('http://127.0.0.1:8000/artwork/all/')
        else:
            selected_gallery = request.POST.get('gallery')
            if selected_gallery:
                gallery = get_object_or_404(ArtCollection, id=selected_gallery)
                gallery.artworks.add(artwork)
                messages.success(request, "L'œuvre a été ajoutée à la galerie avec succès !")
                return redirect('http://127.0.0.1:8000/artwork/all/')

    form = ArtCollectionForm()
    return render(request, 'artwork/add_to_gallery.html', {
        'artwork': artwork,
        'galleries': galleries,
        'form': form
    })

    @login_required  
    def collection_detail(request, pk):
        gallery = get_object_or_404(ArtCollection, pk=pk)
        return render(request, 'artwork/gallery_detail.html', {'gallery': gallery})

def collection_list(request):
    if request.user.is_authenticated:
        galleries = ArtCollection.objects.filter(user=request.user)
    else:
        galleries = []  

    return render(request, 'artwork/gallery_list.html', {'galleries': galleries})

@login_required  
def collection_detail(request, gallery_id):
    gallery = get_object_or_404(ArtCollection, id=gallery_id)

    if request.method == 'POST':
        artwork_id = request.POST.get('artwork_id')
        artwork = get_object_or_404(Artwork, id=artwork_id)

        if artwork.user == request.user and artwork in gallery.artworks.all():
            gallery.artworks.remove(artwork)

            return redirect('collection_detail', gallery_id=gallery.id)

    return render(request, 'artwork/gallery_detail.html', {'gallery': gallery})


@login_required
def remove_artwork_from_gallery(request, gallery_id, artwork_id):
    gallery = get_object_or_404(ArtCollection, id=gallery_id)
    artwork = get_object_or_404(Artwork, id=artwork_id)

    if gallery.user != request.user:
        return redirect('collection_list') 

    gallery.artworks.remove(artwork)
    
    messages.success(request, 'L\'œuvre d\'art a été retirée de la galerie avec succès.')

    return redirect('collection_detail', gallery_id=gallery.id) 

@login_required  
def collection_delete(request, gallery_id):
    gallery = get_object_or_404(ArtCollection, id=gallery_id)

    if gallery.user != request.user:
        return redirect('collection_list') 

    if request.method == 'POST':
        gallery.delete()
        messages.success(request, 'La galerie a été supprimée avec succès.')  
        return redirect('collection_list')  

    return render(request, 'artwork/gallery_confirm_delete.html', {'gallery': gallery})