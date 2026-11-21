"""Management command to seed the database with computer hardware inventory data in Indian Rupees (₹)."""

from decimal import Decimal
from django.core.management.base import BaseCommand
from inventory.models import (
    Category, InventoryTransaction, Product, Sale, SaleItem, Supplier, User,
)


class Command(BaseCommand):
    help = 'Seed the database with computer products, categories, suppliers, and transactions in Rupees (₹).'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing products, categories, suppliers, transactions, and sales before seeding.',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Seeding database with Computer Hardware Inventory...'))

        # Clear old catalog if requested or by default clean old demo items
        if options.get('clear', True):
            SaleItem.objects.all().delete()
            Sale.objects.all().delete()
            InventoryTransaction.objects.all().delete()
            Product.objects.all().delete()
            Category.objects.all().delete()
            Supplier.objects.all().delete()
            self.stdout.write(self.style.WARNING('  Cleared existing catalog data.'))

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
            self.stdout.write('  Admin user verified.')

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
            self.stdout.write('  Staff user verified.')

        # ── Computer Categories ───────────────────────────────────
        categories_data = [
            ('Laptops & Desktops', 'High-performance laptops, ultrabooks, workstations, and all-in-one desktop PCs'),
            ('Computer Peripherals', 'Keyboards, gaming mice, 4K webcams, audio headsets, and input devices'),
            ('PC Components & Storage', 'CPUs, graphics cards, motherboards, DDR5 RAM, and high-speed NVMe PCIe SSDs'),
            ('Networking & Connectivity', 'Wi-Fi 6E routers, gigabit managed switches, network adapters, and Ethernet cables'),
            ('Displays & Monitors', 'High refresh-rate gaming monitors, 4K IPS HDR displays, and workstation monitors'),
        ]
        categories = {}
        for name, desc in categories_data:
            cat, _ = Category.objects.get_or_create(name=name, defaults={'description': desc})
            categories[name] = cat
        self.stdout.write(self.style.SUCCESS(f'  Categories: {len(categories)}'))

        # ── Computer Hardware Suppliers ───────────────────────────
        suppliers_data = [
            ('Apex Computer Distributors', '+91 98200 11223', 'sales@apexcomputers.in', 'Nehru Place Hardware Market, New Delhi, India'),
            ('Silicon Valley Peripherals Ltd', '+91 98450 33445', 'orders@siliconperipherals.com', 'SP Road Electronic Zone, Bengaluru, Karnataka, India'),
            ('GigaTech Components & Solutions', '+91 98310 55667', 'supply@gigatechindia.com', 'Lamington Road IT Hub, Mumbai, Maharashtra, India'),
            ('NetConnect Infrastructure Co', '+91 98840 77889', 'wholesale@netconnect.co.in', 'Ritchie Street IT Park, Chennai, Tamil Nadu, India'),
            ('UltraVision Displays India', '+91 98765 99001', 'distribution@ultravision.in', 'Cyber City Tech Corridor, Hyderabad, Telangana, India'),
        ]
        suppliers = {}
        for name, phone, email, address in suppliers_data:
            sup, _ = Supplier.objects.get_or_create(
                name=name,
                defaults={'phone': phone, 'email': email, 'address': address},
            )
            suppliers[name] = sup
        self.stdout.write(self.style.SUCCESS(f'  Suppliers: {len(suppliers)}'))

        # ── Computer Products (Priced in Indian Rupees ₹) ────────
        products_data = [
            # Laptops & Desktops
            ('Dell XPS 15 Laptop (Intel i9, 32GB RAM, 1TB SSD)', 'Laptops & Desktops', 'Apex Computer Distributors', '149999.00', 12, 3),
            ('HP Pavilion Gaming Desktop (Ryzen 7, RTX 4060)', 'Laptops & Desktops', 'Apex Computer Distributors', '84999.00', 8, 2),
            ('Lenovo ThinkPad X1 Carbon Ultrabook 14"', 'Laptops & Desktops', 'Apex Computer Distributors', '124999.00', 0, 3),

            # Computer Peripherals
            ('Logitech MX Master 3S Wireless Mouse', 'Computer Peripherals', 'Silicon Valley Peripherals Ltd', '8995.00', 45, 10),
            ('Corsair K70 RGB Mechanical Gaming Keyboard', 'Computer Peripherals', 'Silicon Valley Peripherals Ltd', '12499.00', 25, 8),
            ('Logitech Brio 4K Ultra HD Pro Webcam', 'Computer Peripherals', 'Silicon Valley Peripherals Ltd', '16995.00', 4, 10),
            ('SteelSeries Arctis Nova Pro Wireless Headset', 'Computer Peripherals', 'Silicon Valley Peripherals Ltd', '28999.00', 6, 5),

            # PC Components & Storage
            ('Samsung 990 PRO 2TB NVMe PCIe 4.0 SSD', 'PC Components & Storage', 'GigaTech Components & Solutions', '17499.00', 30, 8),
            ('Kingston Fury Beast 32GB (2x16GB) DDR5 6000MHz RAM', 'PC Components & Storage', 'GigaTech Components & Solutions', '10499.00', 50, 15),
            ('ASUS ROG Strix GeForce RTX 4070 Ti Super 16GB', 'PC Components & Storage', 'GigaTech Components & Solutions', '84999.00', 5, 5),
            ('MSI MAG B650 Tomahawk WiFi Motherboard', 'PC Components & Storage', 'GigaTech Components & Solutions', '21999.00', 18, 5),
            ('Corsair RM850x 850W 80+ Gold Fully Modular PSU', 'PC Components & Storage', 'GigaTech Components & Solutions', '11999.00', 0, 5),
            ('Western Digital 4TB Red Plus NAS Internal HDD', 'PC Components & Storage', 'GigaTech Components & Solutions', '9499.00', 22, 6),

            # Networking & Connectivity
            ('TP-Link Archer AXE75 Tri-Band Wi-Fi 6E Router', 'Networking & Connectivity', 'NetConnect Infrastructure Co', '12999.00', 16, 5),
            ('Cisco CBS250 24-Port Gigabit Managed Switch', 'Networking & Connectivity', 'NetConnect Infrastructure Co', '24999.00', 2, 4),
            ('Cat6 RJ45 Gigabit Ethernet Patch Cable 10m', 'Networking & Connectivity', 'NetConnect Infrastructure Co', '499.00', 120, 30),

            # Displays & Monitors
            ('LG UltraGear 27" QHD 240Hz Nano IPS Gaming Monitor', 'Displays & Monitors', 'UltraVision Displays India', '32999.00', 15, 4),
            ('Dell UltraSharp 32" 4K USB-C Hub Monitor (U3223QE)', 'Displays & Monitors', 'UltraVision Displays India', '76999.00', 0, 2),
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

        # ── Sample Inventory Transactions ─────────────────────────
        txn_data = [
            ('Dell XPS 15 Laptop (Intel i9, 32GB RAM, 1TB SSD)', admin, 'STOCK_IN', 15, 'Direct import from OEM distributor'),
            ('Samsung 990 PRO 2TB NVMe PCIe 4.0 SSD', staff, 'STOCK_IN', 35, 'Bulk procurement for system integrations'),
            ('Logitech MX Master 3S Wireless Mouse', staff, 'STOCK_OUT', 5, 'Shipped to enterprise client order'),
            ('SteelSeries Arctis Nova Pro Wireless Headset', admin, 'ADJUSTMENT', -1, 'Defective packaging replaced via RMA'),
            ('TP-Link Archer AXE75 Tri-Band Wi-Fi 6E Router', staff, 'STOCK_IN', 20, 'Seasonal replenishment'),
            ('Cat6 RJ45 Gigabit Ethernet Patch Cable 10m', admin, 'STOCK_IN', 150, 'Standard cabling stock arrival'),
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

        # ── Sample Sale (in Indian Rupees ₹) ──────────────────────
        # Sale of 1 mouse (₹8,995), 1 SSD (₹17,499), and 2 Cat6 cables (2 * ₹499 = ₹998)
        # Total = ₹27,492.00
        total_sale_amount = Decimal('8995.00') + Decimal('17499.00') + (Decimal('499.00') * 2)
        sale = Sale.objects.create(user=admin, total_amount=total_sale_amount)

        SaleItem.objects.create(
            sale=sale, product=products['Logitech MX Master 3S Wireless Mouse'],
            quantity=1, unit_price=Decimal('8995.00'),
        )
        SaleItem.objects.create(
            sale=sale, product=products['Samsung 990 PRO 2TB NVMe PCIe 4.0 SSD'],
            quantity=1, unit_price=Decimal('17499.00'),
        )
        SaleItem.objects.create(
            sale=sale, product=products['Cat6 RJ45 Gigabit Ethernet Patch Cable 10m'],
            quantity=2, unit_price=Decimal('499.00'),
        )

        for item in sale.items.all():
            InventoryTransaction.objects.create(
                product=item.product,
                user=admin,
                type='SALE',
                quantity=item.quantity,
                notes=f'Sale #{sale.pk}',
            )
        self.stdout.write(self.style.SUCCESS(f'  Sales: 1 (Total: ₹{total_sale_amount:,.2f} with {sale.items.count()} items)'))

        self.stdout.write(self.style.SUCCESS('\nComputer Inventory Database seeded successfully!'))
        self.stdout.write(self.style.WARNING('\nDefault Credentials:'))
        self.stdout.write('  Admin: admin / admin123')
        self.stdout.write('  Staff: staff / staff123')
