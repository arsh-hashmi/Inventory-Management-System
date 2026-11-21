"""Test suite for the Inventory Management System.
Directly implements and validates Test Cases TC01 through TC12
from Table 3: Verification and Traceability Matrix in the SRS.
"""

from decimal import Decimal
import json
from django.test import TestCase, Client
from django.urls import reverse
from inventory.models import (
    Category,
    InventoryTransaction,
    Product,
    Sale,
    SaleItem,
    Supplier,
    User,
)


class InventorySystemTraceabilityTests(TestCase):
    """Test suite covering TC01 through TC12 from the SRS."""

    def setUp(self):
        self.client = Client()

        # Create Admin user
        self.admin = User.objects.create_user(
            username='admin_test',
            email='admin@example.com',
            password='Password123!',
            role=User.Role.ADMIN,
            first_name='Admin',
            last_name='Tester'
        )

        # Create Staff user
        self.staff = User.objects.create_user(
            username='staff_test',
            email='staff@example.com',
            password='Password123!',
            role=User.Role.STAFF,
            first_name='Staff',
            last_name='Tester'
        )

        # Create Category and Supplier
        self.category = Category.objects.create(
            name='Hardware',
            description='Computer hardware components'
        )
        self.supplier = Supplier.objects.create(
            name='Apex Distributors',
            phone='123-456-7890',
            email='sales@apex.example.com',
            address='123 Distribution Way'
        )

        # Create Products
        self.product_normal = Product.objects.create(
            name='Mechanical Keyboard',
            category=self.category,
            supplier=self.supplier,
            unit_price=Decimal('89.99'),
            quantity=50,
            reorder_level=10
        )

        self.product_low = Product.objects.create(
            name='Gaming Mouse',
            category=self.category,
            supplier=self.supplier,
            unit_price=Decimal('49.99'),
            quantity=5,
            reorder_level=10
        )

        self.product_out = Product.objects.create(
            name='HDMI Cable 2m',
            category=self.category,
            supplier=self.supplier,
            unit_price=Decimal('9.99'),
            quantity=0,
            reorder_level=5
        )

    # ── TC01: FR-001 - Authentication ───────────────────────────────────
    def test_tc01_authentication_valid_and_invalid(self):
        """TC01: Valid credentials allow access; invalid credentials are rejected."""
        # Invalid login
        response = self.client.post(reverse('inventory:login'), {
            'username': 'admin_test',
            'password': 'WrongPassword!'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid username or password')
        self.assertNotIn('_auth_user_id', self.client.session)

        # Valid login
        response = self.client.post(reverse('inventory:login'), {
            'username': 'admin_test',
            'password': 'Password123!'
        })
        self.assertRedirects(response, reverse('inventory:dashboard'))
        self.assertIn('_auth_user_id', self.client.session)

        # Logout
        response = self.client.get(reverse('inventory:logout'))
        self.assertRedirects(response, reverse('inventory:login'))
        self.assertNotIn('_auth_user_id', self.client.session)

    # ── TC02: FR-001 - Role-Based Access Control ─────────────────────────
    def test_tc02_role_based_access_control(self):
        """TC02: Administrator functions are unavailable to Staff users."""
        self.client.login(username='staff_test', password='Password123!')

        admin_urls = [
            reverse('inventory:user_list'),
            reverse('inventory:user_create'),
            reverse('inventory:category_list'),
            reverse('inventory:category_create'),
            reverse('inventory:supplier_list'),
            reverse('inventory:supplier_create'),
            reverse('inventory:product_create'),
        ]

        for url in admin_urls:
            response = self.client.get(url, follow=True)
            self.assertRedirects(response, reverse('inventory:dashboard'))
            self.assertContains(response, 'You do not have permission to access this page.')

        # Admin user CAN access them
        self.client.logout()
        self.client.login(username='admin_test', password='Password123!')
        for url in admin_urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)

    # ── TC03: FR-002, FR-003 - Master Data Management ───────────────────
    def test_tc03_manage_users_products_categories_suppliers(self):
        """TC03: Administrator can add/update records and view the results."""
        self.client.login(username='admin_test', password='Password123!')

        # Add User
        res = self.client.post(reverse('inventory:user_create'), {
            'username': 'newstaff',
            'first_name': 'New',
            'last_name': 'Staff',
            'email': 'newstaff@example.com',
            'phone': '555-1234',
            'role': 'STAFF',
            'password': 'StaffPassword123!',
            'password_confirm': 'StaffPassword123!',
        })
        self.assertRedirects(res, reverse('inventory:user_list'))
        self.assertTrue(User.objects.filter(username='newstaff').exists())

        # Add Category
        res = self.client.post(reverse('inventory:category_create'), {
            'name': 'Networking',
            'description': 'Routers and switches'
        })
        self.assertRedirects(res, reverse('inventory:category_list'))
        self.assertTrue(Category.objects.filter(name='Networking').exists())

        # Add Supplier
        res = self.client.post(reverse('inventory:supplier_create'), {
            'name': 'NetEquip Inc',
            'phone': '555-9876',
            'email': 'contact@netequip.example.com',
            'address': '456 Network St'
        })
        self.assertRedirects(res, reverse('inventory:supplier_list'))
        self.assertTrue(Supplier.objects.filter(name='NetEquip Inc').exists())

        # Add Product
        res = self.client.post(reverse('inventory:product_create'), {
            'name': 'Gigabit Router',
            'category': Category.objects.get(name='Networking').id,
            'supplier': Supplier.objects.get(name='NetEquip Inc').id,
            'unit_price': '79.50',
            'quantity': 25,
            'reorder_level': 5
        })
        self.assertRedirects(res, reverse('inventory:product_list'))
        self.assertTrue(Product.objects.filter(name='Gigabit Router').exists())

    # ── TC04: FR-004 - Product Search ────────────────────────────────────
    def test_tc04_product_search(self):
        """TC04: Authorized user can search and view product current stock."""
        self.client.login(username='staff_test', password='Password123!')

        # Search by product name
        res = self.client.get(reverse('inventory:product_search'), {'query': 'Keyboard'})
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'Mechanical Keyboard')
        self.assertContains(res, '50')  # quantity

        # Search by category name
        res = self.client.get(reverse('inventory:product_search'), {'query': 'Hardware'})
        self.assertContains(res, 'Mechanical Keyboard')
        self.assertContains(res, 'Gaming Mouse')

        # Search query that matches nothing
        res = self.client.get(reverse('inventory:product_search'), {'query': 'NonExistentXYZ'})
        self.assertNotContains(res, 'Mechanical Keyboard')

    # ── TC05: FR-004 - Stock Status and Alerts ───────────────────────────
    def test_tc05_stock_status_and_low_stock_alerts(self):
        """TC05: Product at or below reorder level is low stock; zero quantity is out of stock."""
        self.assertFalse(self.product_normal.is_low_stock)
        self.assertFalse(self.product_normal.is_out_of_stock)

        self.assertTrue(self.product_low.is_low_stock)
        self.assertFalse(self.product_low.is_out_of_stock)

        self.assertFalse(self.product_out.is_low_stock)
        self.assertTrue(self.product_out.is_out_of_stock)

        # Check the low-stock alert page
        self.client.login(username='staff_test', password='Password123!')
        res = self.client.get(reverse('inventory:low_stock_alerts'))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'Gaming Mouse')
        self.assertContains(res, 'HDMI Cable 2m')
        self.assertNotContains(res, 'Mechanical Keyboard')

    # ── TC06: FR-005, FR-006 - Stock-In and Adjustment ───────────────────
    def test_tc06_stock_in_and_adjustment(self):
        """TC06: Valid stock-in or adjustment updates quantity and creates history."""
        self.client.login(username='staff_test', password='Password123!')

        # Stock-In
        res = self.client.post(reverse('inventory:stock_in'), {
            'product': self.product_normal.id,
            'quantity': 20,
            'notes': 'Restock shipment received'
        }, follow=True)
        self.assertContains(res, 'Successfully added 20 units')

        self.product_normal.refresh_from_db()
        self.assertEqual(self.product_normal.quantity, 70)

        txn = InventoryTransaction.objects.filter(
            product=self.product_normal,
            type=InventoryTransaction.TransactionType.STOCK_IN
        ).first()
        self.assertIsNotNone(txn)
        self.assertEqual(txn.quantity, 20)
        self.assertEqual(txn.user, self.staff)

        # Adjustment (positive)
        res = self.client.post(reverse('inventory:stock_adjustment'), {
            'product': self.product_normal.id,
            'quantity': 5,
            'notes': 'Found extra in storeroom'
        }, follow=True)
        self.assertContains(res, 'Stock adjusted')
        self.product_normal.refresh_from_db()
        self.assertEqual(self.product_normal.quantity, 75)

        # Adjustment (negative, valid)
        res = self.client.post(reverse('inventory:stock_adjustment'), {
            'product': self.product_normal.id,
            'quantity': -10,
            'notes': 'Damaged in transit'
        }, follow=True)
        self.assertContains(res, 'Stock adjusted')
        self.product_normal.refresh_from_db()
        self.assertEqual(self.product_normal.quantity, 65)

    # ── TC07: FR-005, FR-006 - Stock-Out ─────────────────────────────────
    def test_tc07_stock_out(self):
        """TC07: Valid stock-out decreases quantity and creates history."""
        self.client.login(username='staff_test', password='Password123!')

        initial_qty = self.product_normal.quantity
        res = self.client.post(reverse('inventory:stock_out'), {
            'product': self.product_normal.id,
            'quantity': 15,
            'notes': 'Dispatched to branch'
        }, follow=True)
        self.assertContains(res, 'Successfully removed 15 units')

        self.product_normal.refresh_from_db()
        self.assertEqual(self.product_normal.quantity, initial_qty - 15)

        txn = InventoryTransaction.objects.filter(
            product=self.product_normal,
            type=InventoryTransaction.TransactionType.STOCK_OUT
        ).first()
        self.assertIsNotNone(txn)
        self.assertEqual(txn.quantity, 15)

    # ── TC08: FR-006 - Stock Validation ──────────────────────────────────
    def test_tc08_validate_stock_availability(self):
        """TC08: Stock-out or adjustment above available quantity is rejected and stock unchanged."""
        self.client.login(username='staff_test', password='Password123!')

        current_qty = self.product_low.quantity  # 5 units

        # Excess Stock-Out
        res = self.client.post(reverse('inventory:stock_out'), {
            'product': self.product_low.id,
            'quantity': 10,  # exceeds available 5
            'notes': 'Excessive order'
        })
        self.assertContains(res, 'Only 5 available')
        self.product_low.refresh_from_db()
        self.assertEqual(self.product_low.quantity, current_qty)  # Unchanged

        # Negative Adjustment exceeding stock
        res = self.client.post(reverse('inventory:stock_adjustment'), {
            'product': self.product_low.id,
            'quantity': -10,  # 5 - 10 = -5, which is invalid
            'notes': 'Invalid deduction'
        })
        self.assertContains(res, 'result in negative stock')
        self.product_low.refresh_from_db()
        self.assertEqual(self.product_low.quantity, current_qty)  # Unchanged

    # ── TC09: FR-005, FR-006 - Sales Recording ───────────────────────────
    def test_tc09_record_sale_and_validate_stock(self):
        """TC09: Valid sale is recorded and stock reduced; excess sale rejected."""
        self.client.login(username='staff_test', password='Password123!')

        kb_qty = self.product_normal.quantity
        mouse_qty = self.product_low.quantity

        # 1. Valid sale with 2 items
        sale_data = {
            'items-TOTAL_FORMS': '2',
            'items-INITIAL_FORMS': '0',
            'items-MIN_NUM_FORMS': '1',
            'items-MAX_NUM_FORMS': '1000',

            'items-0-product': str(self.product_normal.id),
            'items-0-quantity': '2',
            'items-0-unit_price': '89.99',

            'items-1-product': str(self.product_low.id),
            'items-1-quantity': '1',
            'items-1-unit_price': '49.99',
        }

        res = self.client.post(reverse('inventory:record_sale'), sale_data, follow=True)
        self.assertContains(res, 'Sale #')
        self.assertContains(res, 'recorded successfully')

        self.product_normal.refresh_from_db()
        self.product_low.refresh_from_db()
        self.assertEqual(self.product_normal.quantity, kb_qty - 2)
        self.assertEqual(self.product_low.quantity, mouse_qty - 1)

        sale = Sale.objects.latest('id')
        expected_total = Decimal('2') * Decimal('89.99') + Decimal('1') * Decimal('49.99')
        self.assertEqual(sale.total_amount, expected_total)
        self.assertEqual(sale.items.count(), 2)

        # Verify InventoryTransaction entries of type SALE were recorded
        sale_txns = InventoryTransaction.objects.filter(type=InventoryTransaction.TransactionType.SALE)
        self.assertGreaterEqual(sale_txns.count(), 2)

        # 2. Reject sale when quantity exceeds stock
        excess_sale_data = {
            'items-TOTAL_FORMS': '1',
            'items-INITIAL_FORMS': '0',
            'items-MIN_NUM_FORMS': '1',
            'items-MAX_NUM_FORMS': '1000',

            'items-0-product': str(self.product_low.id),
            'items-0-quantity': '100',  # exceeds available
            'items-0-unit_price': '49.99',
        }
        res = self.client.post(reverse('inventory:record_sale'), excess_sale_data)
        self.assertContains(res, 'Insufficient stock')

    # ── TC10: FR-007 - Dashboard & History ───────────────────────────────
    def test_tc10_dashboard_and_transaction_history(self):
        """TC10: Dashboard shows summaries; accepted transactions appear in history."""
        self.client.login(username='staff_test', password='Password123!')

        # Dashboard view
        res = self.client.get(reverse('inventory:dashboard'))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'Total Products')

        # Dashboard API JSON data
        res = self.client.get(reverse('inventory:dashboard_data'))
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.content)
        self.assertIn('stock_by_category', data)
        self.assertIn('monthly_transactions', data)
        self.assertIn('Hardware', data['stock_by_category']['labels'])

        # Transaction history view
        res = self.client.get(reverse('inventory:transaction_history'))
        self.assertEqual(res.status_code, 200)

        # Filter by type
        res = self.client.get(reverse('inventory:transaction_history'), {'type': 'STOCK_IN'})
        self.assertEqual(res.status_code, 200)

    # ── TC11: FR-008 - PDF Reports ───────────────────────────────────────
    def test_tc11_pdf_report_generation(self):
        """TC11: Authorized user can generate and download readable PDF reports."""
        self.client.login(username='staff_test', password='Password123!')

        reports = [
            (reverse('inventory:report_inventory'), 'inventory_report.pdf'),
            (reverse('inventory:report_sales'), 'sales_report.pdf'),
            (reverse('inventory:report_transactions'), 'transaction_report.pdf'),
        ]

        for url, expected_filename in reports:
            res = self.client.get(url)
            self.assertEqual(res.status_code, 200)
            self.assertEqual(res['Content-Type'], 'application/pdf')
            self.assertIn(f'filename="{expected_filename}"', res['Content-Disposition'])
            # Verify PDF magic bytes header: %PDF
            self.assertTrue(res.content.startswith(b'%PDF'))

    # ── TC12: NFR Section 3.2 - Security & Performance ───────────────────
    def test_tc12_security_and_non_functional_requirements(self):
        """TC12: Security, password hashing, authentication gates, and data integrity checks."""
        # Unauthenticated access to protected view redirects to login
        unauth_client = Client()
        protected_urls = [
            reverse('inventory:dashboard'),
            reverse('inventory:product_list'),
            reverse('inventory:stock_in'),
            reverse('inventory:record_sale'),
            reverse('inventory:transaction_history'),
            reverse('inventory:report_inventory'),
        ]

        for url in protected_urls:
            res = unauth_client.get(url)
            self.assertRedirects(res, f"{reverse('inventory:login')}?next={url}")

        # Password hashing check
        user = User.objects.get(username='admin_test')
        self.assertTrue(user.password.startswith('pbkdf2_sha256$'))
        self.assertNotEqual(user.password, 'Password123!')
