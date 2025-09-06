import subprocess
import yaml
from pathlib import Path
from string import Template
import os
import click
import time

from . import samples

PACKAGE_DRIVERS = {
    "winget": 'winget install --id "{pkg}" --silent --accept-source-agreements --accept-package-agreements',
    "scoop": "scoop install {pkg}",
    "chocolatey": "choco install {pkg} -y",
    "brew": "brew install {pkg}",
    "apt": "sudo apt-get install -y {pkg}",
    "pacman": "sudo pacman -S --noconfirm {pkg}",
    "dnf": "sudo dnf install -y {pkg}",
}


def run_cmd(
    cmd: str,
    cwd: str = None,
    params: dict = {},
    verbose: bool = True,
    dry_run: bool = False,
):
    """Run a shell command with optional cwd and template substitution."""
    final_cmd = Template(cmd).safe_substitute(params)
    final_cwd = Template(cwd).safe_substitute(params) if cwd else None

    if dry_run:
        click.echo(
            f"[DRY-RUN] ➡️ Running: {final_cmd}"
            + (f" in {final_cwd}" if final_cwd else "")
        )
        return

    click.echo(f"➡️ Running: {final_cmd}" + (f" in {final_cwd}" if final_cwd else ""))
    if verbose:
        subprocess.run(final_cmd, shell=True, check=True, cwd=final_cwd)
    else:
        subprocess.run(
            final_cmd,
            shell=True,
            check=True,
            cwd=final_cwd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )


def expand_list_params(cmd, params):
    """Expand commands if any param is a list. Returns a list of commands."""
    result_cmds = [cmd]
    for key, val in params.items():
        if isinstance(val, list):
            temp_cmds = []
            for c in result_cmds:
                if f"{{{{{key}}}}}" in c:
                    for item in val:
                        temp_cmds.append(c.replace(f"{{{{{key}}}}}", f'"{item}"'))
                else:
                    temp_cmds.append(c)
            result_cmds = temp_cmds
    final_cmds = []
    for c in result_cmds:
        final_cmds.append(Template(c).safe_substitute(params))
    return final_cmds


def process_commands(commands, params, verbose=True, dry_run=False):
    """Process a list of commands (strings or dict with cmd+dir)."""
    for item in commands:
        if isinstance(item, dict):
            cmd, cwd = item.get("cmd"), item.get("dir")
        else:
            cmd, cwd = item, None
        for c in expand_list_params(cmd, params):
            run_cmd(c, cwd, params, verbose, dry_run)


def install_software(software_list, driver, params, verbose=True, dry_run=False):
    """Install software using the chosen package driver, handling list params."""
    driver_template = PACKAGE_DRIVERS.get(driver)
    if not driver_template:
        raise ValueError(f"Unknown driver '{driver}'")
    processed_list = []
    for pkg in software_list:
        if isinstance(pkg, str) and "{{" in pkg:
            processed_list.extend(expand_list_params(pkg, params))
        else:
            processed_list.append(pkg)
    for pkg in processed_list:
        run_cmd(driver_template.format(pkg=pkg), verbose=verbose, dry_run=dry_run)


def create_files(files_dict, params, dry_run=False):
    """Create files with content substitution."""
    for path_str, content in files_dict.items():
        path = Path(os.path.expandvars(os.path.expanduser(path_str)))
        if dry_run:
            click.echo(f"[dry-run] 📝 Would create file: {path}")
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(Template(content).safe_substitute(params), encoding="utf-8")
            click.echo(f"📝 Created file: {path}")


def show_drivers():
    """Show available drivers."""
    click.echo("Available drivers:")
    for driver in PACKAGE_DRIVERS.keys():
        click.echo(f"{driver}: {PACKAGE_DRIVERS[driver]}")


def generate_sample_template(template: str):
    """Generate a sample template or show all available templates automatically from module globals."""

    # Extract all attributes ending with _full or _minimal
    templates_samples = {
        name: getattr(samples, name)
        for name in dir(samples)
        if name.endswith("_full") or name.endswith("_minimal")
    }

    if template == None:
        click.echo("Available templates:")
        for name in templates_samples:
            click.echo(f"  - {name}")
        return

    if template not in templates_samples:
        click.echo(f"❌ Unknown template: {template}")
        click.echo("Available templates:")
        for name in templates_samples:
            click.echo(f"  - {name}")
        return

    # Print the selected template content
    click.echo(templates_samples[template])


@click.command()
@click.argument("yaml_file", type=click.Path(exists=True), required=False)
@click.option(
    "-v", "--verbose", is_flag=True, default=False, help="Show detailed command output"
)
@click.option(
    "-d",
    "--dry-run",
    is_flag=True,
    default=False,
    help="Show commands without executing",
)
@click.option(
    "-l",
    "--list",
    "show_driver",
    is_flag=True,
    default=False,
    help="Show available installer drivers",
)
@click.option(
    "-g",
    "--generate",
    "generate_template_name",
    required=False,
    default=None,
    help="Generate sample template (e.g., 'windows-full'). If not provided, will list "
    "all available templates.",
)
@click.option("-t", "--list-templates", is_flag=True, help="List all available templates")
def main(yaml_file, verbose, dry_run, show_driver, generate_template_name, list_templates):
    """Quick developer machine setup based on YAML."""

    if show_driver:
        show_drivers()
        return

    if list_templates:
        generate_sample_template(None)
        return

    if generate_template_name:
        generate_sample_template(generate_template_name)
        return

    if not yaml_file:
        raise click.BadParameter("yaml_file is required unless using -l/--list")

    start_time = time.time()
    with open(yaml_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    driver = data.get("driver", "winget")
    params = data.get("params", {})
    before = data.get("before", [])
    install_list = data.get("install", [])
    after_dict = data.get("after", {})
    files_dict = data.get("files", {})

    if before:
        click.echo("⏳ Running before commands...")
        process_commands(before, params, verbose, dry_run)

    if install_list:
        click.echo("⏳ Installing software...")
        install_software(install_list, driver, params, verbose, dry_run)

    if after_dict:
        click.echo("⏳ Running after commands...")
        for section, cmds in after_dict.items():
            click.echo(f"📍 << {section} >>")
            process_commands(cmds, params, verbose, dry_run)

    if files_dict:
        click.echo("⏳ Creating files...")
        create_files(files_dict, params, dry_run)

    elapsed = time.time() - start_time
    click.echo(f"✅ Setup completed in {elapsed:.2f} seconds")


if __name__ == "__main__":
    main()
