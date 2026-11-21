# Inventory Management System (IMS)

A centralized, responsive web-based platform for managing products, categories, suppliers, stock movements, sales transactions, audit histories, low-stock alerts, analytics dashboards, and PDF reports.

Built strictly according to the **Software Requirements Specification (SRS)** using **Python 3**, **Django**, **Bootstrap 5**, **Chart.js**, and **ReportLab**.

---

## 🌟 Key Features

| Requirement | Description | Status |
| :--- | :--- | :---: |
| **FR-001: Authentication & RBAC** | Secure authentication with PBKDF2 hashing. Distinct roles for **Administrator** and **Staff** with permission decorators. | ✅ |
| **FR-002: User Account Management** | Administrators can create and update user accounts and assign roles. | ✅ |
| **FR-003: Master Data Management** | Full CRUD for Products, Categories, and Suppliers with relational integrity. | ✅ |
| **FR-004: Search & Stock Status** | Real-time multi-attribute search. Automatic identification of **Low Stock** (<= reorder level) and **Out of Stock** (== 0). | ✅ |
| **FR-005: Transactions** | Stock-In, Stock-Out, authorized Stock Adjustments (+/-), and multi-item Sales. | ✅ |
| **FR-006: Stock Validation** | Atomic database transactions prevent negative stock and reject excess stock-out/sales requests. | ✅ |
| **FR-007: Dashboard & History** | Analytics dashboard with Chart.js charts (Category distribution, Monthly transaction trends), KPI cards, and filterable transaction history. | ✅ |
| **FR-008: PDF Report Generation** | Downloadable, professional PDF reports for Inventory, Sales, and Transaction history powered by ReportLab. | ✅ |

---

## 🛠️ Technology Stack

- **Backend Logic:** Python 3.10+ / Django
- **Database:** SQLite (default for development; production ready for MySQL)
- **Frontend / UI:** HTML5, CSS3, JavaScript, Bootstrap 5, Font Awesome 6
- **Data Visualizations:** Chart.js 4.x
- **PDF Engine:** ReportLab

---

## 📂 Project Structure

```text
inventory_management_system/
├── IMS_SRS.md                          # Full SRS documentation in Markdown
├── README.md                           # Project overview & running instructions
├── requirements.txt                    # Python dependencies
├── manage.py                           # Django CLI entrypoint
├── db.sqlite3                          # SQLite database (with seeded data)
├── ims_project/                        # Django project configuration
│   ├── __init__.py
│   ├── settings.py                     # Custom User, Apps, Static, Templates config
│   ├── urls.py                         # Root URL routing
│   └── wsgi.py
├── inventory/                          # Core inventory application
│   ├── admin.py                        # Django Admin integration
│   ├── apps.py
│   ├── decorators.py                   # @admin_required permission decorator
│   ├── forms.py                        # Django forms and formsets
│   ├── models.py                       # 7 Relational entities (User, Product, Sale, etc.)
│   ├── reports.py                      # ReportLab PDF generators
│   ├── tests.py                        # Test suite verifying TC01 through TC12
│   ├── urls.py                         # Application URL routing
│   ├── views.py                        # Business logic, stock validation & dashboard API
│   ├── management/
│   │   └── commands/
│   │       └── seed_data.py            # Sample data seeder
│   ├── templatetags/
│   │   └── inventory_tags.py           # Badge filters for status and roles
│   └── templates/inventory/            # Bootstrap 5 HTML templates
│       ├── base.html                   # Master layout with responsive navbar & alerts
│       ├── login.html                  # Styled login portal
│       ├── dashboard.html              # Analytics & KPI cards
│       ├── user_list.html & user_form.html
│       ├── category_list.html & category_form.html
│       ├── supplier_list.html & supplier_form.html
│       ├── product_list.html & product_form.html
│       ├── product_search.html
│       ├── stock_in.html
│       ├── stock_out.html
│       ├── stock_adjustment.html
│       ├── record_sale.html            # Dynamic multi-item sales invoice form
│       ├── transaction_history.html    # Filterable audit log
│       └── low_stock_alerts.html       # Visual warnings
└── static/
    ├── css/
    │   └── style.css                   # Custom theme styling & badges
    └── js/
        ├── dashboard.js                # Chart.js asynchronous fetch & render
        └── sale.js                     # Dynamic line item calculation
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- Python 3.10+ installed
- Git (optional)

### 2. Setup Virtual Environment (Optional but Recommended)
```bash
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Apply Migrations & Seed Data
```bash
python manage.py migrate
python manage.py seed_data
```

### 5. Start the Development Server
```bash
python manage.py runserver
```
Visit **`http://127.0.0.1:8000/`** in your browser.

---

## 🔑 Default Credentials

The database seeder automatically creates the following test accounts:

| Role | Username | Password | Access Privileges |
| :--- | :--- | :--- | :--- |
| **Administrator** | `admin` | `admin123` | Full access: Users, Categories, Suppliers, Products CRUD, Stock Ops, Sales, Reports, Admin Panel |
| **Inventory Staff** | `staff` | `staff123` | Operational access: Products Search, Stock In / Out / Adjust, Record Sales, History, Reports, Alerts |

---

## 🧪 Verification and Traceability (SRS Matrix)

To execute the automated verification test suite verifying all acceptance criteria (`TC01` to `TC12` from Section 5.3 of the SRS):

```bash
python manage.py test inventory
```

Tests verified:
- **TC01:** Authentication validation and rejection of invalid credentials.
- **TC02:** Role-based access control protecting administrative endpoints from staff.
- **TC03:** User, Product, Category, and Supplier master data CRUD operations.
- **TC04:** Product search with multi-field queries.
- **TC05:** Accurate stock status calculations (In Stock, Low Stock, Out of Stock).
- **TC06:** Stock-In and adjustment audit log generation and inventory incrementation.
- **TC07:** Stock-Out quantity deduction and acting user tracking.
- **TC08:** Rejection of requests exceeding available stock.
- **TC09:** Atomic multi-item sales processing with synchronized stock reduction.
- **TC10:** Dynamic dashboard KPI calculation and transaction history filtering.
- **TC11:** Pixel-formatted PDF report generation (Inventory, Sales, Transactions).
- **TC12:** Security gates, password hashing, and non-functional requirements.

---

## 📄 Documentation

The complete specifications, diagrams (Architecture, ER, Use Case, DFD 0/1, Class, Activity, and Sequence Diagrams), and traceability tables are converted to Markdown in:
👉 **[`IMS_SRS.md`](IMS_SRS.md)**
