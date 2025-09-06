# Quick Setup

Quick Setup is a Python-based tool that automates the setup of a developer environment on 
Windows, macOS, or Linux. It reads a YAML configuration file describing software to install,
commands to run before and after installation, and files to create.

The tool supports multiple package managers and can iterate over lists of parameters for repeated tasks.

# Usage
 ```bash
 $ quick-setup --help                   
Usage: quick-setup [OPTIONS] YAML_FILE

  Quick developer machine setup based on YAML.

Options:
  -v, --verbose  Show detailed command output
  -d, --dry-run  Show commands without executing
  --help         Show this message and exit.
 ```

# 🚀 Features

* Install software with winget, scoop, chocolatey, brew, apt, pacman, or dnf.
* Run pre-install (before) and post-install (after) commands.
* Automatically handle list parameters for iteration (e.g., multiple repos or SDK versions).
* Create configuration files with template substitution.
* Optionally run in verbose mode to see all output.
* Prints total setup time at the end.
* Dry run will only print the commands without running it.

# 🎯 Intention

The goal of Quick Setup is to simplify the process of setting up a new development machine, ensuring that all tools, programming languages, cloud CLIs, IDEs, and Kubernetes tooling are installed correctly and consistently, with minimal manual steps.

It is especially useful for:

* Developers provisioning new machines.
* Teams wanting a reproducible environment.
* Multi-platform setups (Windows, macOS, Linux).

Automating repetitive setup tasks across multiple machines.

# 📄 YAML Configuration

The YAML file defines:
* Driver
* before commands
* install software usign the driver
* after commands
* file creation


## Driver – Which package manager to use:

driver: winget  # options: winget, scoop, chocolatey, brew, apt, pacman, dnf


Params – Variables for templates:
```yaml
params:
  name: Joe Doe
  email: joe@email.com
  ssh_key_path: ~/.ssh/id_rsa
  python_default: 3.12
  repos:
    - git@github.com:user/repo1.git
    - git@github.com:user/repo2.git
  repos_dir: ~/Projects
  dotnet_sdk:
    - 8
    - 10
```

## Before commands – Commands to run before installation:
```yaml
before:
  - sudo apt update
  - sudo apt upgrade -y
  - mkdir -p "{{repos_dir}}"
```

## Install – List of software packages (supports template iteration):

```yaml
install:
  - git
  - git-lfs
  - kubectl
  - helm
  - dotnet-sdk-{{dotnet_sdk}}
```

## After commands – Commands to run after installation:

```yaml
after:
  <whatever-label-you-whant>:
    - git config --global user.name "{{name}}"
    - git config --global user.email "{{email}}"
    - git lfs install
  python:
    - uv python install 3.10
    - uv python install {{python_default}}
    - uv python list
  clone-repos:
    - cmd: git clone {{repos}}
      dir: {{repos_dir}}
```

## Files – Create configuration files with templated content:

```yaml
files:
  "~/.config/my_app_config.ini": |
    [settings]
    enabled=true
    name={{name}}
    email={{email}}
```

# 💻 Usage

Install Quick Setup
```bash
pip install quick-setup
```

Run with a YAML file
```bash
quick-setup path/to/setup.yml
```

Run in verbose mode
```bash
quick-setup path/to/setup.yml -v
```

Run in dry run mode
```bash
quick-setup path/to/setup.yml -d
```

# 🛠 Use Cases

* New Developer Machine
  - Automatically install Git, Docker, NodeJS, Python, .NET SDKs, Kubernetes tools, and IDEs.

* Team Reproducibility
  - Share a single YAML config for all team members to ensure consistent environments.

* Multi-platform Setup
  - Supports Windows, macOS, and Linux via the appropriate package manager.

* Automated Repo Cloning
  - Clones multiple repositories and sets up SSH keys automatically.

* Custom Config Files
  - Create .ini, .yaml, or any config files with templated content.

# ⚡ Example: Minimal macOS YAML
Please check the examples folder.

# 🔧 Supported Package Managers
Platform	Manager
Windows	winget, scoop, chocolatey
macOS	brew
Linux	apt, pacman, dnf

# 📌 Notes
* List Parameters: Any params that are lists will be automatically iterated in install and after commands.
* Template Syntax: Use {{param_name}} to substitute a variable.
* Verbose Flag: -v shows all command outputs; without it, output is suppressed.
* Files: Paths support ~ and environment variables like %USERPROFILE% or $HOME.