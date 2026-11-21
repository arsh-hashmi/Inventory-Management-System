"""Views for the Inventory Management System.

Every view (except login) is protected by @login_required.
Admin-only views additionally use @admin_required.
"""

from datetime import datetime, timedelta
from decimal import Decimal

from django.utils import timezone

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import transaction as db_transaction
from django.db.models import Count, Q, Sum
from django.db.models.functions import TruncMonth
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .decorators import admin_required
from .forms import (
    CategoryForm,
    LoginForm,
    ProductForm,
    ProductSearchForm,
    SaleForm,
    SaleItemFormSet,
    StockAdjustmentForm,
    StockInForm,
    StockOutForm,
    SupplierForm,
    UserCreateForm,
    UserUpdateForm,
)
from .models import (
    Category,
    InventoryTransaction,
    Product,
    Sale,
    SaleItem,
    Supplier,
    User,
)
from .reports import (
    generate_inventory_pdf,
    generate_sales_pdf,
    generate_transaction_pdf,
)


# ═══════════════════════════════════════════════════════════════════════════
# Authentication
# ═══════════════════════════════════════════════════════════════════════════

def login_view(request):
    """Authenticate users and log them in."""
    if request.user.is_authenticated:
        return redirect('inventory:dashboard')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
                next_url = request.GET.get('next', 'inventory:dashboard')
                return redirect(next_url)
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()

    return render(request, 'inventory/login.html', {'form': form})


@login_required
def logout_view(request):
    """Log the user out and redirect to login page."""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('inventory:login')


# ═══════════════════════════════════════════════════════════════════════════
# Dashboard
# ═══════════════════════════════════════════════════════════════════════════

@login_required
def dashboard(request):
    """Display the main dashboard with summary statistics."""
    total_products = Product.objects.count()
    low_stock_count = Product.objects.filter(
        quantity__gt=0, quantity__lte=models_F_reorder()
    ).count()
    out_of_stock_count = Product.objects.filter(quantity=0).count()
    total_categories = Category.objects.count()
    total_suppliers = Supplier.objects.count()
    recent_transactions = InventoryTransaction.objects.select_related(
        'product', 'user',
    ).order_by('-date_time')[:10]

    context = {
        'total_products': total_products,
        'low_stock_count': low_stock_count,
        'out_of_stock_count': out_of_stock_count,
        'total_categories': total_categories,
        'total_suppliers': total_suppliers,
        'recent_transactions': recent_transactions,
    }
    return render(request, 'inventory/dashboard.html', context)


def models_F_reorder():
    """Return an F expression for reorder_level (helper to keep import tidy)."""
    from django.db.models import F
    return F('reorder_level')


@login_required
def dashboard_data(request):
    """Return JSON data consumed by Chart.js on the dashboard.

    Data includes:
    - stock_by_category: {labels: [...], data: [...]}
    - monthly_transactions: {labels: [...], data: [...]}
    """
    # Stock totals grouped by category
    category_data = (
        Product.objects
        .values('category__name')
        .annotate(total_qty=Sum('quantity'))
        .order_by('category__name')
    )
    stock_labels = [
        item['category__name'] or 'Uncategorised'
        for item in category_data
    ]
    stock_values = [item['total_qty'] or 0 for item in category_data]

    # Monthly transaction counts for the last 12 months
    twelve_months_ago = timezone.now() - timedelta(days=365)
    monthly_data = (
        InventoryTransaction.objects
        .filter(date_time__gte=twelve_months_ago)
        .annotate(month=TruncMonth('date_time'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )
    monthly_labels = [
        item['month'].strftime('%b %Y') for item in monthly_data
    ]
    monthly_values = [item['count'] for item in monthly_data]

    return JsonResponse({
        'stock_by_category': {
            'labels': stock_labels,
            'data': stock_values,
        },
        'monthly_transactions': {
            'labels': monthly_labels,
            'data': monthly_values,
        },
    })


# ═══════════════════════════════════════════════════════════════════════════
# User CRUD (Admin only)
# ═══════════════════════════════════════════════════════════════════════════

@login_required
@admin_required
def user_list(request):
    """List all users."""
    users = User.objects.all().order_by('username')
    return render(request, 'inventory/user_list.html', {'users': users})


@login_required
@admin_required
def user_create(request):
    """Create a new user."""
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User created successfully.')
            return redirect('inventory:user_list')
    else:
        form = UserCreateForm()
    return render(request, 'inventory/user_form.html', {'form': form, 'title': 'Create User'})


@login_required
@admin_required
def user_update(request, pk):
    """Update an existing user."""
    user_obj = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'User updated successfully.')
            return redirect('inventory:user_list')
    else:
        form = UserUpdateForm(instance=user_obj)
    return render(request, 'inventory/user_form.html', {'form': form, 'title': 'Update User'})


# ═══════════════════════════════════════════════════════════════════════════
# Category CRUD (Admin only)
# ═══════════════════════════════════════════════════════════════════════════

@login_required
@admin_required
def category_list(request):
    """List all categories."""
    categories = Category.objects.all()
    return render(request, 'inventory/category_list.html', {'categories': categories})


@login_required
@admin_required
def category_create(request):
    """Create a new category."""
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category created successfully.')
            return redirect('inventory:category_list')
    else:
        form = CategoryForm()
    return render(request, 'inventory/category_form.html', {'form': form, 'title': 'Create Category'})


@login_required
@admin_required
def category_update(request, pk):
    """Update an existing category."""
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully.')
            return redirect('inventory:category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'inventory/category_form.html', {'form': form, 'title': 'Update Category'})


# ═══════════════════════════════════════════════════════════════════════════
# Supplier CRUD (Admin only)
# ═══════════════════════════════════════════════════════════════════════════

@login_required
@admin_required
def supplier_list(request):
    """List all suppliers."""
    suppliers = Supplier.objects.all()
    return render(request, 'inventory/supplier_list.html', {'suppliers': suppliers})


@login_required
@admin_required
def supplier_create(request):
    """Create a new supplier."""
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Supplier created successfully.')
            return redirect('inventory:supplier_list')
    else:
        form = SupplierForm()
    return render(request, 'inventory/supplier_form.html', {'form': form, 'title': 'Create Supplier'})


@login_required
@admin_required
def supplier_update(request, pk):
    """Update an existing supplier."""
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            messages.success(request, 'Supplier updated successfully.')
            return redirect('inventory:supplier_list')
    else:
        form = SupplierForm(instance=supplier)
    return render(request, 'inventory/supplier_form.html', {'form': form, 'title': 'Update Supplier'})


# ═══════════════════════════════════════════════════════════════════════════
# Product CRUD
# ═══════════════════════════════════════════════════════════════════════════

@login_required
def product_list(request):
    """List all products (accessible by all authenticated users)."""
    products = Product.objects.select_related('category', 'supplier').all()
    return render(request, 'inventory/product_list.html', {'products': products})


@login_required
@admin_required
def product_create(request):
    """Create a new product (admin only)."""
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product created successfully.')
            return redirect('inventory:product_list')
    else:
        form = ProductForm()
    return render(request, 'inventory/product_form.html', {'form': form, 'title': 'Create Product'})


@login_required
@admin_required
def product_update(request, pk):
    """Update an existing product (admin only)."""
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully.')
            return redirect('inventory:product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'inventory/product_form.html', {'form': form, 'title': 'Update Product'})


@login_required
def product_search(request):
    """Search products by name, category, or supplier."""
    form = ProductSearchForm(request.GET or None)
    products = Product.objects.select_related('category', 'supplier').all()

    if form.is_valid():
        query = form.cleaned_data.get('query', '').strip()
        if query:
            products = products.filter(
                Q(name__icontains=query)
                | Q(category__name__icontains=query)
                | Q(supplier__name__icontains=query)
            )

    return render(request, 'inventory/product_search.html', {
        'form': form,
        'products': products,
    })


# ═══════════════════════════════════════════════════════════════════════════
# Stock Operations
# ═══════════════════════════════════════════════════════════════════════════

@login_required
def stock_in(request):
    """Add stock to a product."""
    if request.method == 'POST':
        form = StockInForm(request.POST)
        if form.is_valid():
            product = form.cleaned_data['product']
            qty = form.cleaned_data['quantity']
            notes = form.cleaned_data.get('notes', '')

            product.quantity += qty
            product.save(update_fields=['quantity'])

            InventoryTransaction.objects.create(
                product=product,
                user=request.user,
                type=InventoryTransaction.TransactionType.STOCK_IN,
                quantity=qty,
                notes=notes,
            )
            messages.success(
                request,
                f'Successfully added {qty} units to "{product.name}". '
                f'New quantity: {product.quantity}.',
            )
            return redirect('inventory:stock_in')
    else:
        form = StockInForm()

    return render(request, 'inventory/stock_in.html', {'form': form})


@login_required
def stock_out(request):
    """Remove stock from a product. Validates quantity <= available stock."""
    if request.method == 'POST':
        form = StockOutForm(request.POST)
        if form.is_valid():
            product = form.cleaned_data['product']
            qty = form.cleaned_data['quantity']
            notes = form.cleaned_data.get('notes', '')

            if qty > product.quantity:
                messages.error(
                    request,
                    f'Cannot remove {qty} units from "{product.name}". '
                    f'Only {product.quantity} available.',
                )
                return render(request, 'inventory/stock_out.html', {'form': form})

            product.quantity -= qty
            product.save(update_fields=['quantity'])

            InventoryTransaction.objects.create(
                product=product,
                user=request.user,
                type=InventoryTransaction.TransactionType.STOCK_OUT,
                quantity=qty,
                notes=notes,
            )
            messages.success(
                request,
                f'Successfully removed {qty} units from "{product.name}". '
                f'New quantity: {product.quantity}.',
            )
            return redirect('inventory:stock_out')
    else:
        form = StockOutForm()

    return render(request, 'inventory/stock_out.html', {'form': form})


@login_required
def stock_adjustment(request):
    """Adjust stock (positive or negative). Validates resulting qty >= 0."""
    if request.method == 'POST':
        form = StockAdjustmentForm(request.POST)
        if form.is_valid():
            product = form.cleaned_data['product']
            qty = form.cleaned_data['quantity']
            notes = form.cleaned_data.get('notes', '')

            new_quantity = product.quantity + qty
            if new_quantity < 0:
                messages.error(
                    request,
                    f'Adjustment would result in negative stock for "{product.name}". '
                    f'Current quantity: {product.quantity}, adjustment: {qty}.',
                )
                return render(request, 'inventory/stock_adjustment.html', {'form': form})

            product.quantity = new_quantity
            product.save(update_fields=['quantity'])

            InventoryTransaction.objects.create(
                product=product,
                user=request.user,
                type=InventoryTransaction.TransactionType.ADJUSTMENT,
                quantity=qty,
                notes=notes,
            )
            messages.success(
                request,
                f'Stock adjusted for "{product.name}" by {qty:+d}. '
                f'New quantity: {product.quantity}.',
            )
            return redirect('inventory:stock_adjustment')
    else:
        form = StockAdjustmentForm()

    return render(request, 'inventory/stock_adjustment.html', {'form': form})


# ═══════════════════════════════════════════════════════════════════════════
# Sales
# ═══════════════════════════════════════════════════════════════════════════

@login_required
def record_sale(request):
    """Record a sale with multiple line items.

    Uses django.db.transaction.atomic() to ensure the sale, sale-items,
    stock decrements, and inventory transactions are all committed together.
    """
    if request.method == 'POST':
        sale_form = SaleForm(request.POST)
        # We need a Sale instance for the formset but won't save it yet.
        # Create a temporary unsaved instance.
        sale_instance = Sale(user=request.user)
        formset = SaleItemFormSet(request.POST, instance=sale_instance)

        if sale_form.is_valid() and formset.is_valid():
            # Pre-validate stock availability for every item
            errors = []
            items_data = []
            for item_form in formset:
                if item_form.cleaned_data and not item_form.cleaned_data.get('DELETE', False):
                    product = item_form.cleaned_data['product']
                    qty = item_form.cleaned_data['quantity']
                    unit_price = item_form.cleaned_data['unit_price']
                    if qty > product.quantity:
                        errors.append(
                            f'Insufficient stock for "{product.name}": '
                            f'requested {qty}, available {product.quantity}.'
                        )
                    items_data.append((product, qty, unit_price))

            if errors:
                for error in errors:
                    messages.error(request, error)
                return render(request, 'inventory/record_sale.html', {
                    'sale_form': sale_form,
                    'formset': formset,
                })

            if not items_data:
                messages.error(request, 'Please add at least one sale item.')
                return render(request, 'inventory/record_sale.html', {
                    'sale_form': sale_form,
                    'formset': formset,
                })

            # All good — commit atomically
            with db_transaction.atomic():
                # Calculate total
                total_amount = sum(
                    qty * price for _, qty, price in items_data
                )

                sale = Sale.objects.create(
                    user=request.user,
                    total_amount=total_amount,
                )

                for product, qty, unit_price in items_data:
                    SaleItem.objects.create(
                        sale=sale,
                        product=product,
                        quantity=qty,
                        unit_price=unit_price,
                    )

                    # Decrease product stock
                    product.quantity -= qty
                    product.save(update_fields=['quantity'])

                    # Record inventory transaction
                    InventoryTransaction.objects.create(
                        product=product,
                        user=request.user,
                        type=InventoryTransaction.TransactionType.SALE,
                        quantity=qty,
                        notes=f'Sale #{sale.pk}',
                    )

            messages.success(
                request,
                f'Sale #{sale.pk} recorded successfully. Total: ${total_amount:,.2f}.',
            )
            return redirect('inventory:record_sale')
    else:
        sale_form = SaleForm()
        formset = SaleItemFormSet()

    return render(request, 'inventory/record_sale.html', {
        'sale_form': sale_form,
        'formset': formset,
    })


# ═══════════════════════════════════════════════════════════════════════════
# Transaction History
# ═══════════════════════════════════════════════════════════════════════════

@login_required
def transaction_history(request):
    """List all inventory transactions, filterable by type and date range."""
    transactions = InventoryTransaction.objects.select_related(
        'product', 'user',
    ).all()

    # Filters
    txn_type = request.GET.get('type', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')

    if txn_type:
        transactions = transactions.filter(type=txn_type)

    if date_from:
        try:
            dt_from = datetime.strptime(date_from, '%Y-%m-%d')
            transactions = transactions.filter(date_time__gte=dt_from)
        except ValueError:
            pass

    if date_to:
        try:
            dt_to = datetime.strptime(date_to, '%Y-%m-%d')
            # Include the whole day
            dt_to = dt_to + timedelta(days=1)
            transactions = transactions.filter(date_time__lt=dt_to)
        except ValueError:
            pass

    type_choices = InventoryTransaction.TransactionType.choices

    context = {
        'transactions': transactions,
        'type_choices': type_choices,
        'selected_type': txn_type,
        'date_from': date_from,
        'date_to': date_to,
    }
    return render(request, 'inventory/transaction_history.html', context)


# ═══════════════════════════════════════════════════════════════════════════
# Low-Stock Alerts
# ═══════════════════════════════════════════════════════════════════════════

@login_required
def low_stock_alerts(request):
    """List products where quantity <= reorder_level."""
    from django.db.models import F

    products = (
        Product.objects
        .select_related('category', 'supplier')
        .filter(quantity__lte=F('reorder_level'))
        .order_by('quantity')
    )
    return render(request, 'inventory/low_stock_alerts.html', {'products': products})


# ═══════════════════════════════════════════════════════════════════════════
# PDF Report Views
# ═══════════════════════════════════════════════════════════════════════════

@login_required
def generate_inventory_report(request):
    """Generate and return a PDF inventory report."""
    products = Product.objects.select_related('category', 'supplier').all()
    return generate_inventory_pdf(products)


@login_required
def generate_sales_report(request):
    """Generate and return a PDF sales report."""
    sales = Sale.objects.select_related('user').prefetch_related('items__product').all()
    return generate_sales_pdf(sales)


@login_required
def generate_transaction_report(request):
    """Generate and return a PDF transaction report (applies active filters)."""
    transactions = InventoryTransaction.objects.select_related(
        'product', 'user',
    ).all()

    # Apply same filters as transaction_history if present
    txn_type = request.GET.get('type', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')

    if txn_type:
        transactions = transactions.filter(type=txn_type)
    if date_from:
        try:
            dt_from = datetime.strptime(date_from, '%Y-%m-%d')
            transactions = transactions.filter(date_time__gte=dt_from)
        except ValueError:
            pass
    if date_to:
        try:
            dt_to = datetime.strptime(date_to, '%Y-%m-%d')
            dt_to = dt_to + timedelta(days=1)
            transactions = transactions.filter(date_time__lt=dt_to)
        except ValueError:
            pass

    return generate_transaction_pdf(transactions)
