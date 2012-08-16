from ctypes import c_uint32, cdll, c_int, c_void_p, POINTER, byref
from ctypes.util import find_library
from CoreFoundation import CFStringCreateWithCString, CFRelease, kCFStringEncodingASCII
from objc import pyobjc_id

libIOKit = cdll.LoadLibrary(find_library("/System/Library/Frameworks/IOKit.framework/IOKit"))
libIOKit.IOPMAssertionCreateWithName.argtypes = [ c_void_p, c_uint32, c_void_p, POINTER(c_uint32) ]
libIOKit.IOPMAssertionCreateWithName.restype = c_int
libIOKit.IOPMAssertionRelease.argtypes = [ c_uint32 ]
libIOKit.IOPMAssertionRelease.restype = c_int

def CFSTR(py_string):
    return CFStringCreateWithCString(None, py_string, kCFStringEncodingASCII)

def raw_ptr(pyobjc_string):
    return pyobjc_id(pyobjc_string.nsstring())

kIOPMAssertionTypeNoDisplaySleep = CFSTR("NoDisplaySleepAssertion")
kIOPMAssertionTypeNoIdleSleep = CFSTR("NoIdleSleepAssertion")
kIOPMAssertionLevelOn = c_uint32(255)
kIOPMAssertionLevelOff = c_uint32(0)
assertID = c_uint32(0)
reason = CFSTR("python would like the computer to not idle sleep")

# Stop idle sleep
errcode = libIOKit.IOPMAssertionCreateWithName(raw_ptr(kIOPMAssertionTypeNoIdleSleep),
    kIOPMAssertionLevelOn, raw_ptr(reason), byref(assertID))

# Let it go again
errcode = libIOKit.IOPMAssertionRelease(assertID)

# Clean up
CFRelease(kIOPMAssertionTypeNoDisplaySleep)
CFRelease(kIOPMAssertionTypeNoIdleSleep)
CFRelease(reason)
