# Building without GitHub Packages

Run `bash ci/build.sh` on Linux with JDK 17 and an Android SDK containing
platforms 33, 34, 35, 36 and build-tools 36.0.0. The workflows install these.

The build uses public source downloads, not GitHub authentication. It first
publishes these upstream projects to an isolated local Maven repository:

| Project | Version | Source commit |
| --- | --- | --- |
| Morphe patches Gradle plugin | 1.3.2-dev.1 | `5fdc47459085d990c63b73071b25c7b6d4f4047f` |
| multidexlib2 | b6365a84f4 | `41cccc644cf1804362f7aa2fae96a6ffe67ffd22` |
| Morphe Apktool | 2.11.2.r3 | `04517bc7c687a6cfdcd813abb02e3134487baa95` |
| Morphe patcher | 1.3.3 | `be0585cd1449f73bffeda61ae0f1a1f921b09758` |
| Morphe patches/extension libraries | 1.0.2-dev.2 | `ea1705c0d9e4422875d112a959f41b1051c8c3d9` |

Source comes from the corresponding public `MorpheApp` repositories. Standard
dependencies still come from Maven Central, Google and JitPack. No sources are
modified. Upstream source/license files remain in each cached source tree.

`public-build.init.gradle` removes GitHub Packages repositories and disables
publication signing and Javadoc generation for local dependency builds.
The `unused` Gradle properties satisfy upstream's eager credential lookup;
they are placeholders, not credentials, and the GitHub Packages repositories
are removed before dependency resolution.

The default cache is `~/.cache/infinity-plus-deps`. Set `INFINITY_DEPS_HOME`
to another directory to test with a fresh local Maven repository. A completion
marker is written only after all dependency publications succeed. Its key
includes the build script and initialization script. CI also keys its cache
on those files, the version catalog and project settings.

When upgrading Morphe, update the source commits in `build.sh`, the versions
in `settings.gradle.kts` and `gradle/libs.versions.toml`, and this table together.
Validate with a fresh `INFINITY_DEPS_HOME` before pushing. The final `.mpp`
build still uses the project's Gradle wrapper and `:patches:buildAndroid` task.

The build produces a bundle; it does not test patching an APK or phone behavior.
The manual GitHub [**Publish Infinity+ source** workflow](../.github/workflows/publish-infinity-source.yml)
runs on `main` using the `github-infinity` self-hosted runner. It builds the bundle,
publishes a GitHub Release using `GITHUB_TOKEN`, and commits updated
`patches-bundle.json` metadata pointing to the GitHub release asset.

The separate `publish_gitea.py` helper is retained for Gitea publishing; it is
not used by the GitHub publish workflow. It creates a draft, uploads and verifies
the asset, publishes the release, then generates source metadata from Gitea's
returned download URL.
Run the helper's mocked API tests with `python3 -m unittest discover -s ci -p 'test_*.py'`.
No release is published by the tests.
