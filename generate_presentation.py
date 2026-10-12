"""
generate_presentation.py
Generates a comprehensive, professional, 18-slide widescreen (16:9) PowerPoint presentation
for the Integrated Multi-Layer Performance Optimization Framework (IMPOF).
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor

# -----------------------------------------------------------------------------
# Color Palette Constants (Modern Executive / Deep Tech Dark & Light Theme)
# -----------------------------------------------------------------------------
NAVY_DARK = RGBColor(15, 23, 42)      # #0F172A - Deep Background / Header
SLATE_CARD = RGBColor(30, 41, 59)     # #1E293B - Card Dark
SLATE_BORDER = RGBColor(51, 65, 85)   # #334155 - Card Border Dark
CYAN_ACCENT = RGBColor(14, 165, 233)  # #0EA5E9 - Primary Accent
CYAN_LIGHT = RGBColor(56, 189, 248)   # #38BDF8 - Bright Accent
EMERALD_GREEN = RGBColor(16, 185, 129)# #10B981 - Gain / Success
CRIMSON_ALERT = RGBColor(239, 68, 68) # #EF4444 - Bottleneck / Alert
PURPLE_AI = RGBColor(139, 92, 246)    # #8B5CF6 - Machine Learning / AI
TEXT_WHITE = RGBColor(255, 255, 255)  # White text
TEXT_LIGHT = RGBColor(226, 232, 240)  # Slate 200
TEXT_MUTED = RGBColor(148, 163, 184)  # Slate 400
TEXT_DARK = RGBColor(15, 23, 42)      # Dark text
BG_OFFWHITE = RGBColor(248, 250, 252) # Slate 50
CARD_WHITE = RGBColor(255, 255, 255)  # Pure White Card
CARD_BORDER_LIGHT = RGBColor(226, 232, 240) # Slate 200
HEADER_BG = RGBColor(241, 245, 249)  # Slate 100

FONT_HEADING = "Segoe UI"
FONT_BODY = "Segoe UI"

def create_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]  # Blank layout

    # Helper: Set background color of slide
    def set_slide_background(slide, color):
        bg_shape = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5)
        )
        bg_shape.fill.solid()
        bg_shape.fill.fore_color.rgb = color
        bg_shape.line.fill.background() # No border
        return bg_shape

    # Helper: Add Standard Slide Header (Dark/Light)
    def add_header(slide, category, title, dark=False):
        # Category Badge / Top Tracker
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.45), Inches(11.7), Inches(0.35))
        tf_c = cat_box.text_frame
        tf_c.word_wrap = True
        tf_c.margin_left = tf_c.margin_right = tf_c.margin_top = tf_c.margin_bottom = 0
        p_c = tf_c.paragraphs[0]
        p_c.text = category.upper()
        p_c.font.name = FONT_HEADING
        p_c.font.size = Pt(10)
        p_c.font.bold = True
        p_c.font.color.rgb = CYAN_LIGHT if dark else CYAN_ACCENT

        # Slide Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.7), Inches(0.65))
        tf_t = title_box.text_frame
        tf_t.word_wrap = True
        tf_t.margin_left = tf_t.margin_right = tf_t.margin_top = tf_t.margin_bottom = 0
        p_t = tf_t.paragraphs[0]
        p_t.text = title
        p_t.font.name = FONT_HEADING
        p_t.font.size = Pt(22)
        p_t.font.bold = True
        p_t.font.color.rgb = TEXT_WHITE if dark else NAVY_DARK

        # Subtle divider line
        divider = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.45), Inches(11.733), Inches(0.02)
        )
        divider.fill.solid()
        divider.fill.fore_color.rgb = SLATE_BORDER if dark else CARD_BORDER_LIGHT
        divider.line.fill.background()

    # Helper: Add Footer
    def add_footer(slide, slide_num, total=18, dark=False):
        footer_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.05), Inches(11.733), Inches(0.3))
        tf_f = footer_box.text_frame
        tf_f.word_wrap = True
        tf_f.margin_left = tf_f.margin_right = tf_f.margin_top = tf_f.margin_bottom = 0
        
        p = tf_f.paragraphs[0]
        p.text = "IMPOF — Integrated Multi-Layer Performance Optimization Framework"
        p.font.name = FONT_BODY
        p.font.size = Pt(9)
        p.font.color.rgb = TEXT_MUTED
        
        # Right aligned slide number
        p_num = tf_f.add_paragraph()
        p_num.text = f"Slide {slide_num} of {total}"
        p_num.alignment = PP_ALIGN.RIGHT
        p_num.font.name = FONT_BODY
        p_num.font.size = Pt(9)
        p_num.font.bold = True
        p_num.font.color.rgb = CYAN_LIGHT if dark else CYAN_ACCENT

    # Helper: Add Card
    def add_card(slide, left, top, width, height, bg_color=CARD_WHITE, border_color=CARD_BORDER_LIGHT):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        if border_color:
            card.line.color.rgb = border_color
            card.line.width = Pt(1)
        else:
            card.line.fill.background()
        return card

    # =========================================================================
    # SLIDE 1: Title Slide (Hero Dark Theme)
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide1, NAVY_DARK)

    # Accent decorative top bar
    bar = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.12))
    bar.fill.solid()
    bar.fill.fore_color.rgb = CYAN_ACCENT
    bar.line.fill.background()

    # Category Pill
    pill = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(1.4), Inches(4.2), Inches(0.42))
    pill.fill.solid()
    pill.fill.fore_color.rgb = SLATE_CARD
    pill.line.color.rgb = CYAN_ACCENT
    pill.line.width = Pt(1)
    tf_pill = pill.text_frame
    p_pill = tf_pill.paragraphs[0]
    p_pill.text = "ACADEMIC MAJOR PROJECT SPECIFICATION & DEFENSE"
    p_pill.font.name = FONT_HEADING
    p_pill.font.size = Pt(10)
    p_pill.font.bold = True
    p_pill.font.color.rgb = CYAN_LIGHT
    p_pill.alignment = PP_ALIGN.CENTER

    # Main Project Title
    t_box = slide1.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(11.333), Inches(1.8))
    tf = t_box.text_frame
    tf.word_wrap = True
    p1 = tf.paragraphs[0]
    p1.text = "Integrated Multi-Layer Performance Optimization Framework"
    p1.font.name = FONT_HEADING
    p1.font.size = Pt(36)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_WHITE

    p_acronym = tf.add_paragraph()
    p_acronym.text = "for Web Applications (IMPOF)"
    p_acronym.font.name = FONT_HEADING
    p_acronym.font.size = Pt(30)
    p_acronym.font.bold = True
    p_acronym.font.color.rgb = CYAN_LIGHT

    # Subtitle / Tagline
    sub_box = slide1.shapes.add_textbox(Inches(1.0), Inches(3.9), Inches(11.333), Inches(0.9))
    tf_s = sub_box.text_frame
    tf_s.word_wrap = True
    p_s = tf_s.paragraphs[0]
    p_s.text = (
        "Cross-Layer Telemetry, Machine Learning Anomaly Detection, "
        "and Controlled Empirical Performance Engineering Across 5 Architectural Tiers"
    )
    p_s.font.name = FONT_BODY
    p_s.font.size = Pt(15)
    p_s.font.color.rgb = TEXT_LIGHT

    # Highlights Row Cards (3 Highlights)
    highlights = [
        ("96.1% Latency Reduction", "Optimization Gain Index (OGI) through end-to-end multi-layer tuning", EMERALD_GREEN),
        ("23.0x Throughput Scaling", "555.6 RPS sustained under 50 concurrent virtual users", CYAN_LIGHT),
        ("ML & Explainable AI", "Isolation Forest Anomaly Detection + 0-100 Rule-based Bottleneck Scorer", PURPLE_AI)
    ]
    for i, (title_h, desc_h, color_h) in enumerate(highlights):
        c_left = Inches(1.0 + i * 3.9)
        card = add_card(slide1, c_left, Inches(4.9), Inches(3.6), Inches(1.4), SLATE_CARD, SLATE_BORDER)
        tb = slide1.shapes.add_textbox(c_left + Inches(0.2), Inches(5.0), Inches(3.2), Inches(1.2))
        tf_h = tb.text_frame
        tf_h.word_wrap = True
        tf_h.margin_left = tf_h.margin_right = tf_h.margin_top = tf_h.margin_bottom = 0
        
        ph1 = tf_h.paragraphs[0]
        ph1.text = title_h
        ph1.font.name = FONT_HEADING
        ph1.font.size = Pt(15)
        ph1.font.bold = True
        ph1.font.color.rgb = color_h
        
        ph2 = tf_h.add_paragraph()
        ph2.text = desc_h
        ph2.font.name = FONT_BODY
        ph2.font.size = Pt(11)
        ph2.font.color.rgb = TEXT_MUTED

    # Metadata Footer Bar
    m_box = slide1.shapes.add_textbox(Inches(1.0), Inches(6.6), Inches(11.333), Inches(0.4))
    tf_m = m_box.text_frame
    p_m = tf_m.paragraphs[0]
    p_m.text = "Full Stack System: React 18 • Node.js/Express • Python FastAPI • PostgreSQL 16 • Redis 7.2 • Docker & K8s"
    p_m.font.name = FONT_BODY
    p_m.font.size = Pt(11)
    p_m.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 2: Executive Summary & Context
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide2, BG_OFFWHITE)
    add_header(slide2, "1. Executive Summary", "Context, Motivation & Paradigm Shift in Web Performance")
    add_footer(slide2, 2)

    # 3 Column Cards
    col_w = Inches(3.7)
    col_gap = Inches(0.3)
    cards_data = [
        ("The 'Siloed Layer' Trap", CRIMSON_ALERT, [
            "Modern web systems are decoupled into frontend, API, database, and caching tiers.",
            "Dev teams optimize each layer in isolation without cross-layer awareness.",
            "A fast React virtual DOM cannot fix a 700ms unindexed query or connection starvation.",
            "Result: Recurring performance regressions, high tail latency, and bloated cloud spend."
        ]),
        ("The IMPOF Paradigm", CYAN_ACCENT, [
            "Holistic Cross-Layer Architecture coordinating all 5 tiers concurrently.",
            "Unified Telemetry propagation linking client Web Vitals to DB query spans.",
            "Causal correlation connecting slow queries to network payload and browser jank.",
            "Closed-loop optimization validating improvements with empirical math (OGI %)."
        ]),
        ("Core Engineering Impact", EMERALD_GREEN, [
            "Latency dropped from 181.8 ms to 7.0 ms (96.1% overall reduction).",
            "Database query execution slashed by 99.9% (31 ms down to <0.1 ms).",
            "Network payloads compressed by 97.3% (142.5 KB to 3.8 KB lean DTO).",
            "Autonomous ML Anomaly Detection pinpointing degradation before SLA breach."
        ])
    ]

    for i, (title_c, col_color, points) in enumerate(cards_data):
        c_left = Inches(0.8 + i * (3.7 + 0.3))
        add_card(slide2, c_left, Inches(1.7), col_w, Inches(4.9), CARD_WHITE, CARD_BORDER_LIGHT)

        # Header Pill in card
        pill = slide2.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left, Inches(1.7), col_w, Inches(0.55))
        pill.fill.solid()
        pill.fill.fore_color.rgb = HEADER_BG
        pill.line.fill.background()
        tf_p = pill.text_frame
        p = tf_p.paragraphs[0]
        p.text = title_c
        p.font.name = FONT_HEADING
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = col_color
        p.alignment = PP_ALIGN.CENTER

        # Points
        tb = slide2.shapes.add_textbox(c_left + Inches(0.25), Inches(2.4), col_w - Inches(0.5), Inches(4.0))
        tf = tb.text_frame
        tf.word_wrap = True
        for j, pt in enumerate(points):
            p = tf.paragraphs[0] if j == 0 else tf.add_paragraph()
            p.text = "• " + pt
            p.font.name = FONT_BODY
            p.font.size = Pt(12)
            p.font.color.rgb = NAVY_DARK
            p.space_after = Pt(10)

    # =========================================================================
    # SLIDE 3: Problem Statement & Industry Gaps
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide3, BG_OFFWHITE)
    add_header(slide3, "2. Problem Statement", "Critical Shortcomings in Existing APM and Performance Paradigms")
    add_footer(slide3, 3)

    gap_data = [
        ("GAP 1: Fragmented & Isolated Telemetry",
         "Existing APM tools monitor frontend, backend, and DB in silos. When latency spikes, engineers waste hours triaging whether it is a client render issue, network throttle, backend thread lock, or DB full scan.",
         "IMPOF links client trace IDs, span durations, and DB execution context into a unified waterfall."),
        
        ("GAP 2: Opaque Black-Box AI vs. Explainable Scoring",
         "Enterprise tools often rely on opaque anomaly thresholds without explaining the architectural root cause. DevOps teams need clear, deterministic causal rules combined with anomaly probabilities.",
         "IMPOF integrates a 0-100 transparent rule-based bottleneck classifier with Scikit-Learn Isolation Forest."),
        
        ("GAP 3: Absence of Controlled Empirical Verification",
         "Performance tuning in industry is often trial-and-error without statistically controlled Before-vs-After verification under identical simulated concurrent workloads.",
         "IMPOF provides an automated Experiment Engine with OGI % metrics and 10-200 concurrent user load tests.")
    ]

    for i, (g_title, g_problem, g_solution) in enumerate(gap_data):
        top_pos = Inches(1.7 + i * 1.65)
        add_card(slide3, Inches(0.8), top_pos, Inches(11.733), Inches(1.45), CARD_WHITE, CARD_BORDER_LIGHT)

        # Indicator tag
        tag = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), top_pos + Inches(0.2), Inches(2.8), Inches(0.35))
        tag.fill.solid()
        tag.fill.fore_color.rgb = SLATE_CARD
        tag.line.fill.background()
        p_tag = tag.text_frame.paragraphs[0]
        p_tag.text = g_title.split(":")[0].strip()
        p_tag.font.name = FONT_HEADING
        p_tag.font.size = Pt(11)
        p_tag.font.bold = True
        p_tag.font.color.rgb = CYAN_LIGHT
        p_tag.alignment = PP_ALIGN.CENTER

        # Content Box
        tb = slide3.shapes.add_textbox(Inches(4.0), top_pos + Inches(0.15), Inches(8.3), Inches(1.2))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0

        p1 = tf.paragraphs[0]
        p1.text = g_title.split(":")[1].strip()
        p1.font.name = FONT_HEADING
        p1.font.size = Pt(13)
        p1.font.bold = True
        p1.font.color.rgb = NAVY_DARK

        p2 = tf.add_paragraph()
        p2.text = "Limitation: " + g_problem
        p2.font.name = FONT_BODY
        p2.font.size = Pt(11)
        p2.font.color.rgb = TEXT_DARK
        p2.space_before = Pt(2)

        p3 = tf.add_paragraph()
        p3.text = "IMPOF Solution: " + g_solution
        p3.font.name = FONT_BODY
        p3.font.size = Pt(11)
        p3.font.bold = True
        p3.font.color.rgb = EMERALD_GREEN
        p3.space_before = Pt(2)

    # =========================================================================
    # SLIDE 4: End-to-End System Architecture
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide4, NAVY_DARK)
    add_header(slide4, "3. System Architecture", "Multi-Service Architecture & Distributed Telemetry Pipeline", dark=True)
    add_footer(slide4, 4, dark=True)

    # 4 Architecture blocks side-by-side
    arch_blocks = [
        ("1. Monitored Target Apps", [
            "Movie Recommendation APP-001",
            "Embedded Web Vitals SDK",
            "Prometheus Metric Exporter",
            "High-resolution latency probes"
        ], CYAN_ACCENT),
        
        ("2. Platform Backend (Node.js)", [
            "JWT Auth & Multi-Tenancy",
            "Metric Ingestion Pipeline (REST)",
            "Controlled Experiment Engine",
            "Virtual User Load Generator"
        ], CYAN_LIGHT),
        
        ("3. AI Analysis Engine (Python)", [
            "FastAPI Microservice (Port 8000)",
            "0-100 Bottleneck Scorer",
            "0-100 Explainable Health Scorer",
            "Scikit-Learn Isolation Forest ML"
        ], PURPLE_AI),
        
        ("4. Storage & Observability", [
            "PostgreSQL 16 Relational Store",
            "Redis 7.2 Distributed Caching",
            "Prometheus Time-Series DB",
            "React 18 DevOps Dashboard"
        ], EMERALD_GREEN)
    ]

    for i, (b_title, b_items, b_color) in enumerate(arch_blocks):
        b_left = Inches(0.8 + i * (2.8 + 0.18))
        add_card(slide4, b_left, Inches(1.8), Inches(2.8), Inches(3.6), SLATE_CARD, SLATE_BORDER)

        # Header
        h_shape = slide4.shapes.add_shape(MSO_SHAPE.RECTANGLE, b_left, Inches(1.8), Inches(2.8), Inches(0.6))
        h_shape.fill.solid()
        h_shape.fill.fore_color.rgb = SLATE_BORDER
        h_shape.line.fill.background()
        tf = h_shape.text_frame
        p = tf.paragraphs[0]
        p.text = b_title
        p.font.name = FONT_HEADING
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = b_color
        p.alignment = PP_ALIGN.CENTER

        # List
        tb = slide4.shapes.add_textbox(b_left + Inches(0.15), Inches(2.5), Inches(2.5), Inches(2.7))
        tf_l = tb.text_frame
        tf_l.word_wrap = True
        for j, item in enumerate(b_items):
            p = tf_l.paragraphs[0] if j == 0 else tf_l.add_paragraph()
            p.text = "• " + item
            p.font.name = FONT_BODY
            p.font.size = Pt(11)
            p.font.color.rgb = TEXT_LIGHT
            p.space_after = Pt(8)

    # Bottom Data Flow Banner
    flow_card = add_card(slide4, Inches(0.8), Inches(5.6), Inches(11.733), Inches(1.2), SLATE_CARD, CYAN_ACCENT)
    tb_flow = slide4.shapes.add_textbox(Inches(1.0), Inches(5.7), Inches(11.333), Inches(1.0))
    tf_f = tb_flow.text_frame
    tf_f.word_wrap = True
    p1 = tf_f.paragraphs[0]
    p1.text = "SYNCHRONOUS & ASYNCHRONOUS TELEMETRY PIPELINE"
    p1.font.name = FONT_HEADING
    p1.font.size = Pt(11)
    p1.font.bold = True
    p1.font.color.rgb = CYAN_LIGHT

    p2 = tf_f.add_paragraph()
    p2.text = (
        "Client Browser (LCP/INP) ──[HTTP/2 Trace ID]──> Express API Ingest ──[Async Worker Dispatch]──> "
        "FastAPI ML Scorer ──> Real-Time Anomaly Scoring ──> React Observability Gantt Waterfall Visualizer"
    )
    p2.font.name = FONT_BODY
    p2.font.size = Pt(12)
    p2.font.color.rgb = TEXT_WHITE
    p2.space_before = Pt(4)

    # =========================================================================
    # SLIDE 5: The 5-Layer Performance Optimization Model
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide5, BG_OFFWHITE)
    add_header(slide5, "4. Multi-Layer Engineering", "Deep Dive: The 5 Pillars of Cross-Layer Optimization")
    add_footer(slide5, 5)

    layers_info = [
        ("Layer 1: Frontend", CYAN_ACCENT, [
            "DOM Virtualization (Windowing 10,000+ items)",
            "Non-blocking async UI state transitions",
            "Core Web Vitals telemetry (LCP, INP, TTFB)"
        ]),
        ("Layer 2: Network & Transport", CYAN_LIGHT, [
            "Brotli & Gzip payload compression (-85%)",
            "HTTP/2 multiplexed streams without head-of-line blocking",
            "Edge CDN Cache-Control headers (0ms RTT)"
        ]),
        ("Layer 3: Backend & API", PURPLE_AI, [
            "Async worker thread pool dispatching",
            "L1 In-Memory LRU Cache (Caffeine-style)",
            "Lean DTO projection serialization"
        ]),
        ("Layer 4: Database Store", NAVY_DARK, [
            "PostgreSQL/MySQL B-Tree Composite Indexing",
            "HikariCP connection pool warm leases",
            "Batched JOINs eliminating N+1 query loops"
        ]),
        ("Layer 5: Cache & Infra", EMERALD_GREEN, [
            "Redis 7.2 distributed key-value store with TTL",
            "Cache stampede prevention with probabilistic locks",
            "Container CPU/RAM autoscaling & limits"
        ])
    ]

    for i, (l_name, l_color, l_points) in enumerate(layers_info):
        l_top = Inches(1.7 + i * 1.0)
        card = add_card(slide5, Inches(0.8), l_top, Inches(11.733), Inches(0.88), CARD_WHITE, CARD_BORDER_LIGHT)

        # Layer Tag Pill
        pill = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), l_top + Inches(0.18), Inches(2.6), Inches(0.52))
        pill.fill.solid()
        pill.fill.fore_color.rgb = l_color
        pill.line.fill.background()
        tf = pill.text_frame
        p = tf.paragraphs[0]
        p.text = l_name
        p.font.name = FONT_HEADING
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE
        p.alignment = PP_ALIGN.CENTER

        # Bullets inline
        tb = slide5.shapes.add_textbox(Inches(3.8), l_top + Inches(0.12), Inches(8.5), Inches(0.65))
        tf_b = tb.text_frame
        tf_b.word_wrap = True
        tf_b.margin_left = tf_b.margin_right = tf_b.margin_top = tf_b.margin_bottom = 0
        for j, pt in enumerate(l_points):
            p = tf_b.paragraphs[0] if j == 0 else tf_b.add_paragraph()
            p.text = "✓  " + pt
            p.font.name = FONT_BODY
            p.font.size = Pt(11)
            p.font.color.rgb = NAVY_DARK
            p.space_after = Pt(2)

    # =========================================================================
    # SLIDE 6: Mathematical Formulations & Latency Decomposition
    # =========================================================================
    slide6 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide6, BG_OFFWHITE)
    add_header(slide6, "5. Mathematical Formulations", "Formal Analytical Models for Latency, Gain & Health")
    add_footer(slide6, 6)

    math_cards = [
        ("1. Total Latency Decomposition", [
            "T_total = T_frontend + T_network + T_backend + T_database + T_queue",
            "• T_frontend: Client DOM parse, style recalculation, script execution.",
            "• T_network: Round-trip time (RTT), DNS resolution, TLS handshake, transfer.",
            "• T_backend: Event loop queue time, middleware, serialization.",
            "• T_database: Query parsing, lock wait time, B-tree index scan, disk I/O.",
            "• T_queue: Thread pool wait & OS context switching."
        ]),
        ("2. Optimization Gain Index (OGI %)", [
            "OGI (%) = [(T_baseline - T_optimized) / T_baseline] × 100",
            "• Quantifies the net percentage latency reduction across full stack.",
            "• Baseline: Unindexed, uncompressed, unpooled, unvirtualized.",
            "• Optimized: Indexed, cached, Brotli compressed, pooled, virtualized.",
            "• Empirical Result: 96.1% reduction achieved in controlled benchmark."
        ]),
        ("3. Explainable 0-100 Application Health Score", [
            "HealthScore = 0.30·S_latency + 0.20·S_avail + 0.20·S_db + 0.15·S_cache + 0.15·S_infra",
            "• Latency (30%): Evaluates P95 response time against 200ms/500ms SLAs.",
            "• Availability (20%): Non-200 HTTP error rates (4xx / 5xx ratios).",
            "• Database (20%): Slow query ratio (>100ms) & connection pool saturation.",
            "• Cache (15%): Redis hit ratio target (>85%) & key eviction velocity.",
            "• Infrastructure (15%): Host & container CPU/Memory thresholds (<75%)."
        ]),
        ("4. Throughput Scaling Factor", [
            "Throughput Gain = RPS_optimized / RPS_baseline",
            "• Measures concurrency handling capacity under high virtual user loads.",
            "• Eliminates thread pool starvation and DB connection exhaustion.",
            "• Empirical Result: 24.2 RPS scaled to 555.6 RPS (23.0x capacity gain)."
        ])
    ]

    for i, (m_title, m_lines) in enumerate(math_cards):
        col = i % 2
        row = i // 2
        c_left = Inches(0.8 + col * (5.7 + 0.33))
        c_top = Inches(1.7 + row * (2.4 + 0.2))

        add_card(slide6, c_left, c_top, Inches(5.7), Inches(2.4), CARD_WHITE, CARD_BORDER_LIGHT)

        # Header
        h_shape = slide6.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left, c_top, Inches(5.7), Inches(0.45))
        h_shape.fill.solid()
        h_shape.fill.fore_color.rgb = HEADER_BG
        h_shape.line.fill.background()
        tf = h_shape.text_frame
        p = tf.paragraphs[0]
        p.text = m_title
        p.font.name = FONT_HEADING
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = NAVY_DARK
        p.alignment = PP_ALIGN.LEFT

        # Text
        tb = slide6.shapes.add_textbox(c_left + Inches(0.2), c_top + Inches(0.55), Inches(5.3), Inches(1.75))
        tf_t = tb.text_frame
        tf_t.word_wrap = True
        tf_t.margin_left = tf_t.margin_right = tf_t.margin_top = tf_t.margin_bottom = 0
        for j, line in enumerate(m_lines):
            p = tf_t.paragraphs[0] if j == 0 else tf_t.add_paragraph()
            p.text = line
            p.font.name = "Consolas" if j == 0 else FONT_BODY
            p.font.size = Pt(11) if j == 0 else Pt(10)
            p.font.bold = True if j == 0 else False
            p.font.color.rgb = CYAN_ACCENT if j == 0 else NAVY_DARK
            p.space_after = Pt(2)

    # =========================================================================
    # SLIDE 7: Python FastAPI Analysis Engine & Explainable AI
    # =========================================================================
    slide7 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide7, BG_OFFWHITE)
    add_header(slide7, "6. Analysis Engine", "Python FastAPI Microservice: Transparent Scoring & Classification")
    add_footer(slide7, 7)

    col_w2 = Inches(5.7)
    # Left Card: Transparent Scoring Architecture
    add_card(slide7, Inches(0.8), Inches(1.7), col_w2, Inches(4.9), CARD_WHITE, CARD_BORDER_LIGHT)
    tb_l = slide7.shapes.add_textbox(Inches(1.1), Inches(1.9), col_w2 - Inches(0.6), Inches(4.5))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True

    p = tf_l.paragraphs[0]
    p.text = "Transparent 0-100 Bottleneck Scoring"
    p.font.name = FONT_HEADING
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = NAVY_DARK

    features_scorer = [
        ("Deterministic Heuristic Rules", "Evaluates exact telemetry values against multi-stage operational thresholds (Healthy, Warning, Critical)."),
        ("Database Bottleneck Detector", "Flags queries >100ms, missing B-tree indexes, unpooled connection stalls, and high disk read ratios."),
        ("Network & Serialization Classifier", "Identifies uncompressed JSON payloads (>50KB) and unprojected relational models causing network lag."),
        ("Frontend Render Scorer", "Analyzes Web Vitals: LCP > 2.5s (Poor), INP > 200ms (High latency), and unvirtualized DOM tables."),
        ("No Black-Box Ambiguity", "Outputs exact contribution breakdown so developers know precisely which line of code or SQL query caused the dip.")
    ]
    for title, desc in features_scorer:
        p_t = tf_l.add_paragraph()
        p_t.text = "• " + title + ":"
        p_t.font.name = FONT_HEADING
        p_t.font.size = Pt(12)
        p_t.font.bold = True
        p_t.font.color.rgb = CYAN_ACCENT
        p_t.space_before = Pt(8)

        p_d = tf_l.add_paragraph()
        p_d.text = desc
        p_d.font.name = FONT_BODY
        p_d.font.size = Pt(11)
        p_d.font.color.rgb = TEXT_DARK

    # Right Card: Automated Recommendation Engine
    add_card(slide7, Inches(6.833), Inches(1.7), col_w2, Inches(4.9), CARD_WHITE, CARD_BORDER_LIGHT)
    tb_r = slide7.shapes.add_textbox(Inches(7.133), Inches(1.9), col_w2 - Inches(0.6), Inches(4.5))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True

    p = tf_r.paragraphs[0]
    p.text = "Prescriptive Architectural Recommendations"
    p.font.name = FONT_HEADING
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = NAVY_DARK

    recs = [
        ("CRITICAL: Database Full Scan Detected", "Action: Add B-Tree composite index on (genre, release_year) and eliminate SELECT * with lean DTO projection."),
        ("HIGH: Connection Pool Saturation (>85%)", "Action: Increase HikariCP maxPoolSize to 25 and set connectionTimeout=3000ms with warm connection leasing."),
        ("MEDIUM: High Network Payload Transfer (>140 KB)", "Action: Enable Brotli / Gzip compression middleware and implement HTTP/2 streaming multiplexing."),
        ("MEDIUM: Cache Stampede Risk (<40% Hit Ratio)", "Action: Deploy Redis distributed caching with 300s TTL and probabilistic early expiration algorithm."),
        ("LOW: Client DOM Thread Jitter (>300ms Render)", "Action: Adopt react-window DOM virtualization for long lists exceeding 100 table rows.")
    ]
    for level_title, action in recs:
        p_t = tf_r.add_paragraph()
        p_t.text = level_title
        p_t.font.name = FONT_HEADING
        p_t.font.size = Pt(11)
        p_t.font.bold = True
        p_t.font.color.rgb = CRIMSON_ALERT if "CRITICAL" in level_title else (PURPLE_AI if "HIGH" in level_title else CYAN_ACCENT)
        p_t.space_before = Pt(8)

        p_d = tf_r.add_paragraph()
        p_d.text = action
        p_d.font.name = FONT_BODY
        p_d.font.size = Pt(11)
        p_d.font.color.rgb = TEXT_DARK

    # =========================================================================
    # SLIDE 8: Machine Learning Anomaly Detection (Isolation Forest)
    # =========================================================================
    slide8 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide8, NAVY_DARK)
    add_header(slide8, "7. Machine Learning", "Scikit-Learn Isolation Forest Anomaly Detection Engine", dark=True)
    add_footer(slide8, 8, dark=True)

    # 3 Section Cards
    col3_w = Inches(3.7)
    ml_sections = [
        ("Multi-Metric Feature Vector", PURPLE_AI, [
            "Input vector x incorporates cross-layer telemetry dimensions:",
            "x = [CPU%, Memory_MB, T_api_latency, T_db_query, Error_Rate, Cache_Hit_Ratio]",
            "Standardized via robust feature scaling to normalize across latency (ms) and percentages (%).",
            "Continuous 10-second sliding metric snapshot evaluation."
        ]),
        ("Mathematical Formulation", CYAN_LIGHT, [
            "Anomaly score s(x, n) is derived from isolation tree path depth:",
            "s(x, n) = 2 ^ ( - E(h(x)) / c(n) )",
            "• h(x): Path length to isolate sample x in tree.",
            "• E(h(x)): Expected path length over ensemble of 100 iTrees.",
            "• c(n) = 2 ln(n - 1) + 0.5772 - 2(n - 1)/n (average BST depth).",
            "Decision boundary: s >= 0.65 flags operational anomaly."
        ]),
        ("Why Isolation Forest for APM?", EMERALD_GREEN, [
            "Linear time complexity O(n log n) suitable for real-time edge telemetry.",
            "Unsupervised: Requires no manual incident labeling.",
            "Resistant to masking effects and swamping in high-dimensional metrics.",
            "Trained on baseline steady-state metrics; flags tail anomalies instantly."
        ])
    ]

    for i, (m_title, m_color, m_items) in enumerate(ml_sections):
        c_left = Inches(0.8 + i * (3.7 + 0.3))
        add_card(slide8, c_left, Inches(1.8), col3_w, Inches(3.6), SLATE_CARD, SLATE_BORDER)

        h_shape = slide8.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left, Inches(1.8), col3_w, Inches(0.55))
        h_shape.fill.solid()
        h_shape.fill.fore_color.rgb = SLATE_BORDER
        h_shape.line.fill.background()
        tf = h_shape.text_frame
        p = tf.paragraphs[0]
        p.text = m_title
        p.font.name = FONT_HEADING
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = m_color
        p.alignment = PP_ALIGN.CENTER

        tb = slide8.shapes.add_textbox(c_left + Inches(0.2), Inches(2.45), col3_w - Inches(0.4), Inches(2.8))
        tf_l = tb.text_frame
        tf_l.word_wrap = True
        for j, item in enumerate(m_items):
            p = tf_l.paragraphs[0] if j == 0 else tf_l.add_paragraph()
            p.text = "• " + item
            p.font.name = FONT_BODY
            p.font.size = Pt(11)
            p.font.color.rgb = TEXT_LIGHT
            p.space_after = Pt(6)

    # Anomaly Confidence Banner
    ban = add_card(slide8, Inches(0.8), Inches(5.6), Inches(11.733), Inches(1.2), SLATE_CARD, PURPLE_AI)
    tb_b = slide8.shapes.add_textbox(Inches(1.0), Inches(5.7), Inches(11.333), Inches(1.0))
    tf_b = tb_b.text_frame
    tf_b.word_wrap = True
    p1 = tf_b.paragraphs[0]
    p1.text = "INTEGRATED ANOMALY CLASSIFICATION PIPELINE"
    p1.font.name = FONT_HEADING
    p1.font.size = Pt(11)
    p1.font.bold = True
    p1.font.color.rgb = PURPLE_AI

    p2 = tf_b.add_paragraph()
    p2.text = (
        "When an anomaly score s(x) exceeds threshold, the engine attaches: "
        "(1) Anomaly Type, (2) Root Cause Severity (Critical/High/Medium), (3) Statistical Confidence Score (e.g. 94.2%), "
        "and (4) Instant Remediation Prescriptions to the live React dashboard."
    )
    p2.font.name = FONT_BODY
    p2.font.size = Pt(12)
    p2.font.color.rgb = TEXT_WHITE
    p2.space_before = Pt(4)

    # =========================================================================
    # SLIDE 9: Database & Query Layer Optimizations
    # =========================================================================
    slide9 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide9, BG_OFFWHITE)
    add_header(slide9, "8. Database Layer", "Relational Indexing, Connection Pooling & N+1 Query Elimination")
    add_footer(slide9, 9)

    db_cards = [
        ("The N+1 Query Anti-Pattern", CRIMSON_ALERT, [
            "Problem: Fetching 100 movies triggers 1 query for movies plus 100 sequential queries for reviews.",
            "Impact: 101 round-trips over TCP, high connection overhead, execution time exceeds 700ms.",
            "IMPOF Fix: Batched indexed JOINs: single multi-table query with grouped projections.",
            "Result: Latency dropped from 720ms to 0.06ms (99.9% query speedup)."
        ]),
        ("B-Tree Composite Indexing", CYAN_ACCENT, [
            "Problem: Unindexed WHERE filters force sequential full-table scans across 100,000+ rows.",
            "Complexity: O(N) full disk scan with severe buffer pool churn and lock contention.",
            "IMPOF Fix: Created composite B-Tree index on (genre, release_year, rating).",
            "Complexity: O(log N) tree traversal; reads reduce from 100,000 rows to 12 rows."
        ]),
        ("HikariCP High-Speed Pooling", EMERALD_GREEN, [
            "Problem: Opening a new TCP socket per request takes 30-50ms TLS/Auth handshake.",
            "Contention: High concurrency causes connection starvation and socket exhaustion.",
            "IMPOF Fix: Warm connection leasing via HikariCP pool (10-25 pre-warmed leases).",
            "Result: Connection acquisition latency reduced from 45ms to 0.2ms warm lease."
        ])
    ]

    for i, (title_db, col_db, pts) in enumerate(db_cards):
        c_left = Inches(0.8 + i * (3.7 + 0.3))
        add_card(slide9, c_left, Inches(1.7), Inches(3.7), Inches(4.9), CARD_WHITE, CARD_BORDER_LIGHT)

        pill = slide9.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left, Inches(1.7), Inches(3.7), Inches(0.55))
        pill.fill.solid()
        pill.fill.fore_color.rgb = HEADER_BG
        pill.line.fill.background()
        tf = pill.text_frame
        p = tf.paragraphs[0]
        p.text = title_db
        p.font.name = FONT_HEADING
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = col_db
        p.alignment = PP_ALIGN.CENTER

        tb = slide9.shapes.add_textbox(c_left + Inches(0.25), Inches(2.4), Inches(3.2), Inches(4.0))
        tf_b = tb.text_frame
        tf_b.word_wrap = True
        for j, pt in enumerate(pts):
            p = tf_b.paragraphs[0] if j == 0 else tf_b.add_paragraph()
            p.text = pt
            p.font.name = FONT_BODY
            p.font.size = Pt(11.5)
            p.font.color.rgb = NAVY_DARK
            p.space_after = Pt(10)

    # =========================================================================
    # SLIDE 10: Caching & Data Transfer Architecture
    # =========================================================================
    slide10 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide10, BG_OFFWHITE)
    add_header(slide10, "9. Caching & Network", "Dual-Tier Caching & Extreme Network Payload Compression")
    add_footer(slide10, 10)

    # Left: Dual-Tier Caching
    add_card(slide10, Inches(0.8), Inches(1.7), Inches(5.7), Inches(4.9), CARD_WHITE, CARD_BORDER_LIGHT)
    tb_c = slide10.shapes.add_textbox(Inches(1.1), Inches(1.9), Inches(5.1), Inches(4.5))
    tf_c = tb_c.text_frame
    tf_c.word_wrap = True

    p = tf_c.paragraphs[0]
    p.text = "Dual-Tier Caching Pipeline"
    p.font.name = FONT_HEADING
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = NAVY_DARK

    cache_bullets = [
        ("L1 In-Memory LRU Cache", "Caffeine-style ultra-fast in-process memory cache. Access latency <0.01ms. Avoids process context switches for hot items."),
        ("L2 Distributed Cache (Redis 7.2)", "Shared distributed key-value store across microservice replicas with configurable TTL (300s) and LRU eviction."),
        ("Cache Stampede Mitigation", "Employs probabilistic early expiration and atomic mutex locks so only one worker queries the database on miss."),
        ("Cache Invalidation Strategies", "Key tagging and event-driven invalidation on DB write/update events ensure strong read consistency.")
    ]
    for title, desc in cache_bullets:
        p_t = tf_c.add_paragraph()
        p_t.text = "• " + title
        p_t.font.name = FONT_HEADING
        p_t.font.size = Pt(12)
        p_t.font.bold = True
        p_t.font.color.rgb = CYAN_ACCENT
        p_t.space_before = Pt(8)

        p_d = tf_c.add_paragraph()
        p_d.text = desc
        p_d.font.name = FONT_BODY
        p_d.font.size = Pt(11)
        p_d.font.color.rgb = TEXT_DARK

    # Right: Payload Compression & DTO Projections
    add_card(slide10, Inches(6.833), Inches(1.7), Inches(5.7), Inches(4.9), CARD_WHITE, CARD_BORDER_LIGHT)
    tb_p = slide10.shapes.add_textbox(Inches(7.133), Inches(1.9), Inches(5.1), Inches(4.5))
    tf_p = tb_p.text_frame
    tf_p.word_wrap = True

    p = tf_p.paragraphs[0]
    p.text = "Network Payload Optimization (-97.3%)"
    p.font.name = FONT_HEADING
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = NAVY_DARK

    payload_bullets = [
        ("Raw Payload (Baseline)", "142.5 KB uncompressed JSON containing redundant columns, internal timestamps, and unprojected relational tables."),
        ("Lean DTO Projections", "Backend selects only the necessary client attributes (title, rating, poster, id), shrinking payload to 18.2 KB (87.2% reduction)."),
        ("Brotli & Gzip Compression", "Dynamic HTTP compression middleware compresses the DTO from 18.2 KB down to 3.8 KB (79.1% further reduction)."),
        ("Cumulative Gain", "Total payload slashed from 142.5 KB to 3.8 KB (97.3% smaller). Lowers mobile network transfer latency from 120ms to 4ms.")
    ]
    for title, desc in payload_bullets:
        p_t = tf_p.add_paragraph()
        p_t.text = "• " + title
        p_t.font.name = FONT_HEADING
        p_t.font.size = Pt(12)
        p_t.font.bold = True
        p_t.font.color.rgb = EMERALD_GREEN if "Gain" in title else CYAN_ACCENT
        p_t.space_before = Pt(8)

        p_d = tf_p.add_paragraph()
        p_d.text = desc
        p_d.font.name = FONT_BODY
        p_d.font.size = Pt(11)
        p_d.font.color.rgb = TEXT_DARK

    # =========================================================================
    # SLIDE 11: Controlled Experimentation & A/B Engine
    # =========================================================================
    slide11 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide11, BG_OFFWHITE)
    add_header(slide11, "10. Experimentation Engine", "Controlled Before-vs-After Optimization Verification")
    add_footer(slide11, 11)

    exp_steps = [
        ("Step 1: Baseline Freeze", CYAN_ACCENT, [
            "Captures a reproducible metric baseline snapshot before any code changes are introduced.",
            "Records p50, p95, p99 latencies, error rate, CPU load, and DB query time under fixed load."
        ]),
        ("Step 2: Configuration Injection", PURPLE_AI, [
            "Applies specific optimization configurations across target layers via feature flags:",
            "• Database B-Tree indexing",
            "• Redis L2 caching layer",
            "• Brotli compression middleware",
            "• DOM windowing virtualization"
        ]),
        ("Step 3: Workload Replay", CYAN_LIGHT, [
            "Executes synthetic traffic generator under identical concurrency (50 virtual users).",
            "Eliminates ambient external network noise and variance across test iterations."
        ]),
        ("Step 4: Delta & OGI Scoring", EMERALD_GREEN, [
            "Automatically computes Delta metrics: Latency Delta, Throughput Delta, Health Score Delta.",
            "Generates immutable Experiment Record with statistical ROI quantification."
        ])
    ]

    for i, (s_title, s_color, s_pts) in enumerate(exp_steps):
        s_left = Inches(0.8 + i * (2.8 + 0.18))
        add_card(slide11, s_left, Inches(1.7), Inches(2.8), Inches(4.9), CARD_WHITE, CARD_BORDER_LIGHT)

        h_shape = slide11.shapes.add_shape(MSO_SHAPE.RECTANGLE, s_left, Inches(1.7), Inches(2.8), Inches(0.55))
        h_shape.fill.solid()
        h_shape.fill.fore_color.rgb = s_color
        h_shape.line.fill.background()
        tf = h_shape.text_frame
        p = tf.paragraphs[0]
        p.text = s_title
        p.font.name = FONT_HEADING
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE
        p.alignment = PP_ALIGN.CENTER

        tb = slide11.shapes.add_textbox(s_left + Inches(0.15), Inches(2.35), Inches(2.5), Inches(4.0))
        tf_b = tb.text_frame
        tf_b.word_wrap = True
        for j, pt in enumerate(s_pts):
            p = tf_b.paragraphs[0] if j == 0 else tf_b.add_paragraph()
            p.text = pt
            p.font.name = FONT_BODY
            p.font.size = Pt(11)
            p.font.color.rgb = NAVY_DARK
            p.space_after = Pt(8)

    # =========================================================================
    # SLIDE 12: Virtual User Load Testing & Tail Latency Analysis
    # =========================================================================
    slide12 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide12, NAVY_DARK)
    add_header(slide12, "11. Stress Testing", "Virtual User Load Generation & Concurrency Scaling", dark=True)
    add_footer(slide12, 12, dark=True)

    # 2 Big Cards: Concurrency Scaling & Tail Latency Analysis
    add_card(slide12, Inches(0.8), Inches(1.8), Inches(5.7), Inches(4.9), SLATE_CARD, SLATE_BORDER)
    tb_l = slide12.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(5.1), Inches(4.5))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True

    p = tf_l.paragraphs[0]
    p.text = "Throughput Under High Concurrency"
    p.font.name = FONT_HEADING
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = CYAN_LIGHT

    load_bullets = [
        ("Simulated Concurrency", "Integrated load engine scales from 10 to 200 concurrent virtual users generating high-frequency request loops."),
        ("Baseline Saturation at 24.2 RPS", "Unoptimized architecture quickly experiences thread pool starvation and DB connection bottlenecks, flatlining at 24.2 RPS."),
        ("IMPOF Scaling to 555.6 RPS", "With HikariCP pooling, Redis L2 caching, and async dispatch, throughput scales linearly to 555.6 RPS (23x scaling factor)."),
        ("CPU Efficiency", "Host CPU utilization dropped from 88% down to 32%, leaving 63.6% computational headroom for burst traffic.")
    ]
    for title, desc in load_bullets:
        p_t = tf_l.add_paragraph()
        p_t.text = "• " + title
        p_t.font.name = FONT_HEADING
        p_t.font.size = Pt(12)
        p_t.font.bold = True
        p_t.font.color.rgb = CYAN_ACCENT
        p_t.space_before = Pt(8)

        p_d = tf_l.add_paragraph()
        p_d.text = desc
        p_d.font.name = FONT_BODY
        p_d.font.size = Pt(11)
        p_d.font.color.rgb = TEXT_LIGHT

    # Right Card: Percentile Latency Distribution
    add_card(slide12, Inches(6.833), Inches(1.8), Inches(5.7), Inches(4.9), SLATE_CARD, SLATE_BORDER)
    tb_r = slide12.shapes.add_textbox(Inches(7.133), Inches(2.0), Inches(5.1), Inches(4.5))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True

    p = tf_r.paragraphs[0]
    p.text = "Percentile & Tail Latency Analysis"
    p.font.name = FONT_HEADING
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = EMERALD_GREEN

    tail_bullets = [
        ("Why Tail Latency Matters", "Mean latency conceals worst-case user experiences. In distributed web systems, P95 and P99 govern user satisfaction and SLA compliance."),
        ("P50 (Median) Response Time", "Baseline: 154 ms ➔ IMPOF: 4.2 ms (97.2% reduction in typical user response time)."),
        ("P90 Percentile Latency", "Baseline: 290 ms ➔ IMPOF: 8.5 ms (Stabilized tail latency under moderate queue loads)."),
        ("P99 Worst-Case Tail Latency", "Baseline: 820 ms ➔ IMPOF: 14.8 ms (Eliminates catastrophic latency spikes and timeout drops).")
    ]
    for title, desc in tail_bullets:
        p_t = tf_r.add_paragraph()
        p_t.text = "• " + title
        p_t.font.name = FONT_HEADING
        p_t.font.size = Pt(12)
        p_t.font.bold = True
        p_t.font.color.rgb = EMERALD_GREEN if "Percentile" in title or "P99" in title else CYAN_LIGHT
        p_t.space_before = Pt(8)

        p_d = tf_r.add_paragraph()
        p_d.text = desc
        p_d.font.name = FONT_BODY
        p_d.font.size = Pt(11)
        p_d.font.color.rgb = TEXT_LIGHT

    # =========================================================================
    # SLIDE 13: Empirical Evaluation & Benchmark Results (The Matrix)
    # =========================================================================
    slide13 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide13, BG_OFFWHITE)
    add_header(slide13, "12. Empirical Benchmarks", "4-Stage Comparative Evaluation Matrix (Empirical Findings)")
    add_footer(slide13, 13)

    # Big Table
    rows = 7
    cols = 6
    t_left = Inches(0.8)
    t_top = Inches(1.7)
    t_width = Inches(11.733)
    t_height = Inches(4.8)

    table_shape = slide13.shapes.add_table(rows, cols, t_left, t_top, t_width, t_height)
    table = table_shape.table

    # Column widths
    table.columns[0].width = Inches(2.6)
    table.columns[1].width = Inches(1.8)
    table.columns[2].width = Inches(1.8)
    table.columns[3].width = Inches(1.8)
    table.columns[4].width = Inches(1.9)
    table.columns[5].width = Inches(1.833)

    table_data = [
        ["Performance Metric", "1. Baseline (Raw)", "2. DB Only", "3. Backend + DB", "4. Full IMPOF", "Net Gain vs Baseline"],
        ["Total Response Time", "181.8 ms", "158.1 ms", "170.8 ms", "7.0 ms", "+96.1% (OGI)"],
        ["Database Query Latency", "31.0 ms (Full Scan)", "0.06 ms (B-Tree)", "0.06 ms (B-Tree)", "0.00 ms (Cached)", "99.9% Faster"],
        ["Network Payload Size", "142.5 KB (Raw)", "142.5 KB (Raw)", "18.2 KB (DTO)", "3.8 KB (Compressed)", "97.3% Smaller"],
        ["Throughput (50 Users)", "24.2 RPS", "85.4 RPS", "180.0 RPS", "555.6 RPS", "23.0x Capacity"],
        ["Largest Contentful Paint", "2.8 s (Poor)", "2.4 s (Needs Imp)", "1.5 s (Good)", "0.6 s (Good)", "4.6x Faster"],
        ["App Health Score", "25 / 100 (Critical)", "48 / 100 (Fair)", "72 / 100 (Good)", "92 / 100 (Healthy)", "+67 Points"]
    ]

    for r_idx, row in enumerate(table_data):
        for c_idx, val in enumerate(row):
            cell = table.cell(r_idx, c_idx)
            cell.text = val
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            
            # Format cell text
            p = cell.text_frame.paragraphs[0]
            p.alignment = PP_ALIGN.LEFT if c_idx == 0 else PP_ALIGN.CENTER
            p.font.name = FONT_HEADING if (r_idx == 0 or c_idx == 0) else FONT_BODY
            p.font.size = Pt(11) if r_idx > 0 else Pt(11.5)
            p.font.bold = True if (r_idx == 0 or c_idx == 4 or c_idx == 5) else False

            # Shading
            if r_idx == 0:
                cell.fill.solid()
                cell.fill.fore_color.rgb = NAVY_DARK
                p.font.color.rgb = TEXT_WHITE
            elif c_idx == 4:
                cell.fill.solid()
                cell.fill.fore_color.rgb = RGBColor(236, 253, 245) # Light Mint
                p.font.color.rgb = EMERALD_GREEN
            elif c_idx == 5:
                cell.fill.solid()
                cell.fill.fore_color.rgb = RGBColor(240, 249, 255) # Light Cyan
                p.font.color.rgb = CYAN_ACCENT
            elif r_idx % 2 == 1:
                cell.fill.solid()
                cell.fill.fore_color.rgb = CARD_WHITE
                p.font.color.rgb = NAVY_DARK
            else:
                cell.fill.solid()
                cell.fill.fore_color.rgb = HEADER_BG
                p.font.color.rgb = NAVY_DARK

    # =========================================================================
    # SLIDE 14: DevOps Observability Dashboard & UX
    # =========================================================================
    slide14 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide14, BG_OFFWHITE)
    add_header(slide14, "13. Observability Dashboard", "Real-Time React 18 UI & Waterfall Span Visualization")
    add_footer(slide14, 14)

    ui_modules = [
        ("Layer Control Matrix", CYAN_ACCENT, [
            "Live interactive toggle switches for each optimization layer.",
            "Presets for instant testing: Baseline, DB Only, Backend+DB, Full IMPOF.",
            "Real-time visual feedback on active architectural configurations."
        ]),
        ("Gantt Waterfall Visualizer", PURPLE_AI, [
            "Sub-millisecond execution span visualizer across 5 tiers.",
            "Highlights exact bottlenecks: DB Query (Cyan), Backend Exec (Purple), Network (Blue), Client Render (Green).",
            "Trace ID and Span ID drilldown."
        ]),
        ("Health & Anomaly Cards", EMERALD_GREEN, [
            "Dynamic 0-100 Health Gauge with layer breakdown.",
            "Machine Learning anomaly alerts with statistical confidence %.",
            "Instant actionable remediation advice cards."
        ]),
        ("Project Report Generator", NAVY_DARK, [
            "Integrated academic report generator modal.",
            "Exports markdown dossier, tables, and system logs.",
            "One-click print/save PDF ready for project presentation."
        ])
    ]

    for i, (m_title, m_color, m_pts) in enumerate(ui_modules):
        col = i % 2
        row = i // 2
        c_left = Inches(0.8 + col * (5.7 + 0.33))
        c_top = Inches(1.7 + row * (2.4 + 0.2))

        add_card(slide14, c_left, c_top, Inches(5.7), Inches(2.4), CARD_WHITE, CARD_BORDER_LIGHT)

        # Header
        h_shape = slide14.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left, c_top, Inches(5.7), Inches(0.45))
        h_shape.fill.solid()
        h_shape.fill.fore_color.rgb = m_color
        h_shape.line.fill.background()
        tf = h_shape.text_frame
        p = tf.paragraphs[0]
        p.text = m_title
        p.font.name = FONT_HEADING
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE
        p.alignment = PP_ALIGN.CENTER

        tb = slide14.shapes.add_textbox(c_left + Inches(0.2), c_top + Inches(0.55), Inches(5.3), Inches(1.75))
        tf_t = tb.text_frame
        tf_t.word_wrap = True
        for j, pt in enumerate(m_pts):
            p = tf_t.paragraphs[0] if j == 0 else tf_t.add_paragraph()
            p.text = "• " + pt
            p.font.name = FONT_BODY
            p.font.size = Pt(11)
            p.font.color.rgb = NAVY_DARK
            p.space_after = Pt(4)

    # =========================================================================
    # SLIDE 15: Cloud Deployment & DevOps Infrastructure
    # =========================================================================
    slide15 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide15, BG_OFFWHITE)
    add_header(slide15, "14. Deployment & DevOps", "Container Orchestration, Kubernetes & Prometheus Telemetry")
    add_footer(slide15, 15)

    infra_cols = [
        ("Docker Compose (7 Services)", CYAN_ACCENT, [
            "Multi-container local orchestration:",
            "1. impof-postgres (PostgreSQL 16)",
            "2. impof-redis (Redis 7.2 Cache)",
            "3. impof-prometheus (Prometheus v2.50)",
            "4. impof-analysis-engine (Python FastAPI)",
            "5. impof-backend (Node.js/Express Core)",
            "6. impof-frontend (Vite/React Dashboard)",
            "7. impof-demo-app (Movie Target App)",
            "Isolated bridge network with persistent volumes."
        ]),
        ("Kubernetes Production Manifests", PURPLE_AI, [
            "Production-grade K8s manifests in /kubernetes:",
            "• Deployments with multi-replica scaling",
            "• ClusterIP & NodePort Services",
            "• ConfigMaps & Secret management",
            "• Liveness & Readiness Probes on /health",
            "• Horizontal Pod Autoscaling (HPA) triggers on CPU > 75% and request latency thresholds."
        ]),
        ("Prometheus Telemetry Exporter", EMERALD_GREEN, [
            "Automated metrics collection scraping:",
            "• http_requests_total (Counter by route)",
            "• http_request_duration_seconds (Histogram)",
            "• db_query_duration_seconds",
            "• redis_cache_hits / redis_cache_misses",
            "10s scrape interval feeding both Python ML engine and time-series telemetry charts."
        ])
    ]

    for i, (i_title, i_color, i_pts) in enumerate(infra_cols):
        c_left = Inches(0.8 + i * (3.7 + 0.3))
        add_card(slide15, c_left, Inches(1.7), Inches(3.7), Inches(4.9), CARD_WHITE, CARD_BORDER_LIGHT)

        pill = slide15.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left, Inches(1.7), Inches(3.7), Inches(0.55))
        pill.fill.solid()
        pill.fill.fore_color.rgb = HEADER_BG
        pill.line.fill.background()
        tf = pill.text_frame
        p = tf.paragraphs[0]
        p.text = i_title
        p.font.name = FONT_HEADING
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = i_color
        p.alignment = PP_ALIGN.CENTER

        tb = slide15.shapes.add_textbox(c_left + Inches(0.2), Inches(2.35), Inches(3.3), Inches(4.1))
        tf_b = tb.text_frame
        tf_b.word_wrap = True
        for j, pt in enumerate(i_pts):
            p = tf_b.paragraphs[0] if j == 0 else tf_b.add_paragraph()
            p.text = pt if (j == 0 or "•" in pt) else ("• " + pt)
            p.font.name = FONT_BODY
            p.font.size = Pt(11)
            p.font.color.rgb = NAVY_DARK
            p.space_after = Pt(6)

    # =========================================================================
    # SLIDE 16: Project Demonstration Case Study (Movie System)
    # =========================================================================
    slide16 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide16, NAVY_DARK)
    add_header(slide16, "15. Case Study", "Applied Validation on Movie Recommendation Platform (APP-001)", dark=True)
    add_footer(slide16, 16, dark=True)

    # Before vs After Case Study
    add_card(slide16, Inches(0.8), Inches(1.8), Inches(5.7), Inches(4.9), SLATE_CARD, SLATE_BORDER)
    tb_b4 = slide16.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(5.1), Inches(4.5))
    tf_b4 = tb_b4.text_frame
    tf_b4.word_wrap = True

    p = tf_b4.paragraphs[0]
    p.text = "Initial State: Severe Bottlenecks"
    p.font.name = FONT_HEADING
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = CRIMSON_ALERT

    b4_points = [
        ("Application Profile", "Movie Platform with 100,000 records, user ratings, and genre filters under 50 concurrent simulated users."),
        ("Database Bottleneck", "Full table scan on WHERE genre = 'Sci-Fi' took 720ms; cold connection per request added 45ms overhead."),
        ("Network Bloat", "Uncompressed raw JSON returning 142.5 KB; client download took 120ms on mobile emulation."),
        ("Client UI Freezing", "Unwindowed DOM rendering 5,000 table nodes caused 2.8s LCP and 340ms interaction lag (INP)."),
        ("Health Score", "Scored 25 / 100 (CRITICAL status) with high anomaly probability flag (0.89).")
    ]
    for title, desc in b4_points:
        p_t = tf_b4.add_paragraph()
        p_t.text = "• " + title + ":"
        p_t.font.name = FONT_HEADING
        p_t.font.size = Pt(12)
        p_t.font.bold = True
        p_t.font.color.rgb = CRIMSON_ALERT
        p_t.space_before = Pt(6)

        p_d = tf_b4.add_paragraph()
        p_d.text = desc
        p_d.font.name = FONT_BODY
        p_d.font.size = Pt(11)
        p_d.font.color.rgb = TEXT_LIGHT

    # After State Card
    add_card(slide16, Inches(6.833), Inches(1.8), Inches(5.7), Inches(4.9), SLATE_CARD, SLATE_BORDER)
    tb_af = slide16.shapes.add_textbox(Inches(7.133), Inches(2.0), Inches(5.1), Inches(4.5))
    tf_af = tb_af.text_frame
    tf_af.word_wrap = True

    p = tf_af.paragraphs[0]
    p.text = "Optimized State: Full IMPOF Deployed"
    p.font.name = FONT_HEADING
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = EMERALD_GREEN

    af_points = [
        ("B-Tree Composite Indexing", "Composite index on (genre, release_year) reduced query scan from 720ms to 0.06ms."),
        ("Redis L2 Caching + Warm Leases", "Subsequent reads hit Redis cache in 0.00ms; HikariCP connection pool eliminated socket handshakes."),
        ("Lean DTO + Brotli Compression", "Payload shrunk from 142.5 KB to 3.8 KB (97.3% reduction); transfer completed in 3.5ms."),
        ("DOM Virtualization (Windowing)", "Rendered only visible viewport rows; LCP improved to 0.6s (4.6x faster) and INP dropped to 12ms."),
        ("Health Score", "Jumped to 92 / 100 (HEALTHY status) with zero false-positive anomaly alerts.")
    ]
    for title, desc in af_points:
        p_t = tf_af.add_paragraph()
        p_t.text = "• " + title + ":"
        p_t.font.name = FONT_HEADING
        p_t.font.size = Pt(12)
        p_t.font.bold = True
        p_t.font.color.rgb = EMERALD_GREEN
        p_t.space_before = Pt(6)

        p_d = tf_af.add_paragraph()
        p_d.text = desc
        p_d.font.name = FONT_BODY
        p_d.font.size = Pt(11)
        p_d.font.color.rgb = TEXT_WHITE

    # =========================================================================
    # SLIDE 17: Conclusion, Key Innovations & Future Scope
    # =========================================================================
    slide17 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide17, BG_OFFWHITE)
    add_header(slide17, "16. Conclusions & Future Work", "Summary of Academic Contributions, Key Innovations & Next Steps")
    add_footer(slide17, 17)

    # 3 Summary Cards
    col3_w = Inches(3.7)
    concl_data = [
        ("Major Contributions", CYAN_ACCENT, [
            "Unified 5-tier performance engineering framework bridging frontend, network, backend, DB, and cache.",
            "Cross-layer telemetry propagation correlating client Web Vitals directly with database query spans.",
            "Mathematical formulation of the Optimization Gain Index (OGI %) for reproducible performance auditing.",
            "All 41 major project requirements implemented and empirically proven."
        ]),
        ("Key Architectural Innovations", PURPLE_AI, [
            "Hybrid AI Model: Combines transparent 0-100 rule-based scoring with Scikit-Learn Isolation Forest ML.",
            "Controlled Experiment Engine: Automated Before-vs-After verification with baseline freeze and delta tracking.",
            "Dynamic Waterfall Visualizer: Real-time Gantt representation of multi-layer latency spans.",
            "Production-ready Docker & Kubernetes deployment manifests."
        ]),
        ("Future Scope & Extensions", EMERALD_GREEN, [
            "Autonomous Auto-Tuning: Closed-loop agent dynamically injecting DB indexes and adjusting pool sizes.",
            "Kernel-Level Profiling: Integrating Linux eBPF probes for zero-overhead OS context switch analysis.",
            "OpenTelemetry (OTel) Standard: Adopting standardized W3C trace context across distributed microservices.",
            "Multi-Cloud Distributed Mesh: Cross-region latency optimization using service meshes like Istio."
        ])
    ]

    for i, (c_title, c_color, c_items) in enumerate(concl_data):
        c_left = Inches(0.8 + i * (3.7 + 0.3))
        add_card(slide17, c_left, Inches(1.7), col3_w, Inches(4.9), CARD_WHITE, CARD_BORDER_LIGHT)

        pill = slide17.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left, Inches(1.7), col3_w, Inches(0.55))
        pill.fill.solid()
        pill.fill.fore_color.rgb = HEADER_BG
        pill.line.fill.background()
        tf = pill.text_frame
        p = tf.paragraphs[0]
        p.text = c_title
        p.font.name = FONT_HEADING
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = c_color
        p.alignment = PP_ALIGN.CENTER

        tb = slide17.shapes.add_textbox(c_left + Inches(0.2), Inches(2.35), col3_w - Inches(0.4), Inches(4.1))
        tf_b = tb.text_frame
        tf_b.word_wrap = True
        for j, pt in enumerate(c_items):
            p = tf_b.paragraphs[0] if j == 0 else tf_b.add_paragraph()
            p.text = "• " + pt
            p.font.name = FONT_BODY
            p.font.size = Pt(11)
            p.font.color.rgb = NAVY_DARK
            p.space_after = Pt(8)

    # =========================================================================
    # SLIDE 18: Thank You & Q&A (Closing Slide)
    # =========================================================================
    slide18 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide18, NAVY_DARK)

    # Top accent bar
    bar18 = slide18.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.12))
    bar18.fill.solid()
    bar18.fill.fore_color.rgb = CYAN_ACCENT
    bar18.line.fill.background()

    # Center Box
    c_box = slide18.shapes.add_textbox(Inches(1.5), Inches(1.8), Inches(10.333), Inches(3.0))
    tf_c = c_box.text_frame
    tf_c.word_wrap = True

    p_pill = tf_c.paragraphs[0]
    p_pill.text = "PROJECT DEFENSE & EVALUATION"
    p_pill.font.name = FONT_HEADING
    p_pill.font.size = Pt(12)
    p_pill.font.bold = True
    p_pill.font.color.rgb = CYAN_LIGHT
    p_pill.alignment = PP_ALIGN.CENTER

    p_t = tf_c.add_paragraph()
    p_t.text = "Thank You!"
    p_t.font.name = FONT_HEADING
    p_t.font.size = Pt(44)
    p_t.font.bold = True
    p_t.font.color.rgb = TEXT_WHITE
    p_t.alignment = PP_ALIGN.CENTER
    p_t.space_before = Pt(10)

    p_sub = tf_c.add_paragraph()
    p_sub.text = "Questions, Feedback & Live Demonstration"
    p_sub.font.name = FONT_BODY
    p_sub.font.size = Pt(18)
    p_sub.font.color.rgb = CYAN_LIGHT
    p_sub.alignment = PP_ALIGN.CENTER
    p_sub.space_before = Pt(8)

    # Info Card in Center
    card_info = add_card(slide18, Inches(2.5), Inches(4.6), Inches(8.333), Inches(1.8), SLATE_CARD, SLATE_BORDER)
    tb_inf = slide18.shapes.add_textbox(Inches(2.7), Inches(4.75), Inches(7.933), Inches(1.5))
    tf_inf = tb_inf.text_frame
    tf_inf.word_wrap = True

    info_lines = [
        ("Framework:", "Integrated Multi-Layer Performance Optimization Framework (IMPOF)"),
        ("Architecture:", "Frontend (React) • Core Backend (Node/Express) • AI Engine (Python FastAPI) • PostgreSQL • Redis"),
        ("Key Result:", "+96.1% Optimization Gain Index (OGI) • 23.0x Throughput Scaling • 97.3% Payload Compression"),
        ("Live Demo URL:", "http://localhost:5173 (React UI) | http://localhost:5000 (API) | http://localhost:8000/docs (FastAPI)")
    ]
    for j, (label, val) in enumerate(info_lines):
        p = tf_inf.paragraphs[0] if j == 0 else tf_inf.add_paragraph()
        p.text = f"{label} {val}"
        p.font.name = FONT_BODY
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_LIGHT
        p.space_after = Pt(3)

    # Save presentation
    output_path = "IMPOF_Project_Presentation.pptx"
    prs.save(output_path)
    print(f"Presentation saved successfully to {os.path.abspath(output_path)}")
    return output_path

if __name__ == "__main__":
    create_presentation()
