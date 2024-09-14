# Fossil-Fighters-Spawn-Editor
This is a simple graphical editor for FF1 and FFC dig site fossil spawns.

You MUST put the ROM in the same folder as the exe, or it won't work.

To use, just drag and drop a ROM onto spawns.exe. If the folder NDS_UNPACK does not exist, it will make that folder and unpack the
ROM into it; be patient as it does so. Then, you can use the editor. It should be mostly self-eplanatory, but please
note the following:
- This editor does not let you Add or Remove spawns, only Change existing ones. This is because the map files are "pointers all
  the way down", and I don't feel like untangling it all
- The editor makes no effort to make sure things add up to 100%. So just make sure not to have it add up to less and crash the game
  or something
- The load button loads the selected combination of file and zone. Reloading, even for the same file, will erase your unsaved
  edits, so make sure to use Save File first (which saves the entire file, to be clear)
- To get an easier grasp on the files and especially the zones, check out FF1-E-Maps-Color.zip and FFC-E-Maps-Color.zip,
  which are all the digsites. in the game color-coded by zone
- In order to fit all three chips in horizontally, certain FFC fossil names had to be shortened (only in the tool; the digsite
  output still uses the full names). The main one to remember is that "Dr." is short for "Dropping"
- As seems to be a tradition at this point, FF1 only lets you edit vivosaur spawns (so no jewels, droppings, etc.) because I
  can't find the rest
- Upon rebuilding, the tool will generate a file named ff1_digsiteOutputNew.txt or ffc_digsiteOutputNew.txt. This will show all of
  the spawn locations of the new ROM (to make distributing hacks and whatnot easier)
- The Recompress All button is for debugging purposes ONLY. It is extremely slow, and should not be necessary unless you are trying
  to help me figure out a problem
  
To download this, if you are confused, press the Green "Code" button in the top right, then choose "Download ZIP."

Finally, many thanks to EchoSpaceZ, for patiently testing this editor and helping me iron out all of the bugs (for FF1 at least).

# Source Codes
- FFTool: https://github.com/jianmingyong/Fossil-Fighters-Tool
- NDSTool: https://github.com/devkitPro/ndstool (this is a later version; the one used here came without a license as part of DSLazy)
- xdelta: https://github.com/jmacd/xdelta-gpl