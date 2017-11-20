class Dbg:
  def __init__(self, settings):
    self.__is_enabled = settings.get("debug")
    settings.add_on_change("debug", lambda: self.__update_state(settings))

  def lg(self, msg=""):
    if self.__is_enabled:
      if isinstance(msg, str):
        print("[Postfixer] " + msg)
      else:
        print("[Postfixer]:")
        print(msg)

  def __update_state(self, settings):
    self.__is_enabled = settings.get("debug")
