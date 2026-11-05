"""Deep resume-analysis core (Task P2).

Single coalesced entry point, ``analyze``, turns raw resume file bytes (or
already-extracted text via ``options["text"]``) into a structured
:class:`AnalysisResult`. Pure logic lives here and in the parsing/scoring core
``utils.resume_analyzer``; the optional AI portion routes through
``utils.ai_resume_analyzer.AIResumeAnalyzer.analyze_resume_with_gemini``.

This module intentionally never imports streamlit.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


# ---------------------------------------------------------------- result ---


@dataclass
class AnalysisResult:
    """Summary of a single resume analysis.

    The wrapped ``data`` dict mirrors the historical shape produced by
    ``utils.resume_analyzer.ResumeAnalyzer.analyze_resume`` so existing UI
    rendering (which indexes like ``analysis["ats_score"]``) keeps working,
    while the named properties expose the summarized view described by P2.
    """

    data: Dict[str, Any] = field(default_factory=dict)

    # -- dict-style access (keeps existing render call sites working) ----
    def __getitem__(self, key: str) -> Any:
        return self.data[key]

    def __contains__(self, key: str) -> bool:
        return key in self.data

    def get(self, key: str, default: Any = None) -> Any:
        return self.data.get(key, default)

    def keys(self):
        return self.data.keys()

    def values(self):
        return self.data.values()

    def items(self):
        return self.data.items()

    def __iter__(self):
        return iter(self.data)

    def __len__(self) -> int:
        return len(self.data)

    # -- summarized view --------------------------------------------------
    @property
    def personal_info(self) -> Dict[str, Any]:
        return {
            k: self.data.get(k)
            for k in ("name", "email", "phone", "linkedin", "github", "portfolio")
        }

    @property
    def education(self):
        return self.data.get("education", [])

    @property
    def experience(self):
        return self.data.get("experience", [])

    @property
    def projects(self):
        return self.data.get("projects", [])

    @property
    def skills(self):
        return self.data.get("skills", [])

    @property
    def keyword_match(self) -> Dict[str, Any]:
        return self.data.get("keyword_match", {})

    @property
    def section_score(self) -> int:
        return self.data.get("section_score", 0)

    @property
    def format_score(self) -> int:
        return self.data.get("format_score", 0)

    @property
    def ats_score(self) -> int:
        return self.data.get("ats_score", 0)

    @property
    def ai_analysis(self) -> Optional[Dict[str, Any]]:
        return self.data.get("ai_analysis")


# -------------------------------------------------------------- analyze ----


def analyze(bytes_: bytes, options: Optional[dict] = None) -> AnalysisResult:
    """Analyze raw resume file bytes.

    ``options`` may carry hints:
      - ``text``: pre-extracted resume text (avoids re-parsing the bytes).
      - ``filename`` / ``file_type``: help format detection for the bytes.
      - ``job_description`` / ``job_role``: forwarded to the AI analyzer.
      - ``required_skills`` / ``require_gpa``: drive core keyword/section scoring.
      - ``use_ai``: if truthy, also run the Gemini-based AI analysis.
    """
    options = options or {}

    text = _obtain_text(bytes_, options)
    result = _core_analysis(text, options)
    result["raw_text"] = text  # handy for callers that persist the text

    if options.get("use_ai"):
        ai = _ai_analysis(text, options)
        if ai is not None:
            result["ai_analysis"] = ai

    return AnalysisResult(data=result)


# ------------------------------------------------------------ internals ----


def _obtain_text(bytes_: bytes, options: dict) -> str:
    text = options.get("text")
    if text is not None:
        return text if isinstance(text, str) else text.decode("utf-8", errors="replace")
    return _extract_from_bytes(bytes_, options)


def _extract_from_bytes(bytes_: bytes, options: dict) -> str:
    fmt = options.get("file_type") or _detect_format(bytes_, options.get("filename"))
    if fmt == "pdf":
        return _core().extract_text_from_pdf(bytes_)
    if fmt == "docx":
        return _core().extract_text_from_docx(bytes_)
    return bytes_.decode("utf-8", errors="replace")


def _detect_format(bytes_: bytes, filename: Optional[str]) -> str:
    name = (filename or "").lower()
    if name.endswith(".pdf") or bytes_[:5] == b"%PDF-":
        return "pdf"
    if name.endswith((".docx", ".doc")) or bytes_[:2] == b"PK":
        return "docx"
    return "txt"


def _core_analysis(text: str, options: dict) -> Dict[str, Any]:
    job_reqs = {
        "required_skills": list((options.get("required_skills") or [])),
        "require_gpa": bool(options.get("require_gpa", False)),
    }
    return _core().analyze_resume({"raw_text": text}, job_reqs)


def _ai_analysis(text: str, options: dict) -> Optional[Dict[str, Any]]:
    try:
        from utils.ai_resume_analyzer import AIResumeAnalyzer

        analyzer = AIResumeAnalyzer()
        return analyzer.analyze_resume_with_gemini(
            text,
            job_description=options.get("job_description"),
            job_role=options.get("job_role"),
        )
    except Exception:
        return None


def _core():
    from utils.resume_analyzer import ResumeAnalyzer

    return ResumeAnalyzer()
