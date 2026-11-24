[app]
title = XvsO
package.name = xvso
package.domain = org.rogotuyt
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,pkl,svg
version = 1.0.0
requirements = python3,kivy
orientation = portrait
fullscreen = 0
icon.filename = %(source.dir)s/assets/icon.png

[buildozer]
log_level = 2
warn_on_root = 1

[app:android]
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a
android.accept_sdk_license = True
