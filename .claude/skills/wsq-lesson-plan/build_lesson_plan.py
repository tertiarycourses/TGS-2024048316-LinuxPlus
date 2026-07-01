#!/usr/bin/env python3
"""build_lesson_plan.py — WSQ Lesson Plan (.docx) for TGS-2024048316.

House format (wsq-lesson-plan skill): cover page, Document Version Control Record,
Word TOC field, Course Overview, Learning Outcomes, a colour-coded daily schedule
(9:00 AM – 6:00 PM, 8 instructional hours/day), a topic-by-topic breakdown that lists
every lab against its exam objective, Resources, and the Assessment block.

Two-day class: final assessment on Day 2, 4:00–6:00 PM = 1 hr Written (SAQ) + 1 hr
Practical Performance (PP), open book.
"""
import os
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

import sys
# prodoc.py is local to this skill; course_content.py (single source) lives in the
# wsq-learner-guide skill alongside build_learner_guide.py.
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
sys.path.insert(0, os.path.join(_HERE, os.pardir, "wsq-learner-guide"))
import prodoc
from prodoc import BRAND, DARK, GREY
from course_content import COURSE, DOMAINS, LEARNING_OUTCOMES, DAY_TOPICS, domain_labs, COURSEWARE

OUT = os.path.join(COURSEWARE, "LP-CompTIA-Linux-Plus-XK0-006.docx")

# ---- schedule rows: (time, duration, activity, method), colour tag for the row --
BREAK = "BREAK"
ASSESS = "ASSESS"
ADMIN = "ADMIN"


def _cell(cell, text, bold=False, size=10, color=DARK, align=None):
    cell.text = ""
    p = cell.paragraphs[0]
    if align:
        p.alignment = align
    r = p.add_run(text); r.bold = bold; r.font.size = Pt(size)
    r.font.color.rgb = color; r.font.name = "Arial"


def schedule_table(doc, rows):
    t = doc.add_table(rows=0, cols=4); t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    widths = [1.2, 1.0, 3.6, 1.2]
    hdr = t.add_row().cells
    for i, h in enumerate(["Time", "Duration", "Topic / Activity", "Method"]):
        _cell(hdr[i], h, bold=True, size=10, color=RGBColor(0xFF, 0xFF, 0xFF))
        prodoc._shade_cell(hdr[i], "C8102E")
    for (time, dur, act, method, tag) in rows:
        cells = t.add_row().cells
        _cell(cells[0], time, size=9.5)
        _cell(cells[1], dur, size=9.5)
        _cell(cells[2], act, size=9.5, bold=(tag in (ASSESS,)))
        _cell(cells[3], method, size=9.5)
        shade = {BREAK: "F2F2F2", ASSESS: "FCE4E4", ADMIN: "EFF3FA"}.get(tag)
        if shade:
            for c in cells:
                prodoc._shade_cell(c, shade)
    for row in t.rows:
        for i, w in enumerate(widths):
            from docx.shared import Inches
            row.cells[i].width = Inches(w)


def h1(doc, text):
    doc.add_heading(text, level=1)


def h2(doc, text):
    doc.add_heading(text, level=2)


def para(doc, text, size=11):
    p = doc.add_paragraph()
    r = p.add_run(text); r.font.size = Pt(size); r.font.name = "Arial"; r.font.color.rgb = DARK
    return p


def bullet(doc, text):
    p = doc.add_paragraph(style="List Bullet")
    r = p.add_run(text); r.font.size = Pt(10.5); r.font.name = "Arial"; r.font.color.rgb = DARK
    return p


# ------------------------------------------------------------------ Day schedules
DAY1_ROWS = [
    ("9:00 AM", "15 min", "Digital Attendance (AM) via TRAQOM/LMS · Trainer & Learner Introduction", "Admin", ADMIN),
    ("9:15 AM", "15 min", "Course Overview, Learning Outcomes & Ground Rules", "Lecture", ADMIN),
    ("9:30 AM", "2 hr 15 min", "Domain 1 — System Management (23%): boot & FHS, kernel modules, "
     "LVM storage, networking, shell operations (Labs 1–5)", "Lecture + Hands-on Labs", None),
    ("11:45 AM", "45 min", "Lunch Break", "", BREAK),
    ("12:30 PM", "1 hr 30 min", "Domain 1 (cont.) — backup & restore, virtualization (Labs 6–7)",
     "Lecture + Hands-on Labs", None),
    ("2:00 PM", "10 min", "Digital Attendance (PM)", "Admin", ADMIN),
    ("2:10 PM", "2 hr 50 min", "Domain 2 — Services and User Management (20%): files, accounts, "
     "processes, packages, systemd, containers (Labs 8–13)", "Lecture + Hands-on Labs", None),
    ("5:00 PM", "50 min", "Domain 2 wrap-up, Q&A and Day 1 recap", "Discussion", None),
    ("5:50 PM", "10 min", "Day 1 review & preview of Day 2", "Discussion", None),
    ("6:00 PM", "", "End of Day 1", "", ADMIN),
]

DAY2_ROWS = [
    ("9:00 AM", "10 min", "Digital Attendance (AM) via TRAQOM/LMS", "Admin", ADMIN),
    ("9:10 AM", "2 hr 35 min", "Domain 3 — Security (18%): AAA/sudo/PAM, firewalls, OS hardening, "
     "account hardening, cryptography, compliance & audit (Labs 14–19)", "Lecture + Hands-on Labs", None),
    ("11:45 AM", "45 min", "Lunch Break", "", BREAK),
    ("12:30 PM", "2 hr 10 min", "Domain 4 — Automation, Orchestration & Scripting (17%): Ansible, "
     "Bash, Python, Git, responsible AI (Labs 20–24)", "Lecture + Hands-on Labs", None),
    ("2:40 PM", "10 min", "Digital Attendance (PM)", "Admin", ADMIN),
    ("2:50 PM", "50 min", "Domain 5 — Troubleshooting (22%): monitoring, storage, network, security, "
     "performance (Labs 25–29)", "Lecture + Hands-on Labs", None),
    ("3:40 PM", "20 min", "Capstone — end-to-end server build & triage (Lab 30)", "Hands-on Lab", None),
    ("4:00 PM", "0 min", "Revision · Briefing for Assessment · Course Feedback & TRAQOM Survey", "Admin", ADMIN),
    ("4:00 PM", "1 hr", "Final Written Assessment (SAQ) — Open Book", "Written Assessment (WA)", ASSESS),
    ("5:00 PM", "1 hr", "Final Practical Performance (PP) — Open Book", "Practical Performance (PP)", ASSESS),
    ("6:00 PM", "", "Submit answers on LMS · Sign Assessment Summary Record · End of Class", "", ADMIN),
]


def build():
    doc = Document()
    prodoc.style_headings(doc)
    prodoc.add_cover_page(doc, "LESSON PLAN", COURSE["title"], COURSE["version"],
                          org_logo=COURSE["org_logo"], course_logo=COURSE["course_logo"])
    prodoc.add_version_control(doc, [
        ("1.0", "1 Jul 2026", "Initial release — aligned to CompTIA Linux+ XK0-006 V8 "
         "exam domains and the 30 hands-on labs.", COURSE["trainer"]),
    ])
    prodoc.add_toc(doc)

    # --- Course Overview
    h1(doc, "Course Overview")
    para(doc, f"{COURSE['title']} ({COURSE['code']}) is a 2-day, hands-on WSQ course that "
              "prepares learners to configure, manage, operate and troubleshoot Linux server "
              "environments while applying security best practices, scripting, containerization, "
              "virtualization and automation. The course is fully aligned to the five CompTIA "
              f"Linux+ {COURSE['exam']} exam domains and is delivered through 30 practical labs "
              "on the free Killercoda Ubuntu Playground.")

    h1(doc, "Learning Outcomes")
    para(doc, "By the end of this course, participants will be able to:")
    for lo in LEARNING_OUTCOMES:
        bullet(doc, lo)

    h1(doc, "Exam Domain Coverage")
    para(doc, f"The course maps 1:1 to the CompTIA Linux+ {COURSE['exam']} exam blueprint. "
              "Each domain's weighting and the labs that cover it:")
    t = doc.add_table(rows=0, cols=4); t.style = "Table Grid"; t.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr = t.add_row().cells
    for i, htxt in enumerate(["Domain", "Exam Weight", "Labs", "Sub-objectives"]):
        _cell(hdr[i], htxt, bold=True, size=10, color=RGBColor(0xFF, 0xFF, 0xFF))
        prodoc._shade_cell(hdr[i], "C8102E")
    for d in DOMAINS:
        cells = t.add_row().cells
        _cell(cells[0], f"{d['num']}. {d['title']}", size=9.5, bold=True)
        _cell(cells[1], f"{d['weight']}%", size=9.5, align=WD_ALIGN_PARAGRAPH.CENTER)
        _cell(cells[2], f"{d['labs'][0]}–{d['labs'][-1]}", size=9.5, align=WD_ALIGN_PARAGRAPH.CENTER)
        _cell(cells[3], ", ".join(o[0] for o in d["objs"]), size=9.5)

    # --- Daily schedule
    h1(doc, "Daily Schedule")
    para(doc, "Each training day runs 9:00 AM – 6:00 PM and delivers 8 instructional hours "
              "(1-hour lunch; tea breaks counted within teaching time).")
    h2(doc, "Day 1 — System Management & Services / User Management")
    schedule_table(doc, DAY1_ROWS)
    doc.add_paragraph()
    h2(doc, "Day 2 — Security, Automation, Troubleshooting & Final Assessment")
    schedule_table(doc, DAY2_ROWS)

    # --- Topic-by-topic breakdown (lists EVERY lab against its objective)
    h1(doc, "Topic-by-Topic Breakdown")
    for d in DOMAINS:
        h2(doc, f"Domain {d['num']} — {d['title']} ({d['weight']}%)")
        objmap = {o[0]: o[1] for o in d["objs"]}
        for lab in domain_labs(d["num"]):
            p = doc.add_paragraph()
            r = p.add_run(f"Lab {lab['num']} — {lab['title']}  [Obj {lab['objective']}]")
            r.bold = True; r.font.size = Pt(10.5); r.font.name = "Arial"; r.font.color.rgb = BRAND
            para(doc, lab["goal"], size=10)

    # --- Resources
    h1(doc, "Resources Required")
    for res in [
        "A laptop with a modern web browser and reliable internet access.",
        f"Free Killercoda Ubuntu Playground — {COURSE['killercoda']} (no local install required).",
        "Course slide deck and Learner Guide (downloaded from the LMS).",
        f"Tertiary Infotech LMS account — {COURSE['lms']} (courseware download and assessment).",
        f"CompTIA Linux+ {COURSE['exam']} Exam Objectives (reference blueprint).",
    ]:
        bullet(doc, res)

    # --- Assessment
    h1(doc, "Assessment")
    para(doc, "The course is assessed on the final afternoon of Day 2 (4:00 PM – 6:00 PM):")
    for b in [
        "Written Assessment (WA) — Short-Answer Questions (SAQ), 1 hour (4:00–5:00 PM), open book.",
        "Practical Performance (PP) — hands-on lab tasks, 1 hour (5:00–6:00 PM), open book.",
        "Open book means learners may refer to the slides, Learner Guide and any approved materials.",
        "Assessment flow: TRAQOM survey (scan the QR code on the LMS) → Assessment Digital Attendance "
        "→ Assessment (WA + PP) → Submit answers on the LMS → Sign the Assessment Summary Record.",
        f"Courseware and the assessment are hosted on the LMS — {COURSE['lms']}.",
    ]:
        bullet(doc, b)
    para(doc, "Funding criteria: learners must attend at least 75% of the course and be assessed "
              "as Competent (C) in both the Written Assessment and the Practical Performance to be "
              "eligible for course funding and certification.")

    prodoc.add_page_numbers(doc)
    prodoc.enable_update_fields(doc)
    doc.save(OUT)
    print("wrote", OUT)


if __name__ == "__main__":
    build()
