"""ReportLab-based PDF report generators for Inventory Management System.

Optimized for Landscape A4 with automated text wrapping, proper line breaks,
and clean multi-line cell formatting to prevent text overlap.
"""

import io
from datetime import datetime
from decimal import Decimal

from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    HRFlowable,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


# ---------------------------------------------------------------------------
# Helpers & Shared Styles
# ---------------------------------------------------------------------------

def _build_response(filename: str) -> tuple[HttpResponse, io.BytesIO]:
    """Return an HttpResponse wired for PDF download and a BytesIO buffer."""
    buf = io.BytesIO()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response, buf


def _draw_page_decorations(canvas, doc):
    """Draw header rule and running footer on each page."""
    canvas.saveState()
    page_w, page_h = doc.pagesize

    # Footer dividing line and text
    canvas.setStrokeColor(colors.HexColor('#cbd5e1'))
    canvas.setLineWidth(0.5)
    canvas.line(15 * mm, 18 * mm, page_w - 15 * mm, 18 * mm)

    canvas.setFont('Helvetica', 8.5)
    canvas.setFillColor(colors.HexColor('#64748b'))
    canvas.drawString(15 * mm, 13 * mm, 'Inventory Management System  ·  Official Generated Report')
    canvas.drawRightString(page_w - 15 * mm, 13 * mm, f'Page {canvas.getPageNumber()}')

    canvas.restoreState()


def _get_report_styles():
    """Return typography styles with proper line leading to support wrapped cells."""
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#0f172a'),
        spaceAfter=4,
    )

    meta_style = ParagraphStyle(
        'DocMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#64748b'),
    )

    # Table Header Styles
    th = ParagraphStyle(
        'TH',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white,
    )
    th_center = ParagraphStyle('THC', parent=th, alignment=1)
    th_right = ParagraphStyle('THR', parent=th, alignment=2)

    # Table Data Styles (with line break & wrapping support)
    td = ParagraphStyle(
        'TD',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#1e293b'),
    )
    td_bold = ParagraphStyle('TDBold', parent=td, fontName='Helvetica-Bold')
    td_center = ParagraphStyle('TDCenter', parent=td, alignment=1)
    td_right = ParagraphStyle('TDRight', parent=td, alignment=2)
    td_right_bold = ParagraphStyle('TDRightBold', parent=td_bold, alignment=2)

    return {
        'title': title_style,
        'meta': meta_style,
        'th': th,
        'th_center': th_center,
        'th_right': th_right,
        'td': td,
        'td_bold': td_bold,
        'td_center': td_center,
        'td_right': td_right,
        'td_right_bold': td_right_bold,
    }


# ---------------------------------------------------------------------------
# Sales Report
# ---------------------------------------------------------------------------

def generate_sales_pdf(sales) -> HttpResponse:
    """Generate a PDF listing all sales with their items and totals.

    Args:
        sales: QuerySet or list of Sale instances.

    Returns:
        HttpResponse containing the PDF file with wrapped, non-overlapping cells.
    """
    response, buf = _build_response('sales_report.pdf')
    doc = SimpleDocTemplate(
        buf,
        pagesize=landscape(A4),
        leftMargin=15 * mm,
        rightMargin=15 * mm,
        topMargin=15 * mm,
        bottomMargin=24 * mm,
    )
    st = _get_report_styles()
    elements = []

    # Title & Metadata
    elements.append(Paragraph('Sales & Invoicing Report', st['title']))
    elements.append(Paragraph(
        f'Generated on: <b>{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</b>  |  '
        f'Currency: <b>Indian Rupees (₹)</b>',
        st['meta'],
    ))
    elements.append(Spacer(1, 12))

    # Table Header (Col Widths total = 750 pt, fits Landscape A4 with 15mm margins)
    # [Sale #, Date, Sold By, Product, Qty, Unit Price, Subtotal, Sale Total]
    col_widths = [50, 95, 75, 215, 45, 85, 90, 95]

    data = [[
        Paragraph('Sale #', st['th_center']),
        Paragraph('Date & Time', st['th']),
        Paragraph('Sold By', st['th']),
        Paragraph('Product Name', st['th']),
        Paragraph('Qty', st['th_center']),
        Paragraph('Unit Price', st['th_right']),
        Paragraph('Subtotal', st['th_right']),
        Paragraph('Sale Total', st['th_right']),
    ]]

    t_style_cmds = [
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0f172a')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
    ]

    grand_total = Decimal('0.00')
    total_sales_count = 0
    total_items_count = 0
    row_idx = 1

    for sale in sales:
        total_sales_count += 1
        items = list(sale.items.select_related('product').all())
        sale_user = sale.user.username if sale.user else '—'
        sale_date = sale.sale_date.strftime('%Y-%m-%d %H:%M') if sale.sale_date else '—'
        first = True

        for item in items:
            total_items_count += item.quantity
            product_name = item.product.name if item.product else 'Deleted Product'
            subtotal = Decimal(item.quantity) * item.unit_price

            data.append([
                Paragraph(f'#{sale.pk}' if first else '', st['td_center']),
                Paragraph(sale_date if first else '', st['td']),
                Paragraph(sale_user if first else '', st['td']),
                # Product name wrapped in Paragraph: will wrap lines cleanly without overlapping adjacent cells
                Paragraph(product_name, st['td']),
                Paragraph(str(item.quantity), st['td_center']),
                Paragraph(f'₹{item.unit_price:,.2f}', st['td_right']),
                Paragraph(f'₹{subtotal:,.2f}', st['td_right']),
                Paragraph(f'₹{sale.total_amount:,.2f}' if first else '', st['td_right_bold']),
            ])

            # Alternating background per sale or row
            bg = colors.HexColor('#ffffff') if total_sales_count % 2 == 1 else colors.HexColor('#f8fafc')
            t_style_cmds.append(('BACKGROUND', (0, row_idx), (-1, row_idx), bg))
            row_idx += 1
            first = False

        # Add a subtle bottom separator line after the last item of each sale
        if items:
            t_style_cmds.append(('LINEBELOW', (0, row_idx - 1), (-1, row_idx - 1), 1.0, colors.HexColor('#94a3b8')))

        grand_total += sale.total_amount

    table = Table(data, colWidths=col_widths, repeatRows=1)
    table.setStyle(TableStyle(t_style_cmds))
    elements.append(table)

    # Summary Box
    elements.append(Spacer(1, 14))
    summary_data = [
        [
            Paragraph(f'<b>Total Completed Sales:</b> {total_sales_count}', st['td']),
            Paragraph(f'<b>Total Units Sold:</b> {total_items_count}', st['td']),
            Paragraph(f'<b>Grand Total Revenue:</b> ₹{grand_total:,.2f}', st['td_right_bold']),
        ]
    ]
    summary_table = Table(summary_data, colWidths=[200, 200, 350])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#eff6ff')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#93c5fd')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    elements.append(summary_table)

    doc.build(elements, onFirstPage=_draw_page_decorations, onLaterPages=_draw_page_decorations)
    pdf = buf.getvalue()
    buf.close()
    response.write(pdf)
    return response


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
    doc = SimpleDocTemplate(
        buf,
        pagesize=landscape(A4),
        leftMargin=15 * mm,
        rightMargin=15 * mm,
        topMargin=15 * mm,
        bottomMargin=24 * mm,
    )
    st = _get_report_styles()
    elements = []

    # Title & Metadata
    elements.append(Paragraph('Inventory & Stock Status Report', st['title']))
    elements.append(Paragraph(
        f'Generated on: <b>{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</b>  |  '
        f'Currency: <b>Indian Rupees (₹)</b>',
        st['meta'],
    ))
    elements.append(Spacer(1, 12))

    # Col Widths total = 750 pt
    # [#, Product Name, Category, Supplier, Unit Price, Quantity, Reorder Level, Stock Status]
    col_widths = [35, 210, 95, 120, 85, 55, 65, 85]

    data = [[
        Paragraph('#', st['th_center']),
        Paragraph('Product Name', st['th']),
        Paragraph('Category', st['th']),
        Paragraph('Supplier', st['th']),
        Paragraph('Unit Price', st['th_right']),
        Paragraph('Stock', st['th_center']),
        Paragraph('Reorder', st['th_center']),
        Paragraph('Status', st['th_center']),
    ]]

    t_style_cmds = [
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0f172a')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
    ]

    total_stock_value = Decimal('0.00')
    total_qty = 0
    product_list = list(products)

    for idx, product in enumerate(product_list, start=1):
        if product.is_out_of_stock:
            status_text = 'OUT OF STOCK'
            status_color = '#dc2626'
        elif product.is_low_stock:
            status_text = 'LOW STOCK'
            status_color = '#d97706'
        else:
            status_text = 'In Stock'
            status_color = '#16a34a'

        category_name = product.category.name if product.category else '—'
        supplier_name = product.supplier.name if product.supplier else '—'
        total_stock_value += (Decimal(product.quantity) * product.unit_price)
        total_qty += product.quantity

        status_style = ParagraphStyle(
            f'Status_{idx}',
            parent=st['td_center'],
            fontName='Helvetica-Bold',
            textColor=colors.HexColor(status_color),
        )

        data.append([
            Paragraph(str(idx), st['td_center']),
            Paragraph(product.name, st['td']),
            Paragraph(category_name, st['td']),
            Paragraph(supplier_name, st['td']),
            Paragraph(f'₹{product.unit_price:,.2f}', st['td_right']),
            Paragraph(str(product.quantity), st['td_center']),
            Paragraph(str(product.reorder_level), st['td_center']),
            Paragraph(status_text, status_style),
        ])

        bg = colors.HexColor('#ffffff') if idx % 2 == 1 else colors.HexColor('#f8fafc')
        t_style_cmds.append(('BACKGROUND', (0, idx), (-1, idx), bg))

    table = Table(data, colWidths=col_widths, repeatRows=1)
    table.setStyle(TableStyle(t_style_cmds))
    elements.append(table)

    # Summary Box
    elements.append(Spacer(1, 14))
    summary_data = [
        [
            Paragraph(f'<b>Total SKUs / Products:</b> {len(product_list)}', st['td']),
            Paragraph(f'<b>Total In-Stock Units:</b> {total_qty}', st['td']),
            Paragraph(f'<b>Total Inventory Valuation:</b> ₹{total_stock_value:,.2f}', st['td_right_bold']),
        ]
    ]
    summary_table = Table(summary_data, colWidths=[200, 200, 350])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#eff6ff')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#93c5fd')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    elements.append(summary_table)

    doc.build(elements, onFirstPage=_draw_page_decorations, onLaterPages=_draw_page_decorations)
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
    doc = SimpleDocTemplate(
        buf,
        pagesize=landscape(A4),
        leftMargin=15 * mm,
        rightMargin=15 * mm,
        topMargin=15 * mm,
        bottomMargin=24 * mm,
    )
    st = _get_report_styles()
    elements = []

    # Title & Metadata
    elements.append(Paragraph('Inventory Transaction Audit Report', st['title']))
    elements.append(Paragraph(
        f'Generated on: <b>{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</b>  |  '
        f'Scope: <b>All Recorded Stock Movements</b>',
        st['meta'],
    ))
    elements.append(Spacer(1, 12))

    # Col Widths total = 750 pt
    # [#, Date/Time, Product, Type, Quantity, User, Notes]
    col_widths = [35, 95, 200, 75, 55, 75, 215]

    data = [[
        Paragraph('#', st['th_center']),
        Paragraph('Date / Time', st['th']),
        Paragraph('Product Name', st['th']),
        Paragraph('Type', st['th_center']),
        Paragraph('Qty Delta', st['th_center']),
        Paragraph('User', st['th']),
        Paragraph('Notes / Reason', st['th']),
    ]]

    t_style_cmds = [
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0f172a')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
    ]

    type_colors = {
        'Stock In': '#16a34a',
        'Stock Out': '#dc2626',
        'Adjustment': '#d97706',
        'Sale': '#2563eb',
    }

    txn_list = list(transactions)

    for idx, txn in enumerate(txn_list, start=1):
        product_name = txn.product.name if txn.product else 'Deleted Product'
        user_name = txn.user.username if txn.user else '—'
        date_str = txn.date_time.strftime('%Y-%m-%d %H:%M') if txn.date_time else '—'
        notes = txn.notes or '—'
        txn_type = txn.get_type_display()
        type_col = type_colors.get(txn_type, '#1e293b')

        type_style = ParagraphStyle(
            f'TxnType_{idx}',
            parent=st['td_center'],
            fontName='Helvetica-Bold',
            textColor=colors.HexColor(type_col),
        )

        data.append([
            Paragraph(str(idx), st['td_center']),
            Paragraph(date_str, st['td']),
            Paragraph(product_name, st['td']),
            Paragraph(txn_type, type_style),
            Paragraph(str(txn.quantity), st['td_center']),
            Paragraph(user_name, st['td']),
            Paragraph(notes, st['td']),
        ])

        bg = colors.HexColor('#ffffff') if idx % 2 == 1 else colors.HexColor('#f8fafc')
        t_style_cmds.append(('BACKGROUND', (0, idx), (-1, idx), bg))

    table = Table(data, colWidths=col_widths, repeatRows=1)
    table.setStyle(TableStyle(t_style_cmds))
    elements.append(table)

    # Summary Box
    elements.append(Spacer(1, 14))
    summary_data = [
        [
            Paragraph(f'<b>Total Audited Transactions:</b> {len(txn_list)}', st['td']),
        ]
    ]
    summary_table = Table(summary_data, colWidths=[750])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#eff6ff')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#93c5fd')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
    ]))
    elements.append(summary_table)

    doc.build(elements, onFirstPage=_draw_page_decorations, onLaterPages=_draw_page_decorations)
    pdf = buf.getvalue()
    buf.close()
    response.write(pdf)
    return response
