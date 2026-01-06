from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from myapp.models import Food, Consume


class HomeViewTests(TestCase):
    def test_home_renders_template(self):
        url = reverse("home")  # make sure your urls.py has name="home"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "myapp/home2.html")


class IndexViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword123",
        )
        self.client.login(username="testuser", password="testpassword123")

        # Create some Food objects with all required fields
        self.food1 = Food.objects.create(
            name="Apple",
            carbs=10.0,
            protein=0.5,
            fats=0.2,
            calories=52,
        )
        self.food2 = Food.objects.create(
            name="Banana",
            carbs=23.0,
            protein=1.3,
            fats=0.3,
            calories=96,
        )

        self.index_url = reverse("index")  # ensure urls.py has name="index"

    def test_index_requires_login(self):
        self.client.logout()
        response = self.client.get(self.index_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.url.lower())

    def test_index_get_shows_foods_and_consumed_food(self):
        # one consumed item for this user
        Consume.objects.create(user=self.user, food_consumed=self.food1)

        response = self.client.get(self.index_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "myapp/index.html")

        # Foods list should contain both foods
        self.assertIn(self.food1, response.context["foods"])
        self.assertIn(self.food2, response.context["foods"])

        consumed_food_qs = response.context["consumed_food"]
        self.assertEqual(consumed_food_qs.count(), 1)
        self.assertEqual(consumed_food_qs.first().food_consumed, self.food1)
        self.assertEqual(consumed_food_qs.first().user, self.user)

    def test_index_post_creates_consume_record(self):
        response = self.client.post(
            self.index_url,
            {"food_consumed": self.food2.name},
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            Consume.objects.filter(user=self.user, food_consumed=self.food2).exists()
        )

        self.assertIn(self.food2, response.context["foods"])
        consumed_food_qs = response.context["consumed_food"]
        self.assertEqual(consumed_food_qs.count(), 1)
        self.assertEqual(consumed_food_qs.first().food_consumed, self.food2)
        self.assertEqual(consumed_food_qs.first().user, self.user)
