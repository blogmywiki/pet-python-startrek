================
PET Python Star Trek
================

About
=====

In 2014 @cosmicr ported a C# version of the 1976 Super Star Trek BASIC game to Python 2.

In 2022 I want a Python version of the Commodore PET version of the 1971 classic Star Trek game.

Rather than code it from scratch, I decided to fork @cosmicr's port, remove some of the functionality that comes with the Super Star Trek variant and make the game play more like the Commodore PET version.

The PET port of Star Trek was surprisingly good, designed to play more like a game on a VDU than a teletype. It even had some simple animation and the BASIC code is so opaque and peculiar to the PET that I think someone in Commodore wrote it, possibly even founder Jack Tramiel's son.

You can read more about the PET Star Trek and why I think a Tramiel was involved in my blog post here: http://www.suppertime.co.uk/blogmywiki/2021/09/one-moment-please-while-i-arrange-the-galaxy/


Changes made so far
===================
- removed ASCII art
- added 'ONE MOMENT PLEASE, WHILE I ARRANGE THE GALAXY' message at start
- removed quadrant names
- removed strings.py and folded remaining strings into main program
- re-ordered status to follow PET version
- added clearing screen
- making SRS appear automatically
- removed <> from <E> and <B>, put SRS in a box
- added box round SRS and co-ordinate axis labels
- simplified shields to work same way as PET version
- made initial shields value 500
- improved cumulative scan to be more compact, label axes and show `***` for unexplored quadrants

To do list
==========
- sort out how program flow deals with showing SRS or cumulative galaxy map with command prompt
- ??dock Status
- co-ordinates are 1-8 in Python Super Star Trek version, they were 0-7 in PET BASIC
- initial energy in pet version is 5000, in python it's 3000
- remove random damage, eg for using the computer too much
- remove computer menu
- translate to Python 3
- add proper help
- check navigation, probably needs a total re-write
- move SRS Y co-ordinates to left
- single letter commands
- reverse video where needed, if possible
