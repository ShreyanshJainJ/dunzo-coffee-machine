def empty_file_content():
    open('result.txt', 'w').close()


def store_log(result: str):
    with open('result.txt', 'a+') as f:
        f.write(result + "\n")


empty_file_content()
