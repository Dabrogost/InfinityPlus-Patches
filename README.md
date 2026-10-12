# Infinity+ Patches

A lightweight [Morphe](https://morphe.software/) patch bundle for **Infinity for Reddit+**, based on [Patcheddit](https://github.com/wchill/patcheddit) v1.4.0, with the Infinity+ 8.3.x subscription fingerprint compatibility change proposed in [PR #108](https://github.com/wchill/patcheddit/pull/108).

**Supported package:** `ml.docilealligator.infinityforreddit.plus` (Infinity+ only; not Patreon).  
**Tested APK version:** 8.3.3.

## Included patches

- **Spoof client:** Replaces Reddit OAuth client ID, redirect URI and user agent. Provides an optional RedReader client ID preset or a custom 22-character ID. Includes support for the old and new Infinity+ subscription activity fingerprints.
- **Modify login WebView:** Applies Patcheddit's existing WebView compatibility hook.

The patches retain Infinity-specific and shared extensions. Patches for other Reddit applications have been removed.

## Install in Morphe Manager

[**Add Infinity+ Patches to Morphe**](https://morphe.software/add-source?github=Dabrogost/InfinityPlus-Patches)

Or open Morphe Manager → **Sources → + → Remote**, enter `https://github.com/Dabrogost/InfinityPlus-Patches`, and tap Add. You can then select an unmodified Infinity+ APK, enable the two patches and configure **Spoof client**.

**Note:** The above GitHub-hosted source and links may be unavailable while the original repository account is suspended. A future mirror will need new release URLs and metadata; this archive does not include the compiled `.mpp` release.

### OAuth settings

- **RedReader preset:** Select **RedReader (shared client ID)** from the OAuth client ID dropdown.
- **Custom OAuth client ID:** Enter an appropriate 22-character client ID manually.
- **Redirect URI:** Defaults to `redreader://rr_oauth_redir` and must match the registered OAuth client configuration.
- **User agent:** Defaults to `org.quantumbadger.redreader/1.25.2`.

The preset is sourced from [Continuum's public code](https://github.com/cygnusx-1-org/continuum). Public availability does not establish permission to reuse RedReader's OAuth identity; Reddit may restrict or revoke it. Users must still authorize their Reddit accounts.

## Build

Use JDK 17 and the Gradle wrapper with access to the required Morphe dependencies:

```bash
./gradlew :patches:buildAndroid --no-daemon
```

On Windows use `gradlew.bat`. The resulting `.mpp` should appear under `patches/build/libs/`.

GitHub **Actions → Build Infinity+ patches** builds an artifact for testing. **Publish Infinity+ source** manually builds, publishes a versioned `.mpp` in GitHub Releases, and updates `patches-bundle.json`. This GitHub-specific publishing workflow will need adaptation if moved to another hosting service.

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
