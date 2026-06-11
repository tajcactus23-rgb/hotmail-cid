[app]
title = Hotmail Inboxer Neural
package.name = hotmail_inboxer
package.domain = org.neuraltech
version = 2.1.0

source.dir = .
source.include.exts = py
requirements = python3,kivy,requests,urllib3

fullscreen = 0
orientation = all

android.permissions = INTERNET, ACCESS_NETWORK_STATE
android.archs = arm64-v8a, armeabi-v7a
android.api = 29
android.minapi = 21
android.enable_androidx = True

[buildozer]
log_level = 2