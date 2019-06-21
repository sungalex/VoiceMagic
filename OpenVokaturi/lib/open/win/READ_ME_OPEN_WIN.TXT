## Contents

### The directory "lib/open/win" contains:

- OpenVokaturi statically linkable object files for Windows (.o),
  for 32-bit i686 processors (-win32.o) and 64-bit x86_64 processors (-win64.o)
- OpenVokaturi shareable object libraries for Windows (.dll),
  for 32-bit i686 processors (-win32.dll) and 64-bit x86_64 processors (-win64.dll)

## Use

The easiest way to work with OpenVokaturi in a Windows app is to include the header file (api/Vokaturi.h) as well as the static object code (lib/open/win/OpenVokaturi-3-3-win64.o) in the Visual Studio project of your app.

The easiest way to work with OpenVokaturi with Python on Windows is to import the module api/Vokaturi.py in your Python script, as in the example script in the examples folder. After this you should dynamically load the shareable object library, as in the example script; adapt the path to the library file if necessary.

## More information

To see how to use the OpenVokaturi libraries, consult the Vokaturi developer site (https://developers.vokaturi.com).

## Upgrading

If you need higher emotion recognition accuracy than OpenVokaturi supplies, consider upgrading to VokaturiPlus instead. The VokaturiPlus libraries can basically be used in exactly the same way as the OpenVokaturi libraries.
