from gptstuff import askGPT


def process(msg: str) -> str:
    model_response = askGPT(msg)
    return model_response


def repl():
    while True:
        msg = input("LemonAid $: ")
        resp = process(msg)
        print("chatGPT:", resp)


if __name__ == "__main__":
    repl()
