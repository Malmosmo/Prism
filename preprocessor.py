import os


def preprocess(source: str):
    idx = 0
    INCLUDE_PATHS = []
    included = True

    while included:
        included = False

        for line in source.splitlines(True):
            length = len(line)

            if line.strip().startswith("include"):
                included = True
                path = line.replace("include", "").strip()

                print("INCLUDE PATH:", path)

                if path in INCLUDE_PATHS:
                    print("FILE ALREADY INCLUDED")
                    source = source[:idx] + source[idx + length:]
                    break

                else:
                    if os.path.isfile(path):
                        with open(path, "r") as file:
                            include_source = file.read()

                        source = source[:idx] + include_source + source[idx + length:]

                        INCLUDE_PATHS.append(path)
                        idx = 0
                        break

                    else:
                        print("PATH DOES NOT EXIST")

            idx += length

    print("----------")
    print("----------")
    print(source)
    print("----------")
    print("----------")

    return source
