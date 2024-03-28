from sys import exit

def handleError(exitcode : int) -> None:
    if exitcode == 0:
        pass
    elif exitcode == 1:
        print("Error")
    elif exitcode == 2:
        print("Compiler inputs error, compiler requires 2 arguments")
    elif exitcode == 3:
        print("Source file does not exist")
    elif exitcode == 4:
        print("Error writing to target")
    elif exitcode == 5:
        print("Incompatible source file, source file must be .fs65")
    elif exitcode == 6:
        print("Unknown error during tokenization")
    elif exitcode == 7:
        print("Problematic token detected")
    elif exitcode == 8:
        print("Syntax Error")
    elif exitcode == 9:
        print("Syntax Error: Expected ;")
    elif exitcode == 10:
        print("Repeat declaration of variable")
    elif exitcode == 10:
        print("Undeclared variable used")
    else:
        print("Unknown Error")
    exit(exitcode)
