
import sys
import subprocess
import os
from rich.console import Console
import json
import pbuild
import runner


CURRENT_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def load_tool_settings_json():
    filepath = os.path.join(CURRENT_SCRIPT_DIR, 'toolsettings.json')
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"The file {filepath} does not exist.")
    with open(filepath, 'r') as file:
        data = json.load(file)
    return data

def load_flasher_commands_json(build_dir):
    filepath = os.path.join(build_dir, 'flasher_commands.json')
    if not os.path.isfile(filepath):
        return None
    with open(filepath, 'r') as file:
        data = json.load(file)
    return data

def execute_build_command(workspace, build_dir):
    pbuild.execute_build_command(workspace, build_dir)

def execute_rebuild_command(workspace, build_dir):
    pbuild.execute_rebuild_command(workspace, build_dir)

def execute_run_command(workspace, build_dir):
    console = Console()
    execute_build_command(workspace, build_dir)
    data = load_flasher_commands_json(build_dir)
    if data is None:
        console.print(f"[red]No flasher commands found in {build_dir}/flasher_commands.json[/red]")
        sys.exit(1)
    toolsettings = load_tool_settings_json()
    stm32_programmer_cli = toolsettings.get('stm32_programmer_cli', None)
    if not stm32_programmer_cli:
        raise ValueError("STM32 Programmer CLI path is not set in toolsettings.json")
    command = f"{stm32_programmer_cli} -c port=SWD -d {data['EXECUTABLE_ELF']} -rst"
    try:
        for line in runner.execute(command, cwd=build_dir):
            raw_bytes = line.encode('latin1')
            correct_line = raw_bytes.decode('cp437').strip()
            print(correct_line)
    except subprocess.CalledProcessError:
        console.print(f"[red]Error while flashing binary: {line.strip()}[/red]")
        sys.exit(1)
    console.print(f"[green]Flash OK![/green]")

def flash_elf(elf_file):
    console = Console()
    toolsettings = load_tool_settings_json()
    stm32_programmer_cli = toolsettings.get('stm32_programmer_cli', None)
    if not stm32_programmer_cli:
        raise ValueError("STM32 Programmer CLI path is not set in toolsettings.json")
    command = f"{stm32_programmer_cli} -c port=SWD -d {elf_file} -rst"
    elf_file = os.path.abspath(elf_file)
    try:
        for line in runner.execute(command):
            raw_bytes = line.encode('latin1')
            correct_line = raw_bytes.decode('cp437').strip()
            print(correct_line)
    except subprocess.CalledProcessError:
        console.print(f"[red]Error while flashing binary: {line.strip()}[/red]")
        sys.exit(1)
    console.print(f"[green]Flash OK![/green]")


if __name__ == "__main__":
    action = sys.argv[1]

    if action == 'build':
        workspace = sys.argv[2]
        build_dir = os.path.join(workspace, 'build')
        execute_build_command(workspace, build_dir)
    elif action == 'rebuild':
        workspace = sys.argv[2]
        build_dir = os.path.join(workspace, 'build')
        execute_rebuild_command(workspace, build_dir)
    elif action == 'run':
        workspace = sys.argv[2]
        build_dir = os.path.join(workspace, 'build')
        execute_run_command(workspace, build_dir)
    elif action == 'flash-elf':
        flash_elf(sys.argv[2])
    else:
        sys.exit(1)
