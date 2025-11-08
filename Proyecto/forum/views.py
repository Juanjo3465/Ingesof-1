from django.shortcuts import render
from .models import Publicacion
from django.http import HttpResponse

# Create your views here.
def main(request):
    posts = Publicacion.objects.all()
    contexto = { 'posts': posts }
    return render(request, 'forum/forum_home.html', contexto)