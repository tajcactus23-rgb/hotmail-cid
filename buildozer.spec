[app]
title = Hotmail Inboxer Neural
package.name = hotmail_inboxer
package.domain = org.neuraltech
version = 2.1.0

source.dir = .
source.include.exts = py
# Simple requirements - let buildozer figure out versions
requirements = python3,kivy

orientation = all
fullscreen = 0

android.permissions = INTERNET
android.archs = arm64-v8a
android.api = 29
android.minapi = 24

android.sdk_path = /home/runner/android-sdk
android.ndk_api = 26

[buildozer]
log_level = 2