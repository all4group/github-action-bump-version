import re
import subprocess
import sys


def clean_flag(flag):
    if flag.startswith("["):
        flag = flag[1:]
    if flag.endswith("]"):
        flag = flag[:-1]
    return " ".join(
        flag.lower()
        .replace(";", " ")
        .replace("'", "")
        .replace("\"", "")
        .split()
    ).strip()


def flags_from_text(text):
    flags = re.findall(r"\[[0-9a-zA-Z\s'\"\.]+\]", string=text)
    return [clean_flag(flag) for flag in flags]


def extract(text):
    result = ""
    flags = flags_from_text(text)
    for flag in flags:
        if flag.startswith("bump version"):
            items = flag.split()
            if len(items) == 3:
                result = f"update --set-version {items[2]}"
    if result:
        pass
    elif "bump ver major" in flags:
        result = "update --major"
    elif "bump ver minor" in flags:
        result = "update --minor"
    elif "bump ver patch" in flags:
        result = "update --patch"
    elif "bump ver empty" in flags or "bump ver" in flags:
        result = "update"
    return result


def version():
    sp = subprocess.run(
        ["bumpver", "show", "--env", "--no-fetch"],
        stdout=subprocess.PIPE
    )
    result = ""
    if sp.returncode == 0 and sp.stdout:
        for line in sp.stdout.decode(encoding="utf-8").splitlines():
            if line.startswith("CURRENT_VERSION="):
                result = line[16:]
    return result


def main():
    args = sys.argv[1:]
    if len(args) == 2 and args[0].lower() == "extract":
        print(extract(args[1]))
    elif len(args) == 1 and args[0].lower() == "version":
        print(version())
    else:
        print(
            "Usage: python parser.py COMMAND [ARG]\n\n"
            "Commands:\n"
            "  extract [string]  Extract version component from string\n"
            "  version           Show current version"
        )


if __name__ == "__main__":
    sys.exit(main())
