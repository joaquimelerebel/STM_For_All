from functions.readings.bin_read import binary_read
from functions.readings.custom_read import custom_read
from functions.readings.file_read import file_read

# Takes a file and an input folder path and decide which function to call


def switch_file(file, input):
    if (file.endswith((".npy"))):
        data = binary_read(
            file, input)
    elif (file.endswith(('.mst'))):
        data = file_read(
            file, input)
    elif (file.endswith(('.bst'))):
        data = custom_read(
            file, input)
    return data
