# FindHardCodedStrings
Find Hard Coded Strings from XCode project's Source Code

find_strings.py:
is for iOS project (If source code is in Objective-C):
Python script , searches for hard coded strings in xcode project's source files and replaces it with
NSLocalizedString macro structure in new files. It shows resource key,value pairs on console.

findscript_android.py:
is for Android project (If source code is in Java).
Android script searches for hard coded strings in .java and .xml files and replaces them with StringResManager.getResourceString  and @string/ format. It will show language dictionary on console only in < string name= \ "%s \ " > %s < /string > format.

- Script ignores image files, source file in frameworks

Usage:
-> place the script in the folder, where you project folder is.
-> open script file, there is one # TODO: section, read and add your folder name accordingly and save.
-> execute script:  python scriptname.py
