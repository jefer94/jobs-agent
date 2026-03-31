"""
sessions.py — Encrypted browser session cookie store.

Usage:
  python3 sessions.py init            # generate SESSION_KEY in .env if missing
  python3 sessions.py check           # verify key is present and valid
  python3 sessions.py encrypt-all     # (re-)encrypt every plain .sessions/*.json

Programmatic API (used by browsing-job-sites):
  from sessions import save_session, load_session, ensure_key

  ensure_key()                        # call once at startup
  save_session('linkedin', cookies)   # list[dict] → encrypted file
  cookies = load_session('linkedin')  # returns list[dict] or None if missing/expired
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

_ROOT = Path(__file__).parent
_SESSIONS_DIR = _ROOT / ".sessions"
_ENV_FILE = _ROOT / ".env"

# ---------------------------------------------------------------------------
# Key management
# ---------------------------------------------------------------------------

def _read_env() -> dict[str, str]:
    env: dict[str, str] = {}
    if _ENV_FILE.exists():
        for line in _ENV_FILE.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                env[k.strip()] = v.strip()
    return env


def _write_env(env: dict[str, str]) -> None:
    lines = []
    if _ENV_FILE.exists():
        # Preserve comments and ordering; replace known keys
        existing = _ENV_FILE.read_text().splitlines()
        written = set()
        for line in existing:
            stripped = line.strip()
            if stripped and not stripped.startswith("#") and "=" in stripped:
                k = stripped.split("=", 1)[0].strip()
                if k in env:
                    lines.append(f"{k}={env[k]}")
                    written.add(k)
                else:
                    lines.append(line)
            else:
                lines.append(line)
        for k, v in env.items():
            if k not in written:
                lines.append(f"{k}={v}")
    else:
        lines = [f"{k}={v}" for k, v in env.items()]
    _ENV_FILE.write_text("\n".join(lines) + "\n")


def _get_fernet():
    """Return a Fernet instance using SESSION_KEY from .env or environment."""
    try:
        from cryptography.fernet import Fernet
    except ImportError:
        print("ERROR: 'cryptography' not installed. Run: pip install cryptography", file=sys.stderr)
        sys.exit(1)

    env = _read_env()
    key = env.get("SESSION_KEY") or os.environ.get("SESSION_KEY")
    if not key:
        print("ERROR: SESSION_KEY not found in .env. Run: python3 sessions.py init", file=sys.stderr)
        sys.exit(1)
    return Fernet(key.encode())


def ensure_key() -> None:
    """Ensure SESSION_KEY exists in .env. Call once at startup."""
    env = _read_env()
    if env.get("SESSION_KEY") or os.environ.get("SESSION_KEY"):
        return
    _generate_key()


def _generate_key() -> None:
    from cryptography.fernet import Fernet
    key = Fernet.generate_key().decode()
    env = _read_env()
    env["SESSION_KEY"] = key
    _write_env(env)
    print(f"SESSION_KEY generated and saved to {_ENV_FILE}")


# ---------------------------------------------------------------------------
# Save / load
# ---------------------------------------------------------------------------

def save_session(portal: str, cookies: list[dict]) -> None:
    """Encrypt and save cookies list for the given portal."""
    _SESSIONS_DIR.mkdir(exist_ok=True)
    f = _get_fernet()
    plaintext = json.dumps(cookies).encode()
    ciphertext = f.encrypt(plaintext)
    (_SESSIONS_DIR / f"{portal}.enc").write_bytes(ciphertext)


def load_session(portal: str) -> list[dict] | None:
    """Decrypt and return cookies for portal, or None if file missing."""
    enc_file = _SESSIONS_DIR / f"{portal}.enc"
    if not enc_file.exists():
        return None
    try:
        f = _get_fernet()
        plaintext = f.decrypt(enc_file.read_bytes())
        return json.loads(plaintext)
    except Exception:
        return None


# ---------------------------------------------------------------------------
# CLI commands
# ---------------------------------------------------------------------------

def cmd_init() -> None:
    env = _read_env()
    if env.get("SESSION_KEY") or os.environ.get("SESSION_KEY"):
        print("SESSION_KEY already present in .env — no action needed.")
    else:
        _generate_key()


def cmd_check() -> None:
    env = _read_env()
    key = env.get("SESSION_KEY") or os.environ.get("SESSION_KEY")
    if not key:
        print("FAIL: SESSION_KEY not found in .env")
        sys.exit(1)
    try:
        from cryptography.fernet import Fernet
        Fernet(key.encode())
        print("OK: SESSION_KEY is present and valid.")
    except Exception as e:
        print(f"FAIL: SESSION_KEY is invalid — {e}")
        sys.exit(1)


def cmd_encrypt_all() -> None:
    """(Re-)encrypt any plain-JSON .sessions/*.json into .sessions/*.enc."""
    _SESSIONS_DIR.mkdir(exist_ok=True)
    plain_files = list(_SESSIONS_DIR.glob("*.json"))
    if not plain_files:
        print("No plain .sessions/*.json files found.")
        return
    for src in plain_files:
        portal = src.stem
        cookies = json.loads(src.read_text())
        save_session(portal, cookies)
        src.unlink()
        print(f"  {portal}: encrypted → .sessions/{portal}.enc (plain file removed)")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "check"
    if cmd == "init":
        cmd_init()
    elif cmd == "check":
        cmd_check()
    elif cmd == "encrypt-all":
        cmd_encrypt_all()
    else:
        print(f"Unknown command: {cmd}. Use: init | check | encrypt-all")
        sys.exit(1)
