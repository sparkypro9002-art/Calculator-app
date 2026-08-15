[app]
title = Calculator
package.name = calculator
package.domain = org.myapp
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,pygame
orientation = portrait
fullscreen = 1
icon.filename = %(source.dir)s/icon.png
presplash.filename = %(source.dir)s/icon.png
android.permissions = INTERNET
android.api = 31
android.minapi = 21
android.ndk = 23b
android.archs = arm64-v8a
android.accept_sdk_license = 1

[buildozer]
log_level = 2
warn_on_root = 1
