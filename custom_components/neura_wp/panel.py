"""HTML for the Neura sidebar panel inside Home Assistant."""
from __future__ import annotations

from pathlib import Path

PANEL_FILE = Path(__file__).resolve().parent / "www" / "index.html"
HA_BOOT = (
    '<script>window.NEURA_API_BASE="/api/neura_wp";window.NEURA_HA=true;</script>\n'
)


def panel_html(source: str | None = None) -> str:
    """Serve the same page as the standalone server, with HA API paths injected."""
    text = source if source is not None else PANEL_FILE.read_text(encoding="utf-8")
    if "window.NEURA_API_BASE=\"/api/neura_wp\"" in text:
        return text
    return text.replace("<head>", "<head>\n  " + HA_BOOT, 1)
