# Infinity+ Patches

A lightweight [Morphe](https://morphe.software/) patch bundle for **Infinity for Reddit+**, based on [Patcheddit](https://github.com/wchill/patcheddit) v1.4.0, with the Infinity+ 8.3.x subscription fingerprint compatibility change proposed in [PR #108](https://github.com/wchill/patcheddit/pull/108).

**Supported package:** `ml.docilealligator.infinityforreddit.plus` (Infinity+ only; not Patreon).  
**Tested APK version:** 8.3.3.

## Included patches

- **Spoof client:** Replaces Reddit OAuth client ID, redirect URI and user agent. Provides an optional RedReader client ID preset or a custom 22-character ID. Includes support for the old and new Infinity+ subscription activity fingerprints.
- **Modify login WebView:** Applies Patcheddit's existing WebView compatibility hook.

The patches retain Infinity-specific and shared extensions. Patches for other Reddit applications have been removed.

## Install in Morphe Manager

1. Open Morphe Manager → **Sources → + → Remote**.
2. Paste this source URL and tap **Add**:

   ```text
https://gitea.com/api/v1/repos/Dabrogost/InfinityPlus-Patches/raw/patches-bundle.json
   ```

3. Select an unmodified Infinity+ APK, enable the two patches and configure **Spoof client**.

Use the full raw `patches-bundle.json` URL above as the source. It is the [source metadata](https://gitea.com/Dabrogost/InfinityPlus-Patches/raw/branch/main/patches-bundle.json) that tells Morphe where to download the patch bundle. The publish workflow updates this same URL's contents for each release, so you can keep the source configured when new versions are published.

### OAuth settings

- **RedReader preset:** Select **RedReader (shared client ID)** from the OAuth client ID dropdown.
- **Custom OAuth client ID:** Enter an appropriate 22-character client ID manually.
- **Redirect URI:** Defaults to `redreader://rr_oauth_redir` and must match the registered OAuth client configuration.
- **User agent:** Defaults to `org.quantumbadger.redreader/1.25.2`.

The preset is sourced from [Continuum's public code](https://github.com/cygnusx-1-org/continuum). Public availability does not establish permission to reuse RedReader's OAuth identity; Reddit may restrict or revoke it. Users must still authorize their Reddit accounts.

## Build

The **Build Infinity+ patches** workflow runs on pushes to `main` on Gitea or GitHub and uploads the `.mpp` as a workflow artifact. You can also start it manually from **Actions → Build Infinity+ patches → Run workflow**. Publishing remains manual. No GitHub account, personal access token, or `GH_PACKAGES_*` secrets are needed for the build. Download the artifact from the successful Actions run.

For a local Linux build, install JDK 17 and Android SDK platforms 33, 34, 35 and 36 plus build-tools 36.0.0, set `ANDROID_HOME`, then run:

```bash
bash ci/build.sh
```

The script builds the required Morphe plugin and libraries from pinned public source revisions and publishes them into a private local Maven directory under `~/.cache/infinity-plus-deps`. It disables GitHub Packages resolution for this build. Public downloads from GitHub, Maven Central, Google and JitPack are still required. The first run builds the dependencies; later runs reuse the workflow cache. See [ci/README.md](ci/README.md) for the pinned versions and maintenance notes.

The resulting bundle is `patches/build/libs/patches-<version>.mpp`. On Windows, use a Linux environment with the SDK (such as WSL2) for this script.

**Publish Infinity+ source** is a manual Gitea workflow. Run it on `main` after pushing these changes. It builds the bundle, creates a draft release for the version in `gradle.properties`, uploads the `.mpp`, publishes the release, and commits `patches-bundle.json` with the download URL returned by Gitea. It uses the built-in `GITEA_TOKEN`; no personal access token is required. Repository/owner Actions settings must allow code and release writes, and branch rules must permit the metadata commit. Increment the version for a new release: an existing asset with different contents is never overwritten. If publication succeeds but the metadata push fails, resolve the branch permissions or concurrent changes before retrying. Identical assets can be reused; a different rebuilt bundle requires a new version.

## Testing and limitations

- Infinity+ 8.3.3 was successfully patched and signed with Morphe Manager 1.35.0 and patcher 1.15.1 on Android 16.
- Successful patching does not guarantee that Reddit's OAuth login succeeds; end-to-end login needs separate verification.
- Billing/subscription fingerprints are optional, so successful patching does not prove each billing hook matched.
- The RedReader preset has not been independently verified for successful login.
- Future Infinity+ releases may require new fingerprints.

## Modifications and credits

This source was adapted October 11, 2026 from Patcheddit v1.4.0, incorporating Infinity+ 8.3.x fingerprint compatibility, reducing the supported app set to Infinity+, adding a RedReader OAuth preset, and adding independent release tooling.

This app uses code from Patcheddit. To learn more, visit https://reddit.com/r/patcheddit

This app uses code from Morphe. To learn more, visit http://morphe.software

Licensed under **GNU GPLv3** subject to applicable additional conditions under Section 7. See [LICENSE](LICENSE), [NOTICE](NOTICE), [COPYRIGHT](COPYRIGHT), and [Morphe's license notice](patches/src/main/resources/branding-license/LICENSE_MORPHE.TXT).

Not affiliated with Reddit, RedReader, Infinity for Reddit, Patcheddit or Morphe.
