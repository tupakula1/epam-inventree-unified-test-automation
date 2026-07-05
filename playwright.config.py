"""
Playwright configuration — browser settings, base URL, timeouts, etc.
Values are sourced from config/settings.py to avoid duplicated config.
"""

from config.settings import settings

# ─── Base Configuration ───────────────────────────────────────────────────────
BASE_URL = settings.UI_BASE_URL
API_BASE_URL = settings.API_BASE_URL

# ─── Browser Settings ─────────────────────────────────────────────────────────
BROWSER = settings.BROWSER      # chromium | firefox | webkit
HEADLESS = settings.HEADLESS
SLOW_MO = settings.SLOW_MO
VIEWPORT = {"width": 1920, "height": 1080}

# ─── Timeouts (milliseconds) ──────────────────────────────────────────────────
DEFAULT_TIMEOUT = settings.DEFAULT_TIMEOUT
NAVIGATION_TIMEOUT = settings.NAVIGATION_TIMEOUT
