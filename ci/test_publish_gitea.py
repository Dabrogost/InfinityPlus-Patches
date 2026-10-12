import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch
from urllib.error import HTTPError

from publish_gitea import Gitea, publish


class PublishTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.bundle = Path(self.temp.name) / "bundle.mpp"
        self.bundle.write_bytes(b"test-bundle")
        self.metadata = Path(self.temp.name) / "patches-bundle.json"
        self.release = {"id": 7, "draft": True, "created_at": "2026-10-12T23:00:00Z"}
        self.asset = {"id": 8, "name": "patches-0.1.2.mpp", "size": len(b"test-bundle"),
                      "browser_download_url": "https://gitea.com/attachments/actual-asset-id"}
        self.api = Mock()

    def run_publish(self):
        publish(self.api, "0.1.2", "a" * 40, self.bundle, self.metadata)

    def test_new_release_uses_draft_upload_then_publish_and_api_download_url(self):
        self.api.request.side_effect = [None, self.release, [], {**self.release, "draft": False}]
        self.api.upload.return_value = self.asset
        self.run_publish()
        calls = self.api.request.call_args_list
        self.assertTrue(calls[1].args[2]["draft"])
        self.assertEqual(calls[1].args[2]["target_commitish"], "a" * 40)
        self.assertEqual(calls[-1].args, ("PATCH", "/releases/7", {"draft": False}))
        self.assertEqual(json.loads(self.metadata.read_text())["download_url"], self.asset["browser_download_url"])

    def test_matching_existing_asset_is_reused(self):
        self.api.request.side_effect = [{**self.release, "draft": False}, [self.asset]]
        self.api.download.return_value = self.bundle.read_bytes()
        self.run_publish()
        self.api.upload.assert_not_called()
        self.assertEqual(len(self.api.request.call_args_list), 2)

    def test_different_existing_asset_is_never_overwritten(self):
        self.api.request.side_effect = [{**self.release, "draft": False}, [self.asset]]
        self.api.download.return_value = b"different"
        with self.assertRaisesRegex(RuntimeError, "different bundle"):
            self.run_publish()
        self.api.upload.assert_not_called()
        self.assertFalse(self.metadata.exists())

    def test_failed_upload_leaves_draft_and_does_not_write_metadata(self):
        self.api.request.side_effect = [None, self.release, []]
        self.api.upload.side_effect = RuntimeError("upload failed")
        with self.assertRaisesRegex(RuntimeError, "upload failed"):
            self.run_publish()
        self.assertFalse(self.metadata.exists())
        self.assertFalse(any(call.args[0] == "PATCH" for call in self.api.request.call_args_list))

    def test_wrong_uploaded_size_does_not_publish(self):
        self.api.request.side_effect = [None, self.release, []]
        self.api.upload.return_value = {**self.asset, "size": 1}
        with self.assertRaisesRegex(RuntimeError, "size and URL"):
            self.run_publish()
        self.assertFalse(self.metadata.exists())

    def test_auth_failure_is_not_treated_as_missing_release(self):
        api = Gitea("https://gitea.com", "owner/repo", "test-token")
        with patch("publish_gitea.urlopen", side_effect=HTTPError(api.base, 403, "forbidden", {}, None)):
            with self.assertRaisesRegex(RuntimeError, "HTTP 403"):
                api.request("GET", "/releases/tags/v0.1.2", allow_missing=True)

    def test_upload_uses_gitea_attachment_multipart_field(self):
        api = Gitea("https://gitea.com", "owner/repo", "test-token")
        with patch.object(api, "request") as request:
            api.upload(7, "patches-0.1.2.mpp", b"test-bundle")
            self.assertIn(b'name="attachment"', request.call_args.args[2])
            self.assertIn(b"test-bundle", request.call_args.args[2])


if __name__ == "__main__":
    unittest.main()
