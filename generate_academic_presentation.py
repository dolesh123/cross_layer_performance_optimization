"""
generate_academic_presentation.py
Generates an academic, comprehensive, 16-slide widescreen (16:9) PowerPoint presentation
for the Integrated Multi-Layer Performance Optimization Framework (IMPOF).
Specifically covers:
  1. Project Title & Overview
  2. Problem Statement & Industry Gaps
  3. Project Objectives & Research Scope
  4. Literature Survey & Related Work
  5. Literature Survey - Comparative Analysis Matrix
  6. Proposed Methodology - End-to-End System Architecture
  7. Proposed Methodology - The 5-Layer Performance Optimization Model
  8. Proposed Methodology - Mathematical Formulations & Latency Decomposition
  9. Proposed Methodology - Machine Learning Anomaly Detection & Explainable AI
  10. Work Completed So Far - Core Platform Microservices & Pipeline
  11. Work Completed So Far - Target Benchmark Application (Movie System)
  12. Work Completed So Far - Empirical Evaluation & Results Matrix
  13. Work Completed So Far - Concurrent Load Testing & Tail Latency Analysis
  14. Future Work Plan & Phased Milestones Roadmap
  15. Academic Conclusion & Key Research Contributions
  16. Project Demonstration, Q&A & Acknowledgments
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor

# -----------------------------------------------------------------------------
# Color Palette Constants (Professional Executive / Academic Deep Tech)
# -----------------------------------------------------------------------------
NAVY_DARK = RGBColor(15, 23, 42)          # #0F172A - Hero Dark Background / Slide Header
SLATE_CARD = RGBColor(30, 41, 59)         # #1E293B - Card Dark
SLATE_BORDER = RGBColor(51, 65, 85)       # #334155 - Card Border Dark
CYAN_ACCENT = RGBColor(14, 165, 233)      # #0EA5E9 - Primary Accent
CYAN_LIGHT = RGBColor(56, 189, 248)       # #38BDF8 - Bright Accent
EMERALD_GREEN = RGBColor(16, 185, 129)    # #10B981 - Gain / Success / Complete
CRIMSON_ALERT = RGBColor(239, 68, 68)     # #EF4444 - Bottleneck / Alert
PURPLE_AI = RGBColor(139, 92, 246)        # #8B5CF6 - Machine Learning / AI
AMBER_WARN = RGBColor(245, 158, 11)       # #F59E0B - Warning / Future Phase

TEXT_WHITE = RGBColor(255, 255, 255)      # White text
TEXT_LIGHT = RGBColor(226, 232, 240)      # Slate 200
TEXT_MUTED = RGBColor(148, 163, 184)      # Slate 400
TEXT_DARK = RGBColor(15, 23, 42)          # Dark text
BG_OFFWHITE = RGBColor(248, 250, 252)     # Slate 50
CARD_WHITE = RGBColor(255, 255, 255)      # Pure White Card
CARD_BORDER_LIGHT = RGBColor(226, 232, 240) # Slate 200
HEADER_BG = RGBColor(241, 245, 249)      # Slate 100

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
        bg_shape.line.fill.background()
        return bg_shape

    # Helper: Add Standard Slide Header
    def add_header(slide, category, title, dark=False):
        # Category Badge
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.32))
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
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.72), Inches(11.7), Inches(0.65))
        tf_t = title_box.text_frame
        tf_t.word_wrap = True
        tf_t.margin_left = tf_t.margin_right = tf_t.margin_top = tf_t.margin_bottom = 0
        p_t = tf_t.paragraphs[0]
        p_t.text = title
        p_t.font.name = FONT_HEADING
        p_t.font.size = Pt(21)
        p_t.font.bold = True
        p_t.font.color.rgb = TEXT_WHITE if dark else NAVY_DARK

        # Subtle divider line
        divider = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.42), Inches(11.733), Inches(0.02)
        )
        divider.fill.solid()
        divider.fill.fore_color.rgb = SLATE_BORDER if dark else CARD_BORDER_LIGHT
        divider.line.fill.background()

    # Helper: Add Footer
    def add_footer(slide, slide_num, total=16, dark=False):
        footer_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.05), Inches(11.733), Inches(0.3))
        tf_f = footer_box.text_frame
        tf_f.word_wrap = True
        tf_f.margin_left = tf_f.margin_right = tf_f.margin_top = tf_f.margin_bottom = 0
        
        p = tf_f.paragraphs[0]
        p.text = "IMPOF  -  Integrated Multi-Layer Performance Optimization Framework | Major Project Defense"
        p.font.name = FONT_BODY
        p.font.size = Pt(9)
        p.font.color.rgb = TEXT_MUTED
        
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
    pill = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(1.15), Inches(4.5), Inches(0.40))
    pill.fill.solid()
    pill.fill.fore_color.rgb = SLATE_CARD
    pill.line.color.rgb = CYAN_ACCENT
    pill.line.width = Pt(1)
    tf_pill = pill.text_frame
    p_pill = tf_pill.paragraphs[0]
    p_pill.text = "ACADEMIC MAJOR PROJECT PRESENTATION & DEFENSE"
    p_pill.font.name = FONT_HEADING
    p_pill.font.size = Pt(10)
    p_pill.font.bold = True
    p_pill.font.color.rgb = CYAN_LIGHT
    p_pill.alignment = PP_ALIGN.CENTER

    # Main Project Title
    t_box = slide1.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(11.333), Inches(1.7))
    tf = t_box.text_frame
    tf.word_wrap = True
    p1 = tf.paragraphs[0]
    p1.text = "Integrated Multi-Layer Performance Optimization Framework"
    p1.font.name = FONT_HEADING
    p1.font.size = Pt(32)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_WHITE

    p_acronym = tf.add_paragraph()
    p_acronym.text = "for Web Applications (IMPOF)"
    p_acronym.font.name = FONT_HEADING
    p_acronym.font.size = Pt(28)
    p_acronym.font.bold = True
    p_acronym.font.color.rgb = CYAN_LIGHT

    # Subtitle / Domain
    sub_box = slide1.shapes.add_textbox(Inches(1.0), Inches(3.45), Inches(11.333), Inches(0.7))
    tf_s = sub_box.text_frame
    tf_s.word_wrap = True
    p_s = tf_s.paragraphs[0]
    p_s.text = (
        "Cross-Layer Distributed Telemetry, Explainable AI Bottleneck Scoring, Machine Learning Anomaly Detection, "
        "and Controlled Empirical Performance Engineering Across 5 Architectural Tiers"
    )
    p_s.font.name = FONT_BODY
    p_s.font.size = Pt(13)
    p_s.font.color.rgb = TEXT_LIGHT

    # Metadata Card (Student / Guide / Department Details)
    meta_card = add_card(slide1, Inches(1.0), Inches(4.35), Inches(11.333), Inches(1.15), SLATE_CARD, SLATE_BORDER)
    meta_box = slide1.shapes.add_textbox(Inches(1.2), Inches(4.45), Inches(10.9), Inches(0.95))
    tf_m = meta_box.text_frame
    tf_m.word_wrap = True
    p_m1 = tf_m.paragraphs[0]
    p_m1.text = "Project Domain: Distributed Systems • Application Performance Monitoring (APM) • Cloud & Web Systems"
    p_m1.font.name = FONT_HEADING
    p_m1.font.size = Pt(11)
    p_m1.font.bold = True
    p_m1.font.color.rgb = CYAN_LIGHT

    p_m2 = tf_m.add_paragraph()
    p_m2.text = "Core Tech Stack: React 18 • Node.js / Express • Python FastAPI • PostgreSQL 16 • Redis 7.2 • Scikit-Learn • Docker"
    p_m2.font.name = FONT_BODY
    p_m2.font.size = Pt(11)
    p_m2.font.color.rgb = TEXT_LIGHT
    p_m2.space_before = Pt(3)

    # Highlights Row Cards (3 Highlights)
    highlights = [
        ("96.1% Latency Reduction", "Optimization Gain Index (OGI) through end-to-end multi-layer tuning", EMERALD_GREEN),
        ("23.0x Throughput Scaling", "555.6 RPS sustained under 50 concurrent virtual users", CYAN_LIGHT),
        ("ML & Explainable AI", "Isolation Forest Anomaly Detection + 0-100 Rule-based Bottleneck Scorer", PURPLE_AI)
    ]
    for i, (title_h, desc_h, color_h) in enumerate(highlights):
        c_left = Inches(1.0 + i * 3.9)
        card = add_card(slide1, c_left, Inches(5.65), Inches(3.6), Inches(1.3), SLATE_CARD, SLATE_BORDER)
        tb = slide1.shapes.add_textbox(c_left + Inches(0.2), Inches(5.75), Inches(3.2), Inches(1.1))
        tf_h = tb.text_frame
        tf_h.word_wrap = True
        tf_h.margin_left = tf_h.margin_right = tf_h.margin_top = tf_h.margin_bottom = 0
        
        ph1 = tf_h.paragraphs[0]
        ph1.text = title_h
        ph1.font.name = FONT_HEADING
        ph1.font.size = Pt(14)
        ph1.font.bold = True
        ph1.font.color.rgb = color_h
        
        ph2 = tf_h.add_paragraph()
        ph2.text = desc_h
        ph2.font.name = FONT_BODY
        ph2.font.size = Pt(10)
        ph2.font.color.rgb = TEXT_LIGHT
        ph2.space_before = Pt(2)

    add_footer(slide1, 1, dark=True)

    # =========================================================================
    # SLIDE 2: Problem Statement & Industry Gaps (Light Theme)
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide2, BG_OFFWHITE)
    add_header(slide2, "1. Problem Statement", "The 'Siloed Optimization Trap' and Critical Shortcomings in Existing APMs")
    add_footer(slide2, 2)

    # Problem Statement Executive Summary Banner
    prob_banner = add_card(slide2, Inches(0.8), Inches(1.6), Inches(11.733), Inches(0.85), CARD_WHITE, CARD_BORDER_LIGHT)
    tb_pb = slide2.shapes.add_textbox(Inches(1.0), Inches(1.68), Inches(11.333), Inches(0.7))
    tf_pb = tb_pb.text_frame
    tf_pb.word_wrap = True
    p_pb = tf_pb.paragraphs[0]
    p_pb.text = "CORE PROBLEM: Performance optimization in modern web architectures remains fundamentally siloed. An optimized React frontend cannot fix a 700ms unindexed SQL query, nor can an indexed database fix uncompressed network payloads or backend event-loop thread starvation. Existing APM tools fail to provide automated cross-layer causal correlation."
    p_pb.font.name = FONT_BODY
    p_pb.font.size = Pt(11)
    p_pb.font.bold = True
    p_pb.font.color.rgb = CRIMSON_ALERT

    gap_data = [
        ("GAP 1: Fragmented & Isolated Telemetry Silos",
         "Commercial APMs (Datadog, Dynatrace) collect metrics separately per layer. When a latency spike occurs, engineers waste hours triaging whether it is client render jank, network throttles, Node.js event-loop blocking, or DB lock contention.",
         "IMPOF Innovation: Propagates distributed Trace IDs and Span IDs connecting frontend Web Vitals (LCP, INP) directly to backend async threads and SQL query execution plans in a unified waterfall."),
        
        ("GAP 2: Opaque Black-Box AI vs. Explainable Root Cause",
         "Enterprise tools rely on opaque AI anomaly alerts without explaining the architectural root cause. DevOps teams cannot trust alerts that do not state why an anomaly triggered or what code/config to modify.",
         "IMPOF Innovation: Transparent dual-engine intelligence: deterministic 0-100 rule-based bottleneck classifier with actionable advice + Scikit-Learn Isolation Forest on multi-dimensional telemetry vectors."),
        
        ("GAP 3: Absence of Controlled Empirical Verification",
         "Performance tuning in enterprise software is largely trial-and-error without statistically controlled Before-vs-After verification under identical simulated concurrent virtual workloads.",
         "IMPOF Innovation: Controlled Experiment Engine computing mathematical Optimization Gain Index (OGI %) and P50-P99 tail latencies under 10-200 concurrent user load tests.")
    ]

    for i, (g_title, g_problem, g_solution) in enumerate(gap_data):
        top_pos = Inches(2.65 + i * 1.4)
        add_card(slide2, Inches(0.8), top_pos, Inches(11.733), Inches(1.28), CARD_WHITE, CARD_BORDER_LIGHT)

        # Indicator tag
        tag = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), top_pos + Inches(0.18), Inches(2.8), Inches(0.32))
        tag.fill.solid()
        tag.fill.fore_color.rgb = SLATE_CARD
        tag.line.fill.background()
        p_tag = tag.text_frame.paragraphs[0]
        p_tag.text = g_title.split(":")[0].strip()
        p_tag.font.name = FONT_HEADING
        p_tag.font.size = Pt(10)
        p_tag.font.bold = True
        p_tag.font.color.rgb = CYAN_LIGHT
        p_tag.alignment = PP_ALIGN.CENTER

        # Content Box
        tb = slide2.shapes.add_textbox(Inches(4.0), top_pos + Inches(0.12), Inches(8.3), Inches(1.05))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0

        p1 = tf.paragraphs[0]
        p1.text = g_title.split(":")[1].strip()
        p1.font.name = FONT_HEADING
        p1.font.size = Pt(12)
        p1.font.bold = True
        p1.font.color.rgb = NAVY_DARK

        p2 = tf.add_paragraph()
        p2.text = "Industry Limitation: " + g_problem
        p2.font.name = FONT_BODY
        p2.font.size = Pt(10)
        p2.font.color.rgb = TEXT_DARK
        p2.space_before = Pt(2)

        p3 = tf.add_paragraph()
        p3.text = g_solution
        p3.font.name = FONT_BODY
        p3.font.size = Pt(10)
        p3.font.bold = True
        p3.font.color.rgb = EMERALD_GREEN
        p3.space_before = Pt(2)

    # =========================================================================
    # SLIDE 3: Project Objectives & Research Scope (Light Theme)
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide3, BG_OFFWHITE)
    add_header(slide3, "2. Project Objectives", "Primary Research Aims & Quantitative Engineering Goals")
    add_footer(slide3, 3)

    # Primary Objective Card (Top Hero)
    prim_card = add_card(slide3, Inches(0.8), Inches(1.6), Inches(11.733), Inches(1.1), CARD_WHITE, CYAN_ACCENT)
    tb_po = slide3.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(11.333), Inches(0.9))
    tf_po = tb_po.text_frame
    tf_po.word_wrap = True
    p_pot = tf_po.paragraphs[0]
    p_pot.text = "PRIMARY OBJECTIVE"
    p_pot.font.name = FONT_HEADING
    p_pot.font.size = Pt(11)
    p_pot.font.bold = True
    p_pot.font.color.rgb = CYAN_ACCENT

    p_pod = tf_po.add_paragraph()
    p_pod.text = "To design, implement, and validate an Integrated Multi-Layer Performance Optimization Framework (IMPOF) that bridges frontend rendering, network transport, backend application runtimes, relational database query plans, and distributed caches into a single explainable, ML-powered, and empirically verifiable platform."
    p_pod.font.name = FONT_BODY
    p_pod.font.size = Pt(11.5)
    p_pod.font.bold = True
    p_pod.font.color.rgb = NAVY_DARK
    p_pod.space_before = Pt(2)

    # 4 Specific Research Objectives Cards
    obj_data = [
        ("Obj 1: Cross-Layer Telemetry", CYAN_ACCENT, [
            "Non-invasive instrumentation across 5 architectural tiers.",
            "Propagation of W3C Trace Context and Span IDs.",
            "Real-time capture of Core Web Vitals (LCP, INP, TTFB), Node.js thread timers, and SQL query latencies.",
            "Unified waterfall timeline correlating frontend jank to database full table scans."
        ]),
        ("Obj 2: Explainable Scoring", PURPLE_AI, [
            "0-100 Weighted Application Health Index combining latency, availability, DB, cache, and host CPU/RAM.",
            "Deterministic 0-100 Bottleneck Classifier eliminating black-box uncertainty.",
            "Immediate heuristic identification of N+1 queries, unindexed filters, connection drops, and payload bloat.",
            "Actionable architectural remediation recommendations."
        ]),
        ("Obj 3: ML Anomaly Detection", CYAN_LIGHT, [
            "Multi-dimensional anomaly detection using Scikit-Learn Isolation Forest.",
            "Feature vector ingestion: [CPU, RAM, API Latency, DB Latency, Error Rate, Cache Hit Ratio].",
            "Continuous anomaly probability score (0.0 to 1.0) and anomaly flagging.",
            "Proactive bottleneck warning before SLA violation."
        ]),
        ("Obj 4: Empirical A/B Engine", EMERALD_GREEN, [
            "Controlled Experiment Engine with side-by-side Before-vs-After benchmark runs.",
            "Formal calculation of Optimization Gain Index (OGI %) and throughput scaling factors.",
            "Synthetic load generator supporting 10 to 200 concurrent virtual users.",
            "Tail latency profiling (P50, P90, P95, P99) under sustained stress."
        ])
    ]

    col4_w = Inches(2.78)
    col4_gap = Inches(0.2)
    for i, (o_title, o_color, o_points) in enumerate(obj_data):
        c_left = Inches(0.8 + i * (2.78 + 0.2))
        add_card(slide3, c_left, Inches(2.9), col4_w, Inches(3.95), CARD_WHITE, CARD_BORDER_LIGHT)

        # Header Pill
        pill = slide3.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left, Inches(2.9), col4_w, Inches(0.48))
        pill.fill.solid()
        pill.fill.fore_color.rgb = HEADER_BG
        pill.line.fill.background()
        tf_p = pill.text_frame
        p = tf_p.paragraphs[0]
        p.text = o_title
        p.font.name = FONT_HEADING
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = o_color
        p.alignment = PP_ALIGN.CENTER

        tb = slide3.shapes.add_textbox(c_left + Inches(0.15), Inches(3.5), col4_w - Inches(0.3), Inches(3.2))
        tf = tb.text_frame
        tf.word_wrap = True
        for j, pt in enumerate(o_points):
            p = tf.paragraphs[0] if j == 0 else tf.add_paragraph()
            p.text = "• " + pt
            p.font.name = FONT_BODY
            p.font.size = Pt(10)
            p.font.color.rgb = NAVY_DARK
            p.space_after = Pt(6)

    # =========================================================================
    # SLIDE 4: Literature Survey & Related Work (Light Theme)
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide4, BG_OFFWHITE)
    add_header(slide4, "3. Literature Survey", "Critical Review of Existing Paradigms & Academic Foundations")
    add_footer(slide4, 4)

    lit_cards = [
        ("1. Commercial APM & Enterprise Observability",
         "Dynatrace, New Relic, Datadog (2018-2023)",
         "Industrial standard for distributed system monitoring. Employs proprietary byte-code injection agents across web tiers.",
         "Limitations: Closed-source, high CPU/RAM agent overhead (3-7%), tier-siloed metrics, and lack of controlled A/B empirical experiment validation with automated optimization gain indices.",
         CRIMSON_ALERT),

        ("2. Distributed Tracing & W3C Trace Context",
         "Google Dapper (Sigcomm), OpenTelemetry / Jaeger (CNCF)",
         "Standardized RPC and HTTP request lifecycle tracing using Trace IDs and Span IDs across microservice boundaries.",
         "Limitations: Focuses exclusively on trace collection and visualization; does not provide automated bottleneck root-cause classification, health scoring, or multi-layer optimization synthesis.",
         CYAN_ACCENT),

        ("3. Database Query & Connection Pool Optimization",
         "Stonebraker et al., PostgreSQL/MySQL Query Optimization Literature",
         "Pioneered B-Tree composite indexing, query execution plan cost estimation, and connection pooling (HikariCP / pgBouncer).",
         "Limitations: Evaluates database performance in complete isolation from client-side network latency, frontend rendering DOM overhead, and backend DTO serialization bloat.",
         PURPLE_AI),

        ("4. Machine Learning & AIOps for Performance",
         "Liu et al. (Isolation Forest), Candido et al. (AIOps Anomalies)",
         "Applied tree-based isolation and unsupervised autoencoders to detect system metrics anomalies and degradation.",
         "Limitations: Most AIOps systems act as opaque black-boxes; they flag anomalies on CPU/RAM but fail to explain application-level root causes (e.g., missing index vs uncompressed payload).",
         EMERALD_GREEN)
    ]

    col2_w = Inches(5.7)
    row2_h = Inches(2.45)
    for i, (l_title, l_ref, l_desc, l_lim, l_color) in enumerate(lit_cards):
        r = i // 2
        c = i % 2
        c_left = Inches(0.8 + c * (5.7 + 0.333))
        c_top = Inches(1.65 + r * (2.45 + 0.2))

        add_card(slide4, c_left, c_top, col2_w, row2_h, CARD_WHITE, CARD_BORDER_LIGHT)

        # Header Pill
        pill = slide4.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left, c_top, col2_w, Inches(0.42))
        pill.fill.solid()
        pill.fill.fore_color.rgb = HEADER_BG
        pill.line.fill.background()
        tf_p = pill.text_frame
        p = tf_p.paragraphs[0]
        p.text = l_title
        p.font.name = FONT_HEADING
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = l_color

        tb = slide4.shapes.add_textbox(c_left + Inches(0.2), c_top + Inches(0.48), col2_w - Inches(0.4), row2_h - Inches(0.55))
        tf = tb.text_frame
        tf.word_wrap = True

        p_ref = tf.paragraphs[0]
        p_ref.text = f"Key Works: {l_ref}"
        p_ref.font.name = FONT_BODY
        p_ref.font.size = Pt(9.5)
        p_ref.font.bold = True
        p_ref.font.color.rgb = TEXT_MUTED

        p_desc = tf.add_paragraph()
        p_desc.text = "Contribution: " + l_desc
        p_desc.font.name = FONT_BODY
        p_desc.font.size = Pt(10)
        p_desc.font.color.rgb = NAVY_DARK
        p_desc.space_before = Pt(3)

        p_lim = tf.add_paragraph()
        p_lim.text = l_lim
        p_lim.font.name = FONT_BODY
        p_lim.font.size = Pt(10)
        p_lim.font.bold = True
        p_lim.font.color.rgb = CRIMSON_ALERT if "Limitations" in l_lim else NAVY_DARK
        p_lim.space_before = Pt(3)

    # =========================================================================
    # SLIDE 5: Literature Survey - Comparative Analysis Matrix (Light Theme)
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide5, BG_OFFWHITE)
    add_header(slide5, "3. Literature Survey", "Feature & Capability Comparison Matrix: Existing Solutions vs. Proposed IMPOF")
    add_footer(slide5, 5)

    # Big Comparative Table
    rows = 7
    cols = 6
    t_left = Inches(0.8)
    t_top = Inches(1.65)
    t_width = Inches(11.733)
    t_height = Inches(5.1)

    table_shape = slide5.shapes.add_table(rows, cols, t_left, t_top, t_width, t_height)
    table = table_shape.table

    table.columns[0].width = Inches(2.733)
    table.columns[1].width = Inches(1.8)
    table.columns[2].width = Inches(1.8)
    table.columns[3].width = Inches(1.8)
    table.columns[4].width = Inches(1.8)
    table.columns[5].width = Inches(1.8)

    comp_table_data = [
        ["Key Architectural Feature", "Commercial APM (Datadog/Dynatrace)", "Distributed Tracing (Jaeger/OTel)", "Prometheus + Grafana", "Database Profilers (pg_stat)", "Proposed IMPOF Framework"],
        ["Cross-Layer Causal Correlation", "Partial (Tier Silos)", "Manual Traces", "No (Metrics Only)", "No (DB Only)", "Yes (5-Layer Unified)"],
        ["Explainable 0-100 Scoring", "No (Opaque Heuristics)", "No", "No", "No", "Yes (Rule-based & Open)"],
        ["Multi-Dim ML Anomaly Detection", "Black-Box ML (Paid)", "No", "No (Threshold Alerts)", "No", "Yes (Isolation Forest)"],
        ["Controlled A/B Experimentation", "No", "No", "No", "No", "Yes (Pre/Post OGI %)"],
        ["Virtual User Load Simulation", "Separate Add-on", "No", "No", "No", "Yes (10-200 Concurrent)"],
        ["Tail Latency (P99) Decomposition", "High Overhead", "Trace Level Only", "Aggregated Histogram", "Query Latency Only", "Full End-to-End Breakdown"]
    ]

    for r_idx, row in enumerate(comp_table_data):
        for c_idx, val in enumerate(row):
            cell = table.cell(r_idx, c_idx)
            cell.text = val
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            p = cell.text_frame.paragraphs[0]
            p.alignment = PP_ALIGN.LEFT if c_idx == 0 else PP_ALIGN.CENTER
            p.font.name = FONT_HEADING if (r_idx == 0 or c_idx == 0) else FONT_BODY
            p.font.size = Pt(10) if r_idx > 0 else Pt(11)
            p.font.bold = True if (r_idx == 0 or c_idx == 5) else False

            # Shading
            if r_idx == 0:
                cell.fill.solid()
                cell.fill.fore_color.rgb = NAVY_DARK
                p.font.color.rgb = TEXT_WHITE
            elif c_idx == 5: # IMPOF Column
                cell.fill.solid()
                cell.fill.fore_color.rgb = RGBColor(236, 253, 245) # Mint
                p.font.color.rgb = EMERALD_GREEN
            elif r_idx % 2 == 1:
                cell.fill.solid()
                cell.fill.fore_color.rgb = CARD_WHITE
                p.font.color.rgb = NAVY_DARK
            else:
                cell.fill.solid()
                cell.fill.fore_color.rgb = HEADER_BG
                p.font.color.rgb = NAVY_DARK

    # =========================================================================
    # SLIDE 6: Proposed Methodology - End-to-End Architecture (Dark Theme)
    # =========================================================================
    slide6 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide6, NAVY_DARK)
    add_header(slide6, "4. Proposed Methodology", "End-to-End Multi-Service System Architecture & Pipeline", dark=True)
    add_footer(slide6, 6, dark=True)

    arch_blocks = [
        ("1. Monitored Target Apps", [
            "Movie Recommendation APP-001",
            "E-Commerce Catalog APP-002",
            "Embedded Web Vitals SDK",
            "Prometheus Metric Exporter",
            "High-resolution latency probes"
        ], CYAN_ACCENT),
        
        ("2. Platform Backend (Node.js)", [
            "JWT Auth & Multi-Tenancy",
            "Metric Ingestion Pipeline (REST)",
            "Controlled Experiment Engine",
            "Virtual User Load Generator",
            "PostgreSQL & Redis DB adapters"
        ], CYAN_LIGHT),
        
        ("3. AI Analysis Engine (Python)", [
            "FastAPI Microservice (Port 8000)",
            "0-100 Bottleneck Classifier",
            "0-100 Health Scorer",
            "Scikit-Learn Isolation Forest ML",
            "Confidence & Anomaly Scoring"
        ], PURPLE_AI),
        
        ("4. DevOps Observability UI", [
            "React 18 + Vite SPA (Port 5173)",
            "Live Health Score Gauges",
            "Interactive Waterfall Gantt Chart",
            "ML Anomaly Diagnostic Cards",
            "Side-by-Side A/B Delta Viewer"
        ], EMERALD_GREEN)
    ]

    col4_w = Inches(2.78)
    col4_gap = Inches(0.2)
    for i, (b_title, b_items, b_color) in enumerate(arch_blocks):
        c_left = Inches(0.8 + i * (2.78 + 0.2))
        add_card(slide6, c_left, Inches(1.65), col4_w, Inches(4.2), SLATE_CARD, SLATE_BORDER)

        pill = slide6.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left, Inches(1.65), col4_w, Inches(0.52))
        pill.fill.solid()
        pill.fill.fore_color.rgb = SLATE_BORDER
        pill.line.fill.background()
        tf_p = pill.text_frame
        p = tf_p.paragraphs[0]
        p.text = b_title
        p.font.name = FONT_HEADING
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = b_color
        p.alignment = PP_ALIGN.CENTER

        tb = slide6.shapes.add_textbox(c_left + Inches(0.15), Inches(2.3), col4_w - Inches(0.3), Inches(3.3))
        tf = tb.text_frame
        tf.word_wrap = True
        for j, itm in enumerate(b_items):
            p = tf.paragraphs[0] if j == 0 else tf.add_paragraph()
            p.text = "• " + itm
            p.font.name = FONT_BODY
            p.font.size = Pt(10)
            p.font.color.rgb = TEXT_LIGHT
            p.space_after = Pt(7)

    # Bottom Architecture Flow Banner
    bot_card = add_card(slide6, Inches(0.8), Inches(6.0), Inches(11.733), Inches(0.85), SLATE_CARD, SLATE_BORDER)
    tb_bot = slide6.shapes.add_textbox(Inches(1.0), Inches(6.05), Inches(11.333), Inches(0.75))
    tf_bot = tb_bot.text_frame
    tf_bot.word_wrap = True
    p_b1 = tf_bot.paragraphs[0]
    p_b1.text = "DISTRIBUTED TELEMETRY FLOW:"
    p_b1.font.name = FONT_HEADING
    p_b1.font.size = Pt(10)
    p_b1.font.bold = True
    p_b1.font.color.rgb = CYAN_LIGHT

    p_b2 = tf_bot.add_paragraph()
    p_b2.text = "Client Web Vitals & HTTP Middleware -> REST Metric Ingestion (Node.js) -> Asynchronous Feature Extraction -> Python FastAPI Isolation Forest -> PostgreSQL Snapshot Storage -> Real-Time WebSocket / REST Polling by React Dashboard."
    p_b2.font.name = FONT_BODY
    p_b2.font.size = Pt(10)
    p_b2.font.color.rgb = TEXT_WHITE
    p_b2.space_before = Pt(2)

    # =========================================================================
    # SLIDE 7: Proposed Methodology - 5-Layer Performance Model (Light Theme)
    # =========================================================================
    slide7 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide7, BG_OFFWHITE)
    add_header(slide7, "4. Proposed Methodology", "The 5-Layer Performance Optimization Model & Inter-Tier Coupling")
    add_footer(slide7, 7)

    layers_data = [
        ("Layer 1: Frontend Layer", "DOM Virtualization & Core Web Vitals", [
            "Virtual windowing rendering only visible DOM nodes (react-window).",
            "Eliminates layout thrashing and client main-thread jank.",
            "Web Vitals tracking: Largest Contentful Paint (LCP < 2.5s), Interaction to Next Paint (INP < 200ms), TTFB."
        ], CYAN_ACCENT),

        ("Layer 2: Network Layer", "Transport Multiplexing & Payload Compression", [
            "Brotli / Gzip stream compression slashing JSON payload sizes by >85%.",
            "HTTP/2 multiplexed streams eliminating head-of-line TCP blocking.",
            "Edge caching headers (Cache-Control: public, max-age=3600, stale-while-revalidate)."
        ], CYAN_LIGHT),

        ("Layer 3: Backend Layer", "Asynchronous Runtimes & Lean DTO Projections", [
            "Non-blocking asynchronous worker thread pools for CPU-intensive operations.",
            "Lean DTO projection stripping unneeded entity relations before serialization.",
            "Dual-tier caching architecture: L1 In-Memory LRU + L2 Distributed Redis."
        ], PURPLE_AI),

        ("Layer 4: Database Layer", "B-Tree Composite Indexing & Connection Pooling", [
            "Composite B-Tree indexing reducing query complexity from O(N) to O(log N).",
            "HikariCP / pg connection pooling eliminating 40ms TCP handshakes per query.",
            "Batched indexed joins eliminating the notorious N+1 ORM query anti-pattern."
        ], CRIMSON_ALERT),

        ("Layer 5: Infrastructure", "Container Health & Resource Allocation", [
            "Container CPU throttling and memory ceiling monitoring (cgroups v2).",
            "Kubernetes Horizontal Pod Autoscaling (HPA) based on request rate and latency.",
            "Host network socket buffer tuning and zero-downtime rolling deployments."
        ], EMERALD_GREEN)
    ]

    card_h = Inches(1.0)
    for i, (l_name, l_sub, l_bullets, l_color) in enumerate(layers_data):
        c_top = Inches(1.6 + i * 1.05)
        add_card(slide7, Inches(0.8), c_top, Inches(11.733), card_h, CARD_WHITE, CARD_BORDER_LIGHT)

        # Left Accent Bar
        l_bar = slide7.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), c_top, Inches(0.12), card_h)
        l_bar.fill.solid()
        l_bar.fill.fore_color.rgb = l_color
        l_bar.line.fill.background()

        # Title & Subtitle Box
        tb_t = slide7.shapes.add_textbox(Inches(1.1), c_top + Inches(0.1), Inches(3.2), Inches(0.8))
        tf_t = tb_t.text_frame
        tf_t.word_wrap = True
        p1 = tf_t.paragraphs[0]
        p1.text = l_name
        p1.font.name = FONT_HEADING
        p1.font.size = Pt(12)
        p1.font.bold = True
        p1.font.color.rgb = l_color

        p2 = tf_t.add_paragraph()
        p2.text = l_sub
        p2.font.name = FONT_BODY
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = TEXT_MUTED

        # Details Box
        tb_d = slide7.shapes.add_textbox(Inches(4.4), c_top + Inches(0.08), Inches(7.9), Inches(0.85))
        tf_d = tb_d.text_frame
        tf_d.word_wrap = True
        for j, b in enumerate(l_bullets):
            p = tf_d.paragraphs[0] if j == 0 else tf_d.add_paragraph()
            p.text = "• " + b
            p.font.name = FONT_BODY
            p.font.size = Pt(9.5)
            p.font.color.rgb = NAVY_DARK
            p.space_after = Pt(1)

    # =========================================================================
    # SLIDE 8: Proposed Methodology - Mathematical Formulations (Light Theme)
    # =========================================================================
    slide8 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide8, BG_OFFWHITE)
    add_header(slide8, "4. Proposed Methodology", "Mathematical Formulations & Quantitative Engineering Formulations")
    add_footer(slide8, 8)

    math_data = [
        ("1. Total Latency Decomposition",
         "T_total = T_client_render + T_network_rtt + T_backend_exec + T_db_query + T_queue_wait",
         "Deconstructs wall-clock latency into distinct additive spans. Cross-layer distributed tracing binds each segment to a specific architectural tier, allowing exact percentage latency attribution.",
         CYAN_ACCENT),

        ("2. Explainable 0-100 Application Health Score",
         "HealthScore = 0.30*S_latency + 0.20*S_avail + 0.20*S_db + 0.15*S_cache + 0.15*S_infra",
         "A normalized composite score (0-100) where each tier sub-score is bounded in [0, 100]. Prevents single-layer false negatives and gives engineering teams an instant operational gauge.",
         PURPLE_AI),

        ("3. Optimization Gain Index (OGI %)",
         "OGI (%) = [ ( T_baseline - T_optimized ) / T_baseline ] × 100",
         "Quantifies the net percentage efficiency gain achieved by an applied optimization experiment under identical synthetic concurrency and payload conditions.",
         EMERALD_GREEN),

        ("4. Isolation Forest Anomaly Scoring Algorithm",
         "s(x, n) = 2^( - E(h(x)) / c(n) )    where c(n) = 2*ln(n - 1) + 0.5772156649 - 2(n - 1)/n",
         "Calculates anomalousness based on tree isolation path depth E(h(x)). Scores close to 1 indicate definitive anomalies; scores < 0.5 represent normal operating conditions.",
         CRIMSON_ALERT)
    ]

    for i, (m_title, m_formula, m_desc, m_color) in enumerate(math_data):
        top_pos = Inches(1.65 + i * 1.3)
        add_card(slide8, Inches(0.8), top_pos, Inches(11.733), Inches(1.18), CARD_WHITE, CARD_BORDER_LIGHT)

        # Left tag
        tag = slide8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), top_pos + Inches(0.15), Inches(3.2), Inches(0.32))
        tag.fill.solid()
        tag.fill.fore_color.rgb = SLATE_CARD
        tag.line.fill.background()
        p_tag = tag.text_frame.paragraphs[0]
        p_tag.text = m_title
        p_tag.font.name = FONT_HEADING
        p_tag.font.size = Pt(10)
        p_tag.font.bold = True
        p_tag.font.color.rgb = CYAN_LIGHT
        p_tag.alignment = PP_ALIGN.CENTER

        # Formula Card (Inner)
        f_card = add_card(slide8, Inches(1.0), top_pos + Inches(0.55), Inches(4.5), Inches(0.48), HEADER_BG, None)
        tb_f = slide8.shapes.add_textbox(Inches(1.1), top_pos + Inches(0.57), Inches(4.3), Inches(0.44))
        tf_f = tb_f.text_frame
        tf_f.word_wrap = True
        p_f = tf_f.paragraphs[0]
        p_f.text = m_formula
        p_f.font.name = "Consolas"
        p_f.font.size = Pt(9.5)
        p_f.font.bold = True
        p_f.font.color.rgb = m_color

        # Description text
        tb_d = slide8.shapes.add_textbox(Inches(5.7), top_pos + Inches(0.15), Inches(6.6), Inches(0.95))
        tf_d = tb_d.text_frame
        tf_d.word_wrap = True
        p_d = tf_d.paragraphs[0]
        p_d.text = m_desc
        p_d.font.name = FONT_BODY
        p_d.font.size = Pt(10)
        p_d.font.color.rgb = NAVY_DARK

    # =========================================================================
    # SLIDE 9: Proposed Methodology - ML & Explainable AI (Light Theme)
    # =========================================================================
    slide9 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide9, BG_OFFWHITE)
    add_header(slide9, "4. Proposed Methodology", "Dual-Engine Intelligence: Explainable Heuristics + Scikit-Learn Isolation Forest")
    add_footer(slide9, 9)

    col2_w = Inches(5.7)
    # Left Card: Explainable 0-100 Bottleneck Classifier
    add_card(slide9, Inches(0.8), Inches(1.65), col2_w, Inches(5.1), CARD_WHITE, CARD_BORDER_LIGHT)
    tb_left = slide9.shapes.add_textbox(Inches(1.0), Inches(1.75), col2_w - Inches(0.4), Inches(4.9))
    tf_l = tb_left.text_frame
    tf_l.word_wrap = True

    p = tf_l.paragraphs[0]
    p.text = "Deterministic Rule-Based Bottleneck Classifier"
    p.font.name = FONT_HEADING
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT

    heuristics = [
        ("Database Full Table Scan", "Query duration > 100ms or Rows Scanned / Rows Returned > 10x -> Generates alert with missing composite B-Tree index recommendation."),
        ("Backend Thread Starvation", "API latency >> DB latency with Host CPU > 80% -> Flags synchronous blocking operations and suggests async worker threads."),
        ("Uncompressed Payload Bloat", "HTTP response payload > 50 KB without 'Content-Encoding: br/gzip' -> Flags missing transport compression."),
        ("Connection Pool Starvation", "Queue wait time > 20ms with active pool connections at max capacity -> Suggests connection pool expansion or connection lease tuning."),
        ("Cache Miss Inefficiency", "Cache Hit Ratio < 50% under repetitive GET endpoints -> Recommends dual-tier Redis caching and TTL warming.")
    ]
    for h_name, h_desc in heuristics:
        p = tf_l.add_paragraph()
        p.text = f"• {h_name}: {h_desc}"
        p.font.name = FONT_BODY
        p.font.size = Pt(9.5)
        p.font.color.rgb = NAVY_DARK
        p.space_before = Pt(6)

    # Right Card: Scikit-Learn Isolation Forest Anomaly Detection
    add_card(slide9, Inches(6.833), Inches(1.65), col2_w, Inches(5.1), CARD_WHITE, CARD_BORDER_LIGHT)
    tb_right = slide9.shapes.add_textbox(Inches(7.033), Inches(1.75), col2_w - Inches(0.4), Inches(4.9))
    tf_r = tb_right.text_frame
    tf_r.word_wrap = True

    p = tf_r.paragraphs[0]
    p.text = "Scikit-Learn Isolation Forest ML Engine"
    p.font.name = FONT_HEADING
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = PURPLE_AI

    ml_points = [
        ("Multi-Dimensional Feature Vector", "Ingests 6 continuous telemetry metrics: x = [CPU %, Memory MB, API Latency, DB Latency, Error Rate, Cache Hit Ratio]."),
        ("Unsupervised Tree Partitioning", "Builds an ensemble of 100 isolation trees (iTrees). Anomalies require fewer random splits to isolate, yielding significantly shorter tree paths."),
        ("Contamination Factor & Tuning", "Configured with contamination=0.08, detecting subtle compound degradations that escape conventional static threshold rules."),
        ("Explainable Confidence Output", "Outputs binary status (Normal vs Anomaly), continuous anomaly score [0.0, 1.0], and feature importance attribution."),
        ("Microservice Architecture", "Exposed as high-performance async REST endpoints via Python FastAPI (sub-5ms inference latency).")
    ]
    for m_name, m_desc in ml_points:
        p = tf_r.add_paragraph()
        p.text = f"• {m_name}: {m_desc}"
        p.font.name = FONT_BODY
        p.font.size = Pt(9.5)
        p.font.color.rgb = NAVY_DARK
        p.space_before = Pt(6)

    # =========================================================================
    # SLIDE 10: Work Completed So Far - Core Platform Microservices (Dark Theme)
    # =========================================================================
    slide10 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide10, NAVY_DARK)
    add_header(slide10, "5. Work Completed So Far", "Core Engineering Implementation: Microservices & Observability Modules", dark=True)
    add_footer(slide10, 10, dark=True)

    completed_modules = [
        ("Module 1: Platform Backend (Node.js/Express)", [
            "Complete REST API with JWT authentication and role-based access control.",
            "Multi-tenant application registry (Register, update, activate target apps).",
            "High-throughput metric ingestion pipeline recording snapshots with timestamps.",
            "Controlled experiment engine managing A/B optimization runs.",
            "Synthetic load generator simulating 10 to 200 concurrent virtual users."
        ], CYAN_ACCENT),

        ("Module 2: AI Analysis Engine (Python FastAPI)", [
            "Async REST microservice running Scikit-Learn Isolation Forest.",
            "0-100 Application Health Score calculator combining 5 weighted tier metrics.",
            "0-100 Bottleneck classifier generating heuristic root-cause explanations.",
            "Live snapshot anomaly evaluation returning scores and remediation tips.",
            "Swagger / OpenAPI documentation ready on port 8000."
        ], PURPLE_AI),

        ("Module 3: DevOps Observability Dashboard (React)", [
            "React 18 + Vite frontend with modern dark-mode responsive design.",
            "Real-time interactive Gantt waterfall decomposing total request spans.",
            "Live Health Score radar/progress gauges with breakdown per layer.",
            "ML Anomaly Diagnostic cards displaying anomaly probability and severity.",
            "Built-in Academic Major Project Report generator (Markdown & PDF ready)."
        ], EMERALD_GREEN),

        ("Module 4: Persistence & Infrastructure Tier", [
            "PostgreSQL 16 relational database with fully normalized tables & schema.",
            "Redis 7.2 distributed caching layer with TTL eviction policies.",
            "Docker Compose orchestration uniting frontend, backend, AI engine, and DBs.",
            "Kubernetes YAML deployment & service manifests with health probes.",
            "High-resolution Prometheus metrics exporter (`process.hrtime.bigint`)."
        ], CYAN_LIGHT)
    ]

    col2_w = Inches(5.7)
    row2_h = Inches(2.45)
    for i, (m_title, m_items, m_color) in enumerate(completed_modules):
        r = i // 2
        c = i % 2
        c_left = Inches(0.8 + c * (5.7 + 0.333))
        c_top = Inches(1.65 + r * (2.45 + 0.2))

        add_card(slide10, c_left, c_top, col2_w, row2_h, SLATE_CARD, SLATE_BORDER)

        pill = slide10.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left, c_top, col2_w, Inches(0.42))
        pill.fill.solid()
        pill.fill.fore_color.rgb = SLATE_BORDER
        pill.line.fill.background()
        tf_p = pill.text_frame
        p = tf_p.paragraphs[0]
        p.text = m_title
        p.font.name = FONT_HEADING
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = m_color

        tb = slide10.shapes.add_textbox(c_left + Inches(0.2), c_top + Inches(0.48), col2_w - Inches(0.4), row2_h - Inches(0.55))
        tf = tb.text_frame
        tf.word_wrap = True
        for j, itm in enumerate(m_items):
            p = tf.paragraphs[0] if j == 0 else tf.add_paragraph()
            p.text = "+ " + itm
            p.font.name = FONT_BODY
            p.font.size = Pt(9.5)
            p.font.color.rgb = TEXT_LIGHT
            p.space_after = Pt(2)

    # =========================================================================
    # SLIDE 11: Work Completed So Far - Benchmark Testbed App (Light Theme)
    # =========================================================================
    slide11 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide11, BG_OFFWHITE)
    add_header(slide11, "5. Work Completed So Far", "Realistic Testbed Application: Movie Recommendation System (APP-001)")
    add_footer(slide11, 11)

    # Top Overview
    top_c = add_card(slide11, Inches(0.8), Inches(1.65), Inches(11.733), Inches(1.15), CARD_WHITE, CARD_BORDER_LIGHT)
    tb_tc = slide11.shapes.add_textbox(Inches(1.0), Inches(1.72), Inches(11.333), Inches(1.0))
    tf_tc = tb_tc.text_frame
    tf_tc.word_wrap = True
    p = tf_tc.paragraphs[0]
    p.text = "REALISTIC EXPERIMENTAL TESTBED: The Movie Recommendation & Catalog System (APP-001)"
    p.font.name = FONT_HEADING
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT

    p2 = tf_tc.add_paragraph()
    p2.text = "To rigorously test IMPOF under authentic production conditions, a full-stack target application was developed containing 100,000+ relational movie, rating, and user records. It includes an Interactive Optimization Lab with 4 toggleable optimization switches, enabling live Before/After benchmark experiments across 16 different optimization permutations."
    p2.font.name = FONT_BODY
    p2.font.size = Pt(10.5)
    p2.font.color.rgb = NAVY_DARK
    p2.space_before = Pt(3)

    # 4 Optimization Switches Cards
    switches = [
        ("Switch 1: Database B-Tree Indexing", CRIMSON_ALERT, [
            "Baseline: Full sequential table scan across 100,000 records (~31 ms per query).",
            "Optimized: Composite B-Tree index on (genre, release_year, rating) reducing query time to 0.06 ms (99.9% faster).",
            "Eliminates disk I/O bottlenecks and connection starvation."
        ]),
        ("Switch 2: Caching & Connection Pool", CYAN_ACCENT, [
            "Baseline: Cold unpooled TCP connections + zero caching (142 ms total latency).",
            "Optimized: HikariCP pre-warmed connection pool + L1/L2 Redis caching with 30s TTL.",
            "Subsequent queries served in 0.00 ms directly from in-memory cache."
        ]),
        ("Switch 3: Lean DTO & Brotli Compression", PURPLE_AI, [
            "Baseline: Raw JSON payload with deep nested entities (142.5 KB raw transfer size).",
            "Optimized: Lean DTO projection + Brotli stream compression reducing payload to 3.8 KB (97.3% smaller).",
            "Slashes network RTT and browser JSON parse duration."
        ]),
        ("Switch 4: Frontend DOM Virtualization", EMERALD_GREEN, [
            "Baseline: Rendering 500+ heavy movie DOM nodes simultaneously causing UI freeze (LCP: 2.8s).",
            "Optimized: Virtual windowing rendering only currently visible elements (LCP: 0.6s).",
            "Guarantees 60 FPS smooth scrolling and zero client main-thread jank."
        ])
    ]

    col4_w = Inches(2.78)
    col4_gap = Inches(0.2)
    for i, (s_title, s_color, s_points) in enumerate(switches):
        c_left = Inches(0.8 + i * (2.78 + 0.2))
        add_card(slide11, c_left, Inches(2.95), col4_w, Inches(3.9), CARD_WHITE, CARD_BORDER_LIGHT)

        pill = slide11.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left, Inches(2.95), col4_w, Inches(0.55))
        pill.fill.solid()
        pill.fill.fore_color.rgb = HEADER_BG
        pill.line.fill.background()
        tf_p = pill.text_frame
        p = tf_p.paragraphs[0]
        p.text = s_title
        p.font.name = FONT_HEADING
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = s_color
        p.alignment = PP_ALIGN.CENTER

        tb = slide11.shapes.add_textbox(c_left + Inches(0.15), Inches(3.6), col4_w - Inches(0.3), Inches(3.1))
        tf = tb.text_frame
        tf.word_wrap = True
        for j, pt in enumerate(s_points):
            p = tf.paragraphs[0] if j == 0 else tf.add_paragraph()
            p.text = "• " + pt
            p.font.name = FONT_BODY
            p.font.size = Pt(9.5)
            p.font.color.rgb = NAVY_DARK
            p.space_after = Pt(6)

    # =========================================================================
    # SLIDE 12: Work Completed So Far - Empirical Evaluation Matrix (Light Theme)
    # =========================================================================
    slide12 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide12, BG_OFFWHITE)
    add_header(slide12, "5. Work Completed So Far", "Empirical Evaluation Results: 4-Stage Comparative Benchmark Matrix")
    add_footer(slide12, 12)

    # Big Empirical Table
    rows = 7
    cols = 6
    t_left = Inches(0.8)
    t_top = Inches(1.65)
    t_width = Inches(11.733)
    t_height = Inches(4.9)

    table_shape = slide12.shapes.add_table(rows, cols, t_left, t_top, t_width, t_height)
    table = table_shape.table

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
            
            p = cell.text_frame.paragraphs[0]
            p.alignment = PP_ALIGN.LEFT if c_idx == 0 else PP_ALIGN.CENTER
            p.font.name = FONT_HEADING if (r_idx == 0 or c_idx == 0) else FONT_BODY
            p.font.size = Pt(11) if r_idx > 0 else Pt(11.5)
            p.font.bold = True if (r_idx == 0 or c_idx == 4 or c_idx == 5) else False

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

    # Bottom Callout
    bot_c = add_card(slide12, Inches(0.8), Inches(6.65), Inches(11.733), Inches(0.35), HEADER_BG, None)
    tb_b = slide12.shapes.add_textbox(Inches(1.0), Inches(6.66), Inches(11.333), Inches(0.32))
    p = tb_b.text_frame.paragraphs[0]
    p.text = "EMPIRICAL PROOF: Applying optimizations to only one tier (DB only) yielded minimal total gain (+13%). Only holistic cross-layer tuning (Full IMPOF) unlocked 96.1% latency reduction and 23.0x throughput scaling."
    p.font.name = FONT_BODY
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = EMERALD_GREEN

    # =========================================================================
    # SLIDE 13: Work Completed So Far - Concurrency & Tail Latencies (Light Theme)
    # =========================================================================
    slide13 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide13, BG_OFFWHITE)
    add_header(slide13, "5. Work Completed So Far", "Virtual User Load Testing & Tail Latency (P50-P99) Stress Analysis")
    add_footer(slide13, 13)

    # 3 Summary Cards Across
    c3_w = Inches(3.7)
    c3_gap = Inches(0.3)
    c3_data = [
        ("P50 / P90 Tail Latency", CYAN_ACCENT, [
            "Baseline @ 50 Users: P50 = 175 ms, P90 = 340 ms.",
            "IMPOF @ 50 Users: P50 = 5.2 ms, P90 = 9.8 ms.",
            "97.1% reduction in standard request latency distribution.",
            "Eliminates thread queue buildup in the Node.js event loop."
        ]),
        ("P95 / P99 Extreme Outliers", PURPLE_AI, [
            "Baseline @ 50 Users: P95 = 580 ms, P99 = 2,240 ms.",
            "IMPOF @ 50 Users: P95 = 14.1 ms, P99 = 24.6 ms.",
            "Unoptimized systems experience severe tail latency collapse under concurrent loads due to connection pool starvation.",
            "IMPOF holds P99 well below the 50ms strict SLA threshold."
        ]),
        ("Throughput Saturation Curve", EMERALD_GREEN, [
            "Baseline hits saturation cliff at only 25 concurrent users (24.2 RPS max).",
            "Connection timeouts and 504 Gateway errors occur beyond 50 users in unoptimized state.",
            "IMPOF scales linearly up to 200 concurrent users (>550 RPS sustained).",
            "Zero HTTP 5xx errors recorded during stress runs."
        ])
    ]

    for i, (title_c, col_color, points) in enumerate(c3_data):
        c_left = Inches(0.8 + i * (3.7 + 0.3))
        add_card(slide13, c_left, Inches(1.65), c3_w, Inches(2.7), CARD_WHITE, CARD_BORDER_LIGHT)

        pill = slide13.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left, Inches(1.65), c3_w, Inches(0.48))
        pill.fill.solid()
        pill.fill.fore_color.rgb = HEADER_BG
        pill.line.fill.background()
        tf_p = pill.text_frame
        p = tf_p.paragraphs[0]
        p.text = title_c
        p.font.name = FONT_HEADING
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = col_color
        p.alignment = PP_ALIGN.CENTER

        tb = slide13.shapes.add_textbox(c_left + Inches(0.2), Inches(2.2), c3_w - Inches(0.4), Inches(2.1))
        tf = tb.text_frame
        tf.word_wrap = True
        for j, pt in enumerate(points):
            p = tf.paragraphs[0] if j == 0 else tf.add_paragraph()
            p.text = "• " + pt
            p.font.name = FONT_BODY
            p.font.size = Pt(9.5)
            p.font.color.rgb = NAVY_DARK
            p.space_after = Pt(4)

    # Concurrency Load Stress Table at Bottom
    rows_c = 5
    cols_c = 6
    t_left_c = Inches(0.8)
    t_top_c = Inches(4.55)
    t_width_c = Inches(11.733)
    t_height_c = Inches(2.3)

    t_shape_c = slide13.shapes.add_table(rows_c, cols_c, t_left_c, t_top_c, t_width_c, t_height_c)
    table_c = t_shape_c.table

    table_c.columns[0].width = Inches(2.2)
    table_c.columns[1].width = Inches(1.9)
    table_c.columns[2].width = Inches(1.9)
    table_c.columns[3].width = Inches(1.9)
    table_c.columns[4].width = Inches(1.9)
    table_c.columns[5].width = Inches(1.933)

    stress_data = [
        ["Concurrent Users", "Baseline Latency (Mean)", "Baseline P99 Tail", "IMPOF Latency (Mean)", "IMPOF P99 Tail", "Throughput Gain"],
        ["10 Virtual Users", "84.2 ms", "190.5 ms", "4.8 ms", "12.1 ms", "12.4x (210 RPS)"],
        ["25 Virtual Users", "142.0 ms", "480.2 ms", "5.9 ms", "18.4 ms", "18.2x (395 RPS)"],
        ["50 Virtual Users", "181.8 ms", "2,240.0 ms", "7.0 ms", "24.6 ms", "23.0x (555.6 RPS)"],
        ["100 Virtual Users", "Timeout / 504 Error", "> 5,000.0 ms", "11.2 ms", "42.0 ms", "Linear Scaling"]
    ]

    for r_idx, row in enumerate(stress_data):
        for c_idx, val in enumerate(row):
            cell = table_c.cell(r_idx, c_idx)
            cell.text = val
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            p = cell.text_frame.paragraphs[0]
            p.alignment = PP_ALIGN.LEFT if c_idx == 0 else PP_ALIGN.CENTER
            p.font.name = FONT_HEADING if (r_idx == 0 or c_idx == 0) else FONT_BODY
            p.font.size = Pt(9.5) if r_idx > 0 else Pt(10)
            p.font.bold = True if (r_idx == 0 or c_idx >= 3) else False

            if r_idx == 0:
                cell.fill.solid()
                cell.fill.fore_color.rgb = NAVY_DARK
                p.font.color.rgb = TEXT_WHITE
            elif c_idx >= 3:
                cell.fill.solid()
                cell.fill.fore_color.rgb = RGBColor(236, 253, 245)
                p.font.color.rgb = EMERALD_GREEN
            elif r_idx % 2 == 1:
                cell.fill.solid()
                cell.fill.fore_color.rgb = CARD_WHITE
                p.font.color.rgb = NAVY_DARK
            else:
                cell.fill.solid()
                cell.fill.fore_color.rgb = HEADER_BG
                p.font.color.rgb = NAVY_DARK

    # =========================================================================
    # SLIDE 14: Future Work Plan & Technical Roadmap (Light Theme)
    # =========================================================================
    slide14 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide14, BG_OFFWHITE)
    add_header(slide14, "6. Future Work Plan", "Project Milestones, Phased Technical Roadmap & Future Scope")
    add_footer(slide14, 14)

    phases_data = [
        ("Phase 1: Core Framework (COMPLETED)", EMERALD_GREEN, "Weeks 1-12 (Achieved)", [
            "Architected and deployed 5-tier telemetry collection pipeline.",
            "Implemented Python FastAPI AI Engine with Isolation Forest and 0-100 Bottleneck Classifier.",
            "Built React DevOps Observability Dashboard with real-time Gantt waterfall.",
            "Conducted 4-stage empirical benchmark matrix demonstrating 96.1% latency reduction and 23.0x scaling."
        ]),

        ("Phase 2: Autonomous Auto-Remediation", CYAN_ACCENT, "Weeks 13-18 (Next Phase)", [
            "Implement automated closed-loop remediation actions triggered by high-confidence ML alerts.",
            "Dynamic B-Tree composite index provisioning in PostgreSQL without manual DBA intervention.",
            "Automated runtime adjustment of database connection pool leases and worker thread counts.",
            "Self-healing cache warming triggers for frequently queried endpoints."
        ]),

        ("Phase 3: Deep Reinforcement Learning (DRL)", PURPLE_AI, "Weeks 19-24 (Advanced Research)", [
            "Deploy a DRL agent (Deep Q-Network / PPO) to learn optimal cache eviction TTLs.",
            "Context-aware prefetching of relational data based on historical user navigation patterns.",
            "Intelligent query plan rewriting substituting costly nested subqueries with indexed CTEs.",
            "Predictive horizontal pod scaling in Kubernetes anticipating flash crowd traffic."
        ]),

        ("Phase 4: Kernel eBPF & OTel Collector", AMBER_WARN, "Weeks 25-28 (Enterprise Packaging)", [
            "Integrate eBPF (Extended Berkeley Packet Filter) probes for zero-overhead kernel-level socket tracing.",
            "Full compatibility with OpenTelemetry (OTel) Collector and W3C standard trace exporters.",
            "Multi-cluster Kubernetes Operator with Helm chart packaging for production enterprise deployment.",
            "Publication of research findings in IEEE / ACM cloud computing and software engineering conferences."
        ])
    ]

    for i, (p_title, p_color, p_time, p_items) in enumerate(phases_data):
        top_pos = Inches(1.65 + i * 1.3)
        add_card(slide14, Inches(0.8), top_pos, Inches(11.733), Inches(1.18), CARD_WHITE, CARD_BORDER_LIGHT)

        # Left Pill
        pill = slide14.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), top_pos + Inches(0.15), Inches(3.4), Inches(0.35))
        pill.fill.solid()
        pill.fill.fore_color.rgb = SLATE_CARD
        pill.line.fill.background()
        p_pill = pill.text_frame.paragraphs[0]
        p_pill.text = p_title.split(":")[0].strip() + ": " + p_title.split(":")[1].split("(")[0].strip()
        p_pill.font.name = FONT_HEADING
        p_pill.font.size = Pt(10)
        p_pill.font.bold = True
        p_pill.font.color.rgb = p_color
        p_pill.alignment = PP_ALIGN.CENTER

        # Timeline badge
        time_box = slide14.shapes.add_textbox(Inches(1.0), top_pos + Inches(0.6), Inches(3.4), Inches(0.45))
        tf_tb = time_box.text_frame
        p_tb = tf_tb.paragraphs[0]
        p_tb.text = f"Timeline: {p_time}"
        p_tb.font.name = FONT_BODY
        p_tb.font.size = Pt(9.5)
        p_tb.font.bold = True
        p_tb.font.color.rgb = p_color

        # Details
        tb = slide14.shapes.add_textbox(Inches(4.6), top_pos + Inches(0.1), Inches(7.7), Inches(1.0))
        tf = tb.text_frame
        tf.word_wrap = True
        for j, itm in enumerate(p_items):
            p = tf.paragraphs[0] if j == 0 else tf.add_paragraph()
            p.text = "• " + itm
            p.font.name = FONT_BODY
            p.font.size = Pt(9.5)
            p.font.color.rgb = NAVY_DARK
            p.space_after = Pt(1)

    # =========================================================================
    # SLIDE 15: Academic Conclusion & Key Contributions (Dark Theme)
    # =========================================================================
    slide15 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide15, NAVY_DARK)
    add_header(slide15, "7. Conclusion", "Summary of Deliverables, Academic Contributions & Project Defense", dark=True)
    add_footer(slide15, 15, dark=True)

    col3_w = Inches(3.7)
    c_cards = [
        ("Key Innovation & Novelty", CYAN_ACCENT, [
            "Replaced fragmented APM silos with an integrated 5-layer telemetry pipeline.",
            "Unified W3C Trace ID propagation connecting frontend Web Vitals to DB query plans.",
            "Pioneered dual-engine AI: explainable 0-100 heuristic scoring + Scikit-Learn Isolation Forest.",
            "Integrated controlled A/B experiment runner with mathematical Optimization Gain Index (OGI %)."
        ]),
        ("Empirical Validation Results", EMERALD_GREEN, [
            "Proved that database-only tuning produces only minor overall improvement (+13%).",
            "Demonstrated that full cross-layer optimization slashes latency by 96.1% (181.8ms to 7.0ms).",
            "Multiplied system throughput by 23.0x under 50 concurrent virtual users (24.2 to 555.6 RPS).",
            "Compressed network payloads by 97.3% and maintained sub-25ms P99 tail latencies."
        ]),
        ("Academic & Practical Value", PURPLE_AI, [
            "Fulfills all engineering and theoretical requirements for the Academic Major Project.",
            "Provides DevOps and SRE teams with an open-source, actionable, low-overhead APM framework.",
            "Complete reproducible code base: Node.js, Python FastAPI, React, PostgreSQL, Docker.",
            "Clear technical foundation established for Phase 2 autonomous auto-remediation."
        ])
    ]

    for i, (c_title, c_color, c_items) in enumerate(c_cards):
        c_left = Inches(0.8 + i * (3.7 + 0.3))
        add_card(slide15, c_left, Inches(1.65), col3_w, Inches(5.1), SLATE_CARD, SLATE_BORDER)

        pill = slide15.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left, Inches(1.65), col3_w, Inches(0.55))
        pill.fill.solid()
        pill.fill.fore_color.rgb = SLATE_BORDER
        pill.line.fill.background()
        tf_p = pill.text_frame
        p = tf_p.paragraphs[0]
        p.text = c_title
        p.font.name = FONT_HEADING
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = c_color
        p.alignment = PP_ALIGN.CENTER

        tb = slide15.shapes.add_textbox(c_left + Inches(0.2), Inches(2.35), col3_w - Inches(0.4), Inches(4.2))
        tf_b = tb.text_frame
        tf_b.word_wrap = True
        for j, pt in enumerate(c_items):
            p = tf_b.paragraphs[0] if j == 0 else tf_b.add_paragraph()
            p.text = "• " + pt
            p.font.name = FONT_BODY
            p.font.size = Pt(10)
            p.font.color.rgb = TEXT_LIGHT
            p.space_after = Pt(8)

    # =========================================================================
    # SLIDE 16: Project Demonstration, Q&A & Acknowledgments (Hero Dark Theme)
    # =========================================================================
    slide16 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide16, NAVY_DARK)

    # Top accent bar
    bar16 = slide16.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.12))
    bar16.fill.solid()
    bar16.fill.fore_color.rgb = CYAN_ACCENT
    bar16.line.fill.background()

    # Center Box
    c_box = slide16.shapes.add_textbox(Inches(1.5), Inches(1.5), Inches(10.333), Inches(2.8))
    tf_c = c_box.text_frame
    tf_c.word_wrap = True

    p_pill = tf_c.paragraphs[0]
    p_pill.text = "ACADEMIC MAJOR PROJECT DEFENSE & EVALUATION"
    p_pill.font.name = FONT_HEADING
    p_pill.font.size = Pt(12)
    p_pill.font.bold = True
    p_pill.font.color.rgb = CYAN_LIGHT
    p_pill.alignment = PP_ALIGN.CENTER

    p_t = tf_c.add_paragraph()
    p_t.text = "Thank You!"
    p_t.font.name = FONT_HEADING
    p_t.font.size = Pt(42)
    p_t.font.bold = True
    p_t.font.color.rgb = TEXT_WHITE
    p_t.alignment = PP_ALIGN.CENTER
    p_t.space_before = Pt(8)

    p_sub = tf_c.add_paragraph()
    p_sub.text = "Questions, Feedback & Live System Demonstration"
    p_sub.font.name = FONT_BODY
    p_sub.font.size = Pt(17)
    p_sub.font.color.rgb = CYAN_LIGHT
    p_sub.alignment = PP_ALIGN.CENTER
    p_sub.space_before = Pt(6)

    # Info Card in Center
    card_info = add_card(slide16, Inches(2.0), Inches(4.3), Inches(9.333), Inches(2.4), SLATE_CARD, SLATE_BORDER)
    tb_inf = slide16.shapes.add_textbox(Inches(2.2), Inches(4.45), Inches(8.933), Inches(2.1))
    tf_inf = tb_inf.text_frame
    tf_inf.word_wrap = True

    info_lines = [
        ("Project Title:", "Integrated Multi-Layer Performance Optimization Framework for Web Applications (IMPOF)", CYAN_LIGHT),
        ("Key Result:", "+96.1% Latency Reduction (OGI) • 23.0x Throughput Scaling • 97.3% Payload Slashed", EMERALD_GREEN),
        ("DevOps Dashboard:", "http://localhost:5173  (React 18 + Vite Live Telemetry UI)", TEXT_WHITE),
        ("Platform Backend:", "http://localhost:5000  (Node.js / Express Ingestion & Experiment Engine)", TEXT_WHITE),
        ("AI Analysis Engine:", "http://localhost:8000/docs  (Python FastAPI Isolation Forest Swagger)", TEXT_WHITE),
        ("Demo Target App:", "http://localhost:3000  (Movie Recommendation App with 100k Records)", TEXT_WHITE)
    ]
    for j, (label, val, col) in enumerate(info_lines):
        p = tf_inf.paragraphs[0] if j == 0 else tf_inf.add_paragraph()
        p.text = f"{label} {val}"
        p.font.name = FONT_BODY
        p.font.size = Pt(10.5)
        p.font.color.rgb = col
        p.space_after = Pt(2)

    add_footer(slide16, 16, dark=True)

    # Save presentation
    output_path = "IMPOF_Project_Presentation.pptx"
    prs.save(output_path)
    print(f"Presentation saved successfully to {os.path.abspath(output_path)}")
    return output_path

if __name__ == "__main__":
    create_presentation()
