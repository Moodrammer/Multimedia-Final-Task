import cv2
import numpy as np
from numpy import save
from HuffmannEncode import huff_encode
from HuffmannDecode import huff_decode

# 1. Read Image
originalImage = np.array(cv2.imread("images/text.tif", 0))
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


save("levels", imageLevelsArray)
save("counts", levelCountsArray)

code_table_levels = {}
coded_levels_string = huff_encode(imageLevels, code_table_levels, "huff_levels")
code_table_counts = {}
coded_counts_string = huff_encode(levelCounts, code_table_counts, "huff_counts")

# ---------------------------------------------------------------------------------------------------------------------
# decoding
decoded_levels = []
huff_decode(code_table_levels, decoded_levels, coded_levels_string)
decoded_counts = []
huff_decode(code_table_counts, decoded_counts, coded_counts_string)

# decoding image
decoded_flattened_image = []
corresponding_count_index = 0
for index in range(len(decoded_levels)):
    if decoded_levels[index] % 2 == 0:
        count = decoded_counts[corresponding_count_index]
        for level_count in range(count):
            decoded_flattened_image.append(decoded_levels[index])
        corresponding_count_index += 1
    else:
        decoded_flattened_image.append(decoded_levels[index] - 1)

# reshaping the image
decoded_flattened_image_array = np.array(decoded_flattened_image, dtype=np.uint8)
decoded_image = decoded_flattened_image_array.reshape((nRows, nColumns))

cv2.imshow("decoded", decoded_image)
cv2.waitKey()