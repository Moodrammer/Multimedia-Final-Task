import cv2
import numpy as np
from numpy import save

# 1. Read Image
originalImage = np.array(cv2.imread("images/peppers2.tif", 0))
nRows = originalImage.shape[0]
nColumns = originalImage.shape[1]

flattenedImage = originalImage.reshape((1, originalImage.size))


# 2. combine levels
nCombinedLevels = 8
for index in range(flattenedImage.size):
    remainder = flattenedImage[0][index] % nCombinedLevels
    if remainder != 0:
        flattenedImage[0][index] -= remainder

# 3. calculate the runs
imageLevels = []
levelCounts = []
runLevel = flattenedImage[0][0]
runCount = 1
runIndex = 1
while runIndex != flattenedImage.size:
    if flattenedImage[0][runIndex] == flattenedImage[0][runIndex - 1] and runCount <= 255:
        runCount += 1
    else:
        if runCount != 1:
            imageLevels.append(runLevel)
            levelCounts.append(runCount)
        else:
            imageLevels.append(runLevel + 1)
        runLevel = flattenedImage[0][runIndex]
        runCount = 1
    runIndex += 1

if runCount != 1:
    imageLevels.append(runLevel)
    levelCounts.append(runCount)
else:
    imageLevels.append(runLevel + 1)

imageLevelsArray = np.array(imageLevels, dtype=np.uint8)
levelCountsArray = np.array(levelCounts, dtype=np.uint8)

print(imageLevels)
print(levelCounts)

save("levels", imageLevelsArray)
save("counts", levelCountsArray)

