# Sample YAML templates

windows_full = """
driver: winget  # options: winget, brew, apt, pacman

params:
  name: Your Name
  email: you@example.com
  ssh_key_path: C:\\Users\\%USERNAME%\\.ssh\\id_rsa
  python_default: 3.12
  repos:
    - git@github.com:user/repo1.git
    - git@github.com:user/repo2.git
  repos_dir: C:\\Projects
  dotnet_sdk:
    - 8
    - 10

install:
  - Google.Chrome
  - Postman.Postman
  - Git.Git
  - Git.GitLFS
  - Microsoft.WSL
  - Docker.DockerDesktop
  - 7zip.7zip
  - Microsoft.WindowsTerminal
  - astral-sh.uv
  - Microsoft.DotNet.SDK.{{dotnet_sdk}}
  - NodeJS.NodeJS
  - Rust.Rust
  - Amazon.AWSCLI
  - Microsoft.VisualStudio.2022.Community
  - Microsoft.VisualStudioCode
  - JetBrains.Rider
  - JetBrains.PyCharm
  - dbeaver.dbeaver
  - Helm.Helm
  - Kubernetes.kubectl
  - derailed.k9s
  - Headlamp.Headlamp

after:
  git:
    - git config --global user.name "{{name}}"
    - git config --global user.email "{{email}}"
    - git lfs install
    - ssh-keygen -t rsa -b 4096 -C "{{email}}" -f "{{ssh_key_path}}" -N ""
  python:
    - uv python install 3.10
    - uv python install 3.11
    - uv python install 3.12
    - uv python install 3.13
    - uv python use {{python_default}}
    - uv python list
  dotnet:
    - dotnet --list-sdks
    - dotnet workload install --all --sdk {{dotnet_sdk}}.0
  docker-images:
    - docker pull postgres
  check-versions:
    - docker --version
    - helm version
    - kubectl version --client
    - k9s version
    - headlamp --version
"""

windows_minimal = """
driver: winget

params:
  name: Your Name
  email: you@example.com
  python_default: 3.12

install:
  - Git.Git
  - Docker.DockerDesktop
  - Microsoft.VisualStudioCode
  - Python.Python.3.12

after:
  git:
    - git config --global user.name "{{name}}"
    - git config --global user.email "{{email}}"
  python:
    - uv python install {{python_default}}
    - uv python use {{python_default}}
"""

mac_full = """
driver: brew

params:
  name: Your Name
  email: you@example.com
  ssh_key_path: ~/.ssh/id_rsa
  python_default: 3.12
  repos:
    - git@github.com:user/repo1.git
    - git@github.com:user/repo2.git
  repos_dir: ~/Projects

install:
  - git
  - git-lfs
  - docker
  - helm
  - kubectl
  - node
  - rust
  - visual-studio-code
  - pycharm
  - jetbrains-rider

after:
  git:
    - git config --global user.name "{{name}}"
    - git config --global user.email "{{email}}"
    - git lfs install
    - ssh-keygen -t rsa -b 4096 -C "{{email}}" -f "{{ssh_key_path}}" -N ""
  python:
    - uv python install 3.10
    - uv python install 3.11
    - uv python install 3.12
    - uv python use {{python_default}}
"""

mac_minimal = """
driver: brew

params:
  name: Your Name
  email: you@example.com
  python_default: 3.12

install:
  - git
  - docker
  - visual-studio-code
  - python

after:
  git:
    - git config --global user.name "{{name}}"
    - git config --global user.email "{{email}}"
  python:
    - uv python install {{python_default}}
    - uv python use {{python_default}}
"""

ubuntu_full = """
driver: apt

params:
  name: Your Name
  email: you@example.com
  ssh_key_path: ~/.ssh/id_rsa
  python_default: 3.12
  repos:
    - git@github.com:user/repo1.git
    - git@github.com:user/repo2.git
  repos_dir: ~/Projects

install:
  - git
  - git-lfs
  - docker.io
  - docker-compose
  - helm
  - kubectl
  - nodejs
  - npm
  - rustc
  - cargo
  - code
  - pycharm
  - jetbrains-rider

after:
  git:
    - git config --global user.name "{{name}}"
    - git config --global user.email "{{email}}"
    - git lfs install
    - ssh-keygen -t rsa -b 4096 -C "{{email}}" -f "{{ssh_key_path}}" -N ""
  python:
    - uv python install 3.10
    - uv python install 3.11
    - uv python install 3.12
    - uv python use {{python_default}}
"""

ubuntu_minimal = """
driver: apt

params:
  name: Your Name
  email: you@example.com
  python_default: 3.12

install:
  - git
  - docker.io
  - code
  - python3

after:
  git:
    - git config --global user.name "{{name}}"
    - git config --global user.email "{{email}}"
  python:
    - uv python install {{python_default}}
    - uv python use {{python_default}}
"""
