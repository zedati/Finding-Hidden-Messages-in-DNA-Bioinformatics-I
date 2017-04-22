def print_array(arr, file=""):
    result = arr# " ".join(map(str,arr))
    if file != "":
        print(result, file=file)
    else:
        print(result)


