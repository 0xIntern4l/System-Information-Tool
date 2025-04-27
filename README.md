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

## 📝 Examples

### Show basic system information:
```bash
python main.py
```

### Show all system information:
```bash
python main.py -a
```

### Show only CPU and memory information:
```bash
python main.py -c -m
```

### Show top 5 processes by CPU usage:
```bash
python main.py -p --sort-by cpu --limit 5
```

### Save all information to a JSON file:
```bash
python main.py -a -o system_info.json
```

### Output in JSON format:
```bash
python main.py -s -c -j
```

## 💡 Tips

- Run the tool with `-a` for a comprehensive system overview
- The output format can be changed to JSON using the `-j` option
- Save information to a file with `-o` for historical tracking
- You can combine options to get just the information you need
- The network and process information is especially useful for troubleshooting

