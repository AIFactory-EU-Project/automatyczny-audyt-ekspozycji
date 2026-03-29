import glob
import os
import shutil
import subprocess


def makedirs(path):
    if os.path.exists(path):
        if not os.path.isdir(path):
            raise IOError("Path is not a directory")
    else:
        os.makedirs(path)


def is_empty(directory):
    return not os.listdir(directory)


def if_exists(path):
    return os.path.exists(path)


def remove_dir(directory):
    if if_exists(directory):
        shutil.rmtree(directory)
        

def remove2(path):
    os.remove(path)
    try:
        os.removedirs(os.path.dirname(path))
    except OSError:
        pass


def open_create(file, *args, **kwargs):
    makedirs(os.path.dirname(file))
    return open(file, *args, **kwargs)


def with_new_lines(lines):
    for line in lines:
        line = str(line)
        if not line.endswith("\n"):
            line = line + "\n"
        yield line


def all_files(directory):
    for dirpath, dirnames, filenames in os.walk(directory):
        for file in filenames:
            yield dirpath + "/" + file


def read_nonempty_lines(lines):
    for line in lines:
        if not line: continue
        if line[-1] == '\n': line = line[:-1]
        if line: yield line


def get_number_of_files(dir_path, extension):
    # it's incredibly faster than len(glob.glob())
    cmd = "find {} -name \"*{}\" | wc -l".format(dir_path, extension)
    process = subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE)
    output = process.stdout.decode('utf-8')
    return int(output)


def find_all_images(directory):
    return find_all_files(directory, [".jpg", ".png", ".jpeg"])


def find_all_pdfs(directory):
    return find_all_files(directory, [".pdf"])


def find_all_jsons(directory):
    return find_all_files(directory, [".json"])


def find_all_files(directory, extensions):
    result = []
    for ext in extensions:
        query = os.path.join(directory, "**", "*" + ext)
        result.extend(glob.glob(query, recursive=True))

    return result


def i_find_all_images(directory):
    return i_find_all_files(directory, [".jpg", ".png"])


def i_find_all_pdfs(directory):
    return i_find_all_files(directory, [".pdf"])


def i_find_all_jsons(directory):
    return i_find_all_files(directory, [".json"])


def i_find_all_files(directory, extensions):
    for ext in extensions:
        query = os.path.join(directory, "**", "*" + ext)
        for path in glob.iglob(query, recursive=True):
            yield path
