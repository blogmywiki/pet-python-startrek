================
PET Python Star Trek
================

About
=====

In 2014 @cosmicr ported a C# version of the 1976 Super Star Trek BASIC game to Python 2.

In 2022 I want a Python version of the 1977 Commodore PET version of the 1971 classic Star Trek game, so I can re-live 
my childhood in the console of whatever computer I'm using and not faff around with emulators and disk images.

Rather than code it from scratch, I decided to fork @cosmicr's port, remove some of the functionality that comes with the Super Star Trek variant and make the game play more like the Commodore PET version.

The PET port of Star Trek was surprisingly good and very simple. It was designed to play more like a video game, using a VDU not a teletype line printer. It even had some simple animation and the BASIC code is so opaque and peculiar to the PET that I think someone in Commodore wrote it, possibly even founder Jack Tramiel's son.

You can read more about the PET Star Trek and why I think a Tramiel was involved in making it in my blog post here: http://www.suppertime.co.uk/blogmywiki/2021/09/one-moment-please-while-i-arrange-the-galaxy/

You can read about the 1971 and 1976 BASIC versions and their port to C# here: https://www.codeproject.com/Articles/28228/Star-Trek-1971-Text-Game

What's different and what's the same and why
============================================

- Commodore PET classic Star Trek plays in 'real time', so if you take too long to enter a command, you lose time and energy etc. My Python version never will work like that because I want to be able to play a game a turn at a time, possibly over a day or two.

- Phasers. I inherited phasers from Super Star Trek. I like phasers. I even think I remember using them, but they're not in the version of PET Star Trek I managed to find. Anyway, I'm keeping them.

- Angles. This version uses horrible polar co-ordinates from 1 to 9. I will try to change this to match the normal 0-359 degrees used by PET Star Trek.

- Access computer. Because the angles are so awful, I'm keeping the navigation and torpedo guidance computer for now.

How to play
===========

I'll add instructions once the gameplay is properly merged and stable.

Search the quadrants of the galaxy to find and destroy Klingon ships before you run out of time or energy.

Use L to get a Long Range Scan of the adjacent quadrants. '369' would mean 3 Klingons, 6 star bases where you can refuel (you wish!) and 9 stars.

C calls up the computer map of every explored quadrant.

M to move. Use distance decimals like 0.1 to move inside a quadrant, whole numbers to move between quadrants.

P to fire phasers - these need no guidance but use a lot of energy.

T to fire photon torepedos. You need to specify an angle. You can use 'A' to access the computer and 'tor' to get the guidance computer to help you.

Try out a very early version of it in your browser here: https://trinket.io/library/trinkets/38adc68043 - this is more like the Super Star Trek port I based this on.


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
- simplified setting shields to work same way as PET version, shields pool shared with energy
- made initial shields value 500
- allow access to cumulative scan from main menu
- added crude help with a diagram of the mad polar co-ordinate system
- improved cumulative scan to be more compact, label axes and show `***` for unexplored quadrants
- moved SRS Y co-ordinate axis labels to left
- initial energy in PET version is 5000, in this Python port it was 3000
- docked status shown as 'D'
- removed random system damage, eg for using the computer too much
- added inverse video for status D & cumulative map current quadrant, blink for status R using ANSI escape sequences
- exception handling eg for torpedo firing direction when you press enter or type a letter, navigation and phaser energy
- sort out how program flow deals with showing SRS or cumulative galaxy map with command prompt
- 2 digit stardates not 4 - shows time remaining removing need for status menu item
- basic polar co-ordinate map added when moving or firing
- single letter commands
- line 11 pays tribute to Leonard Tramiel's hidden REM statement
- stars shown as ● not * (something I find odd about the PET version, I guess they wanted to show off the graphics)
- animate explosions
- co-ordinates are 1-8 in Python Super Star Trek version, they were 0-7 in PET BASIC


To do list
==========
- add proper help
- in PET version if you hit a star you get sent through a space warp, sheilds are stripped - possibly dropped in a random location?
- check navigation, probably needs a total re-write; PET version uses normal angles with 0 being East, 90 North.
- if I fix navigation angles, I can lose the navigation computers
- same for firing torpedos
- remove computer menu
- PET version used real time not turns for stardates, am inclined to leave it as turns but increment on each turn not when you move quadrant
- PET version plays in 'real time', eg if you wait too long to type a fire command you'll be destroyed
- add animtion of moving, firing torpedoes
- translate to Python 3
