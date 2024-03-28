import sys, os
from tokenizer import Token, Tokenizer
from errors import handleError
from parsetree import Parser
from generation import Generator

# CPU ARCHITECTURES
ARM64 = "arm64"
AARCH64 = "aarch64"


def main(argv : list[str]) -> int:
    if len(argv) != 3:
        return 2

    source_path = argv[1]
    asm_path = source_path.rsplit('.',1)[0] + ".s"
    object_path = source_path.rsplit('.',1)[0] + ".o"
    target_path = argv[2]

    cpu = ARM64

    if source_path.rsplit('.',1)[1] != "fs65":
        return 5

    if not os.path.isfile(source_path):
        return 3

    source_contents = ""
    with open(source_path, "rt") as source_file:
        source_contents = source_file.read()

    tokenizer = Tokenizer(source_contents)
    tokens : list[Token] = tokenizer.tokenize()

    parser = Parser(tokens)
    rootNode = parser.parse()
    parser.printTree()

    generator = Generator(rootNode)
    code = generator.generate()

    try:
        with open(asm_path, "wt") as asm_file:
            if cpu == ARM64 or cpu == AARCH64:
                asm_file.write(code)
    except:
        return 4


    os.system(f"as {asm_path} -o {object_path}")
    os.system(f"ld {object_path} -o {target_path} -lSystem -syslibroot `xcrun --show-sdk-path` -e _start -arch arm64")

    return 0


if __name__ == "__main__":
    handleError(main(sys.argv))
