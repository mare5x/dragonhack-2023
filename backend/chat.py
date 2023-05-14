from gptstuff import ask_GPT


def process(msg: str) -> tuple:
    task, response = ask_GPT(msg)
    return task, response

def repl():
    while True:
        msg = input("LemonAid $: ")
        resp = process(msg)
        print("chatGPT:", resp)


if __name__ == "__main__":
    repl()
