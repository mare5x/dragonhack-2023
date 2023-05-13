def process(msg: str) -> str:
    return "Hello, World!"


def repl():
    while True:
        msg = input("LemonAid $: ")
        resp = process(msg)
        print(resp)


if __name__ == "__main__":
    repl()
