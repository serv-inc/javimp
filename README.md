This program was updated to automatically determine the necessary imports. Only import mode was kept. The rest is from @winterweird's implementation (as is the text below).

**DEPENDENCY NOTE:** This Python script depends on the 3rd party modules `lxml`, and `requests`for some of its functionality. If you do not have these modules installed with your Python installation, you may still use the program; however, updating the Java class database (`lxml`/`requests`) is disabled.

This script has been tested and is known to work with Python versions 2.6, 3.3 and 3.4, and it should theoretically work with any Python 2.x/3.x installation with all the required modules installed.

# javimp.py: Java Importer

A Python script which turns incomplete Java `import` statements (e.g. `import ArrayList;`) into complete ones.

> B-but why?

I'm sick and tired of manually finding where all the things I'm using are located. At the same time, I don't want to use an IDE to get their autocomplete features, because of my less-than-ideal experiences with IDEs and the resulting irrational dislike for them. So I made this, so I can continue to write my code in an editor while not having to struggle too hard to import stuff. It's probably not as good as an IDE, but it's the next best thing.

### DESCRIPTION:

This python script goes through the files passed as arguments and matches classes you attempt to import to classes in a database, and prints out the results it finds. You can update the list of classes through web scraping by running the program with no arguments.

### USAGE:

`python javimp.py [options] [args]`

or

`python javimp.py [args] [options]`

or

`python javimp.py [args] [options] [more args]`

or whatever.

Please take note that aside from `-a` mode, only one mode can be in effect at the time. Precedence is `-i` > `-o` > `-c` > `None`

### OPTIONS:

```
-h: Displays the help message
-a: Show all mode; use in combination with any other option to add any additional matches of a class
    as a commented import
-i: Insert mode; insert the complete import statements directly in one or more .java source file(s)
    Example: Given a source file containing these lines:
        import Activity;
        import Bundle;
    The script would correctly replace this with:
        import android.app.Activity;
        import android.os.Bundle;
-c: Clipboard mode; copies the correct import statements to your clipboard (requires pyperclip module)
-o: File output; Creates a file in your current working directory which contains the correct import statements
```

### NOTE:

The included `java_classes.list` file should contain all of the standard library classes and the classes for Android app development as of 2018-10-18. It may be incomplete, contain erroneous information, or be otherwise unsuitable for your purposes. This software comes with no warranty or guarantee. Use at own risk.

#### UPDATE 2016/06/22 Middle-Of-The-Night:00

Due to a bolt of inspiration that kept me from sleeping tonight, I decided to refactor my code to avoid copypasting pieces of it all over. I reworked my way of going through the arguments to something a little less moronic, and I also added the `-a` option to try to patch up the program's most fatal flaw - namely that it's at risk to import the wrong class simply because it was the match it found first. The `-a` option makes the program include all subsequently discovered matches as commented imports, so if your code doesn't work when you first run the script, you can simply comment out one line and uncomment the next, then try again.

Having done this, I decided to make a script which makes it easier to test whether the code I've written actually works as intended. And Python being cross-platform, obviously I had to make both a Batch script for Windows and a Bash script for Linux. During the making of that script, a post on some stackexchange site made me aware of two ways to actually get a file output à la `cat`, but with syntax highlighting! I'm disproportionately hyped about this. And disproportionately disappointed that there wasn't something like that to be found in DOS's toolkit :/ But at any rate, if anyone wants to try these scripts out, feel free. Not sure if they're useful unless you're developing stuff and want quick testing, but meh.

Anyways, having done all that, I decided to write a little feature list for stuff I wanna do when I get around to it (read: when the world has stopped spinning)...

### TODO-LIST

1. Enclose the "update `java_classes.list`" part of my code in a function.
2. Make that function rely on a file which lets you specify how the web scraping is supposed to work (i.e. which pages to search and what to look for). This would make it a lot easier for users to define their own 3rd party libraries they wish to be able to use with `javimp.py`. It would also make it easier to fix the web scraping algorithm if it should ever break because the site maintainers decide to change something or whatever.
3. Factor out the common pieces of the `-i` mode handling algorithm and the rest, for code reuse.
4. Rewrite this tool in either Java or C/C++ in order to make it possible for people to run it without having to have Python randomly installed on their system. If I ever get around to this, I will probably only implement the `-i` mode of this program.
5. Sometime far, far in the future, I might decide to extend this concept and create an entire toolset for us folks who are stubborn and/or stupid enough to code in Java without an IDE. That's only a maybe, though.

Apart from this, I'll think about what sort of improvements I can make, and add them to my code if they're quick and simple to add, or to my TODO-list if otherwise they are not. And maybe, just maybe, I can ever get around to finish coding the app I was gonna make before I got caught up in making app coding oh so much easier. Good night!
