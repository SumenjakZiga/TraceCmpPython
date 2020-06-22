import re

oldLogHandle = open("logold.txt", "r")
newLogHandle = open("lognew.txt", "r")
outFile = open("out.txt", "w")

oldLogList = oldLogHandle.readlines()
newLogList = newLogHandle.readlines()

iteratorOldList = -1
iteratorNewList = -1
najden = 0
lineCount = 0
previous1 = ""
previous2 = ""
currentHexNewModule = 0
oldHexNewModule = 0
currentHexOldModule = 0
oldHexOldModule = 0


while True:
    moduleName1 = re.search("^[A-Za-z0-9\\_\\-]+", oldLogList[iteratorOldList]).group()
    moduleName2 = re.search("^[A-Za-z0-9\\_\\-]+", newLogList[iteratorNewList]).group()

    if iteratorNewList != -1 and iteratorOldList != -1:
            if moduleName1 != moduleName2 and moduleName2 != previous2:
                previous1 = moduleName1
                iteratorOldList += 1
                lineCount += 1
                if najden == 0:
                    outFile.write("%d: New dll not aligned!\n" % lineCount)
                najden = 1

            elif moduleName1 != previous1 and moduleName2 != moduleName1:
                previous2 = moduleName2
                iteratorNewList += 1
                if najden == 0:
                    outFile.write("%d: Old dll not aligned!\n" % lineCount)
                najden = 1

            else:
                previous1 = moduleName1
                previous2 = moduleName2
                lineCount += 1
                iteratorNewList += 1
                iteratorOldList += 1
                if najden == 1:
                    outFile.write("%d: Corrected the file alignment!\n" % lineCount)
                    najden = 0

    else:
        if moduleName1 != moduleName2:
            print("First line Error!\n")
        previous1 = moduleName1
        previous2 = moduleName2
        iteratorNewList = 0
        iteratorOldList = 0

    if iteratorNewList > len(newLogList)-1:
        break
    elif iteratorOldList > len(oldLogList)-1:
        break

    moduleHexOffset1 = int(re.search("[0-9a-fA-F]+$", oldLogList[iteratorOldList]).group(), 16)
    moduleHexOffset2 = int(re.search("[0-9a-fA-F]+$", newLogList[iteratorNewList]).group(), 16)

    deltaNew = currentHexNewModule - oldHexNewModule
    deltaOld = currentHexOldModule - oldHexOldModule
    if deltaNew > 15 or deltaOld > 15 or deltaNew < 0 or deltaOld < 0:
        print("Jump or instruction Error")
    elif deltaNew != deltaOld and flag == 0 and najden == 0:
        outFile.write("Instruction diff here.\n")
        flag = 1
    else:
        flag = 0

    if najden == 0:
        outFile.write("%s\t\t%s" % (oldLogList[iteratorOldList][0:len(oldLogList[iteratorOldList])-2], newLogList[iteratorNewList]))
    else:
        outFile.write("%s\t\t%s - searching alignment\n" % (oldLogList[iteratorOldList][0:len(oldLogList[iteratorOldList])-2], newLogList[iteratorNewList][0:len(newLogList[iteratorNewList])-2]))
    oldHexNewModule = currentHexNewModule
    oldHexOldModule = currentHexOldModule

oldLogHandle.close()
newLogHandle.close()
outFile.close()
