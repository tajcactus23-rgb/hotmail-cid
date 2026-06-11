[app]
title = Hotmail Inboxer Neural
package.name = hotmail_inboxer
package.domain = org.neuraltech
version = 2.1.0

source.dir = .
source.include.exts = py
# Use SDL2 bootstrap with simpler requirements
requirements = python3,kivy,sdl2

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