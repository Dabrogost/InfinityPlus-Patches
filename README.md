# Infinity+ Patches

A lightweight [Morphe](https://morphe.software/) patch bundle for **Infinity for Reddit+**, focused on restoring Reddit OAuth functionality and maintaining compatibility with newer Infinity+ releases.

Based on [Patcheddit](https://github.com/wchill/patcheddit) v1.4.0, with additional Infinity+ compatibility improvements.

This project maintains only the Infinity+ patches, removing the other Reddit clients and their associated patch implementations.

**Supported application:** Infinity for Reddit+  
**Package:** `ml.docilealligator.infinityforreddit.plus`  
**Tested version:** 8.3.3

## Features

### Spoof client

Modifies Infinity+'s Reddit OAuth configuration, including:

- **OAuth client ID:** Use a selectable RedReader preset or enter a custom client ID.
- **Redirect URI:** Defaults to `redreader://rr_oauth_redir`.
- **User agent:** Defaults to `org.quantumbadger.redreader/1.25.2`.
- **Subscription compatibility:** Handles both the older and newer subscription activity fingerprints.

The subscription fingerprint improvements are based on the changes proposed in [Patcheddit PR #108](https://github.com/wchill/patcheddit/pull/108).

### Modify login WebView

Includes Patcheddit's existing WebView compatibility patch to help resolve Reddit login issues.

Both patches retain their required shared extensions and dependencies.

## Installation

### Add to Morphe Manager

[**Add Infinity+ Patches to Morphe Manager**](https://morphe.software/add-source?github=Dabrogost/InfinityPlus-Patches)

If the link does not open Morphe Manager on your device, add the source manually:

1. Open **Morphe Manager**.
2. Navigate to **Sources → + → Remote**.
3. Enter the following repository URL:  
   `https://github.com/Dabrogost/InfinityPlus-Patches`
4. Tap **Add** and allow the patch bundle to download.

### Patch Infinity+

1. Obtain an unmodified Infinity for Reddit+ APK.
2. Select the APK in Morphe Manager.
3. Enable **Spoof client** and **Modify login WebView**.
4. Open the **Spoof client** options and configure your OAuth client ID.
5. Start patching.
6. Install the patched APK and authorize your Reddit account.

If Android rejects installation because of an existing application's signing certificate, you may need to uninstall the existing installation first. Back up your application data before doing so.

**Note:** This repository distributes patches, not a pre-patched Infinity+ APK.

## Reddit OAuth Configuration

Reddit requires a valid OAuth client ID for third-party applications.

The **Spoof client** patch provides two configuration methods.

### Option 1: RedReader preset

Select **RedReader (shared client ID)** from the OAuth client ID dropdown.

The preset uses the public OAuth client ID included in [Continuum](https://github.com/cygnusx-1-org/continuum), an open-source Infinity fork.

This eliminates the need to install RedReader simply to retrieve its client ID.

The default redirect URI and user agent are configured for RedReader.

**Important:** This is an unofficial use of RedReader's OAuth identity. Public availability of its client ID does not establish permission from Reddit or RedReader to reuse it. Shared credentials may be restricted, rate-limited, or revoked at any time.

### Option 2: Custom client ID

Users with their own Reddit OAuth credentials can enter their client ID manually.

The redirect URI must match the URI registered for that OAuth application. The user agent should also be appropriate for the selected client.

Custom configuration is preserved for users who do not want to rely on a shared OAuth identity.

### Login considerations

- Reddit may display **RedReader** during authorization when the RedReader preset is selected. This reflects the OAuth application identity and does not mean RedReader is installed.
- Users must still authorize access to their Reddit accounts.
- Successful patching does not guarantee that Reddit will accept the OAuth credentials.
- If login fails, verify the client ID, redirect URI, and user agent before investigating WebView compatibility.

## Compatibility and Testing

### Verified

- Infinity+ **8.3.3** successfully patched.
- Morphe Manager **1.35.0**, patcher **1.15.1**.
- Android 16, ARM64.
- Both **Spoof client** and **Modify login WebView** completed without patch errors.
- The resulting APK was compiled and signed successfully.

### Known limitations

- The subscription activity fingerprints are optional. Successful patching does not guarantee that every subscription-related modification was applied.
- Future Infinity+ updates may introduce bytecode changes requiring additional patches.
- Other Infinity variants, including the Patreon package, are not supported by this patch source.

Bug reports and compatibility issues can be submitted through [GitHub Issues](https://github.com/Dabrogost/InfinityPlus-Patches/issues).

## Building from Source

### Requirements

- JDK 17
- Git
- Gradle wrapper included in this repository
- Access to the required Morphe Gradle dependencies

Clone the repository:

`git clone https://github.com/Dabrogost/InfinityPlus-Patches.git`

Enter the project directory:

`cd InfinityPlus-Patches`

Build the Android-compatible patch bundle:

`./gradlew :patches:buildAndroid --no-daemon`

The compiled `.mpp` bundle will be available in `patches/build/libs/`.

On Windows, use `gradlew.bat` instead of `./gradlew`.

### GitHub Actions

The repository provides two workflows:

**Build Infinity+ patches**

Compiles the project and uploads a downloadable `.mpp` build artifact. This workflow is intended for compilation checks and testing.

**Publish Infinity+ source**

A manually triggered workflow that:

1. Builds the Android-compatible patch bundle.
2. Creates a versioned GitHub Release containing the `.mpp` file.
3. Updates `patches-bundle.json` with the new release information.
4. Makes the new release available through Morphe Manager's remote source updates.

The version is controlled through `gradle.properties`.

Published patch bundles are currently unsigned.

See [Releases](https://github.com/Dabrogost/InfinityPlus-Patches/releases) for available versions.

## Project Background

This project originated from Patcheddit v1.4.0, which supports multiple third-party Reddit applications.

Infinity+ 8.3.x introduced a subscription activity implementation that could cause the original **Spoof client** patch to fail during fingerprint matching.

The proposed upstream fix added compatibility with the newer activity pattern. This repository incorporates that change while reducing the patch bundle to the Infinity+ components.

The goal is to maintain a small, focused patch source without requiring users to install or maintain the entire Patcheddit patch collection.

### Modifications

Changes introduced October 11, 2026 include:

- Removed unrelated Reddit client patches and dependencies.
- Retained Infinity+-specific bytecode patches and shared extensions.
- Incorporated the newer subscription activity fingerprint handling from [PR #108](https://github.com/wchill/patcheddit/pull/108).
- Added an optional RedReader OAuth client ID preset.
- Updated the default RedReader user agent.
- Established independent GitHub Actions builds and versioned releases.
- Added remote patch source compatibility for Morphe Manager.

## Attribution and License

This project is a derivative of [Patcheddit](https://github.com/wchill/patcheddit), originally developed by **wchill** and contributors, and includes components associated with the [Morphe project](https://github.com/MorpheApp).

Licensed under the **GNU General Public License v3.0**, with applicable additional conditions under Section 7.

### Patcheddit attribution

This app uses code from Patcheddit. To learn more, visit https://reddit.com/r/patcheddit

Patcheddit's additional terms require preservation of attribution and prohibit derivatives from using the Patcheddit project name.

### Morphe attribution

This app uses code from Morphe. To learn more, visit http://morphe.software

Applicable Morphe Section 7 notices are preserved with the redistributed source resources.

### License files

- [LICENSE](LICENSE) — GNU General Public License v3.0
- [NOTICE](NOTICE) — Patcheddit additional licensing conditions
- [COPYRIGHT](COPYRIGHT) — Original copyright and attribution notices
- [LICENSE_MORPHE.TXT](patches/src/main/resources/branding-license/LICENSE_MORPHE.TXT) — Additional Morphe licensing conditions

Original Patcheddit source: https://github.com/wchill/patcheddit

Infinity+ Patches is an independently maintained project and is not officially affiliated with or endorsed by Reddit, RedReader, Infinity for Reddit, Patcheddit, or Morphe.
