"""course_content.py — SINGLE SOURCE OF TRUTH for TGS-2024048316.

CompTIA Certified Linux+ Training (XK0-006 V8), delivered by Tertiary Infotech
Academy Pte Ltd. Every artifact — the PPT deck, the Lesson Plan (LP), the Learner
Guide (LG DOCX) and its Markdown mirror — is generated from the data below, so all
four stay 100% aligned to the 30 hands-on labs and the CompTIA exam domains.

The 30 labs (goal / build / concepts / step-by-step / test) are loaded from the
batch JSON files produced from the labs/ folder, keyed to the exam objectives.
"""
import html
import json
import os

def _find_repo():
    """Locate the course repo root (the dir containing labs/ and courseware/),
    so this module works from inside a skill folder or anywhere else."""
    env = os.environ.get("COURSE_REPO")
    if env and os.path.isdir(os.path.join(env, "labs")):
        return env
    d = os.path.dirname(os.path.abspath(__file__))
    for _ in range(8):
        if os.path.isdir(os.path.join(d, "labs")) and os.path.isdir(os.path.join(d, "courseware")):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            break
        d = parent
    return os.getcwd()


REPO = _find_repo()
COURSEWARE = os.path.join(REPO, "courseware")     # generated documents land here
ASSETS = os.path.join(COURSEWARE, "assets")
# Structured lab content (extracted from labs/) lives in courseware/data/.
BATCH_DIR = os.environ.get("LABS_BATCH_DIR", os.path.join(COURSEWARE, "data"))

# ---------------------------------------------------------------- course metadata
COURSE = dict(
    title="CompTIA Certified Linux+ Training (XK0-006)",
    short="CompTIA Certified Linux+ Training",
    code="TGS-2024048316",
    exam="XK0-006 V8",
    org="Tertiary Infotech Academy Pte Ltd",
    uen="201200696W",
    version="1.0",
    trainer="Dr. Alfred Ang",
    days=2,
    lms="https://lms-tms.tertiaryinfotech.com/",
    killercoda="https://killercoda.com/playgrounds/scenario/ubuntu",
    register="https://www.tertiarycourses.com.sg/wsq-comptia-linux-training.html",
    org_logo=os.path.join(ASSETS, "tertiary-infotech-logo.png"),
    course_logo=os.path.join(ASSETS, "comptia-linux-logo.png"),
)

# ---------------------------------------------------------------- the five domains
# weight = official XK0-006 exam percentage; objs = the sub-objectives (from the
# official Exam Objectives PDF) so the courseware maps 1:1 to the blueprint.
DOMAINS = [
    dict(num=1, title="System Management", weight=23, labs=list(range(1, 8)),
         objs=[
             ("1.1", "Explain basic Linux concepts"),
             ("1.2", "Summarize Linux device management concepts and tools"),
             ("1.3", "Given a scenario, manage storage in a Linux system"),
             ("1.4", "Given a scenario, manage network services and configurations"),
             ("1.5", "Given a scenario, manage a Linux system using common shell operations"),
             ("1.6", "Given a scenario, perform backup and restore operations"),
             ("1.7", "Summarize virtualization on Linux systems"),
         ]),
    dict(num=2, title="Services and User Management", weight=20, labs=list(range(8, 14)),
         objs=[
             ("2.1", "Given a scenario, manage files and directories"),
             ("2.2", "Given a scenario, perform local account management"),
             ("2.3", "Given a scenario, manage processes and jobs"),
             ("2.4", "Given a scenario, configure and manage software"),
             ("2.5", "Given a scenario, manage Linux using systemd"),
             ("2.6", "Given a scenario, manage applications in a container"),
         ]),
    dict(num=3, title="Security", weight=18, labs=list(range(14, 20)),
         objs=[
             ("3.1", "Summarize authorization, authentication, and accounting methods"),
             ("3.2", "Given a scenario, configure and implement firewalls"),
             ("3.3", "Given a scenario, apply OS hardening techniques"),
             ("3.4", "Explain account hardening techniques and best practices"),
             ("3.5", "Explain cryptographic concepts and technologies"),
             ("3.6", "Explain the importance of compliance and audit procedures"),
         ]),
    dict(num=4, title="Automation, Orchestration, and Scripting", weight=17, labs=list(range(20, 25)),
         objs=[
             ("4.1", "Summarize automation and orchestration use cases and techniques"),
             ("4.2", "Given a scenario, perform automated tasks using shell scripting"),
             ("4.3", "Summarize Python basics used for Linux system administration"),
             ("4.4", "Given a scenario, implement version control using Git"),
             ("4.5", "Summarize best practices and responsible uses of AI"),
         ]),
    dict(num=5, title="Troubleshooting", weight=22, labs=list(range(25, 31)),
         objs=[
             ("5.1", "Summarize monitoring concepts and configurations"),
             ("5.2", "Given a scenario, troubleshoot hardware, storage, and OS issues"),
             ("5.3", "Given a scenario, troubleshoot networking issues"),
             ("5.4", "Given a scenario, troubleshoot security issues"),
             ("5.5", "Given a scenario, troubleshoot performance issues"),
         ]),
]

# Course-level learning outcomes (WSQ house wording).
LEARNING_OUTCOMES = [
    "Explain core Linux concepts — the boot process, the Filesystem Hierarchy Standard, "
    "device management and virtualization — and manage storage, networking and shell operations.",
    "Manage files, local user and group accounts, processes and jobs, software packages, "
    "systemd services and containerized applications on a Linux server.",
    "Apply Linux security: authentication/authorization (sudo, PAM), firewalls, OS and account "
    "hardening, cryptography and compliance/audit procedures.",
    "Automate administration with Ansible, Bash and Python, apply Git version control, and use "
    "AI assistants responsibly and securely.",
    "Monitor a Linux system and analyze and troubleshoot hardware, storage, network, security "
    "and performance issues using the right diagnostic tools.",
]

DAY_TOPICS = {
    1: [1, 2],   # Day 1: Domains 1 & 2
    2: [3, 4, 5],  # Day 2: Domains 3, 4, 5 + Capstone + Assessment
}


def _unescape(obj):
    if isinstance(obj, str):
        return html.unescape(obj)
    if isinstance(obj, list):
        return [_unescape(x) for x in obj]
    if isinstance(obj, dict):
        return {k: _unescape(v) for k, v in obj.items()}
    return obj


def load_labs():
    labs = []
    for i in range(1, 6):
        path = os.path.join(BATCH_DIR, f"batch{i}.json")
        with open(path) as fh:
            labs.extend(json.load(fh))
    labs = _unescape(labs)
    labs.sort(key=lambda x: x["num"])
    assert len(labs) == 30, f"expected 30 labs, got {len(labs)}"
    return labs


LABS = load_labs()
LABS_BY_NUM = {l["num"]: l for l in LABS}


def domain_labs(dnum):
    return [LABS_BY_NUM[n] for n in DOMAINS[dnum - 1]["labs"]]


if __name__ == "__main__":
    print(f"Loaded {len(LABS)} labs across {len(DOMAINS)} domains")
    for d in DOMAINS:
        print(f"  Domain {d['num']} ({d['weight']}%) {d['title']}: labs {d['labs']}")
    for l in LABS:
        print(f"  Lab {l['num']:>2} [{l['objective']:>8}] {l['title']} — {len(l['steps'])} steps")
