#find . -name *.m -exec grep '.*@\".*\".*' {} \; | wc

import os
import re

index = 0
pattern = re.compile("(@\".*?[^\\\\]\")")

def is_uncode(s):
    return not all(ord(c) < 128 for c in s)

def should_ignore_line(line):
    line = line.strip()
    return line.startswith("//") or line.startswith("NSLog") or line.startswith("@param")

def copy_file_in_mem(full_file_name):
    file = open(full_file_name)
    file_data = file.read()
    return file_data

def find_hardcoded_string(full_file_name):
    replace_count = 0
    file_data = copy_file_in_mem(full_file_name)
    write_file_name = full_file_name[full_file_name.rindex("/")+1:]
    folder_path = full_file_name.replace(write_file_name, "")

    filename = full_file_name[full_file_name.rindex("/")+1:full_file_name.rindex(".")]
    for i, line in enumerate(open(full_file_name)):
        if should_ignore_line(line):
            continue

        while True:
            match = re.search(pattern, line)
            if match:
                if is_uncode(match.group(0)):
                    value = match.group(0)
                    global index
                    key_index = "\"%s_%d\"" % (filename, index)
                    local_value = "NSLocalizedString(@%s, @%s)" %(key_index, value)
                    file_data = file_data.replace(value, local_value)
                    index = index + 1
                    replace_count = replace_count + 1
                    #print "%s,%s,%s,%s" % (full_file_name, i+1, match.group(0),line.strip())
                line = line[match.end():]
            else:
                break

    if replace_count > 0:
        if not os.path.exists("tmp/" + folder_path):
            os.makedirs("tmp/"+ folder_path)
        write_file = open("tmp/%s%s" % (folder_path, write_file_name), 'w+')
        write_file.write(file_data)
        write_file.close()

def check_if_valid_file_name(full_file_name):
    return not ('.svn' in full_file_name
                or "DS_Store" in full_file_name
                or "gif" in full_file_name
                or "png" in full_file_name
                or "jpeg" in full_file_name
                or "jpg" in full_file_name
                or full_file_name.endswith(".a"))

def should_skip_dir(root):
    return ("cocos2d" in root or
    "chat_vshow.xcodeproj" in root or
    ".framework" in root or
    ".bundle" in root)

for root, dirname, filename in os.walk("show_ios"):
    if should_skip_dir(root):
        continue

    for fname in filename:
        full_file_name = os.path.join(root, fname)
        if check_if_valid_file_name(full_file_name):
            print full_file_name
            find_hardcoded_string(full_file_name)
