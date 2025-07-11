# 🔧 stmtool – Simple STM32 Build & Flash CLI Tool

`stmtool` is a command-line utility to simplify building and flashing STM32 projects using **CMake** and **STM32CubeProgrammer**. Designed with **beginners** in mind, `stmtool` helps you build, rebuild, run, and flash `.elf` files to your STM32 Nucleo boards with minimal effort.

Tested on **Windows** with a **NUCLEO-U545** board — should work on other platforms (since it’s written in Python).

---

## 🚀 Features

- 🏗️ `build` – Configure + compile a CMake project  
- 🔄 `rebuild` – Clean and rebuild from scratch  
- 🏃 `run` – Build + flash the `.elf` to your board  
- 🔥 `flash-elf` – Flash an existing `.elf` binary to the board  

No configuration files. No complex setup. Just point it to your project directory or ELF.

---

## 🧰 Requirements

Make sure the following are installed and available in your system `PATH`:

| Tool                | Purpose               |
|---------------------|-----------------------|
| `cmake`             | Project configuration |
| `ninja`             | Build system          |
| `arm-none-eabi-gcc` | ARM cross-compiler    |
| `STM32CubeProgrammer`| For flashing the board|

> ⚠️ Currently tested on Linux only — contributions welcome to support Windows/macOS.

---

## 📦 Installation

Right now there is no package manager setup. To try it out:

```bash
git clone https://github.com/<your_username>/stmtool.git
cd stmtool
python3 stmtool.py <command> <arg>
```
Alternatively, you can symlink it or add it to your PATH.

## 🕹️ Usage
```bash
stmtool <command> <workspace-or-elf>
Commands
Command	Description
build	Run CMake and compile the project
rebuild	Delete build directory and compile again
run	Build and then flash to the board
flash-elf	Flash an existing ELF binary
```  

## Examples
```bash
stmtool build .
stmtool rebuild my_project/
stmtool run ./blink_project
stmtool flash-elf ./build/firmware.elf
```

## 📂 Project Structure Assumption
Your workspace should be a CMake-based STM32 project with the following structure:

```css
my_project/
├── CMakeLists.txt
├── src/
└── ...
```

## 💬 Contributing
This project is open-source and welcomes contributions!
If you’d like to add new features, support other platforms, or fix bugs — feel free to open a pull request.

## 📄 License
MIT License

🎯 Future Ideas
 Add Windows/macOS support

 Package as a pip installable CLI tool

 Detect board/USB automatically

 Add unit tests or CI

## 🧠 FAQ
Q: Do I need any config files?
A: Nope! Just your CMake project and this script.

Q: Will it work on other STM32 boards?
A: Likely yes, as long as STM32CubeProgrammer can detect and flash them.