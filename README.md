# 💻 System Information Tool

A simple command-line tool to display system information including CPU, memory, disk, network, and running processes.

## ✨ Features

- 🖥️ Display basic system information (OS, version, etc.)
- 🧠 Monitor CPU usage and details
- 📊 View memory and swap usage statistics
- 💾 Check disk space and partitions
- 🌐 View network interfaces and traffic statistics
- 📋 List top processes by CPU or memory usage
- 💾 Save information to JSON file for later analysis

## 📋 Requirements

- Python 3.6 or higher
- psutil library

## 🚀 Installation

1. Clone this repository:
```bash
git clone https://github.com/0xIntern4l/system-info-tool.git
cd system-info-tool
```

2. Install requirements:
```bash
pip install -r requirements.txt
```

3. Make the script executable (Unix/Linux/macOS):
```bash
chmod +x main.py
```

## 🔍 Usage

```bash
python main.py [options]
```

## ⚙️ Options

- `-a, --all`: Show all system information
- `-s, --system`: Show basic system information
- `-c, --cpu`: Show CPU information
- `-m, --memory`: Show memory information
- `-d, --disk`: Show disk information
- `-n, --network`: Show network information
- `-p, --processes`: Show top processes
- `--sort-by`: Sort processes by CPU or memory usage (default: memory)
- `--limit`: Limit number of processes shown (default: 10)
- `-o, --output`: Save output to file
- `-j, --json`: Output in JSON format


