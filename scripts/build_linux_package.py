#!/usr/bin/env python3
import sys
import subprocess
import argparse
from pathlib import Path
import shutil
import re


def run_command(cmd, cwd=None):
    """Execute command and return result"""
    print(f"Executing command: {cmd}")
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Command execution failed: {result.stderr}")
        return False
    print(f"Command executed successfully: {result.stdout}")
    return True


def find_linuxdeploy() -> str:
    """Download linuxdeploy if not available"""
    linuxdeploy_url = "https://github.com/probonopd/linuxdeployqt/releases/download/continuous/linuxdeployqt-continuous-x86_64.AppImage"
    linuxdeploy_path = Path.home() / ".local" / "bin" / "linuxdeployqt"

    if linuxdeploy_path.exists():
        return linuxdeploy_path

    # Create directory if it doesn't exist
    linuxdeploy_path.parent.mkdir(parents=True, exist_ok=True)

    # Download linuxdeploy
    print("Downloading linuxdeploy...")
    if not run_command(f"wget -O {linuxdeploy_path} {linuxdeploy_url}"):
        print("Failed to download linuxdeploy")
        return None

    # Make it executable
    linuxdeploy_path.chmod(0o755)
    return linuxdeploy_path


def find_appimagetool() -> str:
    """Download appimagetool if not available"""
    appimagetool_url = "https://github.com/AppImage/appimagetool/releases/download/continuous/appimagetool-x86_64.AppImage"
    appimagetool_path = Path.home() / ".local" / "bin" / "appimagetool"

    if appimagetool_path.exists():
        return appimagetool_path

    # Create directory if it doesn't exist
    appimagetool_path.parent.mkdir(parents=True, exist_ok=True)

    # Download linuxdeploy
    print("Downloading linuxdeploy...")
    if not run_command(f"wget -O {appimagetool_path} {appimagetool_url}"):
        print("Failed to download appimagetool")
        return None

    # Make it executable
    appimagetool_path.chmod(0o755)
    return appimagetool_path


def get_version(hear_file):
    m = re.search(r"^#define\s+VERSION\s+([^\s]+)", Path(hear_file).read_text(), re.M)
    if not m:
        raise RuntimeError("VERSION not found")
    return m.group(1)


def create_appimage(build_dir, app_name, project_root):
    """Create AppImage package for Linux"""
    print("Creating AppImage package...")

    # Find linuxdeploy
    linuxdeploy = find_linuxdeploy()
    if not linuxdeploy:
        print("Error: linuxdeploy not found and could not be downloaded")
        return False

    # Create AppDir structure
    app_dir = build_dir / "AppDir"
    if app_dir.exists():
        shutil.rmtree(app_dir)
    app_dir.mkdir(exist_ok=True)

    # Copy executable and dependencies
    src_path = build_dir / "src"
    executable_path = src_path / app_name

    if not executable_path.exists():
        print(f"Error: Executable {executable_path} not found")
        return False

    shutil.copy(executable_path, app_dir)
    shutil.copy(project_root / "src/resources/icon.png", app_dir)
    for desktop in (project_root / "src/resources/linux").glob("*.desktop"):
        shutil.copy(desktop, app_dir)

    # Run linuxdeploy
    deploy_cmd = f"{linuxdeploy} {app_name} -appimage"
    if not run_command(deploy_cmd, cwd=app_dir):
        print("Failed to create AppImage structure")
        return False

    version = get_version(project_root / "src/version.h")
    env_vars = {"VERSION": str(version)}

    env_cmd = " ".join([f"{k}={v}" for k, v in env_vars.items()])

    # Find appimagetool
    appimagetool = find_appimagetool()
    if not appimagetool:
        print("Warning: appimagetool not found and could not be downloaded")
        return False

    appimage_cmd = f"{env_cmd} {appimagetool} {app_dir}"
    if not run_command(appimage_cmd, cwd=build_dir):
        print("Failed to create AppImage")
        return False

    print("AppImage creation completed!")
    return True


def main():
    print("=== Linux package tool ===")

    parser = argparse.ArgumentParser(description="Package tool for Linux platforms.")
    parser.add_argument(
        "--output-dir", "-o", type=str, help="The binary output directory"
    )
    parser.add_argument(
        "--app-name", "-a", type=str, help="Name of the executable file"
    )
    parser.add_argument(
        "--format",
        "-f",
        type=str,
        choices=["appimage", "deb", "both"],
        default="appimage",
        help="Package format to create",
    )

    args = parser.parse_args()

    project_root = Path(__file__).parent.parent
    if not (project_root / "CMakeLists.txt").exists():
        print("Error: Please run this script in the project root directory")
        return 1

    # Resolve build directory path
    build_dir = Path(args.output_dir)
    if not build_dir.is_absolute():
        build_dir = project_root / build_dir

    if not build_dir.exists():
        print(
            f"Error: Build directory does not exist: {build_dir} Please run CMake build first"
        )
        return 1

    success = True

    # Create packages based on format
    if args.format in ["appimage", "both"]:
        if not create_appimage(build_dir, args.app_name, project_root):
            success = False

    # if args.format in ["deb", "both"]:
    #     if not create_deb_package(build_dir, args.app_name, project_root):
    #         success = False

    if not success:
        print("Packaging failed!")
        return 1

    print("Linux packaging completed!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
