"""Script to generate a professional, high-impact PowerPoint presentation (.pptx)
for the Inventory Management System (IMS) final-year project, exactly following
the design aesthetic, typography, and 12-slide structure of the reference PPT.
"""

import sys
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE


def create_ims_presentation(output_path):
    prs = pptx.Presentation()
    # 16:9 Widescreen dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    blank_layout = prs.slide_layouts[6]

    # ── Color Palette ────────────────────────────────────────────────────────
    BG_DARK = RGBColor(15, 23, 42)        # Slate 900
    BG_LIGHT = RGBColor(248, 250, 252)   # Slate 50
    CARD_BG = RGBColor(255, 255, 255)    # Pure White
    CARD_ALT = RGBColor(241, 245, 249)   # Slate 100
    BORDER_COLOR = RGBColor(226, 232, 240) # Slate 200

    PRIMARY_BLUE = RGBColor(37, 99, 235) # Blue 600
    ACCENT_TEAL = RGBColor(13, 148, 136)  # Teal 600
    TEXT_DARK = RGBColor(15, 23, 42)     # Slate 900
    TEXT_MUTED = RGBColor(100, 116, 139) # Slate 500
    TEXT_LIGHT = RGBColor(255, 255, 255) # White
    TEXT_SLATE_200 = RGBColor(226, 232, 240)

    TAG_BG = RGBColor(30, 41, 59)        # Slate 800
    TAG_TEXT = RGBColor(148, 163, 184)   # Slate 400

    GREEN_ACCENT = RGBColor(22, 163, 74) # Emerald 600
    AMBER_ACCENT = RGBColor(217, 119, 6) # Amber 600
    RED_ACCENT = RGBColor(220, 38, 38)   # Red 600

    FONT_FAMILY = "Segoe UI"

    def set_slide_background(slide, color):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = color
        bg.line.fill.background()
        return bg

    def add_slide_header(slide, title_text, category_text="MCA FINAL-YEAR PROJECT", slide_number=None):
        # Category pill/breadcrumb
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.45), Inches(8.0), Inches(0.35))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        tf_cat.margin_left = tf_cat.margin_right = tf_cat.margin_top = tf_cat.margin_bottom = 0
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.name = FONT_FAMILY
        p_cat.font.size = Pt(10)
        p_cat.font.bold = True
        p_cat.font.color.rgb = PRIMARY_BLUE

        # Main slide title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(10.0), Inches(0.65))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        tf_title.margin_left = tf_title.margin_right = tf_title.margin_top = tf_title.margin_bottom = 0
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.name = FONT_FAMILY
        p_title.font.size = Pt(24)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_DARK

        # Slide Number
        if slide_number is not None:
            num_box = slide.shapes.add_textbox(Inches(12.0), Inches(0.55), Inches(0.6), Inches(0.4))
            tf_num = num_box.text_frame
            tf_num.margin_left = tf_num.margin_right = tf_num.margin_top = tf_num.margin_bottom = 0
            p_num = tf_num.paragraphs[0]
            p_num.text = str(slide_number)
            p_num.alignment = PP_ALIGN.RIGHT
            p_num.font.name = FONT_FAMILY
            p_num.font.size = Pt(13)
            p_num.font.bold = True
            p_num.font.color.rgb = TEXT_MUTED

    # ═══════════════════════════════════════════════════════════════════════════
    # SLIDE 1: Title Slide (Dark Theme)
    # ═══════════════════════════════════════════════════════════════════════════
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1, BG_DARK)

    # Project badge
    badge = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.8), Inches(3.2), Inches(0.4))
    badge.fill.solid()
    badge.fill.fore_color.rgb = TAG_BG
    badge.line.color.rgb = RGBColor(51, 65, 85)
    tf_badge = badge.text_frame
    p_b = tf_badge.paragraphs[0]
    p_b.text = "MCA FINAL-YEAR PROJECT"
    p_b.alignment = PP_ALIGN.CENTER
    p_b.font.name = FONT_FAMILY
    p_b.font.size = Pt(11)
    p_b.font.bold = True
    p_b.font.color.rgb = RGBColor(96, 165, 250)

    # Title & Subtitle
    t_box = s1.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(11.7), Inches(2.2))
    tf_t = t_box.text_frame
    tf_t.word_wrap = True
    p1 = tf_t.paragraphs[0]
    p1.text = "Inventory Management System"
    p1.font.name = FONT_FAMILY
    p1.font.size = Pt(40)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_LIGHT
    p1.space_after = Pt(10)

    p2 = tf_t.add_paragraph()
    p2.text = "A Centralized Web Platform for Computer Hardware Inventory, Atomic Stock Movement Validation, Multi-Item Sales Invoicing (₹) & Visual Analytics"
    p2.font.name = FONT_FAMILY
    p2.font.size = Pt(16)
    p2.font.color.rgb = RGBColor(203, 213, 225)
    p2.space_after = Pt(18)

    # Core workflow pills (Monitor · Validate · Transact)
    pills_data = [("1. CATALOG & MONITOR", Inches(0.8)), ("2. ATOMIC VALIDATION", Inches(3.6)), ("3. AUDIT & ANALYTICS", Inches(6.4))]
    for text, left_pos in pills_data:
        pill = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_pos, Inches(4.0), Inches(2.6), Inches(0.48))
        pill.fill.solid()
        pill.fill.fore_color.rgb = RGBColor(30, 41, 59)
        pill.line.color.rgb = PRIMARY_BLUE
        tf_pill = pill.text_frame
        p_p = tf_pill.paragraphs[0]
        p_p.text = text
        p_p.alignment = PP_ALIGN.CENTER
        p_p.font.name = FONT_FAMILY
        p_p.font.size = Pt(11)
        p_p.font.bold = True
        p_p.font.color.rgb = RGBColor(147, 197, 253)

    # Institutional & Presenter Details Card
    info_card = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(4.9), Inches(11.733), Inches(1.8))
    info_card.fill.solid()
    info_card.fill.fore_color.rgb = RGBColor(24, 34, 53)
    info_card.line.color.rgb = RGBColor(51, 65, 85)
    tf_info = info_card.text_frame
    tf_info.word_wrap = True
    tf_info.margin_left = Inches(0.4)
    tf_info.margin_top = Inches(0.25)

    p_inst = tf_info.paragraphs[0]
    p_inst.text = "Department of Computer Science  ·  Aligarh Muslim University"
    p_inst.font.name = FONT_FAMILY
    p_inst.font.size = Pt(13)
    p_inst.font.bold = True
    p_inst.font.color.rgb = RGBColor(226, 232, 240)
    p_inst.space_after = Pt(8)

    p_auth = tf_info.add_paragraph()
    p_auth.text = "Presented by: Mohd Wasi Imam                     Supervisor: Dr. Faisal Anwer"
    p_auth.font.name = FONT_FAMILY
    p_auth.font.size = Pt(13)
    p_auth.font.color.rgb = RGBColor(148, 163, 184)
    p_auth.space_after = Pt(6)

    p_tech = tf_info.add_paragraph()
    p_tech.text = "Technology: Python 3 · Django · SQLite/MySQL · Bootstrap 5 · Chart.js · ReportLab · Render Cloud"
    p_tech.font.name = FONT_FAMILY
    p_tech.font.size = Pt(11)
    p_tech.font.color.rgb = RGBColor(96, 165, 250)

    # ═══════════════════════════════════════════════════════════════════════════
    # SLIDE 2: The Problem
    # ═══════════════════════════════════════════════════════════════════════════
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2, BG_LIGHT)
    add_slide_header(s2, "The Problem in Inventory Tracking", slide_number=2)

    problems = [
        ("1", "Manual Record-Keeping Causes Constant Discrepancies",
         "Spreadsheets and paper-based ledgers lack concurrency control and strict data validation, leading to mismatch between physical stock and system records."),
        ("2", "Absence of Atomic Stock Validation Leads to Negative Inventory",
         "Conventional workflows permit sales or stock-out dispatches without verifying on-hand quantity, creating impossible negative stock states and overselling."),
        ("3", "Unnoticed Stock Depletion & Supply Chain Halts",
         "Without automated low-stock identification and reorder-level alerts, fast-moving computer hardware runs out before procurement can react."),
        ("4", "No Accountability or Immutable Audit History",
         "Discrepancies in damaged hardware, returns, or adjustments cannot be traced back to the acting user, lacking timestamped audit integrity."),
        ("5", "Time-Consuming Valuation & Manual Reporting",
         "Calculating total inventory valuation in Rupees (₹) and generating formatted PDF audit sheets for stakeholders requires tedious manual compilation."),
    ]

    card_top = Inches(1.5)
    card_h = Inches(0.85)
    gap = Inches(0.18)

    for i, (num, heading, desc) in enumerate(problems):
        y = card_top + i * (card_h + gap)
        # Card shape
        card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), y, Inches(11.733), card_h)
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = BORDER_COLOR

        # Number circle badge
        num_box = s2.shapes.add_shape(MSO_SHAPE.OVAL, Inches(1.05), y + Inches(0.18), Inches(0.48), Inches(0.48))
        num_box.fill.solid()
        num_box.fill.fore_color.rgb = PRIMARY_BLUE
        num_box.line.fill.background()
        tf_n = num_box.text_frame
        p_n = tf_n.paragraphs[0]
        p_n.text = num
        p_n.alignment = PP_ALIGN.CENTER
        p_n.font.name = FONT_FAMILY
        p_n.font.size = Pt(13)
        p_n.font.bold = True
        p_n.font.color.rgb = TEXT_LIGHT

        # Text inside card
        tb = s2.shapes.add_textbox(Inches(1.7), y + Inches(0.08), Inches(10.6), Inches(0.7))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_top = tf.margin_left = tf.margin_right = tf.margin_bottom = 0
        p_h = tf.paragraphs[0]
        p_h.text = heading
        p_h.font.name = FONT_FAMILY
        p_h.font.size = Pt(12)
        p_h.font.bold = True
        p_h.font.color.rgb = TEXT_DARK
        p_h.space_after = Pt(2)

        p_d = tf.add_paragraph()
        p_d.text = desc
        p_d.font.name = FONT_FAMILY
        p_d.font.size = Pt(10.5)
        p_d.font.color.rgb = TEXT_MUTED

    # Bottom Callout Box (Need)
    need_box = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(6.25), Inches(11.733), Inches(0.75))
    need_box.fill.solid()
    need_box.fill.fore_color.rgb = RGBColor(238, 242, 255) # Indigo 50
    need_box.line.color.rgb = RGBColor(199, 210, 254)
    tf_need = need_box.text_frame
    tf_need.word_wrap = True
    p_need = tf_need.paragraphs[0]
    p_need.text = "Need: A centralized, role-based platform to record stock movements atomically, validate availability before dispatch, prevent negative stock, and automate visual analytics and PDF reports."
    p_need.alignment = PP_ALIGN.CENTER
    p_need.font.name = FONT_FAMILY
    p_need.font.size = Pt(11.5)
    p_need.font.bold = True
    p_need.font.color.rgb = PRIMARY_BLUE

    # ═══════════════════════════════════════════════════════════════════════════
    # SLIDE 3: Project Objectives
    # ═══════════════════════════════════════════════════════════════════════════
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3, BG_LIGHT)
    add_slide_header(s3, "Project Objectives", slide_number=3)

    objectives = [
        ("01", "Role-Based Access Control", "Authenticate users securely with PBKDF2 password hashing; enforce Administrator vs Staff role access via decorators."),
        ("02", "Master Data Management", "Provide administrative CRUD capabilities for Categories, Hardware Suppliers, and Products with referential integrity."),
        ("03", "Atomic Stock Validation", "Enforce atomic validation before processing Stock-Out or Sales; disallow transactions that exceed on-hand quantity."),
        ("04", "Multi-Item Sales Engine", "Build an interactive invoice form supporting multiple line items with live subtotal and grand total calculation in Rupees (₹)."),
        ("05", "Real-Time Stock Status Alerts", "Identify items automatically as Low Stock (qty <= reorder_level) and Out of Stock (qty == 0) with distinct color badges."),
        ("06", "Comprehensive Audit Trail", "Log every Stock-In, Stock-Out, Adjustment (+/-), and Sale into an immutable InventoryTransaction table."),
        ("07", "Interactive Analytics Dashboard", "Surface key operational KPIs with dynamic Chart.js visualizations for category distribution and monthly transaction trends."),
        ("08", "Automated PDF Report Generation", "Generate pixel-accurate, printable ReportLab PDF reports for Inventory, Sales, and Transaction history on demand."),
    ]

    col_w = Inches(5.7)
    row_h = Inches(1.15)
    start_x1 = Inches(0.8)
    start_x2 = Inches(6.833)
    start_y = Inches(1.5)
    gap_y = Inches(0.2)

    for idx, (num, title, desc) in enumerate(objectives):
        x = start_x1 if idx % 2 == 0 else start_x2
        y = start_y + (idx // 2) * (row_h + gap_y)

        card = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, col_w, row_h)
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = BORDER_COLOR

        # Number label
        n_box = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x + Inches(0.2), y + Inches(0.25), Inches(0.65), Inches(0.35))
        n_box.fill.solid()
        n_box.fill.fore_color.rgb = RGBColor(238, 242, 255)
        n_box.line.fill.background()
        tf_nb = n_box.text_frame
        p_nb = tf_nb.paragraphs[0]
        p_nb.text = num
        p_nb.alignment = PP_ALIGN.CENTER
        p_nb.font.name = FONT_FAMILY
        p_nb.font.size = Pt(11)
        p_nb.font.bold = True
        p_nb.font.color.rgb = PRIMARY_BLUE

        # Title & desc
        tb = s3.shapes.add_textbox(x + Inches(1.0), y + Inches(0.12), col_w - Inches(1.15), row_h - Inches(0.2))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_top = tf.margin_left = tf.margin_right = tf.margin_bottom = 0

        pt = tf.paragraphs[0]
        pt.text = title
        pt.font.name = FONT_FAMILY
        pt.font.size = Pt(12)
        pt.font.bold = True
        pt.font.color.rgb = TEXT_DARK
        pt.space_after = Pt(2)

        pd = tf.add_paragraph()
        pd.text = desc
        pd.font.name = FONT_FAMILY
        pd.font.size = Pt(10)
        pd.font.color.rgb = TEXT_MUTED

    # ═══════════════════════════════════════════════════════════════════════════
    # SLIDE 4: Proposed Solution: The Core Operational Engine
    # ═══════════════════════════════════════════════════════════════════════════
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4, BG_LIGHT)
    add_slide_header(s4, "Proposed Solution: Operational Pipeline", slide_number=4)

    phases = [
        ("1", "Catalog & Monitor", [
            ("Master Catalog Structure", "Organized by Category & Supplier with unit price (₹), stock quantity, and threshold."),
            ("Real-Time Multi-Field Search", "Instant search filtering by Product Name, Category Name, or Supplier in sub-second time."),
            ("Proactive Stock Alerts", "Automated badges for Low Stock (<= reorder) and Out of Stock (= 0) for immediate visibility."),
        ]),
        ("2", "Validate & Transact", [
            ("Availability Pre-Check", "Stock-Out and Sales forms check current stock before accepting transaction submission."),
            ("Atomic Transaction Boundary", "Database-level 'db.transaction.atomic()' locks update product stock and record audit history simultaneously."),
            ("Negative Stock Prevention", "Stock adjustments enforce 'quantity + delta >= 0', rejecting invalid reductions instantly."),
        ]),
        ("3", "Analyze & Export", [
            ("Interactive KPI Dashboards", "Total catalog count, low-stock count, suppliers, and sales totals rendered via Bootstrap 5 cards."),
            ("Chart.js Visualizations", "Category stock distribution bar charts and 12-month transaction trend line charts."),
            ("ReportLab PDF Generators", "Downloadable, paginated audit reports with tabular data and stock status highlights in Rupees (₹)."),
        ])
    ]

    card_w = Inches(3.7)
    card_h = Inches(4.5)
    gap_x = Inches(0.3)

    for i, (num, title, items) in enumerate(phases):
        x = Inches(0.8) + i * (card_w + gap_x)
        y = Inches(1.5)

        card = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, card_w, card_h)
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = BORDER_COLOR

        # Phase header banner inside card
        header_banner = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x + Inches(0.2), y + Inches(0.2), card_w - Inches(0.4), Inches(0.65))
        header_banner.fill.solid()
        header_banner.fill.fore_color.rgb = PRIMARY_BLUE if i == 1 else RGBColor(30, 41, 59)
        header_banner.line.fill.background()
        tf_hb = header_banner.text_frame
        p_hb = tf_hb.paragraphs[0]
        p_hb.text = f"{num}. {title.upper()}"
        p_hb.alignment = PP_ALIGN.CENTER
        p_hb.font.name = FONT_FAMILY
        p_hb.font.size = Pt(12)
        p_hb.font.bold = True
        p_hb.font.color.rgb = TEXT_LIGHT

        # Sub-items text
        tb = s4.shapes.add_textbox(x + Inches(0.3), y + Inches(1.05), card_w - Inches(0.6), card_h - Inches(1.2))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_top = tf.margin_left = tf.margin_right = tf.margin_bottom = 0

        for heading, body in items:
            ph = tf.add_paragraph() if tf.paragraphs[0].text else tf.paragraphs[0]
            ph.text = f"• {heading}"
            ph.font.name = FONT_FAMILY
            ph.font.size = Pt(11)
            ph.font.bold = True
            ph.font.color.rgb = TEXT_DARK
            ph.space_after = Pt(2)

            pb = tf.add_paragraph()
            pb.text = f"   {body}"
            pb.font.name = FONT_FAMILY
            pb.font.size = Pt(9.5)
            pb.font.color.rgb = TEXT_MUTED
            pb.space_after = Pt(10)

    # Note at bottom
    note_box = s4.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(6.25), Inches(11.733), Inches(0.7))
    note_box.fill.solid()
    note_box.fill.fore_color.rgb = RGBColor(240, 253, 244) # Green 50
    note_box.line.color.rgb = RGBColor(187, 247, 208)
    tf_nb = note_box.text_frame
    tf_nb.word_wrap = True
    p_n = tf_nb.paragraphs[0]
    p_n.text = "Strict ACID Guarantee: Multi-item sales and stock adjustments are wrapped in atomic database transactions. If any line-item exceeds stock, the entire transaction rolls back, preventing data corruption."
    p_n.alignment = PP_ALIGN.CENTER
    p_n.font.name = FONT_FAMILY
    p_n.font.size = Pt(11)
    p_n.font.bold = True
    p_n.font.color.rgb = GREEN_ACCENT

    # ═══════════════════════════════════════════════════════════════════════════
    # SLIDE 5: System Architecture & Data Flow
    # ═══════════════════════════════════════════════════════════════════════════
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5, BG_LIGHT)
    add_slide_header(s5, "System Architecture & Tiered Data Flow", slide_number=5)

    tiers = [
        ("Presentation Tier (Frontend)", Inches(0.8), [
            ("HTML5 & Bootstrap 5", "Responsive UI, modal dialogs, and table layouts"),
            ("Chart.js Visualizations", "Canvas-based dynamic category and trend charts"),
            ("Vanilla JS Invoice Engine", "Real-time line-item subtotal and grand total in ₹"),
            ("Font Awesome 6", "Clean icons and contextual stock-status badges"),
        ], RGBColor(30, 41, 59)),

        ("Logic Tier (Django Backend)", Inches(4.7), [
            ("URL Router & Middleware", "Session management, CSRF checks & WhiteNoise"),
            ("Authentication & RBAC", "PBKDF2 password hashing & '@admin_required' gate"),
            ("Stock Validation Engine", "Atomic quantity checks preventing negative stock"),
            ("ReportLab PDF Service", "Streamed binary PDF generation for downloads"),
        ], PRIMARY_BLUE),

        ("Data Tier (Persistence)", Inches(8.6), [
            ("Relational ORM Models", "User, Category, Supplier, Product, Transaction, Sale"),
            ("Foreign Key Integrity", "Referential cascade rules and index optimization"),
            ("SQLite (Dev) / MySQL (Prod)", "Zero-config local DB; production ready for MySQL"),
            ("Transaction Audit Log", "Immutable history of every accepted stock change"),
        ], RGBColor(13, 148, 136)),
    ]

    for title, left_pos, items, border_color in tiers:
        card = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_pos, Inches(1.5), Inches(3.9), Inches(4.5))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = border_color
        card.line.width = Pt(1.5)

        # Header box
        hb = s5.shapes.add_shape(MSO_SHAPE.RECTANGLE, left_pos + Inches(0.15), Inches(1.65), Inches(3.6), Inches(0.55))
        hb.fill.solid()
        hb.fill.fore_color.rgb = border_color
        hb.line.fill.background()
        tf_h = hb.text_frame
        p_h = tf_h.paragraphs[0]
        p_h.text = title
        p_h.alignment = PP_ALIGN.CENTER
        p_h.font.name = FONT_FAMILY
        p_h.font.size = Pt(11)
        p_h.font.bold = True
        p_h.font.color.rgb = TEXT_LIGHT

        # Body items
        tb = s5.shapes.add_textbox(left_pos + Inches(0.25), Inches(2.35), Inches(3.4), Inches(3.4))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_top = tf.margin_left = tf.margin_right = tf.margin_bottom = 0

        for h, d in items:
            ph = tf.add_paragraph() if tf.paragraphs[0].text else tf.paragraphs[0]
            ph.text = f"✔ {h}"
            ph.font.name = FONT_FAMILY
            ph.font.size = Pt(11)
            ph.font.bold = True
            ph.font.color.rgb = TEXT_DARK
            ph.space_after = Pt(1)

            pd = tf.add_paragraph()
            pd.text = f"    {d}"
            pd.font.name = FONT_FAMILY
            pd.font.size = Pt(9.5)
            pd.font.color.rgb = TEXT_MUTED
            pd.space_after = Pt(8)

    # Architecture summary footer
    flow_box = s5.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(6.25), Inches(11.733), Inches(0.7))
    flow_box.fill.solid()
    flow_box.fill.fore_color.rgb = RGBColor(241, 245, 249)
    flow_box.line.color.rgb = BORDER_COLOR
    tf_f = flow_box.text_frame
    p_f = tf_f.paragraphs[0]
    p_f.text = "Data Flow: Browser Client ➔ HTTPS Requests ➔ Django Views & Security Decorators ➔ Atomic ORM Transactions ➔ Relational Database ➔ Asynchronous JSON / ReportLab PDF Stream"
    p_f.alignment = PP_ALIGN.CENTER
    p_f.font.name = FONT_FAMILY
    p_f.font.size = Pt(10.5)
    p_f.font.bold = True
    p_f.font.color.rgb = TEXT_DARK

    # ═══════════════════════════════════════════════════════════════════════════
    # SLIDE 6: Technology Stack Justification
    # ═══════════════════════════════════════════════════════════════════════════
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6, BG_LIGHT)
    add_slide_header(s6, "Technology Stack Justification", slide_number=6)

    stack_cards = [
        ("Frontend UI", [
            ("HTML5 & CSS3", "Semantic markup, clean layout"),
            ("Bootstrap 5.3", "Responsive grid, table styling, cards"),
            ("Font Awesome 6", "Intuitive iconography & status badges"),
            ("Vanilla JavaScript", "Dynamic invoice row add/remove & math"),
        ], "Provides responsive, rapid UI without heavyweight SPA frontend build overhead."),

        ("Backend Logic", [
            ("Python 3.11+", "Clean syntax, robust ecosystem"),
            ("Django Framework", "Built-in auth, ORM, CSRF, Admin panel"),
            ("Gunicorn WSGI", "Production-grade multi-worker server"),
            ("WhiteNoise", "Static asset compression & direct serving"),
        ], "Built-in security, ORM atomic transactions, and rapid enterprise feature scaffolding."),

        ("Database & Auth", [
            ("SQLite 3 (Dev)", "Zero-setup portable relational storage"),
            ("MySQL / PostgreSQL", "Production enterprise RDBMS ready"),
            ("Django PBKDF2", "Cryptographic password hashing"),
            ("Role-Based Gates", "Admin vs Staff permission isolation"),
        ], "Preserves full ACID compliance, foreign key referential integrity, and safe auth."),

        ("Reporting & Charts", [
            ("Chart.js 4.x", "Canvas-based bar & line visualizations"),
            ("ReportLab Engine", "Programmatic PDF generation"),
            ("PDF Tables & Styles", "Paginated, branded reports in ₹"),
            ("REST JSON Endpoints", "Asynchronous dashboard metric fetching"),
        ], "Interactive visual insights on-screen and downloadable printable audit reports."),

        ("DevOps & Cloud", [
            ("Git & GitHub", "Source version control & collaboration"),
            ("Render PaaS", "Automated cloud CI/CD container hosting"),
            ("build.sh Automation", "Automated migrations, static & seeding"),
            ("render.yaml", "Infrastructure-as-Code Blueprint config"),
        ], "Zero-configuration automated deployments on code pushes to the GitHub repository."),
    ]

    w_card = Inches(2.26)
    gap_card = Inches(0.12)

    for i, (category, tools, just) in enumerate(stack_cards):
        x = Inches(0.8) + i * (w_card + gap_card)
        y = Inches(1.5)

        card = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w_card, Inches(5.4))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = BORDER_COLOR

        # Header tag
        ht = s6.shapes.add_shape(MSO_SHAPE.RECTANGLE, x + Inches(0.1), y + Inches(0.15), w_card - Inches(0.2), Inches(0.45))
        ht.fill.solid()
        ht.fill.fore_color.rgb = PRIMARY_BLUE
        ht.line.fill.background()
        tf_ht = ht.text_frame
        p_ht = tf_ht.paragraphs[0]
        p_ht.text = category
        p_ht.alignment = PP_ALIGN.CENTER
        p_ht.font.name = FONT_FAMILY
        p_ht.font.size = Pt(11)
        p_ht.font.bold = True
        p_ht.font.color.rgb = TEXT_LIGHT

        # Tools list
        tb = s6.shapes.add_textbox(x + Inches(0.12), y + Inches(0.7), w_card - Inches(0.24), Inches(2.9))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_top = tf.margin_left = tf.margin_right = tf.margin_bottom = 0

        for tool_name, tool_desc in tools:
            pt = tf.add_paragraph() if tf.paragraphs[0].text else tf.paragraphs[0]
            pt.text = f"• {tool_name}"
            pt.font.name = FONT_FAMILY
            pt.font.size = Pt(10)
            pt.font.bold = True
            pt.font.color.rgb = TEXT_DARK

            pd = tf.add_paragraph()
            pd.text = f"  {tool_desc}"
            pd.font.name = FONT_FAMILY
            pd.font.size = Pt(8.5)
            pd.font.color.rgb = TEXT_MUTED
            pd.space_after = Pt(6)

        # Justification box at bottom
        jb = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x + Inches(0.1), y + Inches(3.75), w_card - Inches(0.2), Inches(1.5))
        jb.fill.solid()
        jb.fill.fore_color.rgb = RGBColor(248, 250, 252)
        jb.line.color.rgb = RGBColor(226, 232, 240)
        tf_j = jb.text_frame
        tf_j.word_wrap = True
        p_jh = tf_j.paragraphs[0]
        p_jh.text = "Justification:"
        p_jh.font.name = FONT_FAMILY
        p_jh.font.size = Pt(9)
        p_jh.font.bold = True
        p_jh.font.color.rgb = PRIMARY_BLUE
        p_jh.space_after = Pt(2)

        p_jt = tf_j.add_paragraph()
        p_jt.text = just
        p_jt.font.name = FONT_FAMILY
        p_jt.font.size = Pt(8.5)
        p_jt.font.color.rgb = TEXT_MUTED

    # ═══════════════════════════════════════════════════════════════════════════
    # SLIDE 7: Database Design & Relational Data Model
    # ═══════════════════════════════════════════════════════════════════════════
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7, BG_LIGHT)
    add_slide_header(s7, "Database Design: 7 Relational Entities", slide_number=7)

    entities = [
        ("User", "Stores system credentials & access tier", [
            ("user_id", "Primary Key, AutoField"),
            ("username / email", "Unique credentials, login identifier"),
            ("password_hash", "PBKDF2 SHA-256 encrypted string"),
            ("role", "ADMIN | STAFF choices for RBAC"),
        ]),
        ("Category", "Classifies computer hardware items", [
            ("category_id", "Primary Key, AutoField"),
            ("name", "Unique hardware classification name"),
            ("description", "Category scope & details"),
            ("1 : N Products", "One category groups many products"),
        ]),
        ("Supplier", "Hardware vendors & distributors", [
            ("supplier_id", "Primary Key, AutoField"),
            ("name", "Vendor company or distributor name"),
            ("phone / email", "Contact communications details"),
            ("address", "Physical warehouse / hub location"),
        ]),
        ("Product", "Hardware master catalog & live stock", [
            ("product_id", "Primary Key, AutoField"),
            ("name / price", "Hardware model name & unit_price (₹)"),
            ("quantity", "Current on-hand units (Non-negative)"),
            ("reorder_level", "Automated low-stock threshold trigger"),
        ]),
        ("InventoryTransaction", "Audit log of all stock movements", [
            ("transaction_id", "Primary Key, AutoField"),
            ("type", "STOCK_IN, STOCK_OUT, ADJUST, SALE"),
            ("quantity / date", "Movement count & timestamped record"),
            ("user_id", "Foreign Key: Audit trail of actor"),
        ]),
        ("Sale & SaleItem", "Multi-item customer sales transactions", [
            ("sale_id", "Primary Key, AutoField; total_amount (₹)"),
            ("sale_item_id", "Child record referencing Sale & Product"),
            ("quantity / price", "Units sold & price at sale time"),
            ("Atomic Sync", "Sale creates InventoryTransaction (SALE)"),
        ]),
    ]

    w_box = Inches(3.7)
    h_box = Inches(2.25)
    xs = [Inches(0.8), Inches(4.8), Inches(8.8)]
    ys = [Inches(1.5), Inches(3.95)]

    for idx, (ent_name, ent_sub, attrs) in enumerate(entities):
        row = idx // 3
        col = idx % 3
        x = xs[col]
        y = ys[row]

        box = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w_box, h_box)
        box.fill.solid()
        box.fill.fore_color.rgb = CARD_BG
        box.line.color.rgb = BORDER_COLOR

        # Entity header
        eh = s7.shapes.add_shape(MSO_SHAPE.RECTANGLE, x + Inches(0.12), y + Inches(0.12), w_box - Inches(0.24), Inches(0.42))
        eh.fill.solid()
        eh.fill.fore_color.rgb = PRIMARY_BLUE if "Product" in ent_name or "Sale" in ent_name else RGBColor(30, 41, 59)
        eh.line.fill.background()
        tf_eh = eh.text_frame
        p_eh = tf_eh.paragraphs[0]
        p_eh.text = ent_name.upper()
        p_eh.alignment = PP_ALIGN.CENTER
        p_eh.font.name = FONT_FAMILY
        p_eh.font.size = Pt(11)
        p_eh.font.bold = True
        p_eh.font.color.rgb = TEXT_LIGHT

        # Subtitle
        tb_sub = s7.shapes.add_textbox(x + Inches(0.15), y + Inches(0.55), w_box - Inches(0.3), Inches(0.25))
        tf_sub = tb_sub.text_frame
        tf_sub.margin_top = tf_sub.margin_left = tf_sub.margin_right = tf_sub.margin_bottom = 0
        p_sub = tf_sub.paragraphs[0]
        p_sub.text = ent_sub
        p_sub.font.name = FONT_FAMILY
        p_sub.font.size = Pt(8.5)
        p_sub.font.italic = True
        p_sub.font.color.rgb = TEXT_MUTED

        # Attributes
        tb = s7.shapes.add_textbox(x + Inches(0.15), y + Inches(0.82), w_box - Inches(0.3), Inches(1.35))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_top = tf.margin_left = tf.margin_right = tf.margin_bottom = 0

        for attr_k, attr_v in attrs:
            pa = tf.add_paragraph() if tf.paragraphs[0].text else tf.paragraphs[0]
            pa.text = f"• {attr_k}: "
            pa.font.name = FONT_FAMILY
            pa.font.size = Pt(9.5)
            pa.font.bold = True
            pa.font.color.rgb = TEXT_DARK

            # Value
            run = pa.add_run()
            run.text = attr_v
            run.font.bold = False
            run.font.color.rgb = TEXT_MUTED
            pa.space_after = Pt(2)

    # Bottom Callout: Referential Integrity
    ri_box = s7.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(6.35), Inches(11.733), Inches(0.65))
    ri_box.fill.solid()
    ri_box.fill.fore_color.rgb = RGBColor(241, 245, 249)
    ri_box.line.color.rgb = BORDER_COLOR
    tf_ri = ri_box.text_frame
    p_ri = tf_ri.paragraphs[0]
    p_ri.text = "Referential Integrity: Foreign keys enforce 1:N relations (Category ➔ Products, Supplier ➔ Products, User ➔ Transactions, Sale ➔ SaleItems). Stock quantity is guarded by positive integer constraints."
    p_ri.alignment = PP_ALIGN.CENTER
    p_ri.font.name = FONT_FAMILY
    p_ri.font.size = Pt(10)
    p_ri.font.bold = True
    p_ri.font.color.rgb = TEXT_DARK

    # ═══════════════════════════════════════════════════════════════════════════
    # SLIDE 8: Core Functional Modules & Transaction Workflows
    # ═══════════════════════════════════════════════════════════════════════════
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8, BG_LIGHT)
    add_slide_header(s8, "Core Modules & Transaction Workflows", slide_number=8)

    modules = [
        ("Authentication & RBAC", [
            ("Secure Session Login", "Django session-based login with encrypted cookies and CSRF validation."),
            ("Role Separation", "Administrator has full access; Staff is restricted from admin settings."),
            ("@admin_required Decorator", "Rejects non-admin attempts to edit users, categories, or suppliers."),
            ("Audit Binding", "The authenticated request.user is recorded in every inventory movement."),
        ]),
        ("Stock In & Adjustments", [
            ("Stock-In Restock", "Increments available quantity; records STOCK_IN transaction with notes."),
            ("Authorized Adjustments", "Allows positive additions (surplus) or negative deductions (damaged/RMA)."),
            ("Negative Stock Gate", "Pre-computes 'qty + adjustment'; rejects transaction if result is < 0."),
            ("Audit Logging", "Includes user notes and timestamps for full accountability."),
        ]),
        ("Sales Invoicing Engine (₹)", [
            ("Dynamic Formset UI", "Interactive row addition/deletion in JavaScript with live subtotal calculation."),
            ("Stock Pre-Validation", "Verifies requested quantity <= on-hand stock for all line-items before save."),
            ("Atomic Execution", "Wraps Sale, SaleItems, and Stock decrements in a single atomic transaction."),
            ("Sync History", "Automatically generates corresponding 'SALE' inventory transaction records."),
        ]),
        ("Stock Status & Reports", [
            ("Visual Color Badges", "Green for In Stock, Yellow for Low Stock, Red for Out of Stock."),
            ("Dedicated Alerts View", "Single-click filter displaying all products at or below reorder level."),
            ("ReportLab PDF Service", "Downloadable formatted PDF audit reports for Inventory, Sales, Transactions."),
            ("Indian Rupee (₹) Formatting", "All reports and tables formatted in Indian Rupees (₹) for accuracy."),
        ]),
    ]

    w_m = Inches(2.78)
    gap_m = Inches(0.2)

    for i, (m_title, m_points) in enumerate(modules):
        x = Inches(0.8) + i * (w_m + gap_m)
        y = Inches(1.5)

        card = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w_m, Inches(5.4))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = BORDER_COLOR

        # Card header
        ch = s8.shapes.add_shape(MSO_SHAPE.RECTANGLE, x + Inches(0.12), y + Inches(0.15), w_m - Inches(0.24), Inches(0.55))
        ch.fill.solid()
        ch.fill.fore_color.rgb = PRIMARY_BLUE if i == 2 else RGBColor(30, 41, 59)
        ch.line.fill.background()
        tf_ch = ch.text_frame
        p_ch = tf_ch.paragraphs[0]
        p_ch.text = m_title
        p_ch.alignment = PP_ALIGN.CENTER
        p_ch.font.name = FONT_FAMILY
        p_ch.font.size = Pt(11)
        p_ch.font.bold = True
        p_ch.font.color.rgb = TEXT_LIGHT

        # Bullet items
        tb = s8.shapes.add_textbox(x + Inches(0.15), y + Inches(0.85), w_m - Inches(0.3), Inches(4.3))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_top = tf.margin_left = tf.margin_right = tf.margin_bottom = 0

        for pt_title, pt_desc in m_points:
            pt = tf.add_paragraph() if tf.paragraphs[0].text else tf.paragraphs[0]
            pt.text = f"✔ {pt_title}"
            pt.font.name = FONT_FAMILY
            pt.font.size = Pt(10.5)
            pt.font.bold = True
            pt.font.color.rgb = TEXT_DARK
            pt.space_after = Pt(1)

            pd = tf.add_paragraph()
            pd.text = f"    {pt_desc}"
            pd.font.name = FONT_FAMILY
            pd.font.size = Pt(9)
            pd.font.color.rgb = TEXT_MUTED
            pd.space_after = Pt(10)

    # ═══════════════════════════════════════════════════════════════════════════
    # SLIDE 9: Verification, Testing & Traceability Matrix
    # ═══════════════════════════════════════════════════════════════════════════
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9, BG_LIGHT)
    add_slide_header(s9, "Verification & Traceability Matrix (SRS Table 3)", slide_number=9)

    # Table mapping TC01 to TC12
    table_shape = s9.shapes.add_table(13, 4, Inches(0.8), Inches(1.5), Inches(11.733), Inches(4.7))
    tbl = table_shape.table

    tbl.columns[0].width = Inches(1.1)
    tbl.columns[1].width = Inches(1.5)
    tbl.columns[2].width = Inches(6.8)
    tbl.columns[3].width = Inches(2.333)

    headers = ["Test ID", "Requirement", "Test Scenario & Acceptance Criterion", "Status"]
    for col_idx, h in enumerate(headers):
        cell = tbl.cell(0, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = RGBColor(30, 41, 59)
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.name = FONT_FAMILY
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = TEXT_LIGHT
        p.alignment = PP_ALIGN.CENTER if col_idx in (0, 1, 3) else PP_ALIGN.LEFT

    tests_data = [
        ("TC01", "FR-001", "User Authentication: Valid credentials permit access; invalid passwords rejected.", "PASSED ✔"),
        ("TC02", "FR-001", "Role-Based Access: Admin settings/CRUD restricted from Staff users via @admin_required.", "PASSED ✔"),
        ("TC03", "FR-002, 003", "Master Data Management: Admin creates/updates Categories, Suppliers, Products, and Users.", "PASSED ✔"),
        ("TC04", "FR-004", "Product Search: Multi-field search filters products by Name, Category, or Supplier.", "PASSED ✔"),
        ("TC05", "FR-004", "Stock Status & Alerts: Identifies Low-Stock (qty <= reorder) and Out-of-Stock (qty == 0).", "PASSED ✔"),
        ("TC06", "FR-005, 006", "Stock-In & Adjustments: Correctly increments stock or adjusts (+/-) and logs audit entry.", "PASSED ✔"),
        ("TC07", "FR-005, 006", "Stock-Out: Decreases quantity and records transaction with acting user and timestamp.", "PASSED ✔"),
        ("TC08", "FR-006", "Stock Availability Validation: Rejects excess stock-out or negative adjustment; stock unchanged.", "PASSED ✔"),
        ("TC09", "FR-005, 006", "Multi-Item Sales: Validates stock, decrements quantity, logs Sale, SaleItems & SALE txns.", "PASSED ✔"),
        ("TC10", "FR-007", "Dashboard & History: Dynamic KPI totals, Chart.js graphs, filterable transaction history.", "PASSED ✔"),
        ("TC11", "FR-008", "PDF Report Generation: Downloads valid ReportLab PDF files (Inventory, Sales, Transactions).", "PASSED ✔"),
        ("TC12", "NFR 3.2", "Security & Reliability: PBKDF2 password hashing, CSRF tokens, atomic rollback guarantees.", "PASSED ✔"),
    ]

    for row_idx, (t_id, req, desc, status) in enumerate(tests_data, start=1):
        bg_col = CARD_BG if row_idx % 2 == 1 else RGBColor(241, 245, 249)
        for col_idx, text_val in enumerate([t_id, req, desc, status]):
            cell = tbl.cell(row_idx, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = bg_col
            p = cell.text_frame.paragraphs[0]
            p.text = text_val
            p.font.name = FONT_FAMILY
            p.font.size = Pt(8.5)
            p.alignment = PP_ALIGN.CENTER if col_idx in (0, 1, 3) else PP_ALIGN.LEFT
            if col_idx == 3:
                p.font.bold = True
                p.font.color.rgb = GREEN_ACCENT
            elif col_idx == 0:
                p.font.bold = True
                p.font.color.rgb = PRIMARY_BLUE
            else:
                p.font.color.rgb = TEXT_DARK

    # Summary Callout
    call_box = s9.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(6.35), Inches(11.733), Inches(0.65))
    call_box.fill.solid()
    call_box.fill.fore_color.rgb = RGBColor(240, 253, 244)
    call_box.line.color.rgb = RGBColor(187, 247, 208)
    tf_c = call_box.text_frame
    p_c = tf_c.paragraphs[0]
    p_c.text = "Automated Test Suite: 'python manage.py test inventory' ➔ Ran 12 tests in 22.31s ➔ OK (0 errors, 0 failures, 100% Traceability Pass Rate)"
    p_c.alignment = PP_ALIGN.CENTER
    p_c.font.name = FONT_FAMILY
    p_c.font.size = Pt(10.5)
    p_c.font.bold = True
    p_c.font.color.rgb = GREEN_ACCENT

    # ═══════════════════════════════════════════════════════════════════════════
    # SLIDE 10: Live Demonstration & Computer Hardware Catalog
    # ═══════════════════════════════════════════════════════════════════════════
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10, BG_LIGHT)
    add_slide_header(s10, "Live Demonstration & Computer Catalog", slide_number=10)

    # Left: Demo Walkthrough Steps
    left_card = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4))
    left_card.fill.solid()
    left_card.fill.fore_color.rgb = CARD_BG
    left_card.line.color.rgb = BORDER_COLOR

    lh = s10.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.0), Inches(1.7), Inches(5.2), Inches(0.45))
    lh.fill.solid()
    lh.fill.fore_color.rgb = PRIMARY_BLUE
    lh.line.fill.background()
    tf_lh = lh.text_frame
    p_lh = tf_lh.paragraphs[0]
    p_lh.text = "DEMONSTRATION WORKFLOW"
    p_lh.alignment = PP_ALIGN.CENTER
    p_lh.font.name = FONT_FAMILY
    p_lh.font.size = Pt(11)
    p_lh.font.bold = True
    p_lh.font.color.rgb = TEXT_LIGHT

    demo_steps = [
        ("Step 1: Role-Based Sign In", "Log in as Administrator (admin/admin123) to access master CRUD or Staff (staff/staff123) for operations."),
        ("Step 2: Analytics Dashboard", "Review KPI summary cards (Products, Low Stock, Categories, Suppliers) and dynamic Chart.js visualizations."),
        ("Step 3: Catalog & Search", "Search 18 real computer items (Laptops, Components, Peripherals, Networking, Displays) across name and vendor."),
        ("Step 4: Stock Movement", "Execute Stock-In restock, test excess Stock-Out rejection, and log damage adjustments with notes."),
        ("Step 5: Dynamic Sales Invoicing", "Build a multi-item sale in Indian Rupees (₹), adding items dynamically with instant subtotal and total calculation."),
        ("Step 6: PDF Report Downloads", "Export professional, downloadable PDF reports for Inventory, Sales, and Transactions generated on-the-fly."),
    ]

    tb_demo = s10.shapes.add_textbox(Inches(1.0), Inches(2.3), Inches(5.2), Inches(4.4))
    tf_demo = tb_demo.text_frame
    tf_demo.word_wrap = True
    tf_demo.margin_top = tf_demo.margin_left = tf_demo.margin_right = tf_demo.margin_bottom = 0

    for s_title, s_desc in demo_steps:
        ps = tf_demo.add_paragraph() if tf_demo.paragraphs[0].text else tf_demo.paragraphs[0]
        ps.text = f"✔ {s_title}"
        ps.font.name = FONT_FAMILY
        ps.font.size = Pt(10.5)
        ps.font.bold = True
        ps.font.color.rgb = TEXT_DARK

        pd = tf_demo.add_paragraph()
        pd.text = f"    {s_desc}"
        pd.font.name = FONT_FAMILY
        pd.font.size = Pt(9)
        pd.font.color.rgb = TEXT_MUTED
        pd.space_after = Pt(6)

    # Right: Catalog & Price Overview Card (INR ₹)
    right_card = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.5), Inches(5.733), Inches(5.4))
    right_card.fill.solid()
    right_card.fill.fore_color.rgb = CARD_BG
    right_card.line.color.rgb = BORDER_COLOR

    rh = s10.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(7.0), Inches(1.7), Inches(5.333), Inches(0.45))
    rh.fill.solid()
    rh.fill.fore_color.rgb = RGBColor(30, 41, 59)
    rh.line.fill.background()
    tf_rh = rh.text_frame
    p_rh = tf_rh.paragraphs[0]
    p_rh.text = "HARDWARE CATALOG IN RUPEES (₹)"
    p_rh.alignment = PP_ALIGN.CENTER
    p_rh.font.name = FONT_FAMILY
    p_rh.font.size = Pt(11)
    p_rh.font.bold = True
    p_rh.font.color.rgb = TEXT_LIGHT

    sample_products = [
        ("Dell XPS 15 Laptop (Intel i9, 32GB RAM)", "Laptops & Desktops", "₹1,49,999.00", "In Stock (12)"),
        ("HP Pavilion Gaming Desktop (RTX 4060)", "Laptops & Desktops", "₹84,999.00", "In Stock (8)"),
        ("Lenovo ThinkPad X1 Carbon 14\"", "Laptops & Desktops", "₹1,24,999.00", "Out of Stock (0)"),
        ("Logitech MX Master 3S Wireless Mouse", "Computer Peripherals", "₹8,995.00", "In Stock (45)"),
        ("Corsair K70 RGB Mechanical Keyboard", "Computer Peripherals", "₹12,499.00", "In Stock (25)"),
        ("Logitech Brio 4K Ultra HD Pro Webcam", "Computer Peripherals", "₹16,995.00", "Low Stock (4)"),
        ("Samsung 990 PRO 2TB NVMe PCIe 4.0 SSD", "Components & Storage", "₹17,499.00", "In Stock (30)"),
        ("Kingston Fury Beast 32GB DDR5 6000MHz", "Components & Storage", "₹10,499.00", "In Stock (50)"),
        ("ASUS ROG Strix RTX 4070 Ti Super 16GB", "Components & Storage", "₹84,999.00", "Low Stock (5)"),
        ("Corsair RM850x 850W 80+ Gold Modular PSU", "Components & Storage", "₹11,999.00", "Out of Stock (0)"),
        ("TP-Link Archer AXE75 Tri-Band Wi-Fi 6E", "Networking", "₹12,999.00", "In Stock (16)"),
        ("Cat6 RJ45 Gigabit Ethernet Cable 10m", "Networking", "₹499.00", "In Stock (120)"),
    ]

    tb_cat = s10.shapes.add_textbox(Inches(7.0), Inches(2.25), Inches(5.333), Inches(4.5))
    tf_cat = tb_cat.text_frame
    tf_cat.word_wrap = True
    tf_cat.margin_top = tf_cat.margin_left = tf_cat.margin_right = tf_cat.margin_bottom = 0

    for name, cat, price, status in sample_products:
        p_row = tf_cat.add_paragraph() if tf_cat.paragraphs[0].text else tf_cat.paragraphs[0]
        p_row.text = f"• {name}"
        p_row.font.name = FONT_FAMILY
        p_row.font.size = Pt(9.5)
        p_row.font.bold = True
        p_row.font.color.rgb = TEXT_DARK

        run = p_row.add_run()
        run.text = f" — {price} ({status})"
        run.font.bold = False
        if "Out" in status:
            run.font.color.rgb = RED_ACCENT
        elif "Low" in status:
            run.font.color.rgb = AMBER_ACCENT
        else:
            run.font.color.rgb = GREEN_ACCENT
        p_row.space_after = Pt(2)

    # ═══════════════════════════════════════════════════════════════════════════
    # SLIDE 11: Limitations and Challenges
    # ═══════════════════════════════════════════════════════════════════════════
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11, BG_LIGHT)
    add_slide_header(s11, "Limitations & Scoping Boundaries", slide_number=11)

    limits = [
        ("1", "Single-Store / Single-Warehouse Architecture",
         "The current system is designed for a centralized inventory location. Multi-warehouse inventory routing, inter-branch transfer orders, and regional depot logistics are out of scope."),
        ("2", "Rule-Based Reordering (No Automated Procurement)",
         "While the system triggers real-time low-stock alerts when quantity falls below threshold, it does not automatically generate vendor Purchase Orders (PO) or auto-email suppliers."),
        ("3", "Excluded Point-of-Sale (POS) Hardware & Payment Gateways",
         "The platform manages inventory decrements and records sales totals in Rupees (₹); physical POS barcode thermal receipt printers and online payment gateways (Stripe/Razorpay) are excluded."),
        ("4", "Deterministic Thresholds (No ML Demand Forecasting)",
         "Reorder points are configured by administrators. Predictive machine-learning forecasting based on seasonal demand, sales velocity, or lead times is outside the project boundaries."),
        ("5", "Cloud Deployment Ephemeral Storage Considerations",
         "On free-tier cloud PaaS platforms like Render, SQLite local disk resets on redeployment unless mounted to a persistent cloud disk or connected to managed PostgreSQL."),
    ]

    for i, (num, heading, desc) in enumerate(limits):
        y = Inches(1.5) + i * (Inches(0.9) + Inches(0.15))

        card = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), y, Inches(11.733), Inches(0.9))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = BORDER_COLOR

        # Circle badge
        nb = s11.shapes.add_shape(MSO_SHAPE.OVAL, Inches(1.05), y + Inches(0.2), Inches(0.48), Inches(0.48))
        nb.fill.solid()
        nb.fill.fore_color.rgb = RGBColor(71, 85, 105)
        nb.line.fill.background()
        tf_nb = nb.text_frame
        p_nb = tf_nb.paragraphs[0]
        p_nb.text = num
        p_nb.alignment = PP_ALIGN.CENTER
        p_nb.font.name = FONT_FAMILY
        p_nb.font.size = Pt(13)
        p_nb.font.bold = True
        p_nb.font.color.rgb = TEXT_LIGHT

        # Text
        tb = s11.shapes.add_textbox(Inches(1.7), y + Inches(0.1), Inches(10.6), Inches(0.72))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_top = tf.margin_left = tf.margin_right = tf.margin_bottom = 0

        ph = tf.paragraphs[0]
        ph.text = heading
        ph.font.name = FONT_FAMILY
        ph.font.size = Pt(12)
        ph.font.bold = True
        ph.font.color.rgb = TEXT_DARK
        ph.space_after = Pt(2)

        pd = tf.add_paragraph()
        pd.text = desc
        pd.font.name = FONT_FAMILY
        pd.font.size = Pt(10)
        pd.font.color.rgb = TEXT_MUTED

    # ═══════════════════════════════════════════════════════════════════════════
    # SLIDE 12: Conclusion, Future Scope & Q&A
    # ═══════════════════════════════════════════════════════════════════════════
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12, BG_DARK)

    # Header
    cat_b = s12.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(8.0), Inches(0.35))
    tf_cb = cat_b.text_frame
    p_cb = tf_cb.paragraphs[0]
    p_cb.text = "MCA FINAL-YEAR PROJECT  ·  CONCLUSION & ROADMAP"
    p_cb.font.name = FONT_FAMILY
    p_cb.font.size = Pt(10)
    p_cb.font.bold = True
    p_cb.font.color.rgb = RGBColor(96, 165, 250)

    # Title
    t_box = s12.shapes.add_textbox(Inches(0.8), Inches(0.8), Inches(10.0), Inches(0.6))
    tf_tb = t_box.text_frame
    p_tb = tf_tb.paragraphs[0]
    p_tb.text = "Conclusion and Future Scope"
    p_tb.font.name = FONT_FAMILY
    p_tb.font.size = Pt(24)
    p_tb.font.bold = True
    p_tb.font.color.rgb = TEXT_LIGHT

    # Two column cards (Conclusion vs Future Scope)
    # Left Card: Conclusion
    c_card = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.7), Inches(4.5))
    c_card.fill.solid()
    c_card.fill.fore_color.rgb = RGBColor(24, 34, 53)
    c_card.line.color.rgb = RGBColor(51, 65, 85)

    c_head = s12.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.0), Inches(1.7), Inches(5.3), Inches(0.45))
    c_head.fill.solid()
    c_head.fill.fore_color.rgb = PRIMARY_BLUE
    c_head.line.fill.background()
    tf_ch = c_head.text_frame
    p_ch = tf_ch.paragraphs[0]
    p_ch.text = "PROJECT CONCLUSION"
    p_ch.alignment = PP_ALIGN.CENTER
    p_ch.font.name = FONT_FAMILY
    p_ch.font.size = Pt(11)
    p_ch.font.bold = True
    p_ch.font.color.rgb = TEXT_LIGHT

    tb_c = s12.shapes.add_textbox(Inches(1.05), Inches(2.3), Inches(5.2), Inches(3.5))
    tf_c = tb_c.text_frame
    tf_c.word_wrap = True
    tf_c.margin_top = tf_c.margin_left = tf_c.margin_right = tf_c.margin_bottom = 0

    c_points = [
        ("Full SRS Implementation", "Successfully engineered a centralized web platform fulfilling all FR-001 through FR-008 and NFR requirements."),
        ("Zero Negative Stock Guarantee", "Strict pre-validation and atomic transaction boundaries eliminate phantom inventory and overselling."),
        ("Tailored Computer Catalog", "Customized with 18 real computer components, IT hardware suppliers, and pricing in Indian Rupees (₹)."),
        ("Dual Reporting Engine", "Dynamic Chart.js on-screen visual insights paired with downloadable ReportLab PDF audit reports."),
        ("100% Traceability Pass Rate", "Automated test suite validates all 12 test cases (TC01-TC12) with zero failures."),
    ]

    for h, d in c_points:
        ph = tf_c.add_paragraph() if tf_c.paragraphs[0].text else tf_c.paragraphs[0]
        ph.text = f"✔ {h}: "
        ph.font.name = FONT_FAMILY
        ph.font.size = Pt(10)
        ph.font.bold = True
        ph.font.color.rgb = RGBColor(226, 232, 240)

        run = ph.add_run()
        run.text = d
        run.font.bold = False
        run.font.color.rgb = RGBColor(148, 163, 184)
        ph.space_after = Pt(8)

    # Right Card: Future Scope
    f_card = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.833), Inches(1.5), Inches(5.7), Inches(4.5))
    f_card.fill.solid()
    f_card.fill.fore_color.rgb = RGBColor(24, 34, 53)
    f_card.line.color.rgb = RGBColor(51, 65, 85)

    f_head = s12.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(7.033), Inches(1.7), Inches(5.3), Inches(0.45))
    f_head.fill.solid()
    f_head.fill.fore_color.rgb = ACCENT_TEAL
    f_head.line.fill.background()
    tf_fh = f_head.text_frame
    p_fh = tf_fh.paragraphs[0]
    p_fh.text = "FUTURE ENHANCEMENTS"
    p_fh.alignment = PP_ALIGN.CENTER
    p_fh.font.name = FONT_FAMILY
    p_fh.font.size = Pt(11)
    p_fh.font.bold = True
    p_fh.font.color.rgb = TEXT_LIGHT

    tb_f = s12.shapes.add_textbox(Inches(7.083), Inches(2.3), Inches(5.2), Inches(3.5))
    tf_f = tb_f.text_frame
    tf_f.word_wrap = True
    tf_f.margin_top = tf_f.margin_left = tf_f.margin_right = tf_f.margin_bottom = 0

    f_points = [
        ("Barcode & QR Code Scanning", "Camera/scanner integration for instantaneous stock-in and physical inventory counting."),
        ("Multi-Warehouse Logistics", "Inter-warehouse transfers, bin location tracking, and multi-depot inventory visibility."),
        ("Automated Supplier POs", "Auto-generating and emailing Purchase Orders to vendors when items trigger low stock."),
        ("Razorpay / UPI Payment Gateway", "Direct customer payment processing integrated into sales recording."),
        ("AI Demand Forecasting", "Machine learning regression forecasting seasonal computer hardware requirements."),
    ]

    for h, d in f_points:
        ph = tf_f.add_paragraph() if tf_f.paragraphs[0].text else tf_f.paragraphs[0]
        ph.text = f"➔ {h}: "
        ph.font.name = FONT_FAMILY
        ph.font.size = Pt(10)
        ph.font.bold = True
        ph.font.color.rgb = RGBColor(226, 232, 240)

        run = ph.add_run()
        run.text = d
        run.font.bold = False
        run.font.color.rgb = RGBColor(148, 163, 184)
        ph.space_after = Pt(8)

    # Bottom Banner: Thank You
    ty_box = s12.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(6.25), Inches(11.733), Inches(0.7))
    ty_box.fill.solid()
    ty_box.fill.fore_color.rgb = RGBColor(30, 41, 59)
    ty_box.line.color.rgb = PRIMARY_BLUE
    tf_ty = ty_box.text_frame
    p_ty = tf_ty.paragraphs[0]
    p_ty.text = "Thank you  ·  Questions & Answers"
    p_ty.alignment = PP_ALIGN.CENTER
    p_ty.font.name = FONT_FAMILY
    p_ty.font.size = Pt(13)
    p_ty.font.bold = True
    p_ty.font.color.rgb = RGBColor(147, 197, 253)

    # Save presentation
    prs.save(output_path)
    print(f"Presentation successfully created at: {output_path}")


if __name__ == "__main__":
    out_file = r"C:\Users\mohda\ims\Inventory_Management_System_Presentation.pptx"
    if len(sys.argv) > 1:
        out_file = sys.argv[1]
    create_ims_presentation(out_file)
