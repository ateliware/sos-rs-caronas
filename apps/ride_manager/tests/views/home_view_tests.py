from django.test import RequestFactory
from django.urls import reverse

from apps.core.tests.base_test import BaseTest
from apps.ride_manager.tests.factories.passenger_factory import PassengerFactory
from apps.ride_manager.tests.factories.person_factory import PersonFactory
from apps.ride_manager.tests.factories.ride_factory import RideFactory
from apps.ride_manager.enums.passenger_status_choices import (
    PassengerStatusChoices,
)


class HomeViewTests(BaseTest):
    def setUp(self):
        super().setUp()
        self.client_factory = RequestFactory()
        self.url = reverse("home")

    def test_standard_view_context(self):
        # Given in setUp

        # When
        response = self.view_client.get(self.url)
        response_context = response.context

        # Then
        self.assertFalse(response_context.get("show_caution_modal"))
        self.assertFalse(response_context.get("need_evaluation"))

    def test_context_needs_evaluation_is_true(self):
        # Given
        person = PersonFactory(user=self.user)
        ride = RideFactory(driver=person)
        passenger = PassengerFactory(
            ride=ride,
            is_driver=False,
            status=PassengerStatusChoices.PENDING,
        )

        # When
        response = self.view_client.get(self.url)
        response_context = response.context

        # Then
        self.assertTrue(response_context.get("need_evaluation"))
