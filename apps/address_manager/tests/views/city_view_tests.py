from apps.address_manager.tests.factories import CityFactory, StateFactory
from apps.core.tests.base_test import BaseTest

BASE_TEST_ENDPOINT = "/city/"


class CityViewTests(BaseTest):
    def test_get_city_list(self):
        # Given
        state = StateFactory()
        city = CityFactory(state=state)

        # When
        response = self.client.get(BASE_TEST_ENDPOINT)

        # Then
        response_context = response.context
        cities_response_obj = response_context["cities"][0]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_context["cities"]), 1)
        self.assertEqual(cities_response_obj.id, city.id)
        self.assertEqual(cities_response_obj.name, city.name)
        self.assertEqual(cities_response_obj.state.id, state.id)
        self.assertEqual(cities_response_obj.state.name, state.name)
        self.assertEqual(cities_response_obj.state.code, state.code)
