"""
tests/test_mcp_server.py - Unit tests for VectorForge FastMCP server and top-level package.
"""

import unittest
import json
import vectorforge
from library.mcp_server import handle_rpc

class TestMCPServer(unittest.TestCase):
    def test_top_level_package_exports(self):
        self.assertEqual(vectorforge.__version__, "1.0.0")
        self.assertTrue(hasattr(vectorforge, "build_catalog_metadata"))
        self.assertTrue(hasattr(vectorforge, "apply_parameters"))

    def test_mcp_initialize(self):
        req = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {}
        }
        resp = handle_rpc(req)
        self.assertEqual(resp["id"], 1)
        self.assertIn("serverInfo", resp["result"])
        self.assertEqual(resp["result"]["serverInfo"]["name"], "vectorforge")

    def test_mcp_tools_list(self):
        req = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": {}
        }
        resp = handle_rpc(req)
        tools = resp["result"]["tools"]
        tool_names = [t["name"] for t in tools]
        self.assertIn("vectorforge_list_shapes", tool_names)
        self.assertIn("vectorforge_search_shapes", tool_names)
        self.assertIn("vectorforge_generate_shape", tool_names)

    def test_mcp_tools_call_search(self):
        req = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "vectorforge_search_shapes",
                "arguments": {"query": "raft"}
            }
        }
        resp = handle_rpc(req)
        content_text = resp["result"]["content"][0]["text"]
        data = json.loads(content_text)
        self.assertGreater(data["total_matches"], 0)
        self.assertTrue(any(m["id"] == "raft-consensus-cluster" for m in data["matches"]))

    def test_mcp_tools_call_generate(self):
        req = {
            "jsonrpc": "2.0",
            "id": 4,
            "method": "tools/call",
            "params": {
                "name": "vectorforge_generate_shape",
                "arguments": {
                    "preset_id": "raft-consensus-cluster",
                    "theme": "nord_frost",
                    "params": {"title": "Consensus Node Alpha"}
                }
            }
        }
        resp = handle_rpc(req)
        content_text = resp["result"]["content"][0]["text"]
        data = json.loads(content_text)
        self.assertIn("<svg", data["svg"])
        self.assertIn("Consensus Node Alpha", data["svg"])

if __name__ == "__main__":
    unittest.main()
