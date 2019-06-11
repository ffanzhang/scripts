import re

codes = { \
         "c"    : "43", \
         "cc"   : "50", \
         "cpp"  : "50", \
         "java" : "36", \
         "py"   : "7",  \
}

def guess_language_code(file_name):
    ext = file_name.strip().split('.')[-1].lower()
    return codes.get(ext, "50")

def guess_problem_set_id(file_name):
    fname = file_name.strip().split('.')[0]
    match = re.search(r"\d+", fname)
    if match:
        return match.group(0)
    else:
        return match

def guess_problem_index(file_name):
    fname = file_name.strip().split('.')[0]
    if len(fname) > 0 and str(fname[-1]).isalpha():
        return fname[-1].upper()
    else:
        return None

if __name__ == "__main__":
    assert guess_language_code("cc")    == "50"
    assert guess_language_code("cpp")   == "50"
    assert guess_language_code("java")  == "36"
    assert guess_language_code("py")    == "7"
    assert guess_language_code("adfsadfasdf")  == "50"
    assert guess_problem_set_id("lsajf") == None
    assert guess_problem_set_id("123123lsajf") == "123123"
    assert guess_problem_index("123123.cc") == None 
    assert guess_problem_index("123123d.cc") == 'D'
