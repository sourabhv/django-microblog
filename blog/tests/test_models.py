from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.test import TestCase

from ..models import Post, PostManager

class BlogModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='test')

    def create_post(self, title='Test blog post', published='True'):
        return Post.objects.create(
            title=title,
            published=published,
            author=self.user)

    def test_model_creation(self):
        post = self.create_post()
        self.assertTrue(isinstance(post,Post))
        self.assertEqual(post.__unicode__(), post.title)
        self.assertEqual(post.slug, slugify(post.title))

    def test_model_url(self):
        post = self.create_post()
        self.assertEqual(
            post.get_absolute_url(),
            reverse('blog:detail', kwargs={'slug': post.slug}))

    def test_model_manager(self):
        live_post = self.create_post()
        draft_post = self.create_post(
            title='Draft Post',
            published=False)

        self.assertIn(live_post, Post.objects.live())
        self.assertNotIn(draft_post, Post.objects.live())

    def test_custom_slug(self):
        custom_slug='custom-slug'

        post = Post.objects.create(
            title='custom slug post',
            slug=custom_slug,
            author=self.user)
        self.assertNotEqual(post.slug, slugify(post.title))
        self.assertEqual(post.slug, custom_slug)
