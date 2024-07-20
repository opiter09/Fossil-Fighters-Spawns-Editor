# Fossil-Fighters-Spawn-Editor
This is a simple graphical editor for FF1 (and eventually FFC) dig site fossil spawns.

To use, just drag and drop a ROM onto spawns.exe. If the folder NDS_UNPACK does not exist, it will make that folder and unpack the ROM
into it; be patient as it does so. Then, you can use the editor. It should be mostly self-eplanatory, but please
note the following:
- The load button loads the selected combination of file, zone, and fossil chip. Reloading, even for the same file, will erase
  your unsaved edits, so make sure to use Save File first (which saves the entire file, to be clear).
- To get an easier grasp on the files and especially the zones, check out FF1-E-Maps-Color.zip and FFC-E-Maps-Color.zip,
  which are all the digsites. in the game color-coded by zone.
- Only the Save and Rebuild buttons actually save the file. Apply only changes the data in the editor, while Load does not change
  anything at all (but it does therefore retain your changes in the editor)
- The Recompress All button is for debugging purposes ONLY. It is extremely slow, and should not be necessary unless you are trying
  to help me figure out a problem
  
Also, as with my other tools, the ROM file MUST be in the same folder as teams.exe, or it will not work correctly.
  
To download this, if you are confused, press the Green "Code" button in the top right, then choose "Download ZIP."

Finally, many thanks to EchoSpaceZ, for patiently testing this editor and helping me iron out all of the bugs (for FF1 at least).

# Source Codes
- FFTool: https://github.com/jianmingyong/Fossil-Fighters-Tool
- NDSTool: https://github.com/devkitPro/ndstool (this is a later version; the one used here came without a license as part of DSLazy)
- xdelta: https://github.com/jmacd/xdelta-gpl