#!/usr/bin/env python
# javimp.py

# find probable java import statements for a given list of
# classes specified by root name

import sys, os, fileinput, re, subprocess
MISSING_3RD_PARTY_MODULES = []

try:
    from lxml import html
except ImportError:
    MISSING_3RD_PARTY_MODULES.append("lxml")
try:
    import requests
except ImportError:
    MISSING_3RD_PARTY_MODULES.append("requests")

HELP_MESSAGE_STRING = """
DESCRIPTION:

This python script tries to auto-import the Java files to classes in a
database, and automatically adds them. You can update the list of
classes through web scraping by running the program with no arguments.

USAGE:
python  # update database
or
python %s JavaFile.java [| otherJavaFiles.java]  # auto-import


OPTIONS:
    -h: Displays this help message

NOTE: The included java_classes.list file should contain all of the standard
library classes and the classes for Android app development as of 2018.
It may be incomplete, contain erroneous information, or be otherwise unsuitable
for your purposes. This software comes with no warranty or guarantee. Use at
own risk.
""" %(sys.argv[0])

FILELOCATION = os.path.dirname(os.path.abspath(__file__))


if __name__ == '__main__':
    if "-h" in sys.argv:
        print(HELP_MESSAGE_STRING)
        sys.exit()
    if (MISSING_3RD_PARTY_MODULES):
        sys.stderr.write("Warning - 3rd party modules missing: " + ", ".join(MISSING_3RD_PARTY_MODULES) + "\n")
        sys.stderr.write("Some of this program's functionality will not be available.\n\n")
    
    includeAllMatches = True
    mode = "i"
    
    if len(sys.argv) == 1:
        # only python script supplied
        # update source list
        if not ("lxml" in MISSING_3RD_PARTY_MODULES or "requests" in MISSING_3RD_PARTY_MODULES):
            print("Updating list of classes. This may take a little while...")
            
            # backwards compatible way of not printing a newline at the end
            sys.stdout.write("Fetching Java standard library classes...")
            sys.stdout.flush()
            
            page = requests.get("http://docs.oracle.com/javase/7/docs/api/allclasses-frame.html")
            tree = html.fromstring(page.content)
            
            allStdlibClasses = [a.replace(".html", "").replace("/", ".") for a in tree.xpath('//a[@target="classFrame"]/@href')]
            
            sys.stdout.write("\nFetching Android API classes...")
            sys.stdout.flush()
            
            page = requests.get("https://developer.android.com/reference/classes.html")
            tree = html.fromstring(page.content)
            
            allAndroidClasses = [a.replace("https://developer.android.com/reference/", "").replace(".html", "").replace("/", ".") for a in tree.xpath('//td[@class="jd-linkcol"]/a/@href')]
            allClasses = set(allStdlibClasses+allAndroidClasses)
            
            with open(os.path.join(FILELOCATION, "java_classes.list"), "w") as classlist:
                for a in allClasses:
                    classlist.write(a + "\n")
            
            print("\nList of classes to search for updated.")
        else:
            print("Error - missing modules: " + ("lxml and requests" if "requests" in MISSING_3RD_PARTY_MODULES else "lxml") if "lxml" in MISSING_3RD_PARTY_MODULES else "requests")
    else:
        for i in range(1, len(sys.argv)):
            if sys.argv[i].startswith("-"):
                # option, we don't wanna deal with this
                continue
            found = False # used if includeAllMatches
            javac = subprocess.Popen(["javac", sys.argv[i]],
                                     stderr=subprocess.PIPE)
            (out, err) = javac.communicate()
            to_import = set()
            for line in err.decode().split("\n"):
                if "symbol:" in line:
                    to_import.add(line.split(" ")[-1])

            # insert mode is special, so we handle it separately
            for line in fileinput.input(sys.argv[i], inplace=True):
                while to_import:
                    current = to_import.pop()
                    possibles = []
                    with open(os.path.join(FILELOCATION, "java_classes.list"),
                              "r") as classlist:
                        for cls in classlist:
                            if cls.endswith("." + current + "\n"):
                                possibles.append(cls.rstrip("\n"))
                    try:
                        out = "import {};".format(possibles[0])
                    except IndexError:
                        sys.stderr.write("no import found for: " + current)
                        sys.stderr.write("call this without files to update")
                        continue
                    if possibles[1:]:
                        out += "  // alternative imports:"
                        for item in possibles[1:]:
                            out += " " + item
                    out += "\n"
                    sys.stdout.write(out)

                    # A NOTE ON FILEINPUT:
                    #
                    # With the inplace option set to True, fileinput backs up
                    # the file, and sets sys.stdout to the original file for the
                    # duration of the loop. Any calls to sys.stdout.write or
                    # print will therefore be written on top of the original
                    # file.
                found = False
                if line.startswith("import"):
                    with open(os.path.join(FILELOCATION, "java_classes.list"), "r") as classlist:
                        for c in classlist:
                            if c.rstrip().endswith(".%s" %re.sub("import |;", "", line.rstrip())):
                                if found:
                                    # multiple matches; add new matches as comments just in case
                                    # note how found is set to True AFTER this, so if this is the
                                    # first class found, it will still be False from earlier
                                    sys.stdout.write("//")
                                    
                                sys.stdout.write("import %s;\n" %c.rstrip())
                                found = True
                                if not includeAllMatches:
                                    break # fuck it, let's just hope it's the right one
                if not found:
                        # 1) There was no match for the attempted import
                        # 2) The line didn't start with import, so we jumped straight here
                        # In either case, insert the line as it was
                    sys.stdout.write(line)
