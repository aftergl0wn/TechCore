import logging


def exception_handling(file):
    try:
        with open(file, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return None
    except Exception as e:
        logging.error(f"Ошибка: {e}")
    finally:
        print("Done")


if __name__ == "__main__":
    exception_handling("hj")
