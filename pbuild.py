
import sys
import subprocess
import os
import shutil
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeRemainingColumn, TimeElapsedColumn
from rich.text import Text
from rich.panel import Panel
from rich.live import Live
import json
import re
import time
from runner import execute


class COLORS:
    LIGHT_GRAY = "#c7c7c7"
    LIME_GREEN = "#579C57"


def delete_build_dir(build_dir):
    shutil.rmtree(build_dir, ignore_errors=True)


def run_and_print_build_command(command, cwd=None, description="Running command"):
    console = Console()
    console.log(f"[bold #6A5ACD]{description}...[/bold #6A5ACD]") # Slate Blue for description
    warnings_counter = 0
    errors_counter = 0

    try:
        with Progress(
            SpinnerColumn(spinner_name="dots", style="bold #ADD8E6"),
            TextColumn("[progress.description]{task.description}", style="#ADD8E6"),
            BarColumn(
                bar_width=50,
                style="#27272B",
                complete_style="#A8B3E4",
                finished_style="#ADD8E6"
            ),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%", style="#ADD8E6"),
            TimeRemainingColumn(),
            TimeElapsedColumn(),
            console=console,
            transient=True
        ) as progress:
            task = progress.add_task(f"[#ADD8E6]{description}", total=None)

            for line in execute(command, cwd=cwd):
                stripped_line = line.strip()
                match = re.search(r"\[(\d+)\s*/\s*(\d+)\]", stripped_line)
                if match:
                    current = int(match.group(1))
                    total = int(match.group(2))
                    progress.update(task, completed=current, total=total)

                # Check for errors and warnings
                error_pattern = re.compile(r".+?:\d+:\d+:\s+(fatal\s+error|error):", re.IGNORECASE)
                warning_pattern = re.compile(r".+?:\d+:\s+warning:", re.IGNORECASE)
                if error_pattern.search(stripped_line):
                    errors_counter += 1
                    console.print(f"[bold bright_red]{stripped_line}[/bold bright_red]")
                elif warning_pattern.search(stripped_line):
                    warnings_counter += 1
                    console.print(f"[#FFDAB9]{stripped_line}[/#FFDAB9]")
                else:
                    console.print(f"[{COLORS.LIGHT_GRAY}]{stripped_line}[/{COLORS.LIGHT_GRAY}]")

        if warnings_counter > 0:
            console.print(f"[bold orange3]Warnings: {warnings_counter}[/bold orange3]")  # Orange
        if errors_counter > 0:
            console.print(f"[bold bright_red]Errors: {errors_counter}[/bold bright_red]")  # Red
        console.print(f"[bold #579C57]Build OK[/bold #579C57] 😀 ") # Lime Green

    except subprocess.CalledProcessError as e:
        # The execute function already printed the output, but we need to print the summary and failure message
        if warnings_counter > 0:
            console.print(f"[bold orange3]Warnings: {warnings_counter}[/bold orange3]")  # Orange
        if errors_counter > 0:
            console.print(f"[bold bright_red]Errors: {errors_counter}[/bold bright_red]")  # Red
        console.print(f"[bold bright_red]Build FAILED[/bold bright_red] ☹️ ") # Bright Red
        sys.exit(e.returncode) # Exit with the actual return code

    except FileNotFoundError:
        console.print(Panel(
            Text(f"Error: Command not found. Make sure '{command[0]}' is in your PATH.", style="bold bright_red"),
            title="[bold bright_red]Command Not Found[/bold bright_red]",
            border_style="bright_red"
        ))
        sys.exit(1)
    except Exception as e:
        console.print(Panel(
            Text(f"An unexpected error occurred: {e}", style="bold bright_red"),
            title="[bold bright_red]Unexpected Error[/bold bright_red]",
            border_style="bright_red"
        ))
        sys.exit(1)


def run_cmake_build(workspace, build_dir):
    console = Console()
    cmd = ['cmake', '--build', build_dir]
    console.print(f"[{COLORS.LIGHT_GRAY}]Executing: {" ".join(cmd)}[/{COLORS.LIGHT_GRAY}]")
    run_and_print_build_command(cmd, cwd=workspace)


def execute_cmake(workspace, build_dir):
    console = Console()
    cmd = [
        'cmake',
        '-S', workspace,
        '-B', build_dir,
        '-G', 'Ninja',
        '-DCMAKE_GENERATOR=Ninja' ]
    console.print(f"[{COLORS.LIGHT_GRAY}]Executing: {" ".join(cmd)}[{COLORS.LIGHT_GRAY}]")
    try:
        for line in execute(cmd):
            stripped_line = line.strip()
            console.print(f"[{COLORS.LIGHT_GRAY}]{stripped_line}[/{COLORS.LIGHT_GRAY}]")
    except subprocess.CalledProcessError:
        print("CMake configure failed  ☹️ ")
        sys.exit(0)
    console.print(f"[white]CMake configure OK[/white]")


def execute_build_command(workspace, build_dir):
    execute_cmake(workspace, build_dir)
    run_cmake_build(workspace, build_dir)


def execute_rebuild_command(workspace, build_dir):
    console = Console()
    console.print("Deleting build directory...")
    delete_build_dir(build_dir)
    execute_build_command(workspace, build_dir)
