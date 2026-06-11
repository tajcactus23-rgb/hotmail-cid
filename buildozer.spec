[app]
title = Hotmail Inboxer Neural
package.name = hotmail_inboxer
package.domain = org.neuraltech
version = 2.1.0

source.dir = .
source.include.exts = py
requirements = python3,kivy

orientation = all
fullscreen = 0

android.permissions = INTERNET
android.archs = arm64-v8a
android.api = 29

android.sdk_path = /workspace/android-sdk
android.ndk_path = /workspace/android-sdk/ndk
android.ndk_api = 26

[buildozer]
log_level = 2