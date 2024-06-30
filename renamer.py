def fix_unicode(string) -> str:
    if "u0026" in string:
        string = string.replace("\\", "").replace("u0026", "&")
    if "u003e" in string:
        string = string.replace("\\", "").replace("u003e", ">")
    if "u003c" in string:
        string = string.replace("\\", "").replace("u003c", "<")
    if '\\"' in string:
        string = string.replace("\\", "")
    
    return string

def rename(name, is_path=False) -> str:
    new_name = ""
    
    allowed_chars = "!&-,()$@%#;'+=_ "
    
    # Allows path strings to include slashes and periods when being renamed
    if is_path:
        allowed_chars += "\\/."

    # Fixes potential unicode issues in string caused by HTML scraping
    name = fix_unicode(name)
    
    for i in range(len(name)):
        c = name[i]
        if not c.isalnum() and c not in allowed_chars:
            new_name += ""
        else:
            new_name += name[i]

    return new_name