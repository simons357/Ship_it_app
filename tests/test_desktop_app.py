#!/usr/bin/env python3
"""The Domain Architect desktop app must be openable from this repo."""

from __future__ import annotations

import socket
import subprocess
import tempfile
import time
import unittest
import urllib.request
from pathlib import Path

from domain_architect.app import install_desktop_shortcut


REPO = Path(__file__).resolve().parents[1]
LAUNCHER = REPO / "Open Domain Architect.command"


def _free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


class TestLauncherFile(unittest.TestCase):
    def test_repo_launcher_exists(self):
        self.assertTrue(LAUNCHER.is_file(), f"missing {LAUNCHER}")
        text = LAUNCHER.read_text(encoding="utf-8")
        self.assertIn("domain_architect app", text)
        self.assertTrue(LAUNCHER.stat().st_mode & 0o111)

    def test_shortcut_installer_writes_command_or_desktop(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = install_desktop_shortcut(Path(tmp))
            self.assertTrue(path.is_file())
            body = path.read_text(encoding="utf-8")
            self.assertIn("domain_architect app", body)


class TestLauncherStartsApp(unittest.TestCase):
    def test_command_serves_the_app(self):
        port = _free_port()
        proc = subprocess.Popen(
            ["bash", str(LAUNCHER), "--no-browser", "--port", str(port)],
            cwd=str(REPO),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        try:
            url = f"http://127.0.0.1:{port}/"
            last_error = None
            for _ in range(40):
                try:
                    with urllib.request.urlopen(url, timeout=1) as response:
                        html = response.read().decode("utf-8")
                    self.assertEqual(response.status, 200)
                    self.assertIn("Domain Architect", html)
                    self.assertIn("Swirl identity", html)
                    return
                except OSError as exc:
                    last_error = exc
                    if proc.poll() is not None:
                        out, err = proc.communicate()
                        self.fail(
                            f"launcher exited {proc.returncode}\nstdout:\n{out}\nstderr:\n{err}"
                        )
                    time.sleep(0.1)
            self.fail(f"app did not serve {url}: {last_error}")
        finally:
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()
                proc.wait(timeout=5)


if __name__ == "__main__":
    raise SystemExit(unittest.main())
