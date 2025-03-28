from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import URLMap
from .services import URLShortenerService


class URLShortenerServiceTests(TestCase):
    def setUp(self):
        self.service = URLShortenerService()
        self.test_url = "https://www.django-rest-framework.org/"

    def test_generate_hash(self):
        hash1 = self.service.generate_hash(self.test_url)
        hash2 = self.service.generate_hash(self.test_url)
        self.assertEqual(hash1, hash2)
        self.assertEqual(len(hash1), 6)

    def test_create(self):
        url_map = self.service.create(self.test_url)
        self.assertEqual(url_map.original_url, self.test_url)
        self.assertEqual(len(url_map.hash), 6)


class URLMapAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.test_url = "https://www.django-rest-framework.org/"
        self.service = URLShortenerService()

    def test_create_url(self):
        response = self.client.post(reverse("shortener:create"), {"url": self.test_url}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("original_url", response.data)
        self.assertIn("hash", response.data)
        self.assertIn("_links", response.data)
        self.assertIn("self", response.data["_links"])
        self.assertIn("redirect", response.data["_links"])

    def test_get_original_url(self):
        url_map = self.service.create(self.test_url)
        response = self.client.get(reverse("shortener:details", kwargs={"hash": url_map.hash}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["original_url"], self.test_url)
        self.assertIn("_links", response.data)
        self.assertIn("self", response.data["_links"])
        self.assertIn("redirect", response.data["_links"])

    def test_delete_url(self):
        url_map = self.service.create(self.test_url)
        response = self.client.delete(reverse("shortener:details", kwargs={"hash": url_map.hash}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(URLMap.objects.filter(hash=url_map.hash).exists())

    def test_get_nonexistent_url(self):
        response = self.client.get(reverse("shortener:details", kwargs={"hash": "nonexistent"}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_root_endpoint_not_allowed(self):
        response = self.client.get(reverse("shortener:create"))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class RedirectionTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.test_url = "https://www.django-rest-framework.org/"
        self.service = URLShortenerService()

    def test_redirect_to_original_url(self):
        url_map = self.service.create(self.test_url)
        response = self.client.get(reverse("shortener:redirect", kwargs={"hash": url_map.hash}))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, self.test_url)
