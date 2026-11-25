#!/bin/sh
# Bundle the release build of the menu bar app into CratekitBar.app, signed ad
# hoc with no Apple account (idea 377, decision 2), and zip it with ditto so
# the executable bit and the signature survive an artifact upload. Run from
# anywhere on a Mac with a Swift toolchain; writes only under app/build.
set -eu

here=$(cd "$(dirname "$0")/.." && pwd)
cd "$here"

swift build -c release --product CratekitBar
bin=$(swift build -c release --show-bin-path)

out="$here/build"
app="$out/CratekitBar.app"
rm -rf "$app" "$out/CratekitBar.zip"
mkdir -p "$app/Contents/MacOS" "$app/Contents/Resources"
cp "$bin/CratekitBar" "$app/Contents/MacOS/CratekitBar"
cp Bundle/Info.plist "$app/Contents/Info.plist"
plutil -lint "$app/Contents/Info.plist"

# "-" is the ad hoc identity: a signature with no certificate behind it.
codesign --force --sign - --timestamp=none "$app"
codesign --verify --strict --verbose=2 "$app"

test "$(/usr/libexec/PlistBuddy -c 'Print :LSUIElement' "$app/Contents/Info.plist")" = "true"

ditto -c -k --keepParent "$app" "$out/CratekitBar.zip"
echo "bundled $app"
