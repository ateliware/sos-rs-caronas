from unittest import TestCase

from django.urls import reverse


class CityRoutesTest(TestCase):
    def test_cities_list_url_resolves(self):
        # Given
        url = reverse("cities-list")
        expected_url = "/api/cities/"

        # Then
        self.assertEqual(url, expected_url)

    def test_cities_detail_url_resolves(self):
        # Given
        url = reverse("cities-detail", args=[1])
        expected_url = "/api/cities/1/"

        # Then
        self.assertEqual(url, expected_url)
