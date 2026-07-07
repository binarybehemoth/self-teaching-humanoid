"""
backend/services/registry.py  —  Model Registry
===============================================

The versioned store of skills and models — the source of truth for what a skill is
and how well it works (Parts XV–XVII). A thin wrapper here over the in-memory marketplace.
"""
from __future__ import annotations


class ModelRegistry:
    def __init__(self):
        self._versions: dict[str, list[str]] = {}

    def register(self, name: str, version: str) -> None:
        self._versions.setdefault(name, []).append(version)

    def versions(self, name: str) -> list[str]:
        return self._versions.get(name, [])
