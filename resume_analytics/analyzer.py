"""Resume analytics facade (Task P2).

Previously this held a spaCy-based analyzer with the same class name as the
core ``utils.resume_analyzer.ResumeAnalyzer``. No code in the repo imports this
package (verified by grep), so it is now a thin compatibility facade that
delegates to the deep analysis core, ``utils.resume_analysis.analyze``.
"""

from utils.resume_analysis import AnalysisResult, analyze


class ResumeAnalyzer:
    """Compatibility facade delegating to the deep resume-analysis core."""

    def __init__(self, **kwargs):
        pass

    def analyze_resume(self, resume_bytes, options=None) -> AnalysisResult:
        return analyze(resume_bytes, options)
