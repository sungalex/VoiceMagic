## Contents

### The directory "lib/open/linux" can contain:

- OpenVokaturi statically linkable object file for Linux (.o),
  for 64-bit x86_64 processors (-linux64.o)
- OpenVokaturi shareable object library for Linux (.so),
  for 64-bit x86_64 processors (-linux64.so)
- OpenVokaturi statically linkable object file for ARM Linux (.o),
  for 64-bit ARM processors (-linux_arm64.o)

## Use

The easiest way to work with OpenVokaturi in a Linux app is to include the header file (api/Vokaturi.h) as well as the object file (lib/open/linux/OpenVokaturi-3-3-linux64.o or lib/open/linux/OpenVokaturi-3-3-linux_arm64.o) in your project.

The easiest way to work with OpenVokaturi with Python on Linux is to import the module api/Vokaturi.py in your Python script, as in the example script in the examples folder. After this you should dynamically load the shareable object library, as in the example script; adapt the path to the library file if necessary.

## More information

To see how to use the OpenVokaturi libraries, consult the Vokaturi developer site (https://developers.vokaturi.com).

## Upgrading

If you need higher emotion recognition accuracy than OpenVokaturi supplies, consider upgrading to VokaturiPlus instead. The VokaturiPlus libraries can basically be used in exactly the same way as the OpenVokaturi libraries.
