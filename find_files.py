import argparse
import os
from xml.dom import minidom


def parse_file(file):
    return minidom.parse(file)


def get_number_of_records(file):
    return len(parse_file(file).getElementsByTagName("record"))


def create_035_record_dictionary(file):
    d = {}
    for record in file.getElementsByTagName("record"):
        mms_id = next(
            e.childNodes[0].data
            for e in record.getElementsByTagName("controlfield")
            if e.attributes["tag"].value == "001"
        )
        dd = {}
        for e in record.getElementsByTagName("datafield"):
            if e.attributes["tag"].value == "035":
                for sb in e.getElementsByTagName("subfield"):
                    dd["035$a"] = sb.attributes["code"].value + sb.childNodes[0].data
        d[mms_id] = dd
    return d


def look_up_files(root_dir, pattern):
    files_list = []
    for subdir, dirs, files in os.walk(root_dir):
        for file in files:
            #         print(os.path.join(subdir, file))
            filename = subdir + os.sep + file

            if pattern in filename:
                print("file name: ", file)
                files_list.append(filename)

    return files_list


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--directory", type=str,
                    help="path to lookup directory")
    ap.add_argument("-p", "--pattern", type=str,
                    help="patern of the file names to look for")

    args = vars(ap.parse_args())
    files = look_up_files(args['directory'], args['pattern'])


if __name__ == '__main__':
    main()

