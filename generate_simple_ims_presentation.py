import os
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_presentation(output_path):
    prs = pptx.Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Theme Colors
    C_DARK_BG = RGBColor(15, 23, 42)         # #0F172A Slate 900
    C_LIGHT_BG = RGBColor(248, 250, 252)     # #F8FAFC Slate 50
    C_CARD_BG = RGBColor(255, 255, 255)      # Pure White
    C_CARD_BORDER = RGBColor(226, 232, 240)  # #E2E8F0 Slate 200
    C_BLUE = RGBColor(37, 99, 235)           # #2563EB Primary Blue
    C_BLUE_DARK = RGBColor(29, 78, 216)      # #1D4ED8 Deep Blue
    C_BLUE_LIGHT = RGBColor(239, 246, 255)   # #EFF6FF Tint
    C_GREEN = RGBColor(5, 150, 105)          # #059669 Emerald
    C_GREEN_LIGHT = RGBColor(236, 253, 245)  # #ECFDF5 Tint
    C_AMBER = RGBColor(217, 119, 6)          # #D97706 Amber
    C_AMBER_LIGHT = RGBColor(254, 243, 199)  # #FEF3C7 Tint
    C_TEXT_DARK = RGBColor(15, 23, 42)       # #0F172A
    C_TEXT_MUTED = RGBColor(71, 85, 105)     # #475569 Slate 600
    C_TEXT_LIGHT = RGBColor(255, 255, 255)
    C_TEXT_LIGHT_MUTED = RGBColor(148, 163, 184) # #94A3B8

    def add_bg(slide, color):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = color
        bg.line.fill.background()
        return bg

    def add_header(slide, badge, title, subtitle, dark=False):
        # Badge
        badge_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.45), Inches(2.8), Inches(0.32))
        badge_box.fill.solid()
        badge_box.fill.fore_color.rgb = RGBColor(30, 41, 59) if dark else C_BLUE_LIGHT
        badge_box.line.color.rgb = RGBColor(51, 65, 85) if dark else RGBColor(191, 219, 254)
        badge_box.line.width = Pt(1)
        tf_b = badge_box.text_frame
        tf_b.word_wrap = True
        tf_b.margin_left = tf_b.margin_right = tf_b.margin_top = tf_b.margin_bottom = 0
        p_b = tf_b.paragraphs[0]
        p_b.text = badge.upper()
        p_b.font.size = Pt(10)
        p_b.font.bold = True
        p_b.font.color.rgb = RGBColor(56, 189, 248) if dark else C_BLUE_DARK
        p_b.alignment = PP_ALIGN.CENTER

        # Title
        tb_t = slide.shapes.add_textbox(Inches(0.8), Inches(0.85), Inches(11.7), Inches(0.55))
        tf_t = tb_t.text_frame
        tf_t.word_wrap = True
        tf_t.margin_left = tf_t.margin_right = tf_t.margin_top = tf_t.margin_bottom = 0
        p_t = tf_t.paragraphs[0]
        p_t.text = title
        p_t.font.size = Pt(22)
        p_t.font.bold = True
        p_t.font.color.rgb = C_TEXT_LIGHT if dark else C_TEXT_DARK

        # Subtitle
        tb_s = slide.shapes.add_textbox(Inches(0.8), Inches(1.42), Inches(11.7), Inches(0.35))
        tf_s = tb_s.text_frame
        tf_s.word_wrap = True
        tf_s.margin_left = tf_s.margin_right = tf_s.margin_top = tf_s.margin_bottom = 0
        p_s = tf_s.paragraphs[0]
        p_s.text = subtitle
        p_s.font.size = Pt(12)
        p_s.font.color.rgb = C_TEXT_LIGHT_MUTED if dark else C_TEXT_MUTED

    def add_footer(slide, current, total=12, dark=False):
        tb = slide.shapes.add_textbox(Inches(11.2), Inches(7.05), Inches(1.3), Inches(0.3))
        tf = tb.text_frame
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = f"{current:02d} / {total:02d}"
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = C_TEXT_LIGHT_MUTED if dark else RGBColor(148, 163, 184)
        p.alignment = PP_ALIGN.RIGHT

    def make_card(slide, left, top, width, height, bg=C_CARD_BG, border=C_CARD_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg
        card.line.color.rgb = border
        card.line.width = Pt(1)
        return card

    # =========================================================================
    # SLIDE 1: Title Slide (Dark Hero)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    add_bg(s1, C_DARK_BG)

    # Accent Top Pill
    badge1 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.9), Inches(3.2), Inches(0.35))
    badge1.fill.solid()
    badge1.fill.fore_color.rgb = RGBColor(30, 41, 59)
    badge1.line.color.rgb = RGBColor(51, 65, 85)
    p = badge1.text_frame.paragraphs[0]
    p.text = "MCA FINAL-YEAR PROJECT DEFENSE"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = RGBColor(56, 189, 248)
    p.alignment = PP_ALIGN.CENTER

    # Main Project Title
    tb_title = s1.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(11.7), Inches(1.2))
    p1 = tb_title.text_frame.paragraphs[0]
    p1.text = "Inventory Management System (IMS)"
    p1.font.size = Pt(36)
    p1.font.bold = True
    p1.font.color.rgb = C_TEXT_LIGHT

    p2 = tb_title.text_frame.add_paragraph()
    p2.text = "A Web-Based Stock Control, Relational Traceability & Automated Invoicing System"
    p2.font.size = Pt(16)
    p2.font.color.rgb = RGBColor(147, 197, 253)

    # Description Box
    tb_desc = s1.shapes.add_textbox(Inches(0.8), Inches(2.8), Inches(11.7), Inches(0.8))
    pd = tb_desc.text_frame.paragraphs[0]
    pd.text = "Engineered specifically for computer hardware retailers with real-time stock deduction, ACID transaction safety, automated Indian Rupee (₹) billing, and ReportLab PDF invoice generation."
    pd.font.size = Pt(13)
    pd.font.color.rgb = C_TEXT_LIGHT_MUTED

    # Presenter & Guide Info Card
    info_card = make_card(s1, Inches(0.8), Inches(3.8), Inches(11.733), Inches(1.8), bg=RGBColor(30, 41, 59), border=RGBColor(51, 65, 85))
    tb_info = s1.shapes.add_textbox(Inches(1.1), Inches(4.0), Inches(11.1), Inches(1.4))
    tf_i = tb_info.text_frame
    
    p = tf_i.paragraphs[0]
    p.text = "Presented By:  Mohd Wasi Imam"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_TEXT_LIGHT

    p = tf_i.add_paragraph()
    p.text = "Supervisor:      Dr. Faisal Anwer"
    p.font.size = Pt(13)
    p.font.color.rgb = RGBColor(226, 232, 240)

    p = tf_i.add_paragraph()
    p.text = "Department:    Department of Computer Science  ·  Aligarh Muslim University (AMU)"
    p.font.size = Pt(12)
    p.font.color.rgb = RGBColor(148, 163, 184)

    # Feature Pills at Bottom
    pills = ["Python 3.13 & Django 5.x", "ACID Relational Model", "Rupee (₹) Invoicing", "ReportLab PDF Engine", "Render PaaS Deployment"]
    left_start = Inches(0.8)
    for pill in pills:
        pill_w = Inches(2.2)
        p_box = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_start, Inches(5.9), pill_w, Inches(0.42))
        p_box.fill.solid()
        p_box.fill.fore_color.rgb = RGBColor(15, 23, 42)
        p_box.line.color.rgb = C_BLUE
        p = p_box.text_frame.paragraphs[0]
        p.text = pill
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = RGBColor(191, 219, 254)
        p.alignment = PP_ALIGN.CENTER
        left_start += Inches(2.38)

    add_footer(s1, 1, dark=True)

    # =========================================================================
    # SLIDE 2: The Problem
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_bg(s2, C_LIGHT_BG)
    add_header(s2, "Background & Motivation", "The Problem: Pain Points in Hardware Retail", "High-value computer hardware retail faces severe operational and financial risks without structured software.")

    problems = [
        ("1", "Manual & Paper-Based Stock Tracking", "Spreadsheets and physical registers lead to human counting errors, lost invoices, and inaccurate records of high-value components (CPUs, GPUs, Motherboards).", C_AMBER, C_AMBER_LIGHT),
        ("2", "Inventory Overselling & Stockouts", "Lack of real-time synchronization between sales counters and stockrooms causes accidental selling of out-of-stock items and delayed customer deliveries.", C_BLUE, C_BLUE_LIGHT),
        ("3", "Lack of Transactional Audit Trail", "Store managers cannot trace who modified stock counts, when adjustments occurred, or whether missing items were due to damage, shrinkage, or supplier returns.", C_GREEN, C_GREEN_LIGHT),
        ("4", "Disconnected Billing & Rupee (₹) Pricing", "Traditional billing counters require manual re-entry of items, risking calculation errors, tax inaccuracies, and missing customer invoices.", C_BLUE_DARK, C_BLUE_LIGHT)
    ]

    card_top = Inches(1.9)
    for num, title, desc, num_color, num_bg in problems:
        c = make_card(s2, Inches(0.8), card_top, Inches(11.733), Inches(0.95))
        
        nb = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.05), card_top + Inches(0.18), Inches(0.6), Inches(0.6))
        nb.fill.solid()
        nb.fill.fore_color.rgb = num_bg
        nb.line.color.rgb = num_color
        p = nb.text_frame.paragraphs[0]
        p.text = num
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = num_color
        p.alignment = PP_ALIGN.CENTER

        tb = s2.shapes.add_textbox(Inches(1.85), card_top + Inches(0.12), Inches(10.4), Inches(0.75))
        tf = tb.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.size = Pt(13)
        p1.font.bold = True
        p1.font.color.rgb = C_TEXT_DARK
        
        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(11)
        p2.font.color.rgb = C_TEXT_MUTED
        
        card_top += Inches(1.08)

    callout = make_card(s2, Inches(0.8), Inches(6.32), Inches(11.733), Inches(0.58), bg=C_BLUE_LIGHT, border=RGBColor(191, 219, 254))
    p = callout.text_frame.paragraphs[0]
    p.text = "Need: An integrated web platform providing centralized cataloging, ACID sales deduction, and automated Rupee (₹) invoicing."
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_BLUE_DARK
    p.alignment = PP_ALIGN.CENTER

    add_footer(s2, 2)

    # =========================================================================
    # SLIDE 3: Objectives
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_bg(s3, C_LIGHT_BG)
    add_header(s3, "Project Scope", "Project Objectives", "Designed to deliver complete operational control, data integrity, and compliance for retail stores.")

    objs = [
        ("01", "Secure Role-Based Access Control", "Enforce strict privilege separation between Administrator (catalog, users, suppliers, reports) and Staff (POS billing, stock search) with session authentication.", C_BLUE),
        ("02", "Centralized Hardware Catalog", "Maintain complete computer hardware catalog (CPUs, GPUs, RAM, SSDs, Motherboards) with specifications, supplier links, cost & selling prices in Indian Rupees (₹).", C_GREEN),
        ("03", "Real-Time Low-Stock Warnings", "Automate low-stock alerts based on configurable reorder thresholds to prevent stockouts and provide one-click restocking workflows.", C_AMBER),
        ("04", "ACID-Compliant Sales & Invoicing", "Guarantee zero partial transactions using database atomicity (@transaction.atomic), deducting inventory and generating printable PDF invoices simultaneously.", C_BLUE_DARK)
    ]

    coords = [
        (Inches(0.8), Inches(1.95)),
        (Inches(6.8), Inches(1.95)),
        (Inches(0.8), Inches(4.15)),
        (Inches(6.8), Inches(4.15))
    ]

    for (num, title, desc, col), (left, top) in zip(objs, coords):
        c = make_card(s3, left, top, Inches(5.733), Inches(2.0))
        
        np = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left + Inches(0.3), top + Inches(0.25), Inches(0.7), Inches(0.35))
        np.fill.solid()
        np.fill.fore_color.rgb = C_BLUE_LIGHT
        np.line.color.rgb = col
        p = np.text_frame.paragraphs[0]
        p.text = num
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = col
        p.alignment = PP_ALIGN.CENTER

        tb = s3.shapes.add_textbox(left + Inches(0.3), top + Inches(0.72), Inches(5.1), Inches(1.15))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = C_TEXT_DARK

        p = tf.add_paragraph()
        p.text = desc
        p.font.size = Pt(11)
        p.font.color.rgb = C_TEXT_MUTED

    b_banner = make_card(s3, Inches(0.8), Inches(6.35), Inches(11.733), Inches(0.55), bg=C_GREEN_LIGHT, border=RGBColor(167, 243, 208))
    p = b_banner.text_frame.paragraphs[0]
    p.text = "Target Scope: Complete software coverage of all functional requirements outlined in the SRS."
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_GREEN
    p.alignment = PP_ALIGN.CENTER

    add_footer(s3, 3)

    # =========================================================================
    # SLIDE 4: Proposed Solution: Pipeline
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_bg(s4, C_LIGHT_BG)
    add_header(s4, "Operational Flow", "Proposed Solution: 3-Stage Pipeline", "End-to-end stock and billing management ensuring zero inventory drift.")

    stages = [
        ("Stage 1", "Procure & Catalog", [
            "Register verified computer suppliers (Intel, ASUS, Corsair, etc.)",
            "Classify hardware: Processors, GPUs, RAM, Motherboards, Storage",
            "Define SKU, reorder safety thresholds, and pricing in ₹",
            "Log Stock-In consignments with batch cost and supplier IDs"
        ], C_BLUE),
        ("Stage 2", "Validate & Transact", [
            "Sales staff search hardware via responsive POS terminal",
            "Cart dynamically calculates subtotal, tax, and total in Rupees (₹)",
            "System validates available quantity before order confirmation",
            "Executes atomic deduction using Django ORM transactions"
        ], C_GREEN),
        ("Stage 3", "Invoice & Audit", [
            "Generates unique Invoice ID (e.g., INV-20261121-0001)",
            "Creates immutable InventoryTransaction audit record",
            "Instantly builds downloadable, GST-ready ReportLab PDF invoice",
            "Updates dashboard KPI counters and low-stock warning triggers"
        ], C_BLUE_DARK)
    ]

    card_w = Inches(3.75)
    left_pos = Inches(0.8)
    for st_num, st_title, points, col in stages:
        c = make_card(s4, left_pos, Inches(1.95), card_w, Inches(4.15))

        tag = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_pos + Inches(0.3), Inches(2.2), Inches(1.2), Inches(0.32))
        tag.fill.solid()
        tag.fill.fore_color.rgb = C_BLUE_LIGHT
        tag.line.color.rgb = col
        p = tag.text_frame.paragraphs[0]
        p.text = st_num.upper()
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = col
        p.alignment = PP_ALIGN.CENTER

        tb = s4.shapes.add_textbox(left_pos + Inches(0.3), Inches(2.65), card_w - Inches(0.6), Inches(0.5))
        p = tb.text_frame.paragraphs[0]
        p.text = st_title
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = C_TEXT_DARK

        tb_b = s4.shapes.add_textbox(left_pos + Inches(0.3), Inches(3.2), card_w - Inches(0.6), Inches(2.7))
        tf = tb_b.text_frame
        tf.word_wrap = True
        for idx, pt in enumerate(points):
            p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
            p.text = f"•  {pt}"
            p.font.size = Pt(11)
            p.font.color.rgb = C_TEXT_MUTED
            p.space_after = Pt(8)

        left_pos += Inches(4.0)

    banner = make_card(s4, Inches(0.8), Inches(6.32), Inches(11.733), Inches(0.58), bg=C_BLUE_LIGHT, border=RGBColor(191, 219, 254))
    p = banner.text_frame.paragraphs[0]
    p.text = "ACID Guarantee: If stock deduction fails or quantity is insufficient, entire checkout rolls back with zero data loss."
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_BLUE_DARK
    p.alignment = PP_ALIGN.CENTER

    add_footer(s4, 4)

    # =========================================================================
    # SLIDE 5: System Architecture
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_bg(s5, C_LIGHT_BG)
    add_header(s5, "System Design", "System Architecture & 3-Tier Design", "Clean separation of presentation, business logic, and relational persistence.")

    tiers = [
        ("Presentation Tier (Frontend)", "User Interface & Interaction", [
            "Responsive HTML5 & CSS3 layout powered by Bootstrap 5",
            "Jinja2 server-side rendering for secure template hydration",
            "Vanilla JavaScript for dynamic POS shopping cart & modal dialogs",
            "Cross-device support: Optimized for desktop PCs, POS screens & tablets"
        ], C_BLUE),
        ("Logic Tier (Django Backend)", "Business Rules & Invoicing Engine", [
            "Django 5.x MTV Architecture with strict Role-Based Access Control",
            "Custom session authentication middleware & CSRF security tokens",
            "Sales transaction service wrapped in database atomic locks",
            "ReportLab 4.x PDF Engine generating on-the-fly printable invoices"
        ], C_GREEN),
        ("Data Tier (Database)", "Relational Storage & Data Integrity", [
            "Normalized schema: Users, Categories, Suppliers, Products, Sales",
            "Foreign keys with PROTECT constraints preventing orphan sales records",
            "Enforced non-negative quantity check constraints in database schema",
            "SQLite3 for local testing; production-ready for PostgreSQL cloud"
        ], C_BLUE_DARK)
    ]

    card_w = Inches(3.75)
    left_pos = Inches(0.8)
    for t_name, t_sub, t_pts, col in tiers:
        c = make_card(s5, left_pos, Inches(1.95), card_w, Inches(4.15))

        tb = s5.shapes.add_textbox(left_pos + Inches(0.3), Inches(2.15), card_w - Inches(0.6), Inches(0.8))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = t_name
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = col

        p2 = tf.add_paragraph()
        p2.text = t_sub
        p2.font.size = Pt(10)
        p2.font.color.rgb = C_TEXT_MUTED

        tb_pts = s5.shapes.add_textbox(left_pos + Inches(0.3), Inches(3.05), card_w - Inches(0.6), Inches(2.9))
        tf_pts = tb_pts.text_frame
        tf_pts.word_wrap = True
        for idx, pt in enumerate(t_pts):
            p = tf_pts.paragraphs[0] if idx == 0 else tf_pts.add_paragraph()
            p.text = f"•  {pt}"
            p.font.size = Pt(11)
            p.font.color.rgb = C_TEXT_MUTED
            p.space_after = Pt(8)

        left_pos += Inches(4.0)

    c_banner = make_card(s5, Inches(0.8), Inches(6.32), Inches(11.733), Inches(0.58), bg=C_BLUE_LIGHT, border=RGBColor(191, 219, 254))
    p = c_banner.text_frame.paragraphs[0]
    p.text = "Deployment Architecture: Gunicorn WSGI server with WhiteNoise static asset pipeline deployed on Render PaaS."
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_BLUE_DARK
    p.alignment = PP_ALIGN.CENTER

    add_footer(s5, 5)

    # =========================================================================
    # SLIDE 6: Technology Stack
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_bg(s6, C_LIGHT_BG)
    add_header(s6, "Implementation Tools", "Technology Stack & Rationale", "Selected for reliability, developer velocity, enterprise security, and cloud readiness.")

    techs = [
        ("Backend Framework", "Python 3.13 & Django 5.x", "Powers core application logic, database ORM, user authentication, and admin interfaces. Django's built-in defenses protect against SQL injection, CSRF, and XSS out-of-the-box.", C_BLUE),
        ("Frontend & Styling", "Bootstrap 5 & Vanilla JS", "Delivers clean, modern, responsive UI tailored for retail POS cashiers. Lightweight JavaScript provides dynamic item addition and total recalculation without heavy framework overhead.", C_GREEN),
        ("Database Engine", "SQLite3 / PostgreSQL", "Development uses lightweight SQLite3; production architecture supports enterprise PostgreSQL. Relational foreign keys maintain strict integrity across all sales and stock transactions.", C_AMBER),
        ("Document Generation", "ReportLab 4.x Engine", "Generates professional, printable PDF invoices on demand. Programmatically embeds shop details, customer info, line items, and prices in Indian Rupees (₹).", C_BLUE_DARK),
        ("Cloud Hosting & CI/CD", "Render PaaS & Git", "Configured via render.yaml and build.sh for automatic continuous deployment. Employs WhiteNoise for fast static asset serving and Gunicorn for multi-worker WSGI concurrency.", C_BLUE)
    ]

    card_top = Inches(1.95)
    for role, tech_name, rationale, col in techs:
        c = make_card(s6, Inches(0.8), card_top, Inches(11.733), Inches(0.78))

        rb = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.05), card_top + Inches(0.16), Inches(2.2), Inches(0.45))
        rb.fill.solid()
        rb.fill.fore_color.rgb = C_BLUE_LIGHT
        rb.line.color.rgb = col
        p = rb.text_frame.paragraphs[0]
        p.text = role
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = col
        p.alignment = PP_ALIGN.CENTER

        tb = s6.shapes.add_textbox(Inches(3.45), card_top + Inches(0.1), Inches(8.9), Inches(0.6))
        tf = tb.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = f"{tech_name}  —  "
        p1.font.size = Pt(12)
        p1.font.bold = True
        p1.font.color.rgb = C_TEXT_DARK
        
        run = p1.add_run()
        run.text = rationale
        run.font.size = Pt(11)
        run.font.bold = False
        run.font.color.rgb = C_TEXT_MUTED

        card_top += Inches(0.87)

    add_footer(s6, 6)

    # =========================================================================
    # SLIDE 7: Database Design
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_bg(s7, C_LIGHT_BG)
    add_header(s7, "Data Modeling", "Database Design & Relational Schema", "7 relational tables modeled to ensure consistency, non-negative quantities, and full traceability.")

    col_w = Inches(5.733)
    c1 = make_card(s7, Inches(0.8), Inches(1.95), col_w, Inches(4.15))
    c2 = make_card(s7, Inches(6.8), Inches(1.95), col_w, Inches(4.15))

    # Left Column: Catalog & Auth
    tb_l = s7.shapes.add_textbox(Inches(1.05), Inches(2.1), col_w - Inches(0.5), Inches(3.8))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True

    p = tf_l.paragraphs[0]
    p.text = "Catalog & User Entities"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_BLUE

    entities_left = [
        ("User (Custom RBAC)", "Fields: username, role (ADMIN | STAFF), email, password hash. Enforces role-based view and action permissions."),
        ("Category", "Fields: name, description. Organizes hardware into: Processors, Graphics Cards, Memory, Storage, Motherboards."),
        ("Supplier", "Fields: name, contact_person, email, phone, address. Tracks official hardware distribution partners."),
        ("Product", "Fields: sku, name, category_id, supplier_id, cost_price, selling_price (₹), current_stock, reorder_level. Core hardware inventory table.")
    ]
    for ent, desc in entities_left:
        p = tf_l.add_paragraph()
        p.text = f"•  {ent}: "
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = C_TEXT_DARK
        p.space_before = Pt(6)
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = C_TEXT_MUTED

    # Right Column: Transactions & Sales
    tb_r = s7.shapes.add_textbox(Inches(7.05), Inches(2.1), col_w - Inches(0.5), Inches(3.8))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True

    p = tf_r.paragraphs[0]
    p.text = "Transactional & Audit Entities"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_GREEN

    entities_right = [
        ("Sale (Invoice Header)", "Fields: invoice_number, customer_name, customer_phone, total_amount (₹), payment_mode, created_by, created_at. Stores completed transactions."),
        ("SaleItem (Invoice Line Items)", "Fields: sale_id, product_id, quantity, unit_price (₹), line_total (₹). Captures exact price at moment of sale."),
        ("InventoryTransaction (Audit Trail)", "Fields: product_id, transaction_type (IN | OUT | ADJUST), quantity_delta, previous_stock, new_stock, reason, created_by, timestamp. Immutable ledger.")
    ]
    for ent, desc in entities_right:
        p = tf_r.add_paragraph()
        p.text = f"•  {ent}: "
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = C_TEXT_DARK
        p.space_before = Pt(8)
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = C_TEXT_MUTED

    i_banner = make_card(s7, Inches(0.8), Inches(6.32), Inches(11.733), Inches(0.58), bg=C_BLUE_LIGHT, border=RGBColor(191, 219, 254))
    p = i_banner.text_frame.paragraphs[0]
    p.text = "Referential Integrity: ForeignKey on_delete=PROTECT prevents accidental deletion of products linked to historical sales records."
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_BLUE_DARK
    p.alignment = PP_ALIGN.CENTER

    add_footer(s7, 7)

    # =========================================================================
    # SLIDE 8: Core Functional Modules
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_bg(s8, C_LIGHT_BG)
    add_header(s8, "Application Modules", "Core Functional Modules", "Interactive modules covering user workflows from administration to checkout.")

    modules = [
        ("Module 1: Authentication & RBAC", "Access Control & Security", [
            "Secure session-based login with hashed credentials",
            "Role routing: Admins gain master control; Staff directed to POS",
            "Automatic session timeout and CSRF form protection",
            "Unauthorized users redirected away from administrative URLs"
        ], C_BLUE),
        ("Module 2: Hardware Catalog & Stock", "Inventory & Reorder Rules", [
            "Search, filter, and paginate computer hardware catalog",
            "Stock badges: Green (> reorder level), Amber (low stock), Red (zero)",
            "Stock Inward workflow to receive new consignments from suppliers",
            "Inventory adjustments with mandatory audit explanation"
        ], C_GREEN),
        ("Module 3: POS Billing & Invoicing (₹)", "Sales Counter & Checkout", [
            "Live hardware search with instant stock availability check",
            "Dynamic cart calculation: Unit price, quantity, and line total in ₹",
            "Cash, Card, or UPI payment method tracking",
            "Atomic checkout preventing negative stock commits"
        ], C_BLUE_DARK),
        ("Module 4: Reports & Audit Trail", "Analytics & PDF Generation", [
            "Real-time Dashboard KPI counters: Stock count, Low Stock, Sales in ₹",
            "Instant ReportLab PDF Invoice generation with clean shop header",
            "Comprehensive Inventory Transaction log tracing all movements",
            "Printable daily sales summaries for cashier reconciliation"
        ], C_AMBER)
    ]

    coords = [
        (Inches(0.8), Inches(1.95)),
        (Inches(6.8), Inches(1.95)),
        (Inches(0.8), Inches(4.25)),
        (Inches(6.8), Inches(4.25))
    ]

    for (title, sub, bullets, col), (left, top) in zip(modules, coords):
        c = make_card(s8, left, top, Inches(5.733), Inches(2.1))

        tb = s8.shapes.add_textbox(left + Inches(0.25), top + Inches(0.15), Inches(5.2), Inches(0.55))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = col

        p2 = tf.add_paragraph()
        p2.text = sub
        p2.font.size = Pt(10)
        p2.font.color.rgb = C_TEXT_MUTED

        tb_b = s8.shapes.add_textbox(left + Inches(0.25), top + Inches(0.75), Inches(5.2), Inches(1.25))
        tf_b = tb_b.text_frame
        tf_b.word_wrap = True
        for idx, pt in enumerate(bullets):
            p = tf_b.paragraphs[0] if idx == 0 else tf_b.add_paragraph()
            p.text = f"•  {pt}"
            p.font.size = Pt(10.5)
            p.font.color.rgb = C_TEXT_MUTED
            p.space_after = Pt(3)

    add_footer(s8, 8)

    # =========================================================================
    # SLIDE 9: Testing & Verification Matrix
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_bg(s9, C_LIGHT_BG)
    add_header(s9, "Quality Assurance", "Testing & Verification Matrix", "Validation of functional requirements against the Software Requirements Specification (SRS).")

    col_w = Inches(5.733)
    c_left = make_card(s9, Inches(0.8), Inches(1.95), col_w, Inches(4.15))
    tb_l = s9.shapes.add_textbox(Inches(1.05), Inches(2.1), col_w - Inches(0.5), Inches(3.8))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True

    p = tf_l.paragraphs[0]
    p.text = "SRS Test Suite Coverage (Table 3)"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_BLUE

    test_groups = [
        ("Authentication Tests (TC01 - TC02)", "Valid credentials permit entry; invalid logins rejected; staff prevented from accessing admin settings."),
        ("Product Catalog & CRUD (TC03 - TC04)", "Adding, editing, and categorizing computer hardware components with duplicate SKU prevention."),
        ("Stock Validation & Rules (TC05 - TC06)", "Verifies that negative stock quantities are blocked and low-stock warning flags trigger correctly."),
        ("Atomic Sales Invoicing (TC07 - TC08)", "Simulates concurrent checkout; verifies atomic deduction of stock and total sales calculation in Rupees (₹)."),
        ("PDF Generation & Exports (TC09 - TC10)", "Validates ReportLab invoice rendering with invoice headers, line items, and Rupee formatting.")
    ]
    for grp, desc in test_groups:
        p = tf_l.add_paragraph()
        p.text = f"•  {grp}: "
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = C_TEXT_DARK
        p.space_before = Pt(6)
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = C_TEXT_MUTED

    c_right = make_card(s9, Inches(6.8), Inches(1.95), col_w, Inches(4.15))
    tb_r = s9.shapes.add_textbox(Inches(7.05), Inches(2.1), col_w - Inches(0.5), Inches(3.8))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True

    p = tf_r.paragraphs[0]
    p.text = "Automated Test Execution Results"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_GREEN

    stats = [
        ("Total Test Cases", "12 of 12 Executed"),
        ("Test Execution Status", "OK — 100% Passed"),
        ("Failures / Errors", "0 Failures, 0 Errors"),
        ("Test Suite Runtime", "22.31 Seconds"),
        ("Data Consistency", "100% ACID Integrity Verified")
    ]
    for label, val in stats:
        p = tf_r.add_paragraph()
        p.text = f"{label}: "
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = C_TEXT_DARK
        p.space_before = Pt(8)
        run = p.add_run()
        run.text = val
        run.font.bold = True
        run.font.color.rgb = C_GREEN if "Pass" in val or "OK" in val or "0" in val or "100%" in val else C_BLUE

    term_box = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.05), Inches(4.7), col_w - Inches(0.5), Inches(1.15))
    term_box.fill.solid()
    term_box.fill.fore_color.rgb = C_DARK_BG
    term_box.line.color.rgb = RGBColor(51, 65, 85)
    tf_term = term_box.text_frame
    tf_term.margin_left = Inches(0.15)
    p = tf_term.paragraphs[0]
    p.text = "$ python manage.py test inventory"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = RGBColor(56, 189, 248)
    
    p = tf_term.add_paragraph()
    p.text = "Ran 12 tests in 22.311s\nOK (12 passed, 0 failures)"
    p.font.size = Pt(10)
    p.font.color.rgb = RGBColor(167, 243, 208)

    banner = make_card(s9, Inches(0.8), Inches(6.32), Inches(11.733), Inches(0.58), bg=C_GREEN_LIGHT, border=RGBColor(167, 243, 208))
    p = banner.text_frame.paragraphs[0]
    p.text = "Verification Outcome: Complete functional compliance confirmed against SRS Table 3 verification matrix."
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_GREEN
    p.alignment = PP_ALIGN.CENTER

    add_footer(s9, 9)

    # =========================================================================
    # SLIDE 10: Hardware Catalog & Invoicing Showcase
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_bg(s10, C_LIGHT_BG)
    add_header(s10, "Catalog & Invoicing", "Computer Hardware Catalog & Rupee (₹) Billing", "Configured exclusively for computer hardware items with Indian Rupee currency standard.")

    c_left = make_card(s10, Inches(0.8), Inches(1.95), Inches(6.8), Inches(4.15))
    tb_l = s10.shapes.add_textbox(Inches(1.0), Inches(2.1), Inches(6.4), Inches(3.8))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True

    p = tf_l.paragraphs[0]
    p.text = "Live Computer Hardware Inventory (Sample SKUs)"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_BLUE

    items = [
        ("Intel Core i7-14700K 20-Core", "Processors", "₹38,500", "In Stock (15)"),
        ("AMD Ryzen 7 7800X3D 8-Core", "Processors", "₹39,999", "In Stock (12)"),
        ("NVIDIA GeForce RTX 4070 Super 12GB", "Graphics Cards", "₹54,999", "Low Stock (4)"),
        ("AMD Radeon RX 7600 8GB GDDR6", "Graphics Cards", "₹24,500", "In Stock (10)"),
        ("ASUS ROG Strix B760-F Gaming WiFi", "Motherboards", "₹21,500", "In Stock (8)"),
        ("Corsair Vengeance 32GB (2x16GB) DDR5", "Memory (RAM)", "₹9,800", "In Stock (25)"),
        ("Samsung 990 Pro 2TB PCIe 4.0 NVMe SSD", "Storage", "₹16,500", "In Stock (18)"),
        ("Corsair RM750e 750W 80+ Gold PSU", "Power Supply", "₹8,900", "In Stock (14)")
    ]

    for name, cat, price, status in items:
        p = tf_l.add_paragraph()
        p.text = f"•  {name}  [{cat}]  —  {price}  ({status})"
        p.font.size = Pt(10)
        p.font.color.rgb = C_TEXT_DARK
        p.space_before = Pt(3)

    c_right = make_card(s10, Inches(7.8), Inches(1.95), Inches(4.733), Inches(4.15))
    tb_r = s10.shapes.add_textbox(Inches(8.05), Inches(2.1), Inches(4.2), Inches(3.8))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True

    p = tf_r.paragraphs[0]
    p.text = "Automated Invoicing Workflow"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_GREEN

    flow_steps = [
        ("1. POS Cart Selection", "Staff selects hardware components; quantity and line totals update dynamically in Indian Rupees (₹)."),
        ("2. Real-Time Stock Lock", "System verifies available stock against cart quantities before proceeding to checkout."),
        ("3. Atomic Commit", "Simultaneously creates `Sale`, `SaleItem` rows and deducts inventory counts atomically."),
        ("4. PDF Generation", "ReportLab instantly builds a professional PDF tax invoice with invoice number, date, cashier, itemized prices, and grand total in ₹."),
        ("5. Print & Archive", "Direct browser download and printable copy for customer handoff.")
    ]
    for step_title, step_desc in flow_steps:
        p = tf_r.add_paragraph()
        p.text = f"{step_title}: "
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = C_TEXT_DARK
        p.space_before = Pt(4)
        run = p.add_run()
        run.text = step_desc
        run.font.bold = False
        run.font.color.rgb = C_TEXT_MUTED

    banner = make_card(s10, Inches(0.8), Inches(6.32), Inches(11.733), Inches(0.58), bg=C_BLUE_LIGHT, border=RGBColor(191, 219, 254))
    p = banner.text_frame.paragraphs[0]
    p.text = "Currency Standard: All database records, UI templates, and PDF invoices exclusively calculate and display in Indian Rupees (₹)."
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_BLUE_DARK
    p.alignment = PP_ALIGN.CENTER

    add_footer(s10, 10)

    # =========================================================================
    # SLIDE 11: Limitations & Future Scope
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_bg(s11, C_LIGHT_BG)
    add_header(s11, "Evaluation & Roadmap", "System Limitations & Future Enhancements", "Transparent engineering boundaries and proposed roadmap for scaling to enterprise retail chains.")

    col_w = Inches(5.733)
    c_left = make_card(s11, Inches(0.8), Inches(1.95), col_w, Inches(4.15))
    tb_l = s11.shapes.add_textbox(Inches(1.05), Inches(2.1), col_w - Inches(0.5), Inches(3.8))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True

    p = tf_l.paragraphs[0]
    p.text = "Current Architectural Boundaries"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_AMBER

    limits = [
        ("Single-Store Scope", "Optimized for a single retail showroom; inter-branch transfers and multi-warehouse routing require schema expansion."),
        ("Rule-Based Reorder Thresholds", "Uses static safety reorder quantities rather than predictive machine learning algorithms."),
        ("Hardware Peripheral Connectivity", "Barcode scanners and thermal receipt printers interface via standard browser printing APIs rather than native ESC/POS serial drivers."),
        ("Payment Gateway Hooks", "Tracks Cash, Card, and UPI payments internally without external webhook integration to bank APIs."),
        ("Cloud Ephemeral Disk", "Free-tier Render uses ephemeral disk storage; production deployment benefits from attached persistent PostgreSQL.")
    ]
    for title, desc in limits:
        p = tf_l.add_paragraph()
        p.text = f"•  {title}: "
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = C_TEXT_DARK
        p.space_before = Pt(5)
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = C_TEXT_MUTED

    c_right = make_card(s11, Inches(6.8), Inches(1.95), col_w, Inches(4.15))
    tb_r = s11.shapes.add_textbox(Inches(7.05), Inches(2.1), col_w - Inches(0.5), Inches(3.8))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True

    p = tf_r.paragraphs[0]
    p.text = "Future Development Roadmap"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_GREEN

    roadmap = [
        ("Multi-Branch & Warehouse Transfers", "Support regional retail chains with central inventory consolidation and inter-store stock transfers."),
        ("Native Barcode & Peripheral SDK", "Direct integration with USB/Bluetooth barcode readers and thermal receipt printers for split-second checkout."),
        ("Payment Gateway Integration", "Direct integration with Razorpay / Stripe for dynamic UPI QR code generation and card processing."),
        ("AI Demand Forecasting", "Machine learning models trained on seasonal sales patterns to predict component demand and suggest optimal procurement orders."),
        ("Automated Supplier POs", "Automated email purchase order generation to hardware distributors when stock reaches critical thresholds.")
    ]
    for title, desc in roadmap:
        p = tf_r.add_paragraph()
        p.text = f"•  {title}: "
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = C_TEXT_DARK
        p.space_before = Pt(5)
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = C_TEXT_MUTED

    banner = make_card(s11, Inches(0.8), Inches(6.32), Inches(11.733), Inches(0.58), bg=C_BLUE_LIGHT, border=RGBColor(191, 219, 254))
    p = banner.text_frame.paragraphs[0]
    p.text = "Modularity: The Django MTV architecture enables adding multi-warehouse or payment gateways without refactoring existing logic."
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_BLUE_DARK
    p.alignment = PP_ALIGN.CENTER

    add_footer(s11, 11)

    # =========================================================================
    # SLIDE 12: Conclusion & Q&A (Dark Hero)
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    add_bg(s12, C_DARK_BG)

    badge12 = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.9), Inches(2.6), Inches(0.35))
    badge12.fill.solid()
    badge12.fill.fore_color.rgb = RGBColor(30, 41, 59)
    badge12.line.color.rgb = RGBColor(51, 65, 85)
    p = badge12.text_frame.paragraphs[0]
    p.text = "PROJECT SUMMARY"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = RGBColor(56, 189, 248)
    p.alignment = PP_ALIGN.CENTER

    tb_title = s12.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(11.7), Inches(0.8))
    p1 = tb_title.text_frame.paragraphs[0]
    p1.text = "Conclusion & Key Achievements"
    p1.font.size = Pt(30)
    p1.font.bold = True
    p1.font.color.rgb = C_TEXT_LIGHT

    card_sum = make_card(s12, Inches(0.8), Inches(2.4), Inches(11.733), Inches(2.4), bg=RGBColor(30, 41, 59), border=RGBColor(51, 65, 85))
    tb_s = s12.shapes.add_textbox(Inches(1.1), Inches(2.6), Inches(11.1), Inches(2.0))
    tf_s = tb_s.text_frame
    tf_s.word_wrap = True

    achievements = [
        ("Delivered Production-Ready IMS", "Built a comprehensive, end-to-end inventory management and billing system specifically tailored for computer hardware retailers."),
        ("Guaranteed Transaction Safety", "Enforced ACID relational integrity and non-negative stock constraints, eliminating stock discrepancies and overselling risks."),
        ("Commercial Rupee (₹) Billing", "Implemented real-time shopping cart billing in Indian Rupees (₹) with on-demand ReportLab PDF tax invoices."),
        ("100% SRS Verification", "Successfully verified all 12 test cases (TC01 - TC12) with zero failures, fulfilling all functional requirements."),
        ("Cloud Ready", "Configured and prepared for instant zero-downtime deployment on Render PaaS.")
    ]
    for idx, (head, text) in enumerate(achievements):
        p = tf_s.paragraphs[0] if idx == 0 else tf_s.add_paragraph()
        p.text = f"✔   {head}: "
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = RGBColor(147, 197, 253)
        p.space_before = Pt(4)
        run = p.add_run()
        run.text = text
        run.font.bold = False
        run.font.color.rgb = RGBColor(226, 232, 240)

    qa_card = make_card(s12, Inches(0.8), Inches(5.1), Inches(11.733), Inches(1.0), bg=RGBColor(24, 34, 53), border=C_BLUE)
    tb_qa = s12.shapes.add_textbox(Inches(1.0), Inches(5.2), Inches(11.3), Inches(0.8))
    tf_qa = tb_qa.text_frame
    p = tf_qa.paragraphs[0]
    p.text = "Thank You!  ·  Questions & Evaluation"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = C_TEXT_LIGHT
    p.alignment = PP_ALIGN.CENTER

    p2 = tf_qa.add_paragraph()
    p2.text = "Mohd Wasi Imam  ·  MCA Final Year  ·  Dept. of Computer Science, Aligarh Muslim University"
    p2.font.size = Pt(12)
    p2.font.color.rgb = RGBColor(148, 163, 184)
    p2.alignment = PP_ALIGN.CENTER

    add_footer(s12, 12, dark=True)

    prs.save(output_path)
    print(f"Presentation successfully created at: {output_path}")

if __name__ == '__main__':
    out = r"C:\Users\mohda\ims\Inventory_Management_System_Presentation.pptx"
    create_presentation(out)
