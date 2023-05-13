from gptstuff import ask_GPT


def process(msg: str) -> str:
    model_response, image = ask_GPT(msg)
    return model_response, image


def repl():
    while True:
        msg = input("LemonAid $: ")
        resp = process(msg)
        print("chatGPT:", resp)


if __name__ == "__main__":
    repl()
