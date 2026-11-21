"""Custom template tags and filters for the inventory app."""

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def stock_status_badge(product):
    """Return a Bootstrap badge indicating the product's stock status."""
    if product.is_out_of_stock:
        return mark_safe('<span class="badge bg-danger">Out of Stock</span>')
    elif product.is_low_stock:
        return mark_safe('<span class="badge bg-warning text-dark">Low Stock</span>')
    return mark_safe('<span class="badge bg-success">In Stock</span>')


@register.filter
def role_badge(user):
    """Return a Bootstrap badge for the user's role."""
    if user.role == 'ADMIN':
        return mark_safe('<span class="badge bg-danger">Admin</span>')
    return mark_safe('<span class="badge bg-info">Staff</span>')
