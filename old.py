import subprocess

out = subprocess.check_output(['sudo', 'fdisk', '-l']).splitlines()


def sortFdiskData(fdiskData):
    ## This rearragned an FDISK output to be a dictionary
    deviceCounter = 0
    doubleNewLineCounter = 0
    partitionCounter = 0
    devicesDict = {}
    deviceLines = []
    deviceDict = {}
    partitions = {}
    for line in out:
        if len(line) == 0:
            doubleNewLineCounter += 1
            print(doubleNewLineCounter)
        elif doubleNewLineCounter >= 2:
            deviceCounter += 1
            for data in deviceLines:
                data = data.decode('utf-8')
                if "Disk /" in data:
                    deviceDict['location'] = data.split(' ')[1].split(':')[0]
                    deviceDict['size'] = data.split(' ')[2].split(',')[0]
                    deviceDict['bytes'] = data.split(' ')[3].rstrip()
                elif "Disk model:" in data:
                    deviceDict['model'] = data.split(':')[1]
                elif "Units: " in data:
                    deviceDict['units'] = data.split(':')[1]
                elif "I/O size " in data:
                    deviceDict['ioMinimum'] = data.split(':')[1].split('/')[0]
                    deviceDict['ioOptimal'] = data.split(':')[1].split('/')[1]
                elif "Disklabel type: " in data:
                    deviceDict['disklabelType'] = data.split(':')[1]
                elif "Disk identifier: " in data:
                    deviceDict['diskIdentifier'] = data.split(':')[1]
                elif len(data) > 0:
                    firstCharacter = data[0][0]
                    if "/" == firstCharacter:
                        splitData = list(filter(None, data.split(' ')))
                        key = partitionCounter
                        partitions[key] = {}
                        partitions[key]['partition'] = splitData[0]
                        partitions[key]['start'] = splitData[1]
                        partitions[key]['end'] = splitData[2]
                        partitions[key]['sectors'] = splitData[3]
                        partitions[key]['size'] = splitData[4]
                        partitions[key]['type'] = splitData[6]
                        partitionCounter += 1
            partitionCounter = 0
            print(partitions)
            deviceDict['partitions'] = {}
            for key, value in partitions.items():
                print(key, value)
                deviceDict['partitions'][key] = value
            partitions.clear()
            # Checks to see if the dict exists. This was added because of some previous code. It may need to be removed
            if bool(deviceDict):
                devicesDict[str(deviceCounter)] = deviceDict
            deviceDict = {}
            doubleNewLineCounter = 0
            deviceLines = []
        deviceLines.append(line)

    return devicesDict


print(sortFdiskData(out))