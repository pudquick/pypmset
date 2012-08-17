from ctypes import c_uint32, cdll, c_int, c_void_p, POINTER, byref
from CoreFoundation import CFStringCreateWithCString, CFRelease, kCFStringEncodingASCII
from objc import pyobjc_id

libIOKit = cdll.LoadLibrary('/System/Library/Frameworks/IOKit.framework/IOKit')
libIOKit.IOPMAssertionCreateWithName.argtypes = [ c_void_p, c_uint32, c_void_p, POINTER(c_uint32) ]
libIOKit.IOPMAssertionRelease.argtypes = [ c_uint32 ]

def CFSTR(py_string):
    return CFStringCreateWithCString(None, py_string, kCFStringEncodingASCII)

def raw_ptr(pyobjc_string):
    return pyobjc_id(pyobjc_string.nsstring())

def IOPMAssertionCreateWithName(assert_name, assert_level, assert_msg):
    assertID = c_uint32(0)
    p_assert_name = raw_ptr(CFSTR(assert_name))
    p_assert_msg = raw_ptr(CFSTR(assert_msg))
    errcode = libIOKit.IOPMAssertionCreateWithName(p_assert_name,
        assert_level, p_assert_msg, byref(assertID))
    return (errcode, assertID)

IOPMAssertionRelease = libIOKit.IOPMAssertionRelease

kIOPMAssertionTypeNoIdleSleep = "NoIdleSleepAssertion"
kIOPMAssertionLevelOn = 255
reason = "python would like the computer to not idle sleep"

# Stop idle sleep
errcode, assertID = IOPMAssertionCreateWithName(kIOPMAssertionTypeNoIdleSleep,
    kIOPMAssertionLevelOn, reason)

# prove it to yourself with this on the Terminal: pmset -g assertions

# Let it go again
errcode = IOPMAssertionRelease(assertID)