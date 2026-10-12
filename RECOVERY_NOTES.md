# Repository reconstruction notes (October 12, 2026)

This repository is **reconstructed**, not an exact export of the original suspended GitHub repository at its last commit.

## Source

- The user's `InfinityPlus-Patches.zip` provided the working tree and a valid `.git` directory with its original `57e63a9` initial commit.
- Original archive was version `0.1.0` and contained only `.github/workflows/build.yml`.
- The later files below were restored from exact code or known configuration shown in an earlier ChatGPT conversation. The new README is a newly written, condensed replacement, not a verified copy of the last GitHub README.

## Restored files

- `SpoofClientPatch.kt`: RedReader OAuth preset, updated user agent, descriptions.
- `gradle.properties`: version 0.1.2.
- `patches/build.gradle.kts`: later patch source metadata.
- `.github/workflows/publish-infinity-source.yml`: GitHub publishing workflow.
- `patches-bundle.json`: archived 0.1.2 release metadata. It still links to the suspended GitHub repository; it is not a working current download URL.
- `README.md`: updated setup, feature, testing and license information.

## Caveats

- This reconstruction has **not been compiled or tested** against a real Infinity+ APK.
- No compiled `.mpp` file or release assets were contained in the original ZIP.
- The GitHub-specific publish workflow and metadata are not directly usable on Codeberg/Gitea without changes.
- The original Git history contains only one initial commit, not the original 0.1.1 or 0.1.2 release commits. The reconstruction is one newly created commit on top of that history.
- If GitHub reinstates the account, compare/fetch the original remote history before pushing anything. Do not force-push over any restored remote commits.
