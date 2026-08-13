[app]

# (str) Title of your application
title = Calculator

# (str) Package name
package.name = calculator

# (str) Package domain (needed for android packaging)
package.domain = org.myapp

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (str) Application versioning
version = 0.1

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy,kivymd,pillow

# (str) Orientation (landscape, sensorLandscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (str) Icon of the application
icon.filename = %(source.dir)s/icon.png

# (str) Presplash image of the application
presplash.filename = %(source.dir)s/icon.png

# (list) Permissions
android.permissions = INTERNET

# (int) Target Android API, should be 34 for modern Android 14/15 devices
android.api = 34

# (int) Minimum API required (API 24 = Android 7.0)
android.minapi = 24

# (str) Android NDK version to use
android.ndk = 25b

# (list) The Android archs to build for
android.archs = arm64-v8a

# (bool) Accept SDK license automatically
android.accept_sdk_license = 1

# (str) Python-for-android branch to use (master prevents legacy build errors)
p4a.branch = master

# -----------------------------------------------------------------------------
# Buildozer Global Options
# -----------------------------------------------------------------------------

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
