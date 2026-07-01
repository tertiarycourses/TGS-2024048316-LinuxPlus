#!/usr/bin/env python3
"""build_slides.py — WSQ course slide deck (.pptx) for TGS-2024048316.

All-white house-style deck (python-pptx, 16:9) generated from the single source
course_content.py, so every slide stays aligned to the 30 labs and the CompTIA
Linux+ XK0-006 exam domains.

Follows the wsq-slides house standard:
  * © footer on every slide; org name + UEN on the title slide
  * About the Trainer x2 (blank General template + named trainer)
  * Briefing for Assessment BEFORE the Assessment slide
  * Lesson Plan slide; LMS slide; Certification & TRAQOM survey
  * Canonical admin order, then per-domain concept slides + per-lab slides
"""
import os
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

import sys
# course_content.py (single source) lives in the wsq-learner-guide skill.
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, os.pardir, "wsq-learner-guide"))
from course_content import (COURSE, DOMAINS, LEARNING_OUTCOMES, domain_labs,
                            LABS_BY_NUM, COURSEWARE)

OUT = os.path.join(COURSEWARE, "PPT-CompTIA-Linux-Plus-XK0-006.pptx")

# palette
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
RED   = RGBColor(0xC8, 0x10, 0x2E)
DARK  = RGBColor(0x11, 0x18, 0x27)
GREY  = RGBColor(0x55, 0x5B, 0x66)
LIGHT = RGBColor(0xF4, 0xF5, 0xF7)
GREEN = RGBColor(0x0A, 0x7A, 0x3B)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]
SW, SH = prs.slide_width, prs.slide_height


def _slide(bg=WHITE):
    s = prs.slides.add_slide(BLANK)
    r = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SW, SH)
    r.fill.solid(); r.fill.fore_color.rgb = bg; r.line.fill.background()
    r.shadow.inherit = False
    s.shapes._spTree.remove(r._element); s.shapes._spTree.insert(2, r._element)
    return s


def _box(s, l, t, w, h):
    tb = s.shapes.add_textbox(l, t, w, h)
    tf = tb.text_frame; tf.word_wrap = True
    return tb, tf


def _txt(tf, text, size, color=DARK, bold=False, align=PP_ALIGN.LEFT, font="Arial",
         space_after=4, first=False):
    p = tf.paragraphs[0] if first else tf.add_paragraph()
    p.alignment = align; p.space_after = Pt(space_after)
    r = p.add_run(); r.text = text
    r.font.size = Pt(size); r.font.bold = bold; r.font.color.rgb = color; r.font.name = font
    return p


def _rect(s, l, t, w, h, fill=None, line=None):
    shp = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, l, t, w, h)
    if fill is None:
        shp.fill.background()
    else:
        shp.fill.solid(); shp.fill.fore_color.rgb = fill
    if line is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = line; shp.line.width = Pt(1)
    shp.shadow.inherit = False
    return shp


def _footer(s, idx=None):
    tb, tf = _box(s, Inches(0.4), Inches(7.05), Inches(9.5), Inches(0.35))
    _txt(tf, "© Tertiary Infotech Academy Pte Ltd", 8, GREY, first=True)
    if idx is not None:
        tb2, tf2 = _box(s, Inches(12.2), Inches(7.05), Inches(0.9), Inches(0.35))
        _txt(tf2, str(idx), 8, GREY, align=PP_ALIGN.RIGHT, first=True)


def _accent(s):
    _rect(s, 0, 0, Inches(0.22), SH, fill=RED)


def content_header(s, kicker, title):
    if kicker:
        tb, tf = _box(s, Inches(0.6), Inches(0.45), Inches(11.8), Inches(0.4))
        _txt(tf, kicker, 13, RED, bold=True, first=True)
    tb, tf = _box(s, Inches(0.6), Inches(0.85), Inches(12.1), Inches(0.9))
    _txt(tf, title, 30, DARK, bold=True, first=True)
    _rect(s, Inches(0.62), Inches(1.72), Inches(1.5), Pt(3), fill=RED)


# ============================================================= admin / title slides
def title_slide():
    s = _slide(DARK)
    # logos
    if os.path.exists(COURSE["course_logo"]):
        s.shapes.add_picture(COURSE["course_logo"], Inches(5.5), Inches(0.7), height=Inches(1.6))
    tb, tf = _box(s, Inches(1.0), Inches(2.6), Inches(11.3), Inches(2.2))
    _txt(tf, COURSE["title"], 40, WHITE, bold=True, align=PP_ALIGN.CENTER, first=True)
    _txt(tf, f"WSQ Training  ·  CompTIA Linux+ {COURSE['exam']}", 20,
         RGBColor(0xF3, 0xC5, 0xCB), align=PP_ALIGN.CENTER, space_after=6)
    _txt(tf, f"Course Code: {COURSE['code']}", 16, WHITE, align=PP_ALIGN.CENTER)
    tb, tf = _box(s, Inches(1.0), Inches(5.4), Inches(11.3), Inches(1.6))
    _txt(tf, COURSE["org"], 18, WHITE, bold=True, align=PP_ALIGN.CENTER, first=True)
    _txt(tf, f"UEN: {COURSE['uen']}", 13, RGBColor(0xC9, 0xCE, 0xD6), align=PP_ALIGN.CENTER, space_after=8)
    _txt(tf, f"Trainer: {COURSE['trainer']}     |     Version {COURSE['version']}",
         13, RGBColor(0xC9, 0xCE, 0xD6), align=PP_ALIGN.CENTER)
    tb, tf = _box(s, Inches(0.4), Inches(7.05), Inches(9), Inches(0.35))
    _txt(tf, "© Tertiary Infotech Academy Pte Ltd", 8, RGBColor(0x9A, 0xA1, 0xAC), first=True)


def bullets_slide(kicker, title, bullets, idx, sub=None, numbered=False):
    s = _slide(); _accent(s); content_header(s, kicker, title)
    top = Inches(2.0)
    tb, tf = _box(s, Inches(0.7), top, Inches(12.0), Inches(4.8))
    first = True
    if sub:
        _txt(tf, sub, 14, GREY, first=True); first = False
    for i, b in enumerate(bullets, 1):
        prefix = f"{i}. " if numbered else "•  "
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.space_after = Pt(9)
        r = p.add_run(); r.text = prefix + b
        r.font.size = Pt(15); r.font.color.rgb = DARK; r.font.name = "Arial"
    _footer(s, idx)
    return s


def kv_template_slide(title, rows, idx, note=None):
    s = _slide(); _accent(s); content_header(s, "About the Trainer", title)
    top = 2.1
    for label, val in rows:
        tb, tf = _box(s, Inches(0.7), Inches(top), Inches(3.0), Inches(0.5))
        _txt(tf, label, 14, RED, bold=True, first=True)
        _rect(s, Inches(3.8), Inches(top + 0.05), Inches(8.6), Inches(0.42), fill=LIGHT)
        tb, tf = _box(s, Inches(3.9), Inches(top + 0.06), Inches(8.4), Inches(0.42))
        _txt(tf, val, 13, DARK, first=True)
        top += 0.62
    if note:
        tb, tf = _box(s, Inches(0.7), Inches(top + 0.1), Inches(11.8), Inches(0.6))
        _txt(tf, note, 11, GREY, first=True)
    _footer(s, idx)


def lesson_plan_slide(idx):
    s = _slide(); _accent(s); content_header(s, "Administration", "Lesson Plan — 2 Days (9:00 AM – 6:00 PM)")
    data = [
        ("Day 1", "Domain 1 — System Management (23%) · Domain 2 — Services & User Management (20%)  |  Labs 1–13"),
        ("Day 2 AM", "Domain 3 — Security (18%) · Domain 4 — Automation, Orchestration & Scripting (17%)  |  Labs 14–24"),
        ("Day 2 PM", "Domain 5 — Troubleshooting (22%) · Capstone  |  Labs 25–30"),
        ("Day 2 · 4:00–6:00 PM", "Final Assessment — Written (SAQ) 1 hr + Practical Performance (PP) 1 hr (Open Book)"),
    ]
    top = 2.1
    for k, v in data:
        assess = k.startswith("Day 2 ·")
        _rect(s, Inches(0.7), Inches(top), Inches(2.9), Inches(0.85), fill=(RED if assess else DARK))
        tb, tf = _box(s, Inches(0.75), Inches(top + 0.16), Inches(2.8), Inches(0.6))
        _txt(tf, k, 13, WHITE, bold=True, first=True)
        _rect(s, Inches(3.7), Inches(top), Inches(9.0), Inches(0.85), fill=(RGBColor(0xFC,0xE4,0xE4) if assess else LIGHT))
        tb, tf = _box(s, Inches(3.85), Inches(top + 0.08), Inches(8.7), Inches(0.72))
        _txt(tf, v, 12, DARK, first=True)
        top += 0.98
    tb, tf = _box(s, Inches(0.7), Inches(top + 0.05), Inches(12), Inches(0.5))
    _txt(tf, "Each day = 8 instructional hours (1-hour lunch; tea breaks within). "
             "Breaks may compress to make room for the assessment block.", 11, GREY, first=True)
    _footer(s, idx)


def domains_outline_slide(idx):
    s = _slide(); _accent(s); content_header(s, "Course Outline", "Five Exam Domains · 30 Hands-on Labs")
    top = 2.0
    for d in DOMAINS:
        _rect(s, Inches(0.7), Inches(top), Inches(0.9), Inches(0.72), fill=RED)
        tb, tf = _box(s, Inches(0.7), Inches(top + 0.14), Inches(0.9), Inches(0.5))
        _txt(tf, f"{d['weight']}%", 15, WHITE, bold=True, align=PP_ALIGN.CENTER, first=True)
        tb, tf = _box(s, Inches(1.8), Inches(top + 0.02), Inches(10.8), Inches(0.72))
        _txt(tf, f"Domain {d['num']} — {d['title']}", 16, DARK, bold=True, first=True)
        _txt(tf, f"Labs {d['labs'][0]}–{d['labs'][-1]}  ·  objectives "
                 + ", ".join(o[0] for o in d["objs"]), 11, GREY)
        top += 0.92
    _footer(s, idx)


# ============================================================= content slides
def domain_divider(d, idx):
    s = _slide(DARK); _accent(s)
    tb, tf = _box(s, Inches(0.9), Inches(1.5), Inches(11.5), Inches(1.0))
    _txt(tf, f"DOMAIN {d['num']}", 20, RGBColor(0xF3, 0xC5, 0xCB), bold=True, first=True)
    tb, tf = _box(s, Inches(0.9), Inches(2.2), Inches(11.5), Inches(1.4))
    _txt(tf, d["title"], 40, WHITE, bold=True, first=True)
    tb, tf = _box(s, Inches(0.9), Inches(3.7), Inches(11.5), Inches(0.6))
    _txt(tf, f"{d['weight']}% of the exam  ·  Labs {d['labs'][0]}–{d['labs'][-1]}",
         18, RGBColor(0xC9, 0xCE, 0xD6), first=True)
    # objective list
    top = 4.35
    for o in d["objs"]:
        tb, tf = _box(s, Inches(0.95), Inches(top), Inches(11.5), Inches(0.36))
        _txt(tf, f"{o[0]}   {o[1]}", 12.5, WHITE, first=True)
        top += 0.36
    tb, tf = _box(s, Inches(0.4), Inches(7.05), Inches(9), Inches(0.35))
    _txt(tf, "© Tertiary Infotech Academy Pte Ltd", 8, RGBColor(0x9A, 0xA1, 0xAC), first=True)


def lab_slide(lab, dweight, idx):
    s = _slide(); _accent(s)
    content_header(s, f"Lab {lab['num']}  ·  Objective {lab['objective']}", lab["title"])
    # objective title chip
    tb, tf = _box(s, Inches(0.7), Inches(1.85), Inches(12.0), Inches(0.4))
    _txt(tf, f"Maps to CompTIA Linux+ objective {lab['objective']} — {lab['obj_title']}",
         12, GREY, first=True)
    # Goal
    tb, tf = _box(s, Inches(0.7), Inches(2.35), Inches(7.2), Inches(2.6))
    _txt(tf, "Goal", 14, RED, bold=True, first=True)
    _txt(tf, lab["goal"], 13, DARK, space_after=8)
    _txt(tf, "What you'll do", 14, RED, bold=True)
    _txt(tf, lab["build"], 13, DARK)
    # Key concepts panel
    _rect(s, Inches(8.2), Inches(2.35), Inches(4.5), Inches(3.9), fill=LIGHT)
    tb, tf = _box(s, Inches(8.45), Inches(2.5), Inches(4.1), Inches(3.7))
    _txt(tf, "KEY COMMANDS & CONCEPTS", 12, DARK, bold=True, first=True)
    for c in lab["concepts"]:
        p = tf.add_paragraph(); p.space_after = Pt(5)
        r = p.add_run(); r.text = "▪ " + c
        r.font.size = Pt(12); r.font.color.rgb = DARK; r.font.name = "Consolas"
    # Test it strip
    _rect(s, Inches(0.7), Inches(6.35), Inches(11.95), Inches(0.55), fill=RGBColor(0xE9, 0xF5, 0xEE))
    tb, tf = _box(s, Inches(0.85), Inches(6.4), Inches(11.7), Inches(0.5))
    p = tf.paragraphs[0]; p.space_after = Pt(0)
    r = p.add_run(); r.text = "✓ Test it:  "; r.font.bold = True; r.font.size = Pt(11)
    r.font.color.rgb = GREEN; r.font.name = "Arial"
    r2 = p.add_run(); r2.text = lab["test"]; r2.font.size = Pt(11); r2.font.color.rgb = DARK; r2.font.name = "Arial"
    _footer(s, idx)


def command_slide(lab, idx):
    """A second slide per lab showing two representative command steps verbatim."""
    s = _slide(); _accent(s)
    content_header(s, f"Lab {lab['num']}  ·  {lab['objective']}", lab["title"] + " — Commands")
    steps = lab["steps"][:2] if len(lab["steps"]) >= 2 else lab["steps"]
    top = 1.95
    for step in steps:
        tb, tf = _box(s, Inches(0.7), Inches(top), Inches(12.0), Inches(0.4))
        _txt(tf, step["title"], 14, DARK, bold=True, first=True)
        top += 0.5
        lines = step["code"].split("\n")
        # cap to keep on-slide
        shown = lines[:7]
        h = 0.28 * len(shown) + 0.2
        _rect(s, Inches(0.7), Inches(top), Inches(11.95), Inches(h), fill=RGBColor(0x1E, 0x24, 0x31))
        tb, tf = _box(s, Inches(0.9), Inches(top + 0.08), Inches(11.6), Inches(h))
        for i, ln in enumerate(shown):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.space_after = Pt(0)
            r = p.add_run(); r.text = ln if ln.strip() else " "
            r.font.size = Pt(11); r.font.name = "Consolas"
            r.font.color.rgb = RGBColor(0x8CE, 0x99 & 0xFF, 0xA6) if False else RGBColor(0xD6, 0xF5, 0xDF)
        top += h + 0.35
    tb, tf = _box(s, Inches(0.7), Inches(6.75), Inches(12), Inches(0.4))
    _txt(tf, "Full step-by-step for all steps is in the Learner Guide and the labs/ folder.",
         10, GREY, first=True)
    _footer(s, idx)


# ============================================================= build
def build():
    n = [0]

    def nx():
        n[0] += 1
        return n[0]

    title_slide()
    bullets_slide("Administration", "Digital Attendance", [
        "Take the AM, PM and Assessment digital attendance on every training day.",
        "Scan the attendance QR code on the LMS (TRAQOM) for each session.",
        "Attendance of at least 75% is required for funding and certification.",
        f"LMS: {COURSE['lms']}",
    ], nx())

    kv_template_slide("General Trainer (template)", [
        ("Name", ""), ("Title", ""), ("Qualifications", ""),
        ("Areas of Expertise", ""), ("Industry Experience", ""), ("Contact", ""),
    ], nx(), note="This blank template can be completed by any assigned trainer.")

    kv_template_slide("Your Trainer", [
        ("Name", COURSE["trainer"]),
        ("Title", "Principal Trainer & Consultant, Tertiary Infotech Academy"),
        ("Qualifications", "PhD; ACTA/ACLP-certified adult educator"),
        ("Areas of Expertise", "Linux systems administration, cloud, DevOps, cybersecurity, AI"),
        ("Industry Experience", "20+ years in IT training, software and infrastructure engineering"),
        ("Contact", "enquiry@tertiaryinfotech.com · +65 6100 0613"),
    ], nx())

    bullets_slide("Let's Know Each Other", "Learner Introduction", [
        "Your name and organisation / role.",
        "Your current experience with Linux (beginner → advanced).",
        "Which of the five domains matters most to your day job.",
        "What you want to walk away able to do — and any exam timeline.",
    ], nx())

    bullets_slide("Administration", "Ground Rules", [
        "Be punctual for each session and after every break.",
        "Set devices to silent; give the hands-on labs your full attention.",
        "Ask questions any time — the labs are best learned by doing.",
        "Do the labs yourself on Killercoda; typing builds exam-day muscle memory.",
        "Respect fellow learners and keep shared environments clean (reset between labs).",
    ], nx())

    domains_outline_slide(nx())
    lesson_plan_slide(nx())

    # Briefing for Assessment BEFORE the Assessment slide (house rule)
    bullets_slide("Administration", "Briefing for Assessment", [
        "The assessment is on Day 2, 4:00 PM – 6:00 PM, and is OPEN BOOK.",
        "Written Assessment (SAQ) — 1 hour (4:00–5:00 PM): short-answer knowledge questions.",
        "Practical Performance (PP) — 1 hour (5:00–6:00 PM): hands-on lab tasks.",
        "Open book = you may use the slides, Learner Guide and approved materials.",
        "Flow: TRAQOM survey → Assessment Digital Attendance → Assessment → Submit on LMS → Sign the Assessment Summary Record.",
        "If assessed Not Yet Competent, an appeal and re-assessment process is available.",
    ], nx())

    bullets_slide("Administration", "Assessment & Funding", [
        "Be assessed Competent (C) in BOTH the Written Assessment and the Practical Performance.",
        "Attend at least 75% of the course.",
        "Complete the TRAQOM survey and sign the Assessment Summary Record.",
        f"Courseware download and assessment submission are on the LMS: {COURSE['lms']}",
    ], nx())

    bullets_slide("Course Objectives", "Learning Outcomes", LEARNING_OUTCOMES, nx(), numbered=True)

    # per-domain content
    for d in DOMAINS:
        domain_divider(d, nx())
        for lab in domain_labs(d["num"]):
            lab_slide(lab, d["weight"], nx())
            command_slide(lab, nx())

    # closing
    bullets_slide("Wrap-up", "Summary & Q&A", [
        "You have covered all five CompTIA Linux+ XK0-006 domains through 30 hands-on labs.",
        "System Management · Services & User Management · Security · Automation & Scripting · Troubleshooting.",
        "Keep practising on Killercoda and review the Learner Guide before the exam.",
        "Questions?",
    ], nx())

    bullets_slide("LMS", "Courseware & Assessment on the LMS", [
        "Download the slide deck and Learner Guide from the LMS.",
        "Complete the Written Assessment and Practical Performance on the LMS.",
        f"LMS: {COURSE['lms']}",
        "Contact: enquiry@tertiaryinfotech.com · +65 6100 0613 · www.tertiarycourses.com.sg",
    ], nx())

    bullets_slide("Certification", "Certification & TRAQOM Survey", [
        "Scan the TRAQOM QR code on the LMS and complete the course feedback survey.",
        "A WSQ Statement of Attainment / certificate follows a Competent assessment result.",
        "Your feedback helps us improve — thank you!",
        "Survey & certification portal: ai-lms-tms.tertiaryinfo.tech",
    ], nx())

    s = _slide(DARK); _accent(s)
    tb, tf = _box(s, Inches(1.0), Inches(2.8), Inches(11.3), Inches(1.8))
    _txt(tf, "Thank You!", 48, WHITE, bold=True, align=PP_ALIGN.CENTER, first=True)
    _txt(tf, "All the best for your CompTIA Linux+ XK0-006 certification.",
         18, RGBColor(0xC9, 0xCE, 0xD6), align=PP_ALIGN.CENTER)
    tb, tf = _box(s, Inches(0.4), Inches(7.05), Inches(9), Inches(0.35))
    _txt(tf, "© Tertiary Infotech Academy Pte Ltd", 8, RGBColor(0x9A, 0xA1, 0xAC), first=True)

    prs.save(OUT)
    print("wrote", OUT, "·", len(prs.slides.__iter__.__self__._sldIdLst), "slides")


if __name__ == "__main__":
    build()
