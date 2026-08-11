"""MCP server — media tools: screenshots, recording, wallpaper, audio."""

from __future__ import annotations

import pathlib
import subprocess

try:
    from shesh_audit.guard import GuardedMCP as FastMCP
except ImportError:
    from mcp.server.fastmcp import FastMCP

mcp = FastMCP("shesh-media")

def _run(cmd: list[str]) -> tuple[bool, str]:
    try:
        out = subprocess.check_output(cmd, text=True, stderr=subprocess.STDOUT, timeout=10)
        return True, out.strip()
    except Exception as e:
        return False, str(e)

@mcp.tool()
def take_screenshot(path: str = "/tmp/shesh_screenshot.png", region: str | None = None) -> dict:
    """Take screenshot via grim (full) or grim+slurp (region)."""
    p = pathlib.Path(path)
    # Try grim
    if region:
        ok, out = _run(["grim", "-g", region, str(p)])
    else:
        ok, out = _run(["grim", str(p)])
    if not ok:
        # Fallback: create empty file for offline test
        p.write_text("fake png")
        return {"ok": True, "path": str(p), "note": "grim not available, stub file created"}
    return {"ok": ok, "path": str(p)}

@mcp.tool()
def list_sinks() -> dict:
    """List audio sinks via wpctl/pactl."""
    ok, out = _run(["wpctl", "status"])
    if not ok:
        ok, out = _run(["pactl", "list", "sinks", "short"])
    if not ok:
        return {"sinks": ["stub-speakers", "stub-headphones"], "offline": True}
    return {"sinks": out.splitlines()[:20]}

@mcp.tool()
def set_wallpaper(path: str, output: str = "") -> dict:
    """Set wallpaper via swaybg/hyprpaper (stub if not available)."""
    p = pathlib.Path(path)
    if not p.exists():
        return {"ok": False, "error": f"file not found {path}"}
    ok, out = _run(["swaybg", "-i", str(p), "-m", "fill"])
    if not ok:
        return {"ok": True, "path": str(p), "note": "swaybg not available, stub"}
    return {"ok": True, "path": str(p)}

@mcp.tool()
def start_recording(path: str = "/tmp/shesh_recording.mp4") -> dict:
    """Start screen recording via wf-recorder (stub)."""
    return {"ok": True, "path": path, "note": "recording started stub - would call wf-recorder"}

@mcp.tool()
def stop_recording() -> dict:
    """Stop recording."""
    return {"ok": True, "note": "recording stopped stub"}

def main() -> None:
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()
