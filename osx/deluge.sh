#!/bin/sh

EXEC="exec"

name="`basename $0`"
if [[ "$0" == `pwd`* ]] || [[ "$0" == "//"* ]]; then
    full_path="$0"
else
    full_path="`pwd`/$0"
fi
tmp=`dirname "$full_path"`
tmp=`dirname "$tmp"`
bundle=`dirname "$tmp"`
bundle_contents="$bundle"/Contents
bundle_macos="$bundle_contents"/MacOS
bundle_res="$bundle_contents"/Resources
bundle_lib="$bundle_res"/lib
bundle_bin="$bundle_res"/bin
bundle_data="$bundle_res"/share
bundle_etc="$bundle_res"/etc

export DYLD_LIBRARY_PATH="$bundle_lib"
export XDG_CONFIG_DIRS="$bundle_etc"/xdg
export XDG_DATA_DIRS="$bundle_data"
export GTK_DATA_PREFIX="$bundle_res"
export GTK_EXE_PREFIX="$bundle_res"
export GTK_PATH="$bundle_res"

export GTK2_RC_FILES="$bundle_etc/gtk-2.0/gtkrc"
export GTK_IM_MODULE_FILE="$bundle_etc/gtk-2.0/gtk.immodules"
export GDK_PIXBUF_MODULE_FILE="$bundle_etc/gtk-2.0/gdk-pixbuf.loaders"
export PANGO_RC_FILE="$bundle_etc/pango/pangorc"

#Set $PYTHON to point inside the bundle
export PYTHON="$bundle_macos/Deluge-python"
export PYTHONHOME="$bundle_res"
#Add the bundle's python modules
PYTHONPATH="$bundle_lib:$PYTHONPATH"
PYTHONPATH="$bundle_lib/python/lib-dynload/:$PYTHONPATH"
PYTHONPATH="$bundle_lib/python/:$PYTHONPATH"
PYTHONPATH="$bundle_lib/pygtk/2.0:$PYTHONPATH"
export PYTHONPATH

# We need a UTF-8 locale.
lang=`defaults read .GlobalPreferences AppleLocale 2>/dev/null`
if test "$?" != "0"; then
    lang=`defaults read .GlobalPreferences AppleCollationOrder 2>/dev/null | sed 's/_.*//'`
fi
LANG=""
if test "$lang" != ""; then
    LANG="`grep \"\`echo $lang\`_\" /usr/share/locale/locale.alias | \
           tail -n1 | sed 's/\./ /' | awk '{print $2}'`"
fi
if test "$LANG" == ""; then
    export LANG="C"
else
    export LANG="$LANG.utf8"
fi

if test -f "$bundle_lib/charset.alias"; then
    export CHARSETALIASDIR="$bundle_lib"
fi

# Extra arguments can be added in environment.sh.
EXTRA_ARGS=
if test -f "$bundle_res/environment.sh"; then
    source "$bundle_res/environment.sh"
fi

# Strip out the argument added by the OS.
if [ "x`echo "x$1" | sed -e "s/^x-psn_.*//"`" == "x" ]; then
    shift 1
fi

#Note that we're calling $PYTHON here to override the version in
#pygtk-demo's shebang.
$EXEC "$PYTHON" "$bundle_contents/MacOS/Deluge-bin" #-l ~/.config/deluge/app.log -L debug
