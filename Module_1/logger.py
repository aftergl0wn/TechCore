def logger(message, *args, **kwargs):
    print("-"*50)
    print(f"Message: {message}")
    print("-"*50)
    print("Positional arguments:")
    for index, value in enumerate(args, 1):
        print(f"{index}. {value}")
    print("-"*50)
    print("Keyword arguments:")
    for key, value in kwargs.items():
        print(f"{key}: {value}")
    print("-"*50)


if __name__ == "__main__":
    logger("Test", 1, 2, user="admin")
