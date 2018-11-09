from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm

# Create your views here.

def get_index(request):
    posts = Post.objects.all()
    
    return render(request, "blog/index.html", {"posts": posts})
    

def read_post(request, id):
    post = get_object_or_404(Post, pk=id)
    post.views += 1
    post.save()
    return render(request, "blog/read_post.html", {"post": post})

    
@login_required
def write_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        p = form.save(commit=False) # Save the form, but not to the server (i.e. "commit=False").
        p.author = request.user # Request user.
        p.save() # Save the form and the user to the database.
        
        return redirect(read_post, p.id)
    else:    
        form=PostForm()
        
        return render(request, "blog/post_form.html", {"form": form})
   

def edit_post(request, id):
    post = get_object_or_404(Post, pk=id)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        form.save()
        
        return redirect(read_post, id)
    else:    
        form=PostForm(instance=post)
        
        return render(request, "blog/post_form.html", {"form": form})
    
