def logger(message, *args, **kwargs):
    print("-"*50)
    print("Positional arguments:")
    print(f"1. {message}")
    for index, value in enumerate(args, 2):
        print(f"{index}. {value}")
    print("-"*50)
    print("Keyword arguments:")
    for key, value in kwargs.items():
        print(f"{key}: {value}")
    print("-"*50)


if __name__ == "__main__":
    logger("Test", 1, 2, user="admin")
