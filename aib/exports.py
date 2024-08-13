import os

from .exceptions import UnsupportedExport

EXPORT_DATAS = {
    "qcow2": {
        "filename": "disk.qcow2"
    },
    "image": {
        "filename": "disk.img"
    },
    "ostree-commit": {
        "filename": "repo",
        "is_dir": True,
    },
    "container": {
        "filename": "container.tar"
    },
    "ostree-oci-image": {
        "filename": "image.oci-archive"
    },
    "rootfs": {
        "filename": None,
        "is_dir": True,
        "no_chown": True
    },
    "ext4": {
        "filename": "rootfs.ext4"
    },
    "tar": {
        "filename": "rootfs.tar"
    },
    "aboot": {
        "filename": "images",
        "is_dir": True,
    },
    "rpmlist": {
        "filename": "rpmlist"
    },
    "ext4.simg": {
        "export_arg": "ext4",
        "filename": "rootfs.ext4",
        "convert": "simg",
    },
    "simg": {
        "export_arg": "image",
        "filename": "disk.img",
        "convert": "simg",
    },
    "aboot.simg": {
        "export_arg": "aboot",
        "filename": "images",
        "is_dir": True,
        "convert": "simg",
        "convert_filename": "images/rootfs.img"
    }
}

def get_export_data(exp):
    if exp in EXPORT_DATAS:
        return EXPORT_DATAS[exp]
    raise UnsupportedExport(exp)


def export(outputdir, dest, dest_is_directory, export, runner):
    data = get_export_data(export)
    export = data.get("export_arg", export)
    exportdir = os.path.join(outputdir, export)
    export_is_dir = data.get("is_dir", False)

    filename = data["filename"]
    if filename:
        export_file = os.path.join(exportdir, filename)
    else:
        export_file = os.path.join(exportdir)

    convert = data.get("convert", "")
    if convert == "simg":
        if "convert_filename" in data:
            convert_file = os.path.join(exportdir, data["convert_filename"])
        else:
            convert_file = export_file
        converted_file = convert_file.removesuffix(".img") + ".simg"

        runner.run(["img2simg", convert_file, converted_file], use_sudo=True, use_container=True)
        if export_is_dir:
            runner.run(["rm", "-rf", convert_file], use_sudo=True)
        else:
            export_file = converted_file

    if dest_is_directory:
        dest = os.path.join(dest, os.path.basename(export_file))

    if export_is_dir:
        # The mv won't replace existing destination, so first remove it
        if os.path.isdir(dest) or os.path.isfile(dest):
            runner.run(["rm", "-rf", dest], use_sudo=True)

    if not data.get("no_chown", False):
        runner.run(["chown", f"{os.getuid()}:{os.getgid()}", export_file],
                   use_sudo=True)

    runner.run(["mv", export_file, dest], use_sudo=True)
