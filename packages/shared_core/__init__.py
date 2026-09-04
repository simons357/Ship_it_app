"""Prime Field platform spine — shared kernel v0."""

from packages.shared_core.config import load_registry, load_spell_registry
from packages.shared_core.link_resolver import link_status, resolve_url
from packages.shared_core.spell_runner import list_spells, run_spell

__all__ = [
    "load_registry",
    "load_spell_registry",
    "resolve_url",
    "link_status",
    "list_spells",
    "run_spell",
]
