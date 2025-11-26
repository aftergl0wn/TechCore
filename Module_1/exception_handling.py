import logging


def exception_handling_v1(file):
    try:
        with open(file, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return None
    except Exception as e:
        logging.error(f"Ошибка: {e}")
    finally:
        print("Done")
    print("Exit")


def exception_handling_v2(file):
    try:
        with open(file, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        None
    except Exception as e:
        logging.error(f"Ошибка: {e}")
    finally:
        print("Done")
    print("Exit")


def exception_handling_v3(file):
    try:
        with open(file, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        None
    except Exception as e:
        logging.error(f"Ошибка: {e}")
    finally:
        return "Done"
    print("Exit")


def exception_handling_v4(file):
    try:
        with open(file, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return None
    except Exception as e:
        logging.error(f"Ошибка: {e}")
    finally:
        return "Done"
    print("Exit")


if __name__ == "__main__":
    exception_handling_v2("M")
