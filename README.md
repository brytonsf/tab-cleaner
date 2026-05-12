Run run.sh to start the mongo container & run the script.

TODO: Fix this
Traceback (most recent call last):
  File "/opt/homebrew/lib/python3.11/site-packages/aeosa/appscript/reference.py", line 479, in __call__
    return self.AS_appdata.target().event(self._code, params, atts, codecs=self.AS_appdata).send(timeout, sendflags)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/aeosa/aem/aemsend.py", line 92, in send
    raise EventError(errornum, errormsg, eventresult)
aem.aemsend.EventError: Command failed: Can't get reference. (-1728)

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "main.py", line 82, in <module>
    tabs = read_tabs_from_topmost_open_chrome_instance(close = close)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "main.py", line 39, in read_tabs_from_topmost_open_chrome_instance
    tabs = [Tab(obj) for obj in tabs_raw]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "main.py", line 39, in <listcomp>
    tabs = [Tab(obj) for obj in tabs_raw]
            ^^^^^^^^
  File "main.py", line 28, in __init__
    self.url = appleScriptObject.URL()
               ^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/aeosa/appscript/reference.py", line 661, in __call__
    return self.get(*args, **kargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/aeosa/appscript/reference.py", line 515, in __call__
    raise CommandError(self, (args, kargs), e, self.AS_appdata) from e
appscript.reference.CommandError: Command failed:
                OSERROR: -1728
                MESSAGE: Can't get reference.
                OFFENDING OBJECT: app('/Applications/Google Chrome.app').windows.ID('1909312435').tabs.ID('1909313495')
                COMMAND: app('/Applications/Google Chrome.app').windows.ID('1909312435').tabs.ID('1909313495').URL.get()
