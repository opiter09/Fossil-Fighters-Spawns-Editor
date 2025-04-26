import os

def ff1_DO():
    text = open("ff1_digsiteOutputNew.txt", "wt")
    text.close()
    text = open("ff1_digsiteOutputNew.txt", "at")
    for root, dirs, files in os.walk("NDS_UNPACK/data/map/m/bin"):
        for file in files:
            if (file == "0.bin"):
                f = open(os.path.join(root, file), "rb")
                r = f.read()
                f.close()
                numTables = int.from_bytes(r[0x50:0x54], "little")
                point = int.from_bytes(r[0x54:0x58], "little")
                mapN = os.path.join(root, file).split("\\")[-2]
                mf = open("ff1_mapNames.txt", "rt")
                lines = list(mf.read().split("\n")).copy()
                for t in lines:
                    if (t != ""):
                        nums = list(t.split(":")[0].replace(", ", ",").split(",")).copy()
                        for n in nums:
                            if (int(mapN.split(" [")[0]) == int(n)):
                                mapN = mapN + " [" + t.split(": ")[1] + "]"
                f = open("ff1_vivoNames.txt", "rt")
                vivoNames = [""] + list(f.read().split("\n")).copy()
                f.close()
                realP = []
                loc = point
                for i in range(numTables):
                    realP.append(int.from_bytes(r[loc:(loc + 4)], "little"))
                    loc = loc + 4
                check = 0
                for val in realP:
                    index = int.from_bytes(r[(val + 4):(val + 8)], "little")
                    if (index == 0):
                        continue
                    else:
                        if (check == 0):
                            check = 1
                            text.write(mapN + ":\n")
                    text.write("\tZone " + str(index).zfill(2) + ":\n")
                    chip = int.from_bytes(r[(val + 8):(val + 12)], "little")
                    if (chip in [0x6F, 0x70, 0x71]):
                        chip = str(chip - 0x6F)
                    else:
                        chip = "?"
                    maxFos = int.from_bytes(r[(val + 12):(val + 16)], "little")
                    text.write("\t\tFossil Chips Needed: " + chip + "\n")
                    text.write("\t\tMax Spawns: " + str(maxFos) + "\n")
                    numSpawns = int.from_bytes(r[(val + 0x28):(val + 0x2C)], "little")
                    point3 = int.from_bytes(r[(val + 0x2C):(val + 0x30)], "little")
                    for i in range(numSpawns):
                        point4 = int.from_bytes(r[(val + point3 + (i * 4)):(val + point3 + (i * 4) + 4)], "little")
                        vivoNum = int.from_bytes(r[(val + point4):(val + point4 + 4)], "little")
                        chance = int.from_bytes(r[(val + point4 + 4):(val + point4 + 8)], "little")
                        parts = [
                            int.from_bytes(r[(val + point4 + 16):(val + point4 + 20)], "little"),
                            int.from_bytes(r[(val + point4 + 20):(val + point4 + 24)], "little"),
                            int.from_bytes(r[(val + point4 + 24):(val + point4 + 28)], "little"),
                            int.from_bytes(r[(val + point4 + 28):(val + point4 + 32)], "little")
                        ]
                        s = "\t\t" + "[0x" + hex(val + point4).upper()[2:] + "] " + vivoNames[vivoNum] + ": " + str(chance) + "% "
                        s = s + "(Part 1: " + str(parts[0]) + "%, Part 2: " + str(parts[1]) + "%, Part 3: " + str(parts[2])
                        s = s + "%, Part 4: " + str(parts[3]) + "%)\n"
                        text.write(s)
                if (check == 1):
                    text.write("\n")
    text.close()

def ffc_DO():
    text = open("ffc_digsiteOutputNew.txt", "wt")
    text.close()
    text = open("ffc_digsiteOutputNew.txt", "at")
    for root, dirs, files in os.walk("NDS_UNPACK/data/map/m/bin/"):
        for file in files:
            if (file == "0.bin"):
                f = open(os.path.join(root, file), "rb")
                r = f.read()
                f.close()
                numTables = int.from_bytes(r[0x68:0x6C], "little")
                point = int.from_bytes(r[0x6C:0x70], "little")
                mapN = os.path.join(root, file).split("\\")[-2]
                mapN = mapN.split("/")[-1] # it just works
                f = open("ffc_kasekiNames.txt", "rt")
                fossilNames = list(f.read().split("\n")).copy()
                f.close()
                f = open("ffc_mapNames.txt", "rt")
                mapNames = {}
                for l in (f.read().split("\n")):
                    mapNames[l.split(": ")[0]] = l.split(": ")[1]
                f.close()
                realP = []
                loc = point
                for i in range(numTables):
                    realP.append(int.from_bytes(r[loc:(loc + 4)], "little"))
                    loc = loc + 4
                check = 0
                for val in realP:
                    index = int.from_bytes(r[(val + 2):(val + 4)], "little")
                    if (index == 0):
                        continue
                    else:
                        if (check == 0):
                            check = 1
                            text.write(mapN + " [" + mapNames[mapN] + "]:\n")
                    text.write("\tZone " + str(index).zfill(2) + ":\n")
                    numTables = int.from_bytes(r[(val + 12):(val + 16)], "little")
                    point3 = int.from_bytes(r[(val + 16):(val + 20)], "little")
                    for i in range(numTables):
                        text.write("\t\tFossil Chip " + str(i) + ":\n")
                        point4 = int.from_bytes(r[(val + point3 + (i * 4)):(val + point3 + (i * 4) + 4)], "little")
                        point5 = int.from_bytes(r[(val + point4 + 12):(val + point4 + 16)], "little")
                        maxFos = int.from_bytes(r[(val + point4 + point5 + 4):(val + point4 + point5 + 8)], "little")
                        text.write("\t\t\tMax Spawns: " + str(maxFos) + "\n")
                        numWeird = int.from_bytes(r[(val + point4 + point5 + 8):(val + point4 + point5 + 12)], "little")
                        numSpawns = int.from_bytes(r[(val + point4 + point5 + 16):(val + point4 + point5 + 20)], "little")
                        startSpawns = val + point4 + point5 + 24 + (numWeird * 2)
                        totalChance = 0
                        for j in range(numSpawns):
                            thisStart = startSpawns + (j * 8)
                            totalChance = totalChance + int.from_bytes(r[(thisStart + 4):(thisStart + 6)], "little")
                        for j in range(numSpawns):
                            thisStart = startSpawns + (j * 8)
                            dark = (["N/A", "Normal", "Dark"])[r[thisStart]]
                            rare = (["N/A", "Normal", "Rare"])[r[thisStart + 1]]
                            fossilNum = int.from_bytes(r[(thisStart + 2):(thisStart + 4)], "little")
                            chance = int.from_bytes(r[(thisStart + 4):(thisStart + 6)], "little")
                            if (totalChance > 0):
                                chanceFr = (chance * 100) / totalChance
                            else:
                                chanceFr = 0
                            if (int(chanceFr) == chanceFr):
                                chanceS = str(int(chanceFr))
                            elif (round(chanceFr, 2) == chanceFr):
                                chanceS = str(round(chanceFr, 2))
                            else:
                                chanceS = "~" + str(round(chanceFr, 2))
                                if (len(chanceS) == 4):
                                    chanceS = chanceS + "0"
                            enemy = int.from_bytes(r[(thisStart + 6):(thisStart + 8)], "little")
                            s = "\t\t\t" + "[0x" + hex(thisStart + 2).upper()[2:] + "] " + fossilNames[fossilNum]
                            s = s + " (" + dark + ", " + rare + ")"
                            s = s + ": " + chanceS + "%"
                            s = s + " (Battle: " + str(enemy) + "%)" + "\n"
                            text.write(s)
                if (check == 1):
                    text.write("\n")
    text.close()

def output(rom):
    if (rom == "ff1"):
        ff1_DO()
    else:
        ffc_DO()