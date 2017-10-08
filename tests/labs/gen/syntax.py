import py_compile

def check_syntax(code_file):
    result = False
    if code_file:
        try:
            py_compile.compile(code_file)
            result = True
        except SyntaxError as e:
            result = False
    return (int(result), "Compilation " + ["Failed", "Succeeded"][result])

def get_test_functions():
    return [(check_syntax, 1, "Invalid syntax")]
