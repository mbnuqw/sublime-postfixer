#!/usr/bin/env python3

import os
import sys
import zipfile

files = [
  "postfix.py",
  "dbg.py",
  "Main.sublime-menu",
  "Default.sublime-commands",
  "Postfixer.sublime-settings",
  "postfixes.yml"
]

# Create sublime package
with zipfile.ZipFile("Postfixer.sublime-package", "w") as zf:
  for fn in files:
    zf.write(fn)

# Move to packages dir
if sys.platform == "linux":
  p = os.path.expanduser("~/.config/sublime-text-3/Installed Packages/Postfixer.sublime-package")
  os.rename("Postfixer.sublime-package", p)
elif sys.platform == "darwin":
  p = os.path.expanduser("~/Library/Application Support/Sublime Text 3/Installed Packages/Postfixer.sublime-package")
  os.rename("Postfixer.sublime-package", p)
elif sys.platform == "win32":
  p = os.path.join(os.environ['APPDATA'], "Sublime Text 3\\Installed Packages\\Postfixer.sublime-package")
  os.rename("Postfixer.sublime-package", p)