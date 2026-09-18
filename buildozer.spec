[app]
title = RGB CutShorts
package.name = rgbcutshorts
package.domain = com.rgb

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 1.0.0

requirements = python3,kivy,yt-dlp,google-generativeai,ffmpeg

orientation = portrait

android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 24
android.archs = arm64-v8a
