"""
Tests for secure multi-tenant API views.

Tests cover:
- Authentication requirements
- Multi-tenant isolation
- Data validation
- Permission checks
- Company assignment
"""

from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status

from accounts.models import Company, Profile
from inventario.models.category import Category
from inventario.models.product import Product
from inventario.models.batch import Batch
from inventario.models.movement import Movement


class MultiTenantTestBase(TestCase):
    """Base class for multi-tenant tests."""

    def setUp(self):
        """Set up test data."""
        self.client = APIClient()
        
        # Create companies
        self.company_a = Company.objects.create(name="Company A")
        self.company_b = Company.objects.create(name="Company B")
        
        # Create users and profiles
        self.user_a = User.objects.create_user(
            username="user_a",
            email="user_a@company_a.com",
            password="password123"
        )
        self.profile_a = Profile.objects.create(
            user=self.user_a,
            company=self.company_a,
            role="ADMIN"
        )
        
        self.user_b = User.objects.create_user(
            username="user_b",
            email="user_b@company_b.com",
            password="password123"
        )
        self.profile_b = Profile.objects.create(
            user=self.user_b,
            company=self.company_b,
            role="ADMIN"
        )
        
        # Create test data for Company A
        self.category_a = Category.objects.create(
            name="Category A",
            slug="category-a",
            company=self.company_a
        )
        
        self.category_b_data = Category.objects.create(
            name="Category B",
            slug="category-b",
            company=self.company_b
        )
        
        self.product_a = Product.objects.create(
            name="Product A",
            slug="product-a",
            category=self.category_a,
            supplier="Supplier A",
            company=self.company_a
        )
        
        self.product_b = Product.objects.create(
            name="Product B",
            slug="product-b",
            category=self.category_b_data,
            supplier="Supplier B",
            company=self.company_b
        )


class CategoryAPIViewTests(MultiTenantTestBase):
    """Tests for CategoryAPIView."""

    def test_list_categories_for_company(self):
        """GET /categories/ lists only company categories."""
        self.client.force_authenticate(user=self.user_a)
        response = self.client.get("/api/categories/")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Category A")

    def test_list_categories_no_cross_company(self):
        """User A doesn't see Company B categories."""
        self.client.force_authenticate(user=self.user_a)
        response = self.client.get("/api/categories/")
        
        category_names = [c["name"] for c in response.data]
        self.assertNotIn("Category B", category_names)

    def test_create_category_assigns_company(self):
        """POST /categories/ automatically assigns company."""
        self.client.force_authenticate(user=self.user_a)
        data = {
            "name": "New Category",
            "slug": "new-category",
            "company": 999  # Try to assign different company
        }
        response = self.client.post("/api/categories/", data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["company"], self.company_a.id)

    def test_retrieve_category_own_company(self):
        """GET /categories/{id}/ works for own company."""
        self.client.force_authenticate(user=self.user_a)
        response = self.client.get(f"/api/categories/{self.category_a.id}/")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.category_a.id)

    def test_retrieve_category_other_company(self):
        """GET /categories/{id}/ returns 404 for other company."""
        self.client.force_authenticate(user=self.user_a)
        response = self.client.get(f"/api/categories/{self.category_b_data.id}/")
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_category_preserves_company(self):
        """PUT /categories/{id}/ preserves company."""
        self.client.force_authenticate(user=self.user_a)
        data = {
            "name": "Updated Category",
            "slug": "updated-category",
            "company": self.company_b.id
        }
        response = self.client.put(f"/api/categories/{self.category_a.id}/", data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["company"], self.company_a.id)

    def test_delete_category_own_company(self):
        """DELETE /categories/{id}/ works for own company."""
        self.client.force_authenticate(user=self.user_a)
        response = self.client.delete(f"/api/categories/{self.category_a.id}/")
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Category.objects.filter(id=self.category_a.id).exists())

    def test_delete_category_other_company(self):
        """DELETE /categories/{id}/ returns 404 for other company."""
        self.client.force_authenticate(user=self.user_a)
        response = self.client.delete(f"/api/categories/{self.category_b_data.id}/")
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Category.objects.filter(id=self.category_b_data.id).exists())


class ProductAPIViewTests(MultiTenantTestBase):
    """Tests for ProductAPIView."""

    def test_list_products_for_company(self):
        """GET /products/ lists only company products."""
        self.client.force_authenticate(user=self.user_a)
        response = self.client.get("/api/products/")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Product A")

    def test_list_products_no_cross_company(self):
        """User A doesn't see Company B products."""
        self.client.force_authenticate(user=self.user_a)
        response = self.client.get("/api/products/")
        
        product_names = [p["name"] for p in response.data]
        self.assertNotIn("Product B", product_names)

    def test_create_product_with_own_category(self):
        """POST /products/ works with own company category."""
        self.client.force_authenticate(user=self.user_a)
        data = {
            "name": "New Product",
            "slug": "new-product",
            "category": self.category_a.id,
            "supplier": "New Supplier",
            "company": 999  # Should be ignored
        }
        response = self.client.post("/api/products/", data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["company"], self.company_a.id)

    def test_create_product_with_other_company_category(self):
        """POST /products/ fails with other company category."""
        self.client.force_authenticate(user=self.user_a)
        data = {
            "name": "New Product",
            "slug": "new-product",
            "category": self.category_b_data.id,  # Company B category
            "supplier": "Supplier"
        }
        response = self.client.post("/api/products/", data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_product_own_company(self):
        """GET /products/{id}/ works for own company."""
        self.client.force_authenticate(user=self.user_a)
        response = self.client.get(f"/api/products/{self.product_a.id}/")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.product_a.id)

    def test_retrieve_product_other_company(self):
        """GET /products/{id}/ returns 404 for other company."""
        self.client.force_authenticate(user=self.user_a)
        response = self.client.get(f"/api/products/{self.product_b.id}/")
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_product_preserves_company(self):
        """PUT /products/{id}/ preserves company."""
        self.client.force_authenticate(user=self.user_a)
        data = {
            "name": "Updated Product",
            "slug": "updated-product",
            "category": self.category_a.id,
            "supplier": "Updated Supplier",
            "company": self.company_b.id
        }
        response = self.client.put(f"/api/products/{self.product_a.id}/", data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["company"], self.company_a.id)

    def test_delete_product_own_company(self):
        """DELETE /products/{id}/ works for own company."""
        self.client.force_authenticate(user=self.user_a)
        response = self.client.delete(f"/api/products/{self.product_a.id}/")
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(id=self.product_a.id).exists())


class BatchAPIViewTests(MultiTenantTestBase):
    """Tests for BatchAPIView."""

    def setUp(self):
        """Set up test data including batches."""
        super().setUp()
        self.batch_a = Batch.objects.create(
            product=self.product_a,
            quantity_received=100,
            quantity_available=100,
            purchase_price=10.00,
            expiration_date="2026-12-31",
            supplier="Supplier A"
        )

    def test_list_batches_for_company(self):
        """GET /batches/ lists batches for company products."""
        self.client.force_authenticate(user=self.user_a)
        response = self.client.get("/api/batches/")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_batches_no_cross_company(self):
        """User A doesn't see Company B batches."""
        batch_b = Batch.objects.create(
            product=self.product_b,
            quantity_received=50,
            quantity_available=50,
            purchase_price=20.00,
            expiration_date="2026-12-31",
            supplier="Supplier B"
        )
        
        self.client.force_authenticate(user=self.user_a)
        response = self.client.get("/api/batches/")
        
        self.assertEqual(len(response.data), 1)
        self.assertNotEqual(response.data[0]["id"], batch_b.id)

    def test_retrieve_batch_own_company(self):
        """GET /batches/{id}/ works for own company."""
        self.client.force_authenticate(user=self.user_a)
        response = self.client.get(f"/api/batches/{self.batch_a.id}/")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.batch_a.id)

    def test_delete_batch_own_company(self):
        """DELETE /batches/{id}/ works for own company."""
        self.client.force_authenticate(user=self.user_a)
        response = self.client.delete(f"/api/batches/{self.batch_a.id}/")
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Batch.objects.filter(id=self.batch_a.id).exists())


class MovementAPIViewTests(MultiTenantTestBase):
    """Tests for MovementAPIView."""

    def setUp(self):
        """Set up test data including movements."""
        super().setUp()
        self.batch_a = Batch.objects.create(
            product=self.product_a,
            quantity_received=100,
            quantity_available=100,
            purchase_price=10.00,
            expiration_date="2026-12-31",
            supplier="Supplier A"
        )
        
        self.movement_a = Movement.objects.create(
            batch=self.batch_a,
            movement_type="IN",
            quantity=100
        )

    def test_list_movements_for_company(self):
        """GET /movements/ lists movements for company batches."""
        self.client.force_authenticate(user=self.user_a)
        response = self.client.get("/api/movements/")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_movements_no_cross_company(self):
        """User A doesn't see Company B movements."""
        batch_b = Batch.objects.create(
            product=self.product_b,
            quantity_received=50,
            quantity_available=50,
            purchase_price=20.00,
            expiration_date="2026-12-31",
            supplier="Supplier B"
        )
        Movement.objects.create(
            batch=batch_b,
            movement_type="IN",
            quantity=50
        )
        
        self.client.force_authenticate(user=self.user_a)
        response = self.client.get("/api/movements/")
        
        self.assertEqual(len(response.data), 1)

    def test_retrieve_movement_own_company(self):
        """GET /movements/{id}/ works for own company."""
        self.client.force_authenticate(user=self.user_a)
        response = self.client.get(f"/api/movements/{self.movement_a.id}/")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.movement_a.id)

    def test_delete_movement_own_company(self):
        """DELETE /movements/{id}/ works for own company."""
        self.client.force_authenticate(user=self.user_a)
        response = self.client.delete(f"/api/movements/{self.movement_a.id}/")
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Movement.objects.filter(id=self.movement_a.id).exists())
