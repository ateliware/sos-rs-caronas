from unittest import TestCase

from django.urls import reverse


class FakeCitiesRoutesTest(TestCase):
    def test_fake_cities_url_resolves(self):
        # Given
        url = reverse("fake-cities")
        expected_url = "/api/fake-cities/"

        # Then
        self.assertEqual(url, expected_url)
