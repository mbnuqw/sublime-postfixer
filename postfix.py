import os
import re
import yaml
import sublime
import sublime_plugin

from Postfixer.dbg import Dbg

DEFAULT_POSTFIXES_PATH = "Packages/Postfixer/postfixes.yml"
FIX_RE = re.compile(r"^(\s*)(.+)\.(.+)$")
VAR_CURSOR = "$cursor"
VAR_INDENT = "$-->"
VAR_WHOLE = "$0"


def plugin_loaded():
  # Get settings
  settings = sublime.load_settings("Postfixer.sublime-settings")
  global global_settings

  # Setup debug utils
  global d
  d = Dbg(settings)

  # Get default postfixes file
  postfixes_str = ""
  try:
    postfixes_str = sublime.load_resource(DEFAULT_POSTFIXES_PATH)
  except:
    d.lg("Cannot load default postfixes file: " + DEFAULT_POSTFIXES_PATH)

  # Get user's postfixes file or create new from default
  fixes_path = os.path.join(sublime.packages_path(), "User/postfixes.yml")
  if os.path.isfile(fixes_path):
    with open(fixes_path) as f:
      postfixes_str = f.read()
  else:
    with open(fixes_path, "w") as f:
      f.write(postfixes_str)

  # Parse snippets
  fixes = None
  try:
    fixes = yaml.load(postfixes_str)
  except:
    d.lg("Cannot parse postfixes yaml")
    fixes = {}

  # Prepare snippets to use
  global postfixes
  postfixes = {}
  for scopes, rules in fixes.items():
    for scope in scopes.split(' '):
      postfixes[scope] = rules


class PostfixCommand(sublime_plugin.TextCommand):

  def run(self, edit):
    # get postfixes for current scope
    scope = self.view.scope_name(0).split(' ')[0]
    if scope in postfixes:
      scopefixes = postfixes[scope]
    else:
      d.lg("Cannot find postfixes for scope: " + scope)
      return

    # Get indent type (from syntax / global settings)
    syn = self.view.settings().get("syntax")
    syn = os.path.basename(syn)
    syn = os.path.splitext(syn)[0]
    syn_settings = sublime.load_settings(syn + ".sublime-settings")
    sp_indent = syn_settings.get("translate_tabs_to_spaces")
    if sp_indent is None:
      sp_indent = self.view.settings().get("translate_tabs_to_spaces")

    # Get intent size
    if sp_indent:
      tab_size = syn_settings.get("tab_size")
      if tab_size is None:
        tab_size = self.view.settings().get("tab_size")

    # Set indent
    if sp_indent:
      self.indent_str = " " * tab_size
    else:
      self.indent_str = "\t"

    # Fix all possible occurrences
    cursors = []
    for r in self.view.sel():
      if not r.empty():
        continue

      line_r = sublime.Region(self.view.line(r).begin(), r.b)
      try:
        out, cursor = self.fix(scopefixes, self.view.substr(line_r))
      except ValueError:
        continue
      self.view.replace(edit, line_r, out)
      cursor = line_r.begin() + cursor
      cursors.append(sublime.Region(cursor, cursor))

    # Update cursor(s) position
    if len(cursors) > 0:
      self.view.sel().clear()
      self.view.sel().add_all(cursors)

  def fix(self, fixes, line):
    # Parse line
    parsed_line = FIX_RE.match(line)
    if parsed_line is None:
      raise ValueError("no_fit")
    indent, target, cmd = parsed_line.groups()

    # Find fix
    fix = None
    for f in fixes:
      if cmd == f['cmd']:
        fix = f
        break
    if fix is None:
      raise ValueError("no_fix")

    # Render fix
    target_match = re.match(fix['target'], target)
    parsed = fix['fix'].replace(VAR_WHOLE, target_match.group(0))
    parsed = parsed.replace(VAR_INDENT, self.indent_str)
    if len(target_match.groups()) > 0:
      for i, tm in enumerate(target_match.groups()):
        parsed = parsed.replace("$" + str(i + 1), tm)

    # Indent
    output = []
    nl = "\n"
    if self.view.line_endings() == "Windows":
      nl = "\r\n"
    for rl in parsed.splitlines():
      output.append(indent + rl)
    output = nl.join(output)

    # Get cursor index
    cursor_index = output.find(VAR_CURSOR)
    if cursor_index == -1:
      cursor_index = len(output)
    output = output.replace(VAR_CURSOR, "")

    return (output, cursor_index)
