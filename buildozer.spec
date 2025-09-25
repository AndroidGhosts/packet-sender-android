[app]
title = Cyber Packet Sender
package.name = packetsender
package.domain = org.syria

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 1.0
requirements = python3,kivy

android.permissions = INTERNET,ACCESS_NETWORK_STATE

# أضف هذه الإعدادات الجديدة
android.sdk = 34
android.ndk = 25b
android.build_tools_version = 34.0.0
android.api = 34

[buildozer]
log_level = 2
