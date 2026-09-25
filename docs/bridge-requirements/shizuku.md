# Shizuku plugin bridge requirement

The checked ctrl-mietze/Dioxamine and upstream source currently expose no documented Shizuku/rish namespace to WebView plugins.

The five Shizuku packages are therefore marked requires-native-bridge and installable: false rather than silently relabelling normal ADB as Shizuku.

A future bridge should integrate native Shizuku authorization, add explicit manifest permission validation and expose narrowly scoped permission-gated host operations before these plugins are enabled.
