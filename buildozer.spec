[app]

title = RGB CutShorts
package.name = rgbcutshorts
package.domain = org.rgb

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,json,ttf,otf

version = 0.1

requirements = python3,kivy==2.3.0,requests,urllib3,charset-normalizer,idna,certifi

orientation = portrait
fullscreen = 0

android.permissions = INTERNET

android.api = 33
android.minapi = 24
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a

android.allow_backup = True
android.accept_sdk_license = True

[buildozer]

log_level = 2
warn_on_root = 1
