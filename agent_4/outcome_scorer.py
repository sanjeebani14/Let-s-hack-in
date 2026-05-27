"""
Outcome Clarity Scorer

Evaluates the presence of numeric metrics or concrete parameters in project outcomes.
Distinguishes vague claims ("improved performance") from measurable proofs ("reduced load time by 40%").
Yields an explicit numerical clarity score per project.
"""

import re
from pydantic import BaseModel, Field
from typing import List, Tuple, Optional


class OutcomeMeasure(BaseModel):
    """A single measurable outcome with metric."""
    metric_type: str = Field(
        ...,
        description="Type of metric: 'percentage', 'count', 'time', 'ratio', 'other'",
        examples=["percentage", "count", "time", "ratio"]
    )
    value: str = Field(
        ...,
        description="The numerical value found",
        examples=["40", "50k", "80ms", "2x"]
    )
    unit: str = Field(
        ...,
        description="Unit of measurement",
        examples=["percent", "users", "milliseconds", "times faster"]
    )
    full_statement: str = Field(
        ...,
        description="Complete statement including the metric"
    )


class OutcomeClarityScore(BaseModel):
    """Detailed clarity analysis of project outcomes."""
    clarity_score: float = Field(
        ...,
        description="Overall clarity score (0-1): 0=completely vague, 1=highly specific",
        ge=0.0,
        le=1.0
    )
    is_vague: bool = Field(
        ...,
        description="True if outcome claims are mostly unmeasurable"
    )
    is_specific: bool = Field(
        ...,
        description="True if outcome contains concrete metrics"
    )
    measures_found: List[OutcomeMeasure] = Field(
        default_factory=list,
        description="List of identified metrics/measurements"
    )
    vague_claims: List[str] = Field(
        default_factory=list,
        description="Unmeasurable claims identified"
    )
    summary: str = Field(
        ...,
        description="One-line assessment of outcome clarity"
    )


# Patterns for finding numeric metrics
METRIC_PATTERNS = [
    (r"(\d+)\s*%|percent", "percentage"),
    (r"(\d+(?:k|m|b)?)\s*(?:users|customers|downloads|items|people)", "count"),
    (r"(\d+)\s*(?:ms|milliseconds|seconds?|minutes?|hours?)", "time"),
    (r"(\d+(?:\.\d+)?)\s*x\s*(?:faster|slower|improvement)", "ratio"),
    (r"improved|increased|reduced|decreased\s+(?:by\s+)?(\d+)%", "percentage"),
    (r"(\d+)\s*(?:operations|requests|queries|transactions)\s*(?:per|/)", "throughput"),
    (r"(\d+)-fold|(\d+)x", "multiplier"),
    (r"\$(\d+(?:k|m|b)?)", "financial"),
]

# Vague outcome phrases that lack specificity
VAGUE_PHRASES = [
    "improved performance", "better user experience", "faster", "more efficient",
    "enhanced functionality", "better code quality", "easier to use",
    "streamlined process", "optimized", "reduced complexity", "cleaner",
    "more scalable", "better architecture", "helped with", "contributed to",
    "was involved in improving", "worked on making", "assisted in", "helped make",
    "better", "nicer", "cooler", "smoother", "faster execution", "good results"
]


def extract_metrics(text: str) -> List[Tuple[str, str, str]]:
    """
    Extract numeric metrics from outcome text.
    
    Args:
        text: Outcome description text
        
    Returns:
        List of (metric_type, value, unit) tuples
    """
    found_metrics = []
    
    for pattern, metric_type in METRIC_PATTERNS:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            # Get the first capturing group, or use the full match if no groups
            if match.groups():
                value = match.group(1) if match.group(1) else match.group(0)
            else:
                value = match.group(0)
            
            if value:  # Only add if we have a value
                found_metrics.append((metric_type, value, text[match.start():match.end()]))
    
    return found_metrics


def extract_vague_claims(text: str) -> List[str]:
    """
    Identify unmeasurable/vague claims in text.
    
    Args:
        text: Outcome description text
        
    Returns:
        List of vague phrases found
    """
    vague_found = []
    lower_text = text.lower()
    
    for phrase in VAGUE_PHRASES:
        if phrase in lower_text:
            # Extract surrounding context
            idx = lower_text.find(phrase)
            start = max(0, idx - 20)
            end = min(len(text), idx + len(phrase) + 30)
            context = text[start:end].strip()
            vague_found.append(context)
    
    return vague_found


def score_outcome_clarity(outcome_text: str) -> OutcomeClarityScore:
    """
    Evaluate clarity and specificity of project outcome claims.
    
    Distinguishes concrete, measurable claims from vague statements.
    Returns comprehensive clarity metrics.
    
    Args:
        outcome_text: Raw outcome/results statement
        
    Returns:
        OutcomeClarityScore: Detailed clarity analysis
    """
    
    # Extract metrics
    raw_metrics = extract_metrics(outcome_text)
    measures_found: List[OutcomeMeasure] = []
    
    for metric_type, value, full_stmt in raw_metrics:
        unit_map = {
            "percentage": "%",
            "count": "units/people",
            "time": "time units",
            "ratio": "multiplier",
            "throughput": "operations",
            "multiplier": "x",
            "financial": "currency"
        }
        measures_found.append(OutcomeMeasure(
            metric_type=metric_type,
            value=value,
            unit=unit_map.get(metric_type, metric_type),
            full_statement=full_stmt
        ))
    
    # Extract vague claims
    vague_claims = extract_vague_claims(outcome_text)
    
    # Calculate clarity score
    outcome_length = len(outcome_text.split())
    
    # Base score from metrics presence
    if len(measures_found) >= 3:
        clarity_score = 0.95
    elif len(measures_found) == 2:
        clarity_score = 0.85
    elif len(measures_found) == 1:
        clarity_score = 0.70
    else:
        clarity_score = 0.40
    
    # Adjust for vague language
    if len(vague_claims) > 2:
        clarity_score *= 0.7
    elif len(vague_claims) == 2:
        clarity_score *= 0.85
    elif len(vague_claims) == 1:
        clarity_score *= 0.92
    
    # Check for absolute terms (all, every, definitely, always)
    if any(term in outcome_text.lower() for term in ["all", "every", "always", "definitely"]):
        clarity_score = min(0.95, clarity_score + 0.05)
    
    is_vague = clarity_score < 0.55
    is_specific = clarity_score >= 0.75
    
    # Generate summary
    if is_specific:
        summary = f"Clear & measurable: {len(measures_found)} metrics identified"
    elif clarity_score >= 0.55:
        summary = "Partially clear: some metrics but also vague language"
    else:
        summary = f"Vague: {len(vague_claims)} unquantified claims"
    
    return OutcomeClarityScore(
        clarity_score=min(1.0, clarity_score),
        is_vague=is_vague,
        is_specific=is_specific,
        measures_found=measures_found,
        vague_claims=vague_claims,
        summary=summary
    )
