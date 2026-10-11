# Infinity+ Compatibility Patches

A minimal [Morphe](https://morphe.software/) patch bundle for **Infinity for Reddit+**, based on
[Patcheddit](https://github.com/wchill/patcheddit) v1.4.0, with the Infinity+ 8.3.x subscription
fingerprint compatibility change proposed in [PR #108](https://github.com/wchill/patcheddit/pull/108).

**Supported package:** `ml.docilealligator.infinityforreddit.plus` (Infinity+ only; not Patreon).

## Included patches

- **Spoof client:** Patches the Reddit OAuth client ID, redirect URI and user agent, and handles
  the old/new subscription activity bytecode patterns.
- **Modify login WebView:** Applies the existing Patcheddit WebView compatibility hook.

The two patches share an Infinity-specific extension and a small shared login helper.
Other Reddit applications and their patches have been removed.

## Build

GitHub **Actions > Build Infinity+ patches > Run workflow**, then download the
`infinity-plus-morphe-patches` artifact from the workflow run. Extract the ZIP to obtain the `.mpp`
patch bundle. In Morphe Manager advanced/expert mode, import the `.mpp` as a local patch source
(where supported by your Manager build), select `Infinity+`, and apply the two patches.

You can also run `./gradlew :patches:buildAndroid --no-daemon` using JDK 17 and a configured
GitHub Packages token for the Morphe Gradle plugin.

The original upstream release workflow is intentionally not included. This project does not
publish a signed `.mpp` release or automatically register itself as an updateable GitHub source.

## Testing and known limitations

- The subscription fingerprint fix was reported working with Infinity+ **8.3.0**.
- **Infinity+ 8.3.3 has not yet been APK-tested** with this new bundle.
- A successful patch build does not establish that Reddit's OAuth flow will work. The login
  behavior must be tested separately on an actual installation.
- The newer and older billing fingerprints are optional, following the upstream proposal.
  If a future Infinity update changes both fingerprints, subscription handling may not be
  modified, even if patching completes.

## Attribution and license

This app uses code from Patcheddit. To learn more, visit https://reddit.com/r/patcheddit

Original code: https://github.com/wchill/patcheddit

Licensed under GPL-3.0 with the original additional conditions in `NOTICE`.
This derivative uses a different project name and retains `LICENSE`, `NOTICE`, and `COPYRIGHT`.
