import unittest

from app import app


class AppRouteTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_index_route_loads(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Startup Blueprint", response.data)

    def test_api_requires_both_inputs(self):
        response = self.client.post("/api/plan", json={"industry": "saas"})
        self.assertEqual(response.status_code, 400)

    def test_api_returns_plan(self):
        response = self.client.post("/api/plan", json={"industry": "saas", "country": "India"})
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertEqual(len(payload["yearly_plan"]), 5)
        self.assertEqual(payload["matched_profiles"]["industry_name"], "B2B SaaS")


if __name__ == "__main__":
    unittest.main()
