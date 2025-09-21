# Scripts Directory

## Packaging Scripts

This directory contains scripts used to build installation packages for QtProjectTemplate.

## Script Descriptions

### `build_windows_package.py` - Windows NSIS Installer Build Script

Specifically used to build NSIS installers for the Windows platform.

**Usage:**

First, customize the `PRODUCT_NAME` field in the `.nsi` file for your project name, then run the Python script:

**Prerequisites:**

- NSIS installed ([https://nsis.sourceforge.io/Download](vscode-file://vscode-app/c:/Users/LMR/AppData/Local/Programs/Microsoft VS Code/resources/app/out/vs/code/electron-browser/workbench/workbench.html))
- CMake build completed

### `build_linux_package.py` - Linux Installer Build Script

Specifically used to build AppImage installers for the Linux platform.

**Usage:**

**Prerequisites:**

- Dependencies installed: `sudo apt-get install -y libfuse2 patchelf`
- CMake build completed

**TODO:**

- [ ] Support for deb format

## Build Process

### Local Build

1. **Build the project**
2. **Build the installer**

### CI/CD Build

GitHub Actions will automatically:

1. Install necessary dependencies (Qt, NSIS, etc.)
2. Build the project
3. Run tests
4. Build the installer
5. Upload build artifacts

## About Software Version Information

The Windows NSIS script reads version information from the exe properties, while the Linux Python script automatically reads version information from the `src/version.h` file.