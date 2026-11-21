"""Management command to seed the database with sample data."""

from decimal import Decimal
from django.core.management.base import BaseCommand
from inventory.models import (
    Category, InventoryTransaction, Product, Sale, SaleItem, Supplier, User,
)


class Command(BaseCommand):
    help = 'Seed the database with sample categories, suppliers, products, transactions, and users.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Seeding database...'))

        # ── Users ─────────────────────────────────────────────────
        admin, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'first_name': 'Admin',
                'last_name': 'User',
                'email': 'admin@ims.local',
                'role': 'ADMIN',
                'is_staff': True,
                'is_superuser': True,
            },
        )
        if created:
            admin.set_password('admin123')
            admin.save()
            self.stdout.write(self.style.SUCCESS('  Created admin user (admin / admin123)'))
        else:
            self.stdout.write('  Admin user already exists.')

        staff, created = User.objects.get_or_create(
            username='staff',
            defaults={
                'first_name': 'Staff',
                'last_name': 'Member',
                'email': 'staff@ims.local',
                'role': 'STAFF',
            },
        )
        if created:
            staff.set_password('staff123')
            staff.save()
            self.stdout.write(self.style.SUCCESS('  Created staff user (staff / staff123)'))
        else:
            self.stdout.write('  Staff user already exists.')

        # ── Categories ────────────────────────────────────────────
        categories_data = [
            ('Electronics', 'Electronic devices and accessories'),
            ('Furniture', 'Office and home furniture'),
            ('Office Supplies', 'Stationery, paper, and office essentials'),
            ('Clothing', 'Apparel and accessories'),
            ('Food & Beverages', 'Packaged food items and drinks'),
        ]
        categories = {}
        for name, desc in categories_data:
            cat, _ = Category.objects.get_or_create(name=name, defaults={'description': desc})
            categories[name] = cat
        self.stdout.write(self.style.SUCCESS(f'  Categories: {len(categories)}'))

        # ── Suppliers ─────────────────────────────────────────────
        suppliers_data = [
            ('TechWorld Distributors', '555-0101', 'sales@techworld.com', '123 Tech Blvd, Silicon Valley, CA'),
            ('FurniCraft Ltd.', '555-0202', 'orders@furnicraft.com', '456 Woodwork Ave, Portland, OR'),
            ('OfficeHub Supplies', '555-0303', 'supply@officehub.com', '789 Paper St, Chicago, IL'),
            ('StyleWear Inc.', '555-0404', 'wholesale@stylewear.com', '321 Fashion Dr, New York, NY'),
            ('FreshGoods Co.', '555-0505', 'orders@freshgoods.com', '654 Market St, San Francisco, CA'),
        ]
        suppliers = {}
        for name, phone, email, address in suppliers_data:
            sup, _ = Supplier.objects.get_or_create(
                name=name,
                defaults={'phone': phone, 'email': email, 'address': address},
            )
            suppliers[name] = sup
        self.stdout.write(self.style.SUCCESS(f'  Suppliers: {len(suppliers)}'))

        # ── Products ──────────────────────────────────────────────
        products_data = [
            ('Wireless Mouse', 'Electronics', 'TechWorld Distributors', '29.99', 150, 20),
            ('USB-C Hub', 'Electronics', 'TechWorld Distributors', '49.99', 8, 15),
            ('Bluetooth Keyboard', 'Electronics', 'TechWorld Distributors', '59.99', 45, 10),
            ('27" Monitor', 'Electronics', 'TechWorld Distributors', '299.99', 0, 5),
            ('Webcam HD', 'Electronics', 'TechWorld Distributors', '79.99', 3, 10),
            ('Office Desk', 'Furniture', 'FurniCraft Ltd.', '249.99', 12, 5),
            ('Ergonomic Chair', 'Furniture', 'FurniCraft Ltd.', '399.99', 7, 5),
            ('Filing Cabinet', 'Furniture', 'FurniCraft Ltd.', '129.99', 0, 3),
            ('Bookshelf', 'Furniture', 'FurniCraft Ltd.', '89.99', 20, 5),
            ('A4 Paper (500 sheets)', 'Office Supplies', 'OfficeHub Supplies', '8.99', 200, 50),
            ('Ballpoint Pens (box)', 'Office Supplies', 'OfficeHub Supplies', '12.99', 5, 20),
            ('Stapler', 'Office Supplies', 'OfficeHub Supplies', '15.99', 30, 10),
            ('Whiteboard Markers', 'Office Supplies', 'OfficeHub Supplies', '9.99', 0, 15),
            ('Cotton T-Shirt', 'Clothing', 'StyleWear Inc.', '19.99', 100, 25),
            ('Denim Jeans', 'Clothing', 'StyleWear Inc.', '49.99', 60, 15),
            ('Winter Jacket', 'Clothing', 'StyleWear Inc.', '89.99', 4, 10),
            ('Instant Coffee (jar)', 'Food & Beverages', 'FreshGoods Co.', '12.99', 50, 20),
            ('Bottled Water (pack)', 'Food & Beverages', 'FreshGoods Co.', '6.99', 2, 30),
        ]
        products = {}
        for name, cat_name, sup_name, price, qty, reorder in products_data:
            prod, _ = Product.objects.get_or_create(
                name=name,
                defaults={
                    'category': categories[cat_name],
                    'supplier': suppliers[sup_name],
                    'unit_price': Decimal(price),
                    'quantity': qty,
                    'reorder_level': reorder,
                },
            )
            products[name] = prod
        self.stdout.write(self.style.SUCCESS(f'  Products: {len(products)}'))

        # ── Sample Transactions ───────────────────────────────────
        txn_data = [
            ('Wireless Mouse', admin, 'STOCK_IN', 50, 'Initial bulk order'),
            ('USB-C Hub', staff, 'STOCK_OUT', 5, 'Shipped to branch office'),
            ('Bluetooth Keyboard', admin, 'ADJUSTMENT', -3, 'Damaged in warehouse'),
            ('Office Desk', staff, 'STOCK_IN', 10, 'New shipment arrived'),
            ('A4 Paper (500 sheets)', admin, 'STOCK_IN', 100, 'Monthly restock'),
            ('Cotton T-Shirt', staff, 'STOCK_OUT', 20, 'Retail fulfillment'),
        ]
        txn_count = 0
        for prod_name, user, txn_type, qty, notes in txn_data:
            InventoryTransaction.objects.create(
                product=products[prod_name],
                user=user,
                type=txn_type,
                quantity=qty,
                notes=notes,
            )
            txn_count += 1
        self.stdout.write(self.style.SUCCESS(f'  Transactions: {txn_count}'))

        # ── Sample Sale ───────────────────────────────────────────
        sale = Sale.objects.create(user=admin, total_amount=Decimal('109.97'))
        SaleItem.objects.create(
            sale=sale, product=products['Wireless Mouse'],
            quantity=2, unit_price=Decimal('29.99'),
        )
        SaleItem.objects.create(
            sale=sale, product=products['Ballpoint Pens (box)'],
            quantity=1, unit_price=Decimal('12.99'),
        )
        SaleItem.objects.create(
            sale=sale, product=products['Cotton T-Shirt'],
            quantity=1, unit_price=Decimal('19.99'),
        )
        # Record sale transactions
        for item in sale.items.all():
            InventoryTransaction.objects.create(
                product=item.product,
                user=admin,
                type='SALE',
                quantity=item.quantity,
                notes=f'Sale #{sale.pk}',
            )
        self.stdout.write(self.style.SUCCESS(f'  Sales: 1 (with {sale.items.count()} items)'))

        self.stdout.write(self.style.SUCCESS('\nDatabase seeded successfully!'))
        self.stdout.write(self.style.WARNING('\nDefault Credentials:'))
        self.stdout.write(f'  Admin: admin / admin123')
        self.stdout.write(f'  Staff: staff / staff123')
