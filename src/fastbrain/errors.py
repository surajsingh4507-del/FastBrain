"""Exceptions raised by FastBrain."""

from __future__ import annotations

__all__ = ["ConfigurationError", "FastBrainError"]


class FastBrainError(Exception):
    """Base class for FastBrain errors."""


class ConfigurationError(FastBrainError, ValueError):
    """The engine or a provider was set up in a way that cannot work."""
