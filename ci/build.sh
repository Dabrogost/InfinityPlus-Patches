#!/usr/bin/env bash
# Build on Linux without a GitHub account or GitHub Packages token.
set -euo pipefail
export LANG=C.UTF-8
project_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
deps_dir="${INFINITY_DEPS_HOME:-$HOME/.cache/infinity-plus-deps}"
mkdir -p "$deps_dir"
deps_dir="$(cd "$deps_dir" && pwd)"
export ANDROID_HOME="${ANDROID_HOME:-${ANDROID_SDK_ROOT:-}}"
if [[ -z "$ANDROID_HOME" ]]; then
  echo 'ANDROID_HOME must point to an Android SDK with platforms 33, 34, 35, 36 and build-tools 36.0.0.' >&2
  exit 1
fi
for platform in 33 34 35 36; do
  test -f "$ANDROID_HOME/platforms/android-$platform/android.jar" || {
    echo "Missing Android SDK platform $platform; install it with sdkmanager." >&2
    exit 1
  }
done

# Serialize cache creation if two local builds share this directory.
exec 9>"$deps_dir/build.lock"
flock 9
init_script="$project_dir/ci/public-build.init.gradle"
gradle_args=(-I "$init_script" "-Dmaven.repo.local=$deps_dir/maven" -Pgpr.user=unused -Pgpr.key=unused --no-daemon --max-workers=4)

fetch_source() {
  local name="$1" commit="$2"
  source_dir="$deps_dir/sources/$name-$commit"
  if [[ ! -f "$source_dir/.source-ready" ]]; then
    local staging
    staging="$(mktemp -d "$deps_dir/source-XXXXXX")"
    curl --fail --location --retry 3 "https://codeload.github.com/MorpheApp/$name/tar.gz/$commit" -o "$staging/source.tar.gz"
    mkdir "$staging/tree"
    tar -xzf "$staging/source.tar.gz" --strip-components=1 -C "$staging/tree"
    touch "$staging/tree/.source-ready"
    mkdir -p "$deps_dir/sources"
    mv "$staging/tree" "$source_dir"
    rm "$staging/source.tar.gz"
    rmdir "$staging"
  fi
}
publish_source() {
  local name="$1" commit="$2"
  shift 2
  fetch_source "$name" "$commit"
  echo "Building $name from $commit"
  (cd "$source_dir"; bash gradlew "${gradle_args[@]}" "$@")
}

# These are the source revisions matching the project's existing dependency versions.
cache_key="$(cat "$project_dir/ci/build.sh" "$init_script" | sha256sum | cut -d ' ' -f 1)"
if [[ ! -f "$deps_dir/ready-$cache_key" ]]; then
  publish_source morphe-patches-gradle-plugin 5fdc47459085d990c63b73071b25c7b6d4f4047f publishToMavenLocal
  publish_source multidexlib2 41cccc644cf1804362f7aa2fae96a6ffe67ffd22 publishToMavenLocal
  publish_source Apktool 04517bc7c687a6cfdcd813abb02e3134487baa95 \
    :brut.j.common:publishToMavenLocal :brut.j.util:publishToMavenLocal \
    :brut.j.dir:publishToMavenLocal :brut.j.xml:publishToMavenLocal \
    :brut.apktool:apktool-lib:publishToMavenLocal
  publish_source morphe-patcher be0585cd1449f73bffeda61ae0f1a1f921b09758 publishToMavenLocal
  publish_source morphe-patches-library ea1705c0d9e4422875d112a959f41b1051c8c3d9 publishToMavenLocal
  touch "$deps_dir/ready-$cache_key"
fi
cd "$project_dir"
bash gradlew "${gradle_args[@]}" :patches:buildAndroid
