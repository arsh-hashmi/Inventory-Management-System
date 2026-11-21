"""URL configuration for the inventory app."""

from django.urls import path

from . import views

app_name = 'inventory'

urlpatterns = [
    # ── Authentication ─────────────────────────────────────────────────
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # ── Dashboard ──────────────────────────────────────────────────────
    path('', views.dashboard, name='dashboard'),
    path('dashboard/data/', views.dashboard_data, name='dashboard_data'),

    # ── User Management (Admin only) ──────────────────────────────────
    path('users/', views.user_list, name='user_list'),
    path('users/create/', views.user_create, name='user_create'),
    path('users/<int:pk>/update/', views.user_update, name='user_update'),

    # ── Category Management (Admin only) ──────────────────────────────
    path('categories/', views.category_list, name='category_list'),
    path('categories/create/', views.category_create, name='category_create'),
    path('categories/<int:pk>/update/', views.category_update, name='category_update'),

    # ── Supplier Management (Admin only) ──────────────────────────────
    path('suppliers/', views.supplier_list, name='supplier_list'),
    path('suppliers/create/', views.supplier_create, name='supplier_create'),
    path('suppliers/<int:pk>/update/', views.supplier_update, name='supplier_update'),

    # ── Product Management ────────────────────────────────────────────
    path('products/', views.product_list, name='product_list'),
    path('products/create/', views.product_create, name='product_create'),
    path('products/<int:pk>/update/', views.product_update, name='product_update'),
    path('products/search/', views.product_search, name='product_search'),

    # ── Stock Operations ──────────────────────────────────────────────
    path('stock/in/', views.stock_in, name='stock_in'),
    path('stock/out/', views.stock_out, name='stock_out'),
    path('stock/adjustment/', views.stock_adjustment, name='stock_adjustment'),

    # ── Sales ─────────────────────────────────────────────────────────
    path('sales/record/', views.record_sale, name='record_sale'),

    # ── Transaction History ───────────────────────────────────────────
    path('transactions/', views.transaction_history, name='transaction_history'),

    # ── Alerts ────────────────────────────────────────────────────────
    path('alerts/low-stock/', views.low_stock_alerts, name='low_stock_alerts'),

    # ── PDF Reports ───────────────────────────────────────────────────
    path('reports/inventory/', views.generate_inventory_report, name='report_inventory'),
    path('reports/sales/', views.generate_sales_report, name='report_sales'),
    path('reports/transactions/', views.generate_transaction_report, name='report_transactions'),
]
