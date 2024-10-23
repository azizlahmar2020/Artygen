from django.shortcuts import render
from django.http import HttpResponse
from .models import Post
from django.views.generic import ListView, DetailView, CreateView
# Create your views here.


""" def home(request):
    context={
        'posts':Post.objects.all()
    }
    return render(
        request,
        'Blog/blog.html',context
    )
 """
""" def about (request):
    return HttpResponse("<h1>About</h1>") """
class PostListView(ListView):
    model = Post
    template_name = 'Blog/blog.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']  
    
class PostDetailView(DetailView):
    model = Post
    template_name = 'Blog/detail.html'
 
class PostCreateView(CreateView):
    model = Post
    template_name = 'Blog/create.html'
    fields = ['title','content']
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)