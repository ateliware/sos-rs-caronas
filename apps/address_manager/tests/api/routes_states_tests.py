from unittest import TestCase

from django.urls import reverse


class StateRoutesTest(TestCase):
    def test_states_list_url_resolves(self):
        # Given
        url = reverse("states-list")
        expected_url = "/api/v1/states/"

        # Then
        self.assertEqual(url, expected_url)

    def test_states_detail_url_resolves(self):
        # Given
        url = reverse("states-detail", args=[1])
        expected_url = "/api/v1/states/1/"

        # Then
        self.assertEqual(url, expected_url)
