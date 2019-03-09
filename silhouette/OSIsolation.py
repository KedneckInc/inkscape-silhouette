from __future__ import print_function

import abcplus as abc

import sys
import importlib

class OSIsolation:
    """
    OS Isolation - Contains all of the OS Specific code, in a singleton.
    """
    instance = None

    class __OSCommon(object, metaclass=abc.ABCMeta):
        """
        The parent class for the individual OS classes.
        """

        os_type = None
        # The OS Type, as set by the constructor.

        usb_context = None
        # Only Darwin uses usb_context, as far as I know, because only
        # Darwin sets the value when it's done loading imports for
        # usb.

        usb_vi = None
        usb_vi_string = None
        # Darwin cannot use these, because purportedly it uses libusb1
        # which does not support 'usb.version_info[0]'.

        def __init__(self):
            """
            Initialize the abstract class.

            Parameter 'ost' is a string that identifies the os.
            """
            super().__init__()
            self.os_type = sys.platform.lower()

        def usb_version_info(self):
            try:
                try:
                    self.usb_vi = usb.version_info[0]
                    self.usb_vi_str = str(usb.version_info)
                except AttributeError as e1:
                    self.usb_vi = 0
                    if os_type.startswith('win'):
                        self.usb_vi = 1
                        pass # windows does not seem to detect the usb.version , gives attribute error. Other tests of pyusb work, pyusb is installed.
                    self.usb_vi_str = 'unknown'


                    if self.usb_vi < 1:
                        print("Your python usb module appears to be "+self.usb_vi_str+" -- We need version 1.x", file=sys.stderr)
                        print("For Debian 8 try:\n  echo > /etc/apt/sources.list.d/backports.list 'deb http://ftp.debian.org debian jessie-backports main\n  apt-get update\n  apt-get -t jessie-backports install python-usb", file=sys.stderr)
                        print("\n\n\n", file=sys.stderr)
                        print("For Ubuntu 14.04try:\n  pip install pyusb --upgrade", file=sys.stderr)
                        print("\n\n\n", file=sys.stderr)
                        sys.exit(1)
                        sys.exit(1)
            except NameError as e2:
                pass #on OS X usb.version_info[0] will always fail as libusb1 is being used


    class Win(__OSCommon):
        """
        Class for windows.
        """
        def __init__(self):
            super().__init()
            globals()['usb'] = importlib.import_module("core", "usb")
            self.usb_version_info()

    class Darwin(__OSCommon):
        """
        Class for OS X.
        """
        def __init__(self):
            super().__init__()
            globals()['usb1'] = importlib.import_module("usb1")
            globals()['usb'] = importlib.import_module("core","usb")
            self.usb_context = usb1.USBContext()
            self.usb_version_info()

    class Linux(__OSCommon):
        """
        Class for Linux.
        """
        def __init__(self):
            super().__init__()
            try:
                globals()['usb'] = importlib.import_module("core","usb")
            except Exception as e1:
                try:
                    globals()['usb'] = importlib.import_module("libusb1")
                except Exception as e2:
                    try:
                        globals()['usb'] = importlib.import_module("usb")
                    except Exception as e3:
                        print("The python usb module could not be found. Try", file=sys.stderr)
                        print("\t sudo zypper in python-usb \t\t# if you run SUSE", file=sys.stderr)
                        print("\t sudo apt-get install python-usb   \t\t# if you run Ubuntu", file=sys.stderr)
                        print("\n\n\n", file=sys.stderr)
                        raise e3;
            self.usb_version_info()


    def __init__(self):
        """
        Get the singleton.
        """
        if not OSIsolation.instance:
            sys_platform = sys.platform.lower()
            if sys_platform.startswith('win'):
                OSIsolation.instance = OSIsolation.Win()
            elif sys_platform.startswith('darwin'):
                OSIsolation.instance = OSIsolation.Darwin()
            elif sys_platform.startswith('linux'):
                OSIsolation.instance = OSIsolation.Linux()
            else:
                raise Exception("OSIsolation Error", "Unrecognized OS %s" % sys_platform)
        self

    def __getattr__(self,name):
        return getattr(self.instance, name)
