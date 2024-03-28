# fs65c

fs65c is a compiler for the fs65 language, a custom language with extremely limited functionality, created for fun. This compiler was written in python 3 for the memes, do not expect quick compilation times (could still be faster than rustc though).

## Supported CPU Architectures

Only Darwin aarch64/ARM64 is supported by this compiler, and this is purely because this was written on and for an M2 Macbook, and totally not because OP is too lazy to support other architectures, and not because OP is salty that no games have support on Apple Silicon.

## How to use

Put the `.py` files from this repo into your directory, then create your `.fs65` file. Check out the `Example.fs65` file for some example code. Then, in the command line move to your directory and run the command:
`python fs65c.py <source file name>.fs65 <desired executable name>`
This should create a `.s` file which contains the assembly instructions, an `.o` file, and finally your executable. If you used the `Example.fs65` code, make sure your `Example.s` assembly matches that in the repo.

## Syntax of fs65

fs65 is a language created by FallingSky65, and as of the last update to this readme, it only supports these things.

- `let <variable name> = <expression>;` This declares a variable (with type uint64) set to the value of the expression. Multiple declarations for a variable are not allowed.
- `exit(<expression>);` and `exit <expression>;` will end the program with the exit code corresponding to that of the value of the expression.
- `add(<expr1>, <expr2>)` and `sub(<expr1>,<expr2)` return the sum of and the difference of the two input expressions

## Compilation Steps

First, fs65 tokenizes the code, then it parses the tokens to construct a syntax (?) tree, then it uses the syntax tree to generate the worst assembly ever written.

## Future use of LLVM

As of the most recent update to this README, the fs65c compiler compiles directly to assembly without optimizations. In the future, the code may be updated to first translate into IR (intermediate representation) and optimized and compiled with LLVM.
