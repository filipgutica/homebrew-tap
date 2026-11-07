import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import textwrap
import unittest
from unittest.mock import patch


REPOSITORY = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("update_formulae", REPOSITORY / "scripts/update-formulae.py")
updater = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(updater)


def release(tag, **fields):
    return {"tag_name": tag, "draft": False, "prerelease": False, **fields}


class FormulaUpdates(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        (self.root / "Formula").mkdir()
        shutil.copytree(REPOSITORY / "scripts/templates", self.root / "scripts/templates")
        root_patch = patch.object(updater, "ROOT", self.root)
        self.addCleanup(root_patch.stop)
        root_patch.start()

    def test_cli_release_lookup_skips_plugins_and_unstable_releases_across_pages(self):
        pages = [
            [release("v4.1.0")] * 100,
            [release("cli-v0.3.0", draft=True), release("cli-v0.2.0", prerelease=True), release("cli-v0.1.0")],
        ]
        with patch.object(updater, "urlopen", side_effect=[io.BytesIO(json.dumps(page).encode()) for page in pages]) as request:
            self.assertEqual(updater.latest_release("filip-stack")["tag_name"], "cli-v0.1.0")
        self.assertIn("page=2", request.call_args.args[0].full_url)
        self.assertNotIn("/releases/latest", request.call_args.args[0].full_url)

    def test_no_cli_release_leaves_formula_absent(self):
        with patch.object(updater, "urlopen", return_value=io.BytesIO(json.dumps([release("v4.1.0")]).encode())):
            updater.update_formula("filip-stack")
        self.assertFalse((self.root / "Formula/filip-stack.rb").exists())

    def test_first_cli_release_creates_checksummed_formula_and_repeated_run_is_idempotent(self):
        archive = b"published CLI source archive"
        with patch.object(updater, "latest_release", return_value=release("cli-v0.1.0")), \
             patch.object(updater, "urlopen", return_value=io.BytesIO(archive)) as download:
            updater.update_formula("filip-stack")
            formula = (self.root / "Formula/filip-stack.rb").read_text()
            self.assertIn("/archive/refs/tags/cli-v0.1.0.tar.gz", formula)
            self.assertIn(hashlib.sha256(archive).hexdigest(), formula)
            self.assertNotIn("RELEASE_", formula)
            updater.update_formula("filip-stack")
            self.assertEqual(download.call_count, 1)
            self.assertEqual((self.root / "Formula/filip-stack.rb").read_text(), formula)

    def test_cli_upgrades_use_cli_version_and_never_downgrade(self):
        formula = self.root / "Formula/filip-stack.rb"
        template = (self.root / "scripts/templates/filip-stack.rb").read_text()
        formula.write_text(template.replace("RELEASE_URL", "https://github.com/filipgutica/filip-stack/archive/refs/tags/cli-v0.1.0.tar.gz"))
        with patch.object(updater, "latest_release", return_value=release("cli-v0.2.0")), \
             patch.object(updater, "urlopen", return_value=io.BytesIO(b"new release")):
            updater.update_formula("filip-stack")
        upgraded = formula.read_text()
        self.assertIn("cli-v0.2.0.tar.gz", upgraded)
        with patch.object(updater, "latest_release", return_value=release("cli-v0.1.0")), \
             patch.object(updater, "urlopen") as download:
            updater.update_formula("filip-stack")
            download.assert_not_called()
        self.assertEqual(formula.read_text(), upgraded)

    def test_existing_tools_keep_their_unprefixed_release_contract(self):
        formula = self.root / "Formula/wtree.rb"
        shutil.copyfile(REPOSITORY / "Formula/wtree.rb", formula)
        with patch.object(updater, "latest_release", return_value=release("v99.0.0")), \
             patch.object(updater, "urlopen", return_value=io.BytesIO(b"wtree release")):
            updater.update_formula("wtree")
        self.assertIn("/wtree/archive/refs/tags/v99.0.0.tar.gz", formula.read_text())

    def test_workflow_opens_pr_when_the_only_change_is_the_first_formula(self):
        project = self.root / "project"
        project.mkdir()
        (project / "Formula").mkdir()
        (project / "scripts").mkdir()
        (project / "Formula/wtree.rb").write_text("existing formula\n")
        (project / "scripts/update-formulae.py").write_text(
            'from pathlib import Path\nPath("Formula/filip-stack.rb").write_text("first formula\\n")\n'
        )
        remote = self.root / "remote.git"
        subprocess.run(["git", "init", "--bare", str(remote)], check=True, capture_output=True)

        def git(*args):
            return subprocess.run(["git", *args], cwd=project, check=True, capture_output=True, text=True)

        git("init", "-b", "main")
        git("config", "user.name", "Test")
        git("config", "user.email", "test@example.com")
        git("add", ".")
        git("commit", "-m", "initial")
        git("remote", "add", "origin", str(remote))
        git("push", "-u", "origin", "main")
        fake_bin = self.root / "bin"
        fake_bin.mkdir()
        gh = fake_bin / "gh"
        log = self.root / "created-pr"
        gh.write_text('#!/bin/sh\nif [ "$1 $2" = "pr create" ]; then touch "$GH_TEST_LOG"; fi\n')
        gh.chmod(0o755)
        workflow = (REPOSITORY / ".github/workflows/update-formulae.yml").read_text()
        shell = textwrap.dedent(workflow.split("        run: |\n", 1)[1])
        subprocess.run(
            ["bash", "-e", "-c", shell], cwd=project, check=True, capture_output=True,
            env={**os.environ, "PATH": f"{fake_bin}:{os.environ['PATH']}", "GH_TEST_LOG": str(log)},
        )
        self.assertTrue(log.exists(), "the workflow exited before opening the first formula PR")
        published = git("--git-dir", str(remote), "show", "refs/heads/chore/update-formulae:Formula/filip-stack.rb")
        self.assertEqual(published.stdout, "first formula\n")


if __name__ == "__main__":
    unittest.main()
