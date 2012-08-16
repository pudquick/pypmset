from ctypes import c_uint32, cdll, c_int, c_void_p, POINTER, byref
from ctypes.util import find_library

import CFStringUtil as cfsu
CFSTR = cfsu.create_cfstringref
CFRELEASE = cfsu.release_cfstringref

libIOKit = cdll.LoadLibrary(find_library("/System/Library/Frameworks/IOKit.framework/IOKit"))

libIOKit.IOPMAssertionCreateWithName.argtypes = [ c_void_p, c_uint32, c_void_p, POINTER(c_uint32) ]
libIOKit.IOPMAssertionCreateWithName.restype = c_int
libIOKit.IOPMAssertionRelease.argtypes = [ c_uint32 ]
libIOKit.IOPMAssertionRelease.restype = c_int

kIOPMAssertionTypeNoDisplaySleep = CFSTR("NoDisplaySleepAssertion")
kIOPMAssertionTypeNoIdleSleep = CFSTR("NoIdleSleepAssertion")
kIOPMAssertionLevelOn = c_uint32(255)
kIOPMAssertionLevelOff = c_uint32(0)

assertID = c_uint32(0)
reason = CFSTR("python would like the computer to not idle sleep")

# Stop idle sleep
errcode = libIOKit.IOPMAssertionCreateWithName(kIOPMAssertionTypeNoIdleSleep, kIOPMAssertionLevelOn, reason, byref(assertID))

# Let it go again
errcode = libIOKit.IOPMAssertionRelease(assertID)

# Clean up
CFRELEASE(kIOPMAssertionTypeNoDisplaySleep)
CFRELEASE(kIOPMAssertionTypeNoIdleSleep)
CFRELEASE(reason)
