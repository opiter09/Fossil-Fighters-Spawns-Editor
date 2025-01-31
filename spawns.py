import os
import FreeSimpleGUI as psg
import shutil
import subprocess
import sys
import digOut

f = open(sys.argv[1], "rb")
test = f.read()[12]
f.close()
if (test == ord("Y")):
    rom = "ff1"
else:
    rom = "ffc"

if (os.path.exists("NDS_UNPACK") == False):
    subprocess.run([ "dslazy.bat", "UNPACK", sys.argv[1] ])
    subprocess.run([ "fftool.exe", "NDS_UNPACK/data/map/m" ])
    
if (rom == "ffc"):
    subprocess.run([ "xdelta3-3.0.11-x86_64.exe", "-d", "-f", "-s", "NDS_UNPACK/arm9.bin", "ffc_apFix.xdelta",
        "NDS_UNPACK/arm9x.bin" ])
    if (os.path.exists("NDS_UNPACK/arm9x.bin") == True):
        os.remove("NDS_UNPACK/arm9.bin")
        os.rename("NDS_UNPACK/arm9x.bin", "NDS_UNPACK/arm9.bin") 

if (rom == "ff1"):
    f = open(rom + "_vivoNames.txt", "rt")
    vNames = list(f.read().split("\n"))
    f.close()
    vNamesAlph = vNames.copy()
    vNamesAlph.sort()
    vNames = ["NONE"] + vNames
else:
    f = open(rom + "_kasekiNames_Short.txt", "rt")
    kNames = list(f.read().split("\n"))
    f.close()
    kNamesAlph = [x for x in kNames if x != "Other"]
    for i in range(len(kNamesAlph)):
        kNamesAlph[i] = kNamesAlph[i].replace(" Head", " aHead").replace(" Body", " bBody").replace(" Arms", " cArms").replace(" Legs", " dLegs")
    kNamesAlph.sort() # will be alphabetical, but keep the part order
    for i in range(len(kNamesAlph)):
        kNamesAlph[i] = kNamesAlph[i].replace(" aHead", " Head").replace(" bBody", " Body").replace(" cArms", " Arms").replace(" dLegs", " Legs")    

spawnList = []

if (rom == "ff1"):
    spawns = {}
    for root, dirs, files in os.walk("NDS_UNPACK/data/map/m/bin"):
        for file in files:
            mapN = os.path.join(root, file).split("\\")[-2]
            if ((file == "0.bin") and (os.path.exists("NDS_UNPACK/data/map/e/" + mapN) == True)):
                f = open(os.path.join(root, file), "rb")
                r = f.read()
                f.close()
                point = int.from_bytes(r[0x54:0x58], "little")
                mapName = ""
                mf = open("Map IDs.txt", "rt")
                lines = list(mf.read().split("\n")).copy()
                mf.close()
                for t in lines:
                    if (t != ""):
                        nums = list(t.split(":")[0].replace(", ", ",").split(",")).copy()
                        for n in nums:
                            if (int(mapN) == int(n)):
                                mapName = t.split(": ")[1]
                mapN = mapN + " [" + mapName + "]"
                realP = [ int.from_bytes(r[point:(point + 4)], "little") ]
                loc = point + 4
                while (realP[-1] > 0):
                    realP.append(int.from_bytes(r[loc:(loc + 4)], "little"))
                    loc = loc + 4
                realP = realP[0:-1]
                for val in realP:
                    index = int.from_bytes(r[(val + 4):(val + 8)], "little")
                    if (index == 0):
                        continue
                    else:
                        if (mapN not in spawns.keys()):
                            spawns[mapN] = {}
                            spawnList.append(mapN)
                    if (str(index).zfill(2) not in spawns[mapN].keys()):
                        spawns[mapN][str(index).zfill(2)] = []
                    temp = {}
                    maxFos = int.from_bytes(r[(val + 12):(val + 16)], "little")
                    temp["maxFos"] = [val + 12, maxFos]
                    temp["vivos"] = []
                    numSpawns = int.from_bytes(r[(val + 0x28):(val + 0x2C)], "little")
                    temp["numSpawns"] = numSpawns
                    point3 = int.from_bytes(r[(val + 0x2C):(val + 0x30)], "little")
                    for i in range(numSpawns):
                        point4 = int.from_bytes(r[(val + point3 + (i * 4)):(val + point3 + (i * 4) + 4)], "little")
                        vivoNum = int.from_bytes(r[(val + point4):(val + point4 + 4)], "little")
                        chance = int.from_bytes(r[(val + point4 + 4):(val + point4 + 8)], "little")
                        parts = [
                            val + point4 + 16,
                            int.from_bytes(r[(val + point4 + 16):(val + point4 + 20)], "little"),
                            val + point4 + 20,
                            int.from_bytes(r[(val + point4 + 20):(val + point4 + 24)], "little"),
                            val + point4 + 24,
                            int.from_bytes(r[(val + point4 + 24):(val + point4 + 28)], "little"),
                            val + point4 + 28,
                            int.from_bytes(r[(val + point4 + 28):(val + point4 + 32)], "little")
                        ]
                        temp["vivos"].append([val + point4, vivoNum, val + point4 + 4, chance] + parts)
                    spawns[mapN][str(index).zfill(2)].append(temp)                    
else:
    spawns = {}
    for root, dirs, files in os.walk("NDS_UNPACK/data/map/m/bin/"):
        for file in files:
            mapN = os.path.join(root, file).split("\\")[-2]
            mapN = mapN.split("/")[-1] # it just works
            if ((file == "0.bin") and (os.path.exists("NDS_UNPACK/data/map/e/" + mapN) == True)):
                f = open(os.path.join(root, file), "rb")
                r = f.read()
                f.close()
                point = int.from_bytes(r[0x6C:0x70], "little")
                realP = [ int.from_bytes(r[point:(point + 4)], "little") ]
                loc = point + 4
                while (realP[-1] > 0):
                    realP.append(int.from_bytes(r[loc:(loc + 4)], "little"))
                    loc = loc + 4
                realP = realP[0:-1]
                for val in realP:
                    index = int.from_bytes(r[(val + 2):(val + 4)], "little")
                    if (index == 0):
                        continue
                    else:
                        if (mapN not in spawns.keys()):
                            spawns[mapN] = {}
                            spawnList.append(mapN)
                    if (str(index).zfill(2) not in spawns[mapN].keys()):
                        spawns[mapN][str(index).zfill(2)] = []
                    numTables = int.from_bytes(r[(val + 12):(val + 16)], "little")
                    point3 = int.from_bytes(r[(val + 16):(val + 20)], "little")
                    for i in range(numTables):
                        temp = {}
                        point4 = int.from_bytes(r[(val + point3 + (i * 4)):(val + point3 + (i * 4) + 4)], "little")
                        point5 = int.from_bytes(r[(val + point4 + 12):(val + point4 + 16)], "little")
                        maxFos = int.from_bytes(r[(val + point4 + point5 + 4):(val + point4 + point5 + 8)], "little")
                        temp["maxFos"] = [val + point4 + point5 + 4, maxFos]
                        numWeird = int.from_bytes(r[(val + point4 + point5 + 8):(val + point4 + point5 + 12)], "little")
                        numSpawns = int.from_bytes(r[(val + point4 + point5 + 16):(val + point4 + point5 + 20)], "little")
                        temp["numSpawns"] = numSpawns
                        temp["fossils"] = []
                        startSpawns = val + point4 + point5 + 24 + (numWeird * 2)
                        for j in range(numSpawns):
                            thisStart = startSpawns + (j * 8)
                            dark = r[thisStart]
                            rare = r[thisStart + 1]
                            kasNum = int.from_bytes(r[(thisStart + 2):(thisStart + 4)], "little")
                            spawnChance = int.from_bytes(r[(thisStart + 4):(thisStart + 6)], "little")
                            battleChance = int.from_bytes(r[(thisStart + 6):(thisStart + 8)], "little")
                            temp["fossils"].append([thisStart, dark, thisStart + 1, rare, thisStart + 2, kasNum, thisStart + 4, spawnChance,
                                thisStart + 6, battleChance])
                        spawns[mapN][str(index).zfill(2)].append(temp)

maps = list(spawns.keys()).copy()
for m in maps:
    ind = list(spawns[m].keys()).copy()
    for i in ind:
        if (len(spawns[m][i]) < 3):
            spawns.pop(m)
            spawnList.remove(m)
            break

curr = spawnList[0]
currZ = list(spawns[curr].keys())[0]

def makeLayout():
    global curr
    global currZ
    global spawns

    layout = [
        [ psg.Text("Spawn File:", size = 10), psg.DropDown(spawnList, key = "file", default_value = curr) ],
        [ psg.Text("Zone:", size = 10), psg.DropDown(list(spawns[curr].keys()), key = "zone", default_value = currZ),
            psg.Button("Load", key = "load") ]           
    ]
    cols3 = []
    cols3_scr = []
    for currF in range(len(spawns[curr][currZ])):
        total = 0
        for i in range(spawns[curr][currZ][currF]["numSpawns"]):
            total = total + spawns[curr][currZ][currF]["fossils"][i][7]

        plural = "s"
        if (currF == 1):
            plural = ""
        col = [
            [ psg.Text(str(currF) + " Fossil Chip" + plural + ":") ],
            [ psg.Text("Max Fossils:", size = 10), psg.Input(default_text = spawns[curr][currZ][currF]["maxFos"][1],
            key = str(currF) + "maxFos", size = 5, enable_events = True) ],          
        ]
        if (rom == "ffc"):
            col = col + [[ psg.Text("Spawn Chance Total:", size = 16), psg.Text(str(total), key = str(currF) + "_SCT") ]]
        colR = []
        for i in range(spawns[curr][currZ][currF]["numSpawns"]):
            # print(i)
            if (rom == "ff1"):
                row = [ # yes, I know this is formatted as a column ulol
                    psg.Text("Vivosaur:"),
                    psg.DropDown(vNamesAlph, key = str(currF) + "vivo" + str(i),
                        default_value = vNames[spawns[curr][currZ][currF]["vivos"][i][1]]),
                    psg.Text("% Chance:"),
                    psg.Input(default_text = spawns[curr][currZ][currF]["vivos"][i][3], key = str(currF) + "chance" + str(i),
                        size = 5, enable_events = True)
                ]
                row2 = [
                    psg.Push(),
                    psg.Text("Parts %:"),
                    psg.Input(default_text = spawns[curr][currZ][currF]["vivos"][i][5], key = str(currF) + "part1" + str(i),
                        size = 5, enable_events = True),
                    psg.Input(default_text = spawns[curr][currZ][currF]["vivos"][i][7], key = str(currF) + "part2" + str(i),
                        size = 5, enable_events = True),
                    psg.Input(default_text = spawns[curr][currZ][currF]["vivos"][i][9], key = str(currF) + "part3" + str(i),
                        size = 5, enable_events = True),
                    psg.Input(default_text = spawns[curr][currZ][currF]["vivos"][i][11], key = str(currF) + "part4" + str(i),
                        size = 5, enable_events = True),
                    psg.Push()
                ]
                colR.append(row)
                colR.append(row2)                   
            else:
                row = [ # yes, I know this is formatted as a column ulol
                    psg.Text("Dark:"),
                    psg.DropDown(["N/A", "No", "Yes"], key = str(currF) + "dark" + str(i),
                        default_value = (["N/A", "No", "Yes"])[spawns[curr][currZ][currF]["fossils"][i][1]]),
                    psg.Text("Rare:"),
                    psg.DropDown(["N/A", "No", "Yes"], key = str(currF) + "rare" + str(i),
                        default_value = (["N/A", "No", "Yes"])[spawns[curr][currZ][currF]["fossils"][i][3]]),
                     psg.Text("Fossil:"),
                    psg.DropDown(kNamesAlph, key = str(currF) + "fossil" + str(i),
                        default_value = kNames[spawns[curr][currZ][currF]["fossils"][i][5]])
                ]
                row2 = [
                    psg.Push(),
                    psg.Text("Spawn Chance:"),
                    psg.Input(default_text = spawns[curr][currZ][currF]["fossils"][i][7], key = str(currF) + "spawn" + str(i),
                        size = 5, enable_events = True),
                    psg.Text("Battle %:"),
                    psg.Input(default_text = spawns[curr][currZ][currF]["fossils"][i][9], key = str(currF) + "battle" + str(i),
                        size = 5, enable_events = True),
                    psg.Push()
                ]
                colR.append(row)
                colR.append(row2)
        if (rom == "ff1"):
            cols3.append(psg.Column(col + colR))
            cols3.append(psg.Column([[psg.Text("", size = 0)]]))
        else:
            col[0] = col[0] + [psg.Text("", size = 35)]
            col[1] = col[1] + [psg.Text("", size = 35)]
            col[2] = col[2] + [psg.Text("", size = 35)]
            cols3.append(psg.Column(col))
            cols3_scr.append(psg.Column(colR, scrollable = True, vertical_scroll_only = True))
    layout = layout + [psg.vtop(cols3)] + [psg.vtop(cols3_scr)]
    layout = [[ psg.Button("Save File", key = "save"), psg.Button("Recompress All", key = "recomp"), 
        psg.Button("Rebuild ROM", key = "rebuild") ]] + layout
    return(layout)

def applyValues(values):
    global curr
    global currZ
    global spawns

    for currF in range(len(spawns[curr][currZ])):
        try: # these all need exceptions either to handle non-integers or the buttons not existing for one ROM or the other
            spawns[curr][currZ][currF]["maxFos"][1] = max(0, min(int(values[str(currF) + "maxFos"]), 65535))
        except:
            pass    
        for i in range(spawns[curr][currZ][currF]["numSpawns"]):
            try:
                spawns[curr][currZ][currF]["vivos"][i][1] = vNames.index(values[str(currF) + "vivo" + str(i)])
            except:
                pass
            try:
                spawns[curr][currZ][currF]["vivos"][i][3] = max(0, min(int(values[str(currF) + "chance" + str(i)]), 100))
            except:
                pass
            try:
                spawns[curr][currZ][currF]["vivos"][i][5] = max(0, min(int(values[str(currF) + "part1" + str(i)]), 100))
            except:
                pass
            try:
                spawns[curr][currZ][currF]["vivos"][i][7] = max(0, min(int(values[str(currF) + "part2" + str(i)]), 100))
            except:
                pass
            try:
                spawns[curr][currZ][currF]["vivos"][i][9] = max(0, min(int(values[str(currF) + "part3" + str(i)]), 100))
            except:
                pass
            try:
                spawns[curr][currZ][currF]["vivos"][i][11] = max(0, min(int(values[str(currF) + "part4" + str(i)]), 100))
            except:
                pass
                
            try:
                spawns[curr][currZ][currF]["fossils"][i][1] = (["N/A", "No", "Yes"]).index(values[str(currF) + "dark" + str(i)])
            except:
                pass
            try:
                spawns[curr][currZ][currF]["fossils"][i][3] = (["N/A", "No", "Yes"]).index(values[str(currF) + "rare" + str(i)])
            except:
                pass
            try:
                spawns[curr][currZ][currF]["fossils"][i][5] = kNames.index(values[str(currF) + "fossil" + str(i)])
            except:
                pass
            try:
                spawns[curr][currZ][currF]["fossils"][i][7] = max(0, min(int(values[str(currF) + "spawn" + str(i)]), 65535))
            except:
                pass
            try:
                spawns[curr][currZ][currF]["fossils"][i][9] = max(0, min(int(values[str(currF) + "battle" + str(i)]), 65535))
            except:
                pass

def saveFile():
    global curr
    global currZ
    global spawns

    path = "NDS_UNPACK/data/map/m/bin/" + curr[0:4] + "/0.bin"
    f = open(path, "rb")
    r = f.read()
    f.close()
    f = open(path, "wb")
    f.close()
    f = open(path, "ab")
    
    tupleList = []
    for currF in range(len(spawns[curr][currZ])):
        tupleList.append( (spawns[curr][currZ][currF]["maxFos"][0], spawns[curr][currZ][currF]["maxFos"][1]) )
        if (rom == "ff1"):
            for i in range(spawns[curr][currZ][currF]["numSpawns"]):
                tupleList.append( (spawns[curr][currZ][currF]["vivos"][i][0], spawns[curr][currZ][currF]["vivos"][i][1]) )
                tupleList.append( (spawns[curr][currZ][currF]["vivos"][i][2], spawns[curr][currZ][currF]["vivos"][i][3]) )
                tupleList.append( (spawns[curr][currZ][currF]["vivos"][i][4], spawns[curr][currZ][currF]["vivos"][i][5]) )
                tupleList.append( (spawns[curr][currZ][currF]["vivos"][i][6], spawns[curr][currZ][currF]["vivos"][i][7]) )
                tupleList.append( (spawns[curr][currZ][currF]["vivos"][i][8], spawns[curr][currZ][currF]["vivos"][i][9]) )
                tupleList.append( (spawns[curr][currZ][currF]["vivos"][i][10], spawns[curr][currZ][currF]["vivos"][i][11]) )
        else:
            for i in range(spawns[curr][currZ][currF]["numSpawns"]):
                tupleList.append( (spawns[curr][currZ][currF]["fossils"][i][0], spawns[curr][currZ][currF]["fossils"][i][1]) )
                tupleList.append( (spawns[curr][currZ][currF]["fossils"][i][2], spawns[curr][currZ][currF]["fossils"][i][3]) ) 
                tupleList.append( (spawns[curr][currZ][currF]["fossils"][i][4], spawns[curr][currZ][currF]["fossils"][i][5]) )
                tupleList.append( (spawns[curr][currZ][currF]["fossils"][i][6], spawns[curr][currZ][currF]["fossils"][i][7]) )
                tupleList.append( (spawns[curr][currZ][currF]["fossils"][i][8], spawns[curr][currZ][currF]["fossils"][i][9]) )   
    tupleList.sort()
    f.write(r[0:tupleList[0][0]])
    for i in range(len(tupleList) - 1):
        if ((tupleList[i + 1][0] - tupleList[i][0]) == 1):
            f.write(tupleList[i][1].to_bytes(1, "little"))
        else:
            f.write(tupleList[i][1].to_bytes(2, "little"))
            f.write(r[(tupleList[i][0] + 2):tupleList[i + 1][0]])
    f.write(tupleList[-1][1].to_bytes(2, "little"))
    f.write(r[(tupleList[-1][0] + 2):])
    f.close()
    subprocess.run([ "fftool.exe", "compress", "NDS_UNPACK/data/map/m/bin/" + curr[0:4], "-c", "None", "-c", "None",
        "-i", "0.bin", "-o", "NDS_UNPACK/data/map/m/" + curr[0:4] ])

    psg.popup("File saved!", font = "-size 12")

res = makeLayout()
window = psg.Window("", res, grab_anywhere = True, resizable = True, font = "-size 12")

while True:
    event, values = window.read()
    # See if user wants to quit or window was closed
    if (event == psg.WINDOW_CLOSED) or (event == "Quit"):
        break
    elif (event == "load"):
        curr = values["file"]
        currZ = values["zone"]
        window.close()
        res = makeLayout()
        window = psg.Window("", res, grab_anywhere = True, resizable = True, font = "-size 12")
    elif (event == "apply"):
        applyValues(values)
        window.close()
        res = makeLayout()
        window = psg.Window("", res, grab_anywhere = True, resizable = True, font = "-size 12")
    elif (event == "save"):
        applyValues(values)
        saveFile()
    elif (event == "rebuild"):
        applyValues(values)
        saveFile()
        digOut.output(rom)
        shutil.move("NDS_UNPACK/data/map/m/bin/", "bin/")
        subprocess.run([ "dslazy.bat", "PACK", "out.nds" ])
        shutil.move("bin/", "NDS_UNPACK/data/map/m/bin/")
        subprocess.run([ "xdelta3-3.0.11-x86_64.exe", "-e", "-f", "-s", sys.argv[1], "out.nds", "out.xdelta" ])
        psg.popup("You can now play out.nds!", font = "-size 12")
        break
    elif (event == "recomp"):
        applyValues(values)
        saveFile()
        for root, dirs, files in os.walk("NDS_UNPACK/data/map/m/bin"):
            for file in files:
                if (file == "0.bin"):
                    f = open(os.path.join(root, file), "rb")
                    r = f.read()
                    f.close()
                    spawnN = os.path.join(root, file).split("\\")[-2]
                    subprocess.run([ "fftool.exe", "compress", "NDS_UNPACK/data/map/m/bin/" + spawnN, "-c", "None", "-c",
                        "None", "-i", "0.bin", "-o", "NDS_UNPACK/data/map/m/" + spawnN ])
        psg.popup("Files recompressed! Don't forget to rebuild!", font = "-size 12")
    elif (event[1:6] == "spawn"):
        for currF in range(len(spawns[curr][currZ])):
            total = 0
            for i in range(spawns[curr][currZ][currF]["numSpawns"]):
                try:
                    total = total + max(0, min(int(values[str(currF) + "spawn" + str(i)]), 65535))
                except:
                    pass
            window[str(currF) + "_SCT"].update(str(total))