import os
import zipfile

# Add libfile to path
# MUST BE POSITIONED BEFORE `import magic`
new_path = os.path.abspath("deps\\file-windows")
path_separator = os.pathsep
os.environ["PATH"] = f"{new_path}{path_separator}{os.environ['PATH']}"

import magic


def check_mime(fname: str) -> str:
    mime = magic.from_file(fname, mime=True)

    # Zipfile check
    if mime == "application/zip":
        with zipfile.ZipFile(fname, "r") as jar:
            names = {name.lower() for name in jar.namelist()}
            if "meta-inf/manifest.mf" in names:
                mime = "application/java-archive"
            elif "word/document.xml" in names:
                mime = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

    return mime


if __name__ == "__main__":
    x = check_mime("C:\\Users\\mayhem6328\\Downloads\\74\\DC\\17072026\\Assets\\Blade-8a1398f95a8b1001.blend")
    print(x)
