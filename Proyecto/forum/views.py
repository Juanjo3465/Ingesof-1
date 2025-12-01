from django.shortcuts import render, redirect
from .models import Publicacion
from core.models import Usuario
from core.services.decorators import login_required, role_required

# Create your views here.

@login_required
def main(request):
    posts = Publicacion.objects.filter(visibilidad=1)
    contexto = { 'posts': posts }
    return render(request, 'forum/forum_home.html', contexto)


@login_required
def create_post(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descripcion = request.POST.get('descripcion')
        categoria = request.POST.get('categoria')
        
        user = Usuario.objects.get(correo = request.user)  # Replace with actual user retrieval logic

        # Create and save the new post
        visibilidad = 1 if user.rol == Usuario.Rol_Administrador else None
            
        Publicacion.objects.create(
            id_usuario=user,
            titulo=titulo,
            descripcion=descripcion,
            categoria=categoria,
            visibilidad=visibilidad
        )

        # Redirect back to the main page after saving
    return redirect('forum')  # Replace 'main' with the name of your main view
      
    
def filter_by_category(request, category):
    posts = Publicacion.objects.filter(categoria=category, visibilidad=1)
    contexto = { 'posts': posts, 'selected_category': category }
    return render(request, 'forum/forum_home.html', contexto)

@login_required
def mis_publicaciones(request):
    user = Usuario.objects.get(correo=request.user)  # Replace with actual user retrieval logic
    posts = Publicacion.objects.filter(id_usuario=user.id_usuario)
    contexto = { 'posts': posts, 'selected_category': 'mis_publicaciones' }
    return render(request, 'forum/forum_home.html', contexto) 

@role_required(Usuario.Rol_Administrador)
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