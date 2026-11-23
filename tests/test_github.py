from pathlib import Path
import runpy
import subprocess
import unittest
from unittest.mock import patch

module = runpy.run_path(str(Path(__file__).resolve().parents[1] / "bin/arche-waybar-github"))


class GithubNotifications(unittest.TestCase):
    def status(self, code, stdout="", stderr=""):
        with patch("subprocess.run", return_value=subprocess.CompletedProcess([], code, stdout, stderr)):
            return module["current_status"]()

    def test_empty_inbox(self):
        self.assertEqual(self.status(0, "[[]]"), {"text": ""})

    def test_missing_login_and_network_failure(self):
        self.assertEqual(self.status(1, stderr="please run: gh auth login")["class"], "auth-required")
        self.assertEqual(self.status(1, stderr="HTTP 401")["class"], "auth-required")
        self.assertEqual(self.status(1, stderr="connection refused")["class"], "unavailable")

    def test_paginated_unread_notifications(self):
        def thread(kind, title):
            return {"unread": True, "reason": "review_requested",
                    "repository": {"full_name": "example/project"}, "subject": {"type": kind, "title": title}}
        result = module["notification_status"]([[thread("PullRequest", "Review <this>")], [thread("Issue", "Fix")]])
        self.assertEqual(result["text"], "PR 1 · Issues 1")
        self.assertIn("Review &lt;this&gt;", result["tooltip"])


if __name__ == "__main__":
    unittest.main()
