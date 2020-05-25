import cv2
import numpy as np
import os
from numpy import save
from HuffmannEncode import huff_encode
from HuffmannDecode import huff_decode
import timing

# 1. Read Image
file_path = input("Enter an image file path without quotes: ")
path, extension = os.path.splitext(file_path)
originalImage = np.array(cv2.imread(file_path, 0))
nRows = originalImage.shape[0]
nColumns = originalImage.shape[1]

# 2. Flatten the image to a 1D vector
flattenedImage = originalImage.reshape((1, originalImage.size))

# 3. combine levels of grey scale and map them to the vector
nCombinedLevels = int(input("Enter the number of levels to combine from greyscale(2, 4, 8, 16, 32, 64, 128): "))


# snap time at start of encoding
print("Start Encoding ..")
start_of_encoding_time = timing.snap()

for index in range(flattenedImage.size):
    remainder = flattenedImage[0][index] % nCombinedLevels
    if remainder != 0:
        flattenedImage[0][index] -= remainder

# 4. calculate the runs (level + count)
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

# 5. Use Huffman encoding to encode the levels and the counts arrays
coded_levels_string, lvl_levels_list, lvl_prob_list = huff_encode(imageLevels, "huff_levels")
coded_counts_string, cnts_levels_list, cnts_prob_list = huff_encode(levelCounts, "huff_counts")

# saving the lists passed to decoder to rebuild the huffman tree
lvl_levels_list_array = np.array(lvl_levels_list, dtype=np.uint8)
cnt_levels_list_array = np.array(cnts_levels_list, dtype=np.uint8)
lvl_prob_list_array = np.array(lvl_prob_list)
cnt_prob_list_array = np.array(cnts_prob_list)
save("lvl_levels_list", lvl_levels_list_array)
save("lvl_prob_list", lvl_prob_list_array)
save("cnts_levels_list", cnt_levels_list_array)
save("cnts_prob_list", cnt_prob_list_array)

# snap time at the end of encoding
end_of_encoding_time = timing.snap()
encoding_time = end_of_encoding_time - start_of_encoding_time
timing.log("Encoding Time excluding time to take input from user", timing.secondsToStr(encoding_time))
# ---------------------------------------------------------------------------------------------------------------------
# Inputs to the decoder
#   - Image size : number of Rows and number of Columns in the original image
#   - code table used to encode both the levels and the counts arrays
#   - The encoded Huffman binary strings for both the levels and the counts
#   - original image extension to write an image file after decoding
# ---------------------------------------------------------------------------------------------------------------------
# decoding
# take a snap at start of decoding
start_of_decoding_time = timing.snap();
print("Start Decoding")

decoded_levels = []
huff_decode(lvl_levels_list, lvl_prob_list, coded_levels_string,  decoded_levels)
decoded_counts = []
huff_decode(cnts_levels_list, cnts_prob_list, coded_counts_string,  decoded_counts)

# 1. decoding image
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

# 2. reshaping the image
decoded_flattened_image_array = np.array(decoded_flattened_image, dtype=np.uint8)
decoded_image = decoded_flattened_image_array.reshape((nRows, nColumns))

# take a snap at end of decoding
end_of_decoding_time = timing.snap()
decoding_time = end_of_decoding_time - start_of_decoding_time
timing.log("Decoding Time", timing.secondsToStr(decoding_time))

# 3. writing the image to the same directory
cv2.imwrite("images/DecodedImage" + extension, decoded_image)
