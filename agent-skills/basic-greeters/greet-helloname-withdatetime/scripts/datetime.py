import time

def main() -> None:
    print(time.strftime("%Y-%m-%d-%H%M%S", time.localtime()))

if __name__ == "__main__":
    main()