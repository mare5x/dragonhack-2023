from gptstuff import ask_GPT


def process(msg: str) -> str:
    task, (model_response, image) = ask_GPT(msg)
    return task, (model_response, image)

def repl():
    while True:
        msg = input("LemonAid $: ")
        resp = process(msg)
        print("chatGPT:", resp)


if __name__ == "__main__":
    repl()
