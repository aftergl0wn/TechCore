def process(data):
    result = []
    breakpoint()
    for i in range(len(data)):
        result.append(data[i + 1] * 2)
    return result


if __name__ == "__main__":
    arr = [1, 2, 3]
    print(process(arr))
