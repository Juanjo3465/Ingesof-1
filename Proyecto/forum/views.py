from django.shortcuts import render, redirect
from .models import Publicacion, Usuario
from django.http import HttpResponse

# Create your views here.
def main(request):
    posts = Publicacion.objects.filter(visibilidad=1)
    contexto = { 'posts': posts }
    return render(request, 'forum/forum_home.html', contexto)

def create_post(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descripcion = request.POST.get('descripcion')
        categoria = request.POST.get('categoria')
        
        user = Usuario.objects.first()  # Replace with actual user retrieval logic

        # Create and save the new post
        Publicacion.objects.create(
            id_usuario=user,
            titulo=titulo,
            descripcion=descripcion,
            categoria=categoria,
        )

        # Redirect back to the main page after saving
        return redirect('forum')  # Replace 'main' with the name of your main view
    else:
        return render(request, 'forum/forum_home.html')
    
def filter_by_category(request, category):
    posts = Publicacion.objects.filter(categoria=category, visibilidad=1)
    contexto = { 'posts': posts, 'selected_category': category }
    return render(request, 'forum/forum_home.html', contexto)

def admin_approval(request):
    approval_pending_posts = Publicacion.objects.filter(visibilidad=None)
    contexto = { 'pending_posts': approval_pending_posts }
    return render(request, 'forum/admin_approval.html', contexto)

def accept_post(request, post_id):
    post = Publicacion.objects.get(pk=post_id)
    post.visibilidad = 1
    post.save()
    return redirect("admin_approval")

def reject_post(request, post_id):
    post = Publicacion.objects.get(pk=post_id)
    post.visibilidad = 2
    post.save()
    return redirect("admin_approval")