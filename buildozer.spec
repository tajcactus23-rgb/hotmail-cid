[app]
title = Hotmail Inboxer Neural
package.name = hotmail_inboxer
package.domain = org.neuraltech
version = 2.1.0

source.include.exts = py,png,jpg,kv,ttf,json
requirements = python3,kivy,requests,urllib3,pywin32
orientation = all
fullscreen = 0

# Android specific
android.permissions = INTERNET, ACCESS_NETWORK_STATE, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE
android.archs = arm64-v8a, armeabi-v7a, x86_64
android.api = 29
android.minapi = 21
android.allow_backup = True
android.enable_androidx = True

# App icon (will use default if not found)
# android.icon = icon.png

# Presplash
# android.presplash.color = #0a0a12

[buildozer]
log_level = 2
warn_on_root = 1
build_dir = ./.buildozer
bin_dir = ./bin