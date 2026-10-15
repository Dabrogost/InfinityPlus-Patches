"""Publish the staged bundle to Gitea; write metadata only after upload succeeds."""
import hashlib
import json
import os
from pathlib import Path
import re
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode, urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener, urlopen
import uuid


class Gitea:
    def __init__(self, server, repository, token):
        parsed = urlsplit(server)
        if parsed.scheme != "https" or not parsed.netloc or parsed.username or parsed.password:
            raise ValueError("GITEA_SERVER_URL must be an HTTPS server URL")
        if not re.fullmatch(r"[\w.-]+/[\w.-]+", repository):
            raise ValueError("GITEA_REPOSITORY must be owner/repository")
        if not token:
            raise ValueError("GITEA_TOKEN is missing; enable repository Actions write permissions")
        self.base = f"{server.rstrip('/')}/api/v1/repos/{repository}"
        self.token = token

    def download(self, url):
        parsed = urlsplit(url)
        if parsed.scheme != "https" or parsed.netloc != urlsplit(self.base).netloc:
            raise ValueError("Expected an asset URL on the Gitea server")
        class AssetRedirect(HTTPRedirectHandler):
            def redirect_request(self, request, fp, code, msg, headers, newurl):
                redirected = super().redirect_request(request, fp, code, msg, headers, newurl)
                if redirected is not None:
                    redirected.remove_header("Authorization")
                return redirected
        request = Request(url, headers={"Authorization": f"token {self.token}"})
        with build_opener(AssetRedirect()).open(request, timeout=120) as response:
            return response.read()

    def request(self, method, path, payload=None, content_type="application/json", allow_missing=False):
        body = json.dumps(payload).encode() if isinstance(payload, dict) else payload
        request = Request(self.base + path, data=body, method=method, headers={
            "Authorization": f"token {self.token}",
            "Content-Type": content_type,
            "Accept": "application/json",
        })
        try:
            with urlopen(request, timeout=120) as response:
                return json.load(response)
        except HTTPError as error:
            if allow_missing and error.code == 404:
                return None
            raise RuntimeError(
                f"Gitea {method} {path} failed (HTTP {error.code}). "
                "For 401/403, check Actions token permissions for code and releases."
            ) from None

    def upload(self, release_id, name, content):
        boundary = uuid.uuid4().hex
        body = (
            f'--{boundary}\r\nContent-Disposition: form-data; name="attachment"; '
            f'filename="{name}"\r\nContent-Type: application/octet-stream\r\n\r\n'
        ).encode() + content + f"\r\n--{boundary}--\r\n".encode()
        return self.request("POST", f"/releases/{release_id}/assets?{urlencode({'name': name})}",
                            body, f"multipart/form-data; boundary={boundary}")


def publish(api, version, commit, bundle, metadata_path):
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        raise ValueError("Expected a semantic release version such as 0.1.2")
    if not re.fullmatch(r"[0-9a-fA-F]{40,64}", commit):
        raise ValueError("Expected the full workflow commit SHA")
    content = bundle.read_bytes()
    if not content:
        raise ValueError("Refusing to publish an empty bundle")
    name = f"patches-{version}.mpp"
    tag = f"v{version}"
    release = api.request("GET", f"/releases/tags/{quote(tag, safe='')}", allow_missing=True)
    if release is None:
        release = api.request("POST", "/releases", {
            "tag_name": tag, "target_commitish": commit, "draft": True,
            "prerelease": False, "name": f"Infinity+ Patches {tag}",
            "body": "Infinity+ Morphe compatibility patches. Includes code adapted from Patcheddit.",
        })
    release_id = release["id"]
    assets = api.request("GET", f"/releases/{release_id}/assets")
    matches = [asset for asset in assets if asset["name"] == name]
    if len(matches) > 1:
        raise RuntimeError("Multiple matching release assets exist; resolve them before rerunning")
    if matches:
        asset = matches[0]
        existing = api.download(asset["browser_download_url"])
        if hashlib.sha256(existing).digest() != hashlib.sha256(content).digest():
            raise RuntimeError("This release already contains a different bundle. Bump version in gradle.properties.")
    else:
        if not release.get("draft", False):
            raise RuntimeError("An existing published release has no matching bundle. Bump the version or repair it manually.")
        asset = api.upload(release_id, name, content)
    if not asset.get("browser_download_url") or asset.get("size") != len(content):
        raise RuntimeError("Gitea did not confirm the expected uploaded asset size and URL")
    if urlsplit(asset["browser_download_url"]).scheme != "https":
        raise RuntimeError("Gitea returned a non-HTTPS download URL")
    if release.get("draft", False):
        release = api.request("PATCH", f"/releases/{release_id}", {"draft": False})
    metadata = {
        "created_at": release["created_at"][:19],
        "description": f"Infinity+ Morphe patches {tag}. Based on Patcheddit; see NOTICE.",
        "download_url": asset["browser_download_url"],
        "signature_download_url": "",
        "version": version,
    }
    metadata_path.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    print(f"Published {name}; updated {metadata_path}")


def main():
    api = Gitea(os.environ["GITEA_SERVER_URL"], os.environ["GITEA_REPOSITORY"], os.environ.get("GITEA_TOKEN", ""))
    version = os.environ["VERSION"]
    publish(api, version, os.environ["GITEA_SHA"], Path("dist") / f"patches-{version}.mpp", Path("patches-bundle.json"))


if __name__ == "__main__":
    try:
        main()
    except (KeyError, ValueError, RuntimeError, OSError, URLError) as error:
        raise SystemExit(str(error)) from None
