# -*- encoding: utf-8 -*

import os
import re

pattern = re.compile("(\"(.*?)\")")

index = 0
replace_index = 0
dict_strings = dict()

def is_uncode(s):
    #this checks for double byte strings, return True if you want to check only English strings
    return not all(ord(c) < 128 for c in s)

def should_ignore_line(line):
    line = line.strip()
    return line.startswith("//") or line.startswith("NSLog") or line.startswith("@param")

def format_keys(key):
    special_chars = [':','?','！','：','】','【','，','.','%','%s','%d','%f','-',' ','一','(',')',' ','①','②','③','④','⑤','⑥','⑦','⑧','⑨',']','[','0''-','9','０','１','２','３','４','５','６','７','８','９']
    #
    for char in special_chars:
        key = key.replace(char,'')

    if len(key) > 10:
        return key[:12].replace('')
    else:
        return key

def copy_file_in_mem(full_file_name):
    file = open(full_file_name)
    file_data = file.read()
    return file_data

def get_file_type(full_file_name):
    filetype = ""
    if ".xml" in full_file_name:
        filetype = "xml"
    if ".java" in full_file_name:
        filetype = "java"
    return filetype

def replace_values(full_file_name):
    replace_count = 0
    file_data = copy_file_in_mem(full_file_name)
    write_file_name = full_file_name[full_file_name.rindex("/")+1:]
    folder_path = full_file_name.replace(write_file_name, "")
    filetype = get_file_type(full_file_name)

    filename = full_file_name[full_file_name.rindex("/")+1:full_file_name.rindex(".")]
    for i, line in enumerate(open(full_file_name)):
        if should_ignore_line(line):
            continue

        while True:
            match = re.search(pattern, line)
            if match:
                if is_uncode(match.group(0)):
                    #print "%s,%s,%s,%s" % (full_file_name, i+1, match.group(0),line.strip())
                    value = match.group(0)
                    key_index = ""
                    for s_key, s_value in dict_strings.iteritems():
                        if s_value == value.replace('"',''):
                            key_index = s_key
                    if key_index:
                        global replace_index
                        local_value = ""
                        if filetype == "java":
                            local_value = "StringResManager.getResourceString(com.tiange.vshow.R.string.%s)" % (key_index)
                        if filetype == "xml":
                            local_value = "\"@string/%s\"" % (key_index)
                        if local_value:
                            file_data = file_data.replace(value, local_value.strip())
                            replace_count = replace_count + 1
                            replace_index = replace_index + 1
                line = line[match.end():]
            else:
                break

    if replace_count > 0:
        if not os.path.exists("tmp/" + folder_path):
            os.makedirs("tmp/"+ folder_path)
        write_file = open("tmp/%s%s" % (folder_path, write_file_name), 'w+')
        write_file.write(file_data)
        write_file.close()


def find_hardcoded_string(full_file_name):
    filename = full_file_name[full_file_name.rindex("/")+1:full_file_name.rindex(".")]
    for i, line in enumerate(open(full_file_name)):
        if should_ignore_line(line):
            continue

        while True:
            match = re.search(pattern, line)
            if match:
                if is_uncode(match.group(0)):
                    #print "%s,%s,%s,%s" % (full_file_name, i+1, match.group(0),line.strip())
                    value = match.group(0)
                    global index
                        
                    string_value = value[1:-1]
                    string_key = "key_%d" % index
                    #print "\"%s_%d\" = %s_cn\";" % (filename, index, value[1:-1])
                    print "<string name=\"%s\">%s</string>" % (string_key.strip(), string_value)
                    global dict_strings
                    dict_strings[string_key.strip()] = string_value
                    index = index + 1
                line = line[match.end():]
            else:
                break

def check_if_valid_file_name(full_file_name):
    return not ('.svn' in full_file_name
                or "DS_Store" in full_file_name
                or "gif" in full_file_name
                or "png" in full_file_name
                or "jpeg" in full_file_name
                or "jpg" in full_file_name
                or full_file_name.endswith(".a")
                or full_file_name.endswith(".apk")
                or "msp" in full_file_name)

def should_skip_dir(root):
    return "cocos2d" in root or \
           "chat_vshow.xcodeproj" in root or \
           ".framework" in root or \
           "gen" in root or \
           "bin" in root or \
           "raw" in root or \
           "values" in root or \
           "libs" in root

def main():
    try:
        for root, dirname, filename in os.walk("trunk"):
            if should_skip_dir(root):
                continue

            for fname in filename:
                full_file_name = os.path.join(root, fname)
                if check_if_valid_file_name(full_file_name):
                    find_hardcoded_string(full_file_name)
                    if dict_strings:
                        replace_values(full_file_name)
        print "The eagle has landed"
    except Exception as e:
        print e

if __name__ == '__main__':
    main()

