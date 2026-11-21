"""ReportLab-based PDF report generators for Inventory Management System."""

import io
from datetime import datetime

from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch, mm
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _build_response(filename: str) -> tuple[HttpResponse, io.BytesIO]:
    """Return an HttpResponse wired for PDF download and a BytesIO buffer."""
    buf = io.BytesIO()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response, buf


def _page_number(canvas, doc):
    """Draw page number footer on every page."""
    canvas.saveState()
    canvas.setFont('Helvetica', 9)
    page_num = canvas.getPageNumber()
    text = f"Page {page_num}"
    canvas.drawRightString(doc.pagesize[0] - 30 * mm, 15 * mm, text)
    canvas.restoreState()


def _default_table_style():
    """Return a consistent TableStyle for all reports."""
    return TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#343a40')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('TOPPADDING', (0, 0), (-1, 0), 8),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 5),
        ('TOPPADDING', (0, 1), (-1, -1), 5),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.whitesmoke, colors.white]),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ])


# ---------------------------------------------------------------------------
# Inventory Report
# ---------------------------------------------------------------------------

def generate_inventory_pdf(products) -> HttpResponse:
    """Generate a PDF listing all products with quantities, prices, and stock status.

    Args:
        products: QuerySet or list of Product instances.

    Returns:
        HttpResponse containing the PDF file.
    """
    response, buf = _build_response('inventory_report.pdf')
    doc = SimpleDocTemplate(buf, pagesize=landscape(A4),
                            leftMargin=20 * mm, rightMargin=20 * mm,
                            topMargin=20 * mm, bottomMargin=25 * mm)
    styles = getSampleStyleSheet()
    elements = []

    # Title
    title_style = ParagraphStyle('ReportTitle', parent=styles['Title'],
                                 fontSize=18, spaceAfter=6)
    elements.append(Paragraph('Inventory Report', title_style))
    elements.append(Paragraph(
        f'Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
        styles['Normal'],
    ))
    elements.append(Spacer(1, 12))

    # Table header
    data = [['#', 'Product Name', 'Category', 'Supplier', 'Unit Price',
             'Quantity', 'Reorder Level', 'Stock Status']]

    for idx, product in enumerate(products, start=1):
        if product.is_out_of_stock:
            status = 'OUT OF STOCK'
        elif product.is_low_stock:
            status = 'LOW STOCK'
        else:
            status = 'In Stock'

        category_name = product.category.name if product.category else '—'
        supplier_name = product.supplier.name if product.supplier else '—'

        data.append([
            str(idx),
            product.name,
            category_name,
            supplier_name,
            f'${product.unit_price:,.2f}',
            str(product.quantity),
            str(product.reorder_level),
            status,
        ])

    col_widths = [30, 130, 90, 90, 70, 60, 70, 80]
    table = Table(data, colWidths=col_widths, repeatRows=1)
    style = _default_table_style()

    # Highlight stock status
    for row_idx in range(1, len(data)):
        status = data[row_idx][-1]
        if status == 'OUT OF STOCK':
            style.add('TEXTCOLOR', (-1, row_idx), (-1, row_idx), colors.red)
            style.add('FONTNAME', (-1, row_idx), (-1, row_idx), 'Helvetica-Bold')
        elif status == 'LOW STOCK':
            style.add('TEXTCOLOR', (-1, row_idx), (-1, row_idx), colors.orange)
            style.add('FONTNAME', (-1, row_idx), (-1, row_idx), 'Helvetica-Bold')

    table.setStyle(style)
    elements.append(table)

    # Summary
    elements.append(Spacer(1, 16))
    total_products = len(list(products))
    elements.append(Paragraph(f'<b>Total Products:</b> {total_products}', styles['Normal']))

    doc.build(elements, onFirstPage=_page_number, onLaterPages=_page_number)
    pdf = buf.getvalue()
    buf.close()
    response.write(pdf)
    return response


# ---------------------------------------------------------------------------
# Sales Report
# ---------------------------------------------------------------------------

def generate_sales_pdf(sales) -> HttpResponse:
    """Generate a PDF listing all sales with their items and totals.

    Args:
        sales: QuerySet or list of Sale instances (prefetch 'items__product' recommended).

    Returns:
        HttpResponse containing the PDF file.
    """
    response, buf = _build_response('sales_report.pdf')
    doc = SimpleDocTemplate(buf, pagesize=landscape(A4),
                            leftMargin=20 * mm, rightMargin=20 * mm,
                            topMargin=20 * mm, bottomMargin=25 * mm)
    styles = getSampleStyleSheet()
    elements = []

    # Title
    title_style = ParagraphStyle('ReportTitle', parent=styles['Title'],
                                 fontSize=18, spaceAfter=6)
    elements.append(Paragraph('Sales Report', title_style))
    elements.append(Paragraph(
        f'Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
        styles['Normal'],
    ))
    elements.append(Spacer(1, 12))

    # Build a flat table: one row per sale-item, with sale header info repeated
    data = [['Sale #', 'Date', 'Sold By', 'Product', 'Qty', 'Unit Price',
             'Subtotal', 'Sale Total']]

    grand_total = 0
    for sale in sales:
        items = sale.items.select_related('product').all()
        sale_user = sale.user.username if sale.user else '—'
        sale_date = sale.sale_date.strftime('%Y-%m-%d %H:%M') if sale.sale_date else '—'
        first = True
        for item in items:
            product_name = item.product.name if item.product else 'Deleted Product'
            subtotal = item.quantity * item.unit_price
            data.append([
                str(sale.pk) if first else '',
                sale_date if first else '',
                sale_user if first else '',
                product_name,
                str(item.quantity),
                f'${item.unit_price:,.2f}',
                f'${subtotal:,.2f}',
                f'${sale.total_amount:,.2f}' if first else '',
            ])
            first = False
        grand_total += sale.total_amount

    col_widths = [50, 100, 80, 120, 40, 70, 70, 80]
    table = Table(data, colWidths=col_widths, repeatRows=1)
    table.setStyle(_default_table_style())
    elements.append(table)

    elements.append(Spacer(1, 16))
    elements.append(Paragraph(
        f'<b>Grand Total:</b> ${grand_total:,.2f}', styles['Normal'],
    ))

    doc.build(elements, onFirstPage=_page_number, onLaterPages=_page_number)
    pdf = buf.getvalue()
    buf.close()
    response.write(pdf)
    return response


# ---------------------------------------------------------------------------
# Transaction Report
# ---------------------------------------------------------------------------

def generate_transaction_pdf(transactions) -> HttpResponse:
    """Generate a PDF listing inventory transactions.

    Args:
        transactions: QuerySet or list of InventoryTransaction instances.

    Returns:
        HttpResponse containing the PDF file.
    """
    response, buf = _build_response('transaction_report.pdf')
    doc = SimpleDocTemplate(buf, pagesize=landscape(A4),
                            leftMargin=20 * mm, rightMargin=20 * mm,
                            topMargin=20 * mm, bottomMargin=25 * mm)
    styles = getSampleStyleSheet()
    elements = []

    # Title
    title_style = ParagraphStyle('ReportTitle', parent=styles['Title'],
                                 fontSize=18, spaceAfter=6)
    elements.append(Paragraph('Transaction Report', title_style))
    elements.append(Paragraph(
        f'Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
        styles['Normal'],
    ))
    elements.append(Spacer(1, 12))

    data = [['#', 'Date/Time', 'Product', 'Type', 'Quantity', 'User', 'Notes']]

    for idx, txn in enumerate(transactions, start=1):
        product_name = txn.product.name if txn.product else 'Deleted Product'
        user_name = txn.user.username if txn.user else '—'
        date_str = txn.date_time.strftime('%Y-%m-%d %H:%M') if txn.date_time else '—'
        notes = (txn.notes or '')[:80]  # truncate long notes for table width

        data.append([
            str(idx),
            date_str,
            product_name,
            txn.get_type_display(),
            str(txn.quantity),
            user_name,
            notes,
        ])

    col_widths = [30, 100, 120, 80, 60, 80, 170]
    table = Table(data, colWidths=col_widths, repeatRows=1)
    style = _default_table_style()

    # Colour-code transaction types
    type_colours = {
        'Stock In': colors.HexColor('#198754'),
        'Stock Out': colors.HexColor('#dc3545'),
        'Adjustment': colors.HexColor('#fd7e14'),
        'Sale': colors.HexColor('#0d6efd'),
    }
    for row_idx in range(1, len(data)):
        txn_type = data[row_idx][3]
        colour = type_colours.get(txn_type)
        if colour:
            style.add('TEXTCOLOR', (3, row_idx), (3, row_idx), colour)
            style.add('FONTNAME', (3, row_idx), (3, row_idx), 'Helvetica-Bold')

    table.setStyle(style)
    elements.append(table)

    elements.append(Spacer(1, 16))
    elements.append(Paragraph(
        f'<b>Total Transactions:</b> {len(list(transactions))}', styles['Normal'],
    ))

    doc.build(elements, onFirstPage=_page_number, onLaterPages=_page_number)
    pdf = buf.getvalue()
    buf.close()
    response.write(pdf)
    return response
