"""
tests/test_visitor_security.py - Unit tests for Visitor Ledger sanitization and 24-hour rate limiting.
"""

import unittest
from datetime import datetime, timezone, timedelta
from scripts.visitor_terminal_action import sanitize, check_rate_limit

class TestVisitorSecurity(unittest.TestCase):
    def test_sanitize_html_and_scripts(self):
        malicious = '<script>alert("pwned")</script>Hello <b>World</b>'
        clean = sanitize(malicious)
        self.assertNotIn("<script>", clean)
        self.assertNotIn("<b>", clean)
        self.assertIn("Hello World", clean)

    def test_sanitize_urls(self):
        text_with_url = 'Check out https://evil-phishing.com/test for free coins'
        clean = sanitize(text_with_url)
        self.assertNotIn("https://", clean)
        self.assertNotIn("evil-phishing.com", clean)

    def test_sanitize_length(self):
        long_text = "A" * 200
        clean = sanitize(long_text, max_len=45)
        self.assertEqual(len(clean), 45)

    def test_rate_limit_blocks_within_24h(self):
        recent_entry = {
            "username": "spammer",
            "timestamp": (datetime.now(timezone.utc) - timedelta(hours=2)).isoformat()[:19] + "Z",
            "command": "ping",
            "message": "ping"
        }
        visitors = [recent_entry]
        self.assertTrue(check_rate_limit("spammer", visitors))

    def test_rate_limit_allows_after_24h(self):
        old_entry = {
            "username": "good_citizen",
            "timestamp": (datetime.now(timezone.utc) - timedelta(hours=25)).isoformat()[:19] + "Z",
            "command": "ping",
            "message": "ping"
        }
        visitors = [old_entry]
        self.assertFalse(check_rate_limit("good_citizen", visitors))

if __name__ == "__main__":
    unittest.main()
