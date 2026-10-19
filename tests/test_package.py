import importlib.util
import json
from pathlib import Path
import re
import tarfile
import tempfile
import tomllib
import unittest
from urllib.parse import urlsplit, parse_qs

ROOT = Path(__file__).resolve().parents[1]

class ExtensionContractTests(unittest.TestCase):
    def setUp(self):
        self.manifest = json.loads((ROOT / "gemini-extension.json").read_text())

    def test_credential_is_native_sensitive_and_only_sent_to_suno(self):
        settings = self.manifest["settings"]
        self.assertEqual(len(settings), 1)
        self.assertTrue(settings[0]["sensitive"])
        self.assertEqual(settings[0]["envVar"], "ACEDATACLOUD_SUNO_TOKEN")
        servers = self.manifest["mcpServers"]
        self.assertEqual(list(servers), ["suno-by-ace-data-cloud"])
        server = servers["suno-by-ace-data-cloud"]
        self.assertEqual(server["httpUrl"], "https://suno.mcp.acedata.cloud/mcp")
        self.assertEqual(server["headers"], {"Authorization": "Bearer ${ACEDATACLOUD_SUNO_TOKEN}"})
        self.assertNotIn("trust", server)
        self.assertNotIn("hooks", self.manifest)
        self.assertNotIn("command", server)

    def test_tools_are_focused_and_cover_both_generation_and_query(self):
        tools = self.manifest["mcpServers"]["suno-by-ace-data-cloud"]["includeTools"]
        self.assertEqual(len(tools), len(set(tools)))
        self.assertIn("suno_generate_music", tools)
        self.assertIn("suno_get_task", tools)
        self.assertIn("suno_list_models", tools)
        self.assertFalse(any(word in t for t in tools for word in ("delete", "upload", "voice", "train", "archive")))

    def test_commands_parse_and_keep_task_argument_as_data(self):
        commands = {p.stem: tomllib.loads(p.read_text()) for p in (ROOT / "commands").glob("*.toml")}
        self.assertEqual(set(commands), {"suno-check", "suno-task"})
        self.assertIn("{{args}}", commands["suno-task"]["prompt"])
        self.assertNotIn("!{", str(commands))
        self.assertIn("suno_list_models", commands["suno-check"]["prompt"])

    def test_package_is_self_contained_with_manifest_at_root(self):
        spec = importlib.util.spec_from_file_location("package_extension", ROOT / "scripts/package_extension.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as folder:
            output = module.build(Path(folder) / "suno.tar.gz")
            with tarfile.open(output) as archive:
                names = archive.getnames()
                self.assertIn("gemini-extension.json", names)
                self.assertIn("skills/suno-music/SKILL.md", names)
                self.assertIn("VALIDATION.md", names)
                self.assertTrue(all(not name.startswith("/") and ".." not in Path(name).parts for name in names))
                self.assertFalse(any(".env" in Path(name).parts or ".git" in Path(name).parts for name in names))
                for member in archive.getmembers():
                    self.assertFalse(member.issym() or member.islnk())

    def test_readme_local_links_exist_and_acquisition_links_have_four_utm_fields(self):
        for document in (ROOT / "README.md", ROOT / "readme/README_zh_Hans.md"):
            text = document.read_text()
            for target in re.findall(r"\]\(([^)]+)\)", text):
                if target.startswith("https://platform.acedata.cloud"):
                    query = parse_qs(urlsplit(target).query)
                    self.assertTrue({"utm_source", "utm_medium", "utm_campaign", "utm_content"} <= query.keys(), target)
                    self.assertEqual(query["utm_source"], ["gemini-cli"])
                elif not urlsplit(target).scheme and not target.startswith("#"):
                    self.assertTrue((document.parent / target.split("#", 1)[0]).is_file(), target)

if __name__ == "__main__":
    unittest.main()
