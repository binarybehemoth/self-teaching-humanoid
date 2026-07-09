"""
platform/studio.py  —  The Teaching Studio
==========================================

Where a person teaches a robot. A teaching contribution carries what was
taught, by whom, and on what — with consent and provenance. This illustrates the
interface; the studio is a front-end surface backed by the training service.
"""
from __future__ import annotations
import time


def make_contribution(teacher: str, skill: str, modality: str,
                      consent: str = "training-only") -> dict:
    """Build a teaching-contribution record (see schemas/teaching_contribution.json)."""
    return {
        "schema_version": "1.0",
        "record": "teaching_contribution",
        "teacher": teacher,
        "skill": skill,
        "modality": modality,        # demonstration | correction | teleoperation | feedback
        "consent": consent,          # travels with the data as provenance
        "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
