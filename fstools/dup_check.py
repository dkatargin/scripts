import os
import sys
import xml.etree.cElementTree as ET


def main(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    for elem in root:
        if elem.attrib.get("checked", False):
            continue
        if elem.attrib.get("mime-type", "none/none").split("/")[0] not in [
            "video",
            "image",
        ]:
            continue
        dupmap = []
        select_msg = ""
        for i, c in enumerate(elem):
            dupmap.append(c.attrib["path"])
            select_msg += f"[{i}] {c.attrib['path']}\n"
        select_msg += f"[{len(dupmap)}] skip"

        print(select_msg)
        selected = int(input("Select original file:"))
        if selected > len(dupmap) - 1:
            continue

        del elem[selected]
        elem.set("checked", "true")
        print(f"Selected path is: {dupmap[selected]}\n")

        with open(xml_file, "wb") as f:
            f.write(ET.tostring(root))


if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print("Usage: python3 " + sys.argv[0] + " <path>")
