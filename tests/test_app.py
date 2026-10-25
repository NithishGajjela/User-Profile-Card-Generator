import unittest

from app import app


class GenerateProfileTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_home_page_is_served(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"User Profile Card Generator", response.data)

    def test_valid_profile_is_processed(self):
        response = self.client.post(
            "/generate-profile",
            json={
                "name": "  Alex   Morgan ",
                "bio": "  Designer and maker. ",
                "image_url": "https://example.com/alex.jpg",
                "role": " Product Designer ",
                "skills": "Research, Figma, Prototyping",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_json()["profile"],
            {
                "name": "Alex Morgan",
                "bio": "Designer and maker.",
                "image_url": "https://example.com/alex.jpg",
                "role": "Product Designer",
                "skills": ["Research", "Figma", "Prototyping"],
            },
        )

    def test_missing_required_fields_returns_field_errors(self):
        response = self.client.post("/generate-profile", json={})
        self.assertEqual(response.status_code, 400)
        self.assertIn("name", response.get_json()["fields"])
        self.assertIn("bio", response.get_json()["fields"])

    def test_invalid_image_url_is_rejected(self):
        response = self.client.post(
            "/generate-profile",
            json={"name": "Alex", "bio": "Hello", "image_url": "javascript:alert(1)"},
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("image_url", response.get_json()["fields"])

    def test_length_limits_are_enforced(self):
        response = self.client.post(
            "/generate-profile",
            json={"name": "A" * 81, "bio": "Hello"},
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("name", response.get_json()["fields"])

    def test_non_json_request_is_rejected(self):
        response = self.client.post("/generate-profile", data="name=Alex")
        self.assertEqual(response.status_code, 415)

    def test_malformed_json_returns_json_error(self):
        response = self.client.post(
            "/generate-profile",
            data="{not valid json",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("valid JSON object", response.get_json()["error"])

    def test_invalid_url_port_is_rejected(self):
        response = self.client.post(
            "/generate-profile",
            json={
                "name": "Alex",
                "bio": "Hello",
                "image_url": "https://example.com:invalid/photo.jpg",
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("image_url", response.get_json()["fields"])


if __name__ == "__main__":
    unittest.main()
