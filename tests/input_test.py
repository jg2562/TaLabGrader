from contextlib import contextmanager
import io
import sys

@contextmanager
def redirect_stdin(stream):
    old_stdin = sys.stdin
    sys.stdin = stream
    stream.seek(0)
    yield
    sys.stdin = old_stdin

if __name__ == "__main__":
    in_str = io.StringIO()
    in_str.write("Hello Nicole\n")
    in_str.write("What's up?")

    with redirect_stdin(in_str):
        print(input())
        print(input())

    print(input("Does stdin work again?: "))
