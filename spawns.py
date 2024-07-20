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

if (rom == "ff1"):
    f = open(rom + "_vivoNames.txt", "rt")
    vNames = list(f.read().split("\n"))
    f.close()
    vNamesAlph = vNames.copy()
    vNamesAlph.sort()
    vNames = ["NONE"] + vNames
else:
    f = open(rom + "_kasekiNames.txt", "rt")
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
                        temp["vivos"].append([val + point4, vivoNum, val + point4 + 4, chance])
                    spawns[mapN][str(index).zfill(2)].append(temp)
else:
    pass

curr = spawnList[0]
currZ = list(spawns[curr].keys())[0]
currF = "00"

def makeLayout():
    global curr
    global currZ
    global currF
    global spawns

    layout = [
        [ psg.Text("Spawn File:", size = 10), psg.DropDown(spawnList, key = "file", default_value = curr) ],
        [ psg.Text("Zone:", size = 10), psg.DropDown(list(spawns[curr].keys()), key = "zone", default_value = currZ) ],
        [ psg.Text("Fossil Chips:", size = 10), psg.DropDown(["00", "01", "02"], key = "chips", default_value = currF),
            psg.Button("Load", key = "load") ],
        [ psg.Text("Max Fossils:", size = 10), psg.Input(default_text = spawns[curr][currZ][int(currF)]["maxFos"][1],
            key = "maxFos", size = 5, enable_events = True) ]            
    ]
    for i in range(spawns[curr][currZ][int(currF)]["numSpawns"]):
        # print(i)
        if (rom == "ff1"):
            row = [ # yes, I know this is formatted as a column ulol
                psg.Text("Vivosaur:"),
                psg.DropDown(vNamesAlph, key = "vivo" + str(i),
                    default_value = vNames[spawns[curr][currZ][int(currF)]["vivos"][i][1]]),
                psg.Text("% Chance:"),
                psg.Input(default_text = spawns[curr][currZ][int(currF)]["vivos"][i][3], key = "chance" + str(i), size = 5,
                    enable_events = True)
            ]
        else:
            pass
        layout = layout + [row]
    layout = layout + [[ psg.Button("Save File", key = "save"), psg.Button("Recompress All", key = "recomp"),
        psg.Button("Rebuild ROM", key = "rebuild") ]]
    return(layout)

def applyValues(values):
    global curr
    global currZ
    global currF
    global spawns

    try: # these all need exceptions either to handle non-integers or the buttons not existing for one ROM or the other
        spawns[curr][currZ][int(currF)]["maxFos"][1] = max(0, min(int(values["maxFos"]), 65535))
    except:
        pass    
    for i in range(spawns[curr][currZ][int(currF)]["numSpawns"]):
        try:
            spawns[curr][currZ][int(currF)]["vivos"][i][1] = vNames.index(values["vivo" + str(i)])
        except:
            pass
        try:
            spawns[curr][currZ][int(currF)]["vivos"][i][3] = max(0, min(int(values["chance" + str(i)]), 100))
        except:
            pass

def saveFile():
    global curr
    global currZ
    global currF
    global spawns

    if (rom == "ff1"):
        path = "NDS_UNPACK/data/map/m/bin/" + curr[0:4] + "/0.bin"
        f = open(path, "rb")
        r = f.read()
        f.close()
        f = open(path, "wb")
        f.close()
        f = open(path, "ab")
        
        tupleList = [ (spawns[curr][currZ][int(currF)]["maxFos"][0], spawns[curr][currZ][int(currF)]["maxFos"][1]) ]
        for i in range(spawns[curr][currZ][int(currF)]["numSpawns"]):
            tupleList.append( (spawns[curr][currZ][int(currF)]["vivos"][i][0], spawns[curr][currZ][int(currF)]["vivos"][i][1]) )
            tupleList.append( (spawns[curr][currZ][int(currF)]["vivos"][i][2], spawns[curr][currZ][int(currF)]["vivos"][i][3]) )
        tupleList.sort()
        f.write(r[0:tupleList[0][0]])
        for i in range(len(tupleList) - 1):
            f.write(tupleList[i][1].to_bytes(4, "little"))
            f.write(r[(tupleList[i][0] + 4):tupleList[i + 1][0]])
        f.write(tupleList[-1][1].to_bytes(4, "little"))
        f.write(r[(tupleList[-1][0] + 4):])
        f.close()
        subprocess.run([ "fftool.exe", "compress", "NDS_UNPACK/data/map/m/bin/" + curr[0:4], "-c", "None", "-c", "None",
            "-i", "0.bin", "-o", "NDS_UNPACK/data/map/m/" + curr[0:4] ])
    else:
        pass
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
        currF = values["chips"]
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