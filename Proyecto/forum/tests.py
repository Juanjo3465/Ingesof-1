from django.test import TestCase
from django.urls import reverse
from forum.models import Publicacion, Usuario

class ForumTests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = Usuario.objects.create(
            cedula=1234567890,
            nombre="Test User",
            correo="testuser@example.com",
            contrasena="password123",
            rol="Admin"
            )
        
        # Create test posts
        self.post1 = Publicacion.objects.create(
            id_usuario=self.user,
            titulo="Test Post 1",
            descripcion="This is a test post in the 'anuncios' category.",
            categoria="anuncios",
            visibilidad=1
        )
        self.post2 = Publicacion.objects.create(
            id_usuario=self.user,
            titulo="Test Post 2",
            descripcion="This is a test post in the 'eventos' category.",
            categoria="eventos",
            visibilidad=1
        )
        self.post3 = Publicacion.objects.create(
            id_usuario=self.user,
            titulo="Pending Post",
            descripcion="This post is pending approval.",
            categoria="novedades",
            visibilidad=None
        )
        self.post4 = Publicacion.objects.create(
            id_usuario=self.user,
            titulo="Pending Post2",
            descripcion="This post is gonna be rejected.",
            categoria="novedades",
            visibilidad=None
        )

    def test_main_view_displays_visible_posts(self):
        """Test that the main view displays only posts with visibilidad=1."""
        response = self.client.get(reverse('forum'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Post 1")
        self.assertContains(response, "Test Post 2")
        self.assertNotContains(response, "Pending Post")

    def test_filter_by_category_view(self):
        """Test that the filter_by_category view filters posts by category."""
        response = self.client.get(reverse('filter_by_category', args=['anuncios']))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Post 1")
        self.assertNotContains(response, "Test Post 2")

    def test_create_post_view(self):
        """Test that a new post can be created via the create_post view."""
        response = self.client.post(reverse('create_post'), {
            'titulo': 'New Test Post',
            'descripcion': 'This is a new test post.',
            'categoria': 'novedades',
        })
        self.assertEqual(response.status_code, 302)  # Redirect after creation
        self.assertTrue(Publicacion.objects.filter(titulo="New Test Post").exists())

    def test_admin_approval_view(self):
        """Test that the admin_approval view displays only pending posts."""
        response = self.client.get(reverse('admin_approval'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Pending Post")
        self.assertContains(response, "Pending Post2")
        self.assertNotContains(response, "Test Post 1")

    def test_accept_post_view(self):
        """Test that the accept_post view updates the visibilidad of a post."""
        response = self.client.get(reverse('accept_post', args=[self.post3.id_publicacion]))
        self.assertEqual(response.status_code, 302)  # Redirect after approval
        self.post3.refresh_from_db()
        self.assertEqual(self.post3.visibilidad, 1)
        
    def test_reject_post_view(self):
        """Test that the reject_post view deletes the post."""
        response = self.client.get(reverse('reject_post', args=[self.post4.id_publicacion]))
        self.assertEqual(response.status_code, 302)  # Redirect after rejection
        self.post4.refresh_from_db()
        self.assertEqual(self.post4.visibilidad, 2)
