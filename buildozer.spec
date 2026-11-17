[app]

title = FF Sensi Lab
package.name = ffsensilab
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

# Kivy app; no internet permission is needed.
requirements = python3,kivy
orientation = portrait
fullscreen = 0

# Android build settings
android.minapi = 23
android.api = 35
android.archs = arm64-v8a, armeabi-v7a

# Keep the app lightweight.
android.allow_backup = False

[buildozer]
log_level = 2
warn_on_root = 1
