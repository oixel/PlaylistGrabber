def fix_unicode(string) -> str:
    if "u0026" in string:
        string = string.replace("\\", "").replace("u0026", "&")
    if "u003e" in string:
        string = string.replace("\\", "").replace("u003e", ">")
    if "u003c" in string:
        string = string.replace("\\", "").replace("u003c", "<")
    
    return string

def rename(name) -> str:
    new_name = ""

    ALLOWED_CHAR = "!&-,()$@%#:;'\"+=_ "

    name = fix_unicode(name)
    
    for i in range(len(name)):
        c = name[i]
        if not c.isalnum() and c not in ALLOWED_CHAR:
            new_name += ""
        else:
            new_name += name[i]

    return new_name