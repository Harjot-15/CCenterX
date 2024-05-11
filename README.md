# [Download CCentreX](https://github.com/Harjot-15/CCentreX/releases/tag/v2.1)
It is a System Utitlies Tool That Includes   Windows 11  ➡️➡️➡️ 🔋Power Commands , 📁 Secret Explorer Folder Shortcuts, 🛠️ Maintenance and Repair Comands, 🔐 Security And Adminstaration Comands, 💻 System Components and Many More.


# <img src="https://raw.githubusercontent.com/Harjot-15/CCentreX/main/Build%20Tools/H.ico" width="50" style="vertical-align: middle;" /> CCentreX

Welcome to the CCentreX repository! This guide provides detailed instructions on how to install, build, and run the CCentreX System Utility application.

## Download The Tool

You can also directly download the pre-built executable from the GitHub Releases:

[Download CCentreX](https://github.com/Harjot-15/CCentreX/releases/tag/v2.1)

## Installation

### Download and Install

1. Download the `CCenterX.zip` file from the latest release on GitHub.
2. Extract the `.zip` file and run the executable `Install_CCenterX.exe`.
3. If your antivirus software blocks the executable, please select "Run Anyway". The application is safe to use but does not yet have an official digital signature.

### Screenshots

Here are some screenshots of the application in action, showing both the Light and Dark modes:

<p float="left">
  <img src="https://github.com/Harjot-15/CCentreX/blob/a054ed4942bef82f8f0cec7f9a92eebdc8f506d0/Images/Dark%20Mode.png" width="45%" />
  <img src="https://github.com/Harjot-15/CCentreX/blob/a054ed4942bef82f8f0cec7f9a92eebdc8f506d0/Images/Light%20Mode.png" width="45%" /> 
</p>


## Building From Source

To build the application from source, follow these steps:

### Prerequisites

Ensure you have the following software installed:
- Python 3.x
- PyQt5
- cx_Freeze

```bash
pip install PyQt5 cx_Freeze
```

### Build the Executable

Navigate to the project directory and run the build script:

```bash
cd path/to/your/project
python Setup_Build.py build
```

This will create an executable in the `build` directory.

### Creating the Installer

To create an installer, you will need Inno Setup:

1. Download and install Inno Setup from [here](https://jrsoftware.org/isdl.php).
2. Open your `.iss` script file with Inno Setup Compiler.
3. Compile the script to create the installer.

The `.iss` file should be configured to include files from the `build` directory where the executable is located.


## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See [LICENSE](https://github.com/Harjot-15/CCentreX/blob/main/LICENSE) for more information. 

## Contact

Your Name – Harjot Singh - harjotsinghtamber15@gmail.com

