"""Dependency-free self-check for utils/resume_analysis.py (Task P2).

Run:  python -I test_resume_analysis.py

It shims the ``utils`` package in sys.modules so importing the deep module does
not execute utils/__init__.py (which pulls streamlit / genai / db deps). Only
pure parts of ``analyze`` are exercised -- no network, no AI.
"""

import os
import sys
import types

REPO = os.path.dirname(os.path.abspath(__file__))

# Shim the `utils` package: avoid executing utils/__init__.py's heavy imports.
_utils = types.ModuleType("utils")
_utils.__path__ = [os.path.join(REPO, "utils")]
sys.modules["utils"] = _utils

from utils.resume_analysis import AnalysisResult, analyze  # noqa: E402


def main():
    resume_text = (
        "Alice Smith\n"
        "alice@example.com | +1 123-456-7890 | linkedin.com/in/alice\n"
        "Summary: Software engineer with 5 years of experience.\n"
        "Education:\nBachelor of Technology, Computer Science, 2019\n"
        "Experience:\nSoftware Engineer at Acme, 2020-2024\n"
        "  - Developed core features in Python\n"
        "Skills:\nPython, SQL, Docker, Kubernetes\n"
        "Projects:\nBuilt a resume analyzer\n"
    )
    raw = resume_text.encode("utf-8")

    result = analyze(raw, {"required_skills": ["Python", "SQL", "Docker", "Kubernetes", "AWS"]})

    assert isinstance(result, AnalysisResult)
    # Attribute + dict access agree with the backing data
    assert result["ats_score"] == result.ats_score == result.data["ats_score"]
    assert result.get("document_type") == "resume"
    assert "ats_score" in result
    assert len(list(result.items())) == len(result.data)

    kw = result.keyword_match
    assert set(kw["found_skills"]) >= {"Python", "SQL"}
    assert "AWS" in kw["missing_skills"]

    assert result.personal_info["email"] == "alice@example.com"
    assert result["raw_text"] == resume_text
    assert result.education and result.experience and result.skills

    # options["text"] shortcut path (uses pre-extracted text, no format detection)
    opts = {"required_skills": ["Python", "SQL", "Docker", "Kubernetes", "AWS"]}
    result2 = analyze(b"", {"text": resume_text, **opts})
    assert result2.ats_score == result.ats_score
    assert result2.keyword_match["score"] == result.keyword_match["score"]

    print("SELF-CHECK PASSED: ats=%d keyword=%d%% found=%s"
          % (result.ats_score, kw["score"], kw["found_skills"]))


if __name__ == "__main__":
    main()
