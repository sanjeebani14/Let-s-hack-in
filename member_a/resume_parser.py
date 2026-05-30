"""Resume file parsing and structured section extraction."""

import re
from io import BytesIO
from typing import Any, Dict, List


def extract_text_from_file(filename: str, content: bytes) -> str:
    """Extract plain text from PDF, DOCX, or plain text uploads."""
    name = (filename or "").lower()

    if name.endswith(".pdf"):
        try:
            from pypdf import PdfReader

            reader = PdfReader(BytesIO(content))
            parts = []
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    parts.append(text)
            return "\n".join(parts).strip()
        except Exception as exc:
            raise ValueError(f"Could not read PDF: {exc}") from exc

    if name.endswith(".docx"):
        try:
            from docx import Document

            doc = Document(BytesIO(content))
            return "\n".join(p.text for p in doc.paragraphs if p.text).strip()
        except Exception as exc:
            raise ValueError(f"Could not read DOCX: {exc}") from exc

    if name.endswith((".txt", ".md", ".rtf")):
        for encoding in ("utf-8", "latin-1", "cp1252"):
            try:
                return content.decode(encoding).strip()
            except UnicodeDecodeError:
                continue
        raise ValueError("Could not decode text file")

    # Fallback: try UTF-8 decode
    try:
        return content.decode("utf-8").strip()
    except UnicodeDecodeError:
        raise ValueError(
            "Unsupported file type. Upload PDF, DOCX, or TXT."
        ) from None


def _find_section_lines(text: str, headers: List[str]) -> List[str]:
    """Collect lines under a resume section header until the next section."""
    lines = text.splitlines()
    collecting = False
    section_lines: List[str] = []

    header_pattern = re.compile(
        r"^(" + "|".join(re.escape(h) for h in headers) + r")\s*:?\s*$",
        re.IGNORECASE,
    )
    any_section = re.compile(
        r"^(experience|work\s+experience|employment|internship|internships|"
        r"education|skills|projects|certifications|summary|objective)\s*:?\s*$",
        re.IGNORECASE,
    )

    for line in lines:
        stripped = line.strip()
        if not stripped:
            if collecting and section_lines:
                section_lines.append("")
            continue

        if header_pattern.match(stripped):
            collecting = True
            continue

        if collecting and any_section.match(stripped):
            break

        if collecting:
            section_lines.append(stripped)

    return section_lines


def _parse_bullet_entries(lines: List[str]) -> List[Dict[str, str]]:
    """Parse experience/internship bullets into structured entries."""
    entries: List[Dict[str, str]] = []
    current: Dict[str, str] = {}

    date_re = re.compile(
        r"(\w+\s+\d{4}|\d{4})\s*[-–—]\s*(\w+\s+\d{4}|\d{4}|present|current)",
        re.IGNORECASE,
    )
    title_at_re = re.compile(
        r"^(.+?)\s+(?:at|@|,)\s+(.+?)(?:\s*[-–—|]\s*(.+))?$",
        re.IGNORECASE,
    )

    for line in lines:
        if line.startswith(("-", "•", "*")):
            bullet = line.lstrip("-•* ").strip()
            if current:
                desc = current.get("description", "")
                current["description"] = f"{desc}\n• {bullet}".strip()
            continue

        m_date = date_re.search(line)
        duration = m_date.group(0) if m_date else ""

        title_line = date_re.sub("", line).strip(" -–—|")
        title = title_line
        company = ""

        m_ta = title_at_re.match(title_line)
        if m_ta:
            title = m_ta.group(1).strip()
            company = m_ta.group(2).strip()

        if current and (title or company):
            entries.append(current)
            current = {}

        if title or company or duration:
            current = {
                "title": title or "Role",
                "company": company or "Company",
                "duration": duration,
                "description": "",
            }

    if current:
        entries.append(current)

    return entries


def extract_structured_sections(resume_text: str) -> Dict[str, Any]:
    """Extract skills, work experience, and internships from resume text."""
    text = resume_text or ""

    exp_lines = _find_section_lines(
        text,
        ["experience", "work experience", "employment", "professional experience"],
    )
    intern_lines = _find_section_lines(
        text,
        ["internship", "internships", "intern experience"],
    )
    project_lines = _find_section_lines(
        text,
        ["projects", "personal projects", "academic projects", "side projects"],
    )
    skill_lines = _find_section_lines(
        text,
        ["skills", "technical skills", "core competencies", "technologies"],
    )

    experiences = _parse_bullet_entries(exp_lines)
    internships = _parse_bullet_entries(intern_lines)
    projects = _parse_bullet_entries(project_lines)

    # If no explicit internship section, tag short roles as internships
    if not internships:
        for exp in experiences:
            desc = (exp.get("description") or "").lower()
            title = (exp.get("title") or "").lower()
            if "intern" in title or "intern" in desc:
                internships.append(exp)
        experiences = [
            e for e in experiences if e not in internships
        ]

    skills: List[str] = []
    if skill_lines:
        skill_blob = " ".join(skill_lines)
        for part in re.split(r"[,;|•\n]", skill_blob):
            s = part.strip()
            if 2 < len(s) < 48:
                skills.append(s)
    else:
        # Pull from common tech keywords in full text
        from member_a.profile_extractor import SKILL_KEYWORDS

        lower = text.lower()
        for keyword, skill_name in SKILL_KEYWORDS.items():
            if keyword in lower and skill_name not in skills:
                skills.append(skill_name)

    return {
        "skills": skills[:20],
        "experiences": experiences[:10],
        "internships": internships[:10],
        "projects": projects[:10],
        "resume_text": text,
    }
