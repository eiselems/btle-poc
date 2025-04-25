
# Bluetooth LE IoT Device Configuration PoC

This repository contains a proof of concept (PoC) demonstrating BLE (Bluetooth Low Energy) communication between an IoT device and a customer setup application. The project simulates the common use case of configuring an IoT device with WiFi credentials via BLE.

---

## Project Overview

The project includes two separate implementations:

### Node.js Implementation
- **IoT Device (Peripheral/GATT Server)** – Advertises and accepts configuration data  

### Python Implementation
- **Customer App (Central/Client)** – Discovers and sends data to the IoT device

---

## Prerequisites

### Node.js Implementation
- Node.js (v12 or later recommended)
- Bluetooth adapter with BLE support
- Linux/macOS (Node.js BLE libraries have limited Windows support)

### Python Implementation
- Python 3.9 or later
- Bluetooth adapter with BLE support
- Platform requirements for [Bleak](https://github.com/hbldh/bleak):
  - macOS 10.15+ (Catalina or newer)
  - Linux with BlueZ ≥ 5.43
  - Windows 10 (May 2019 Update or newer)

---

## Setup Instructions

### Node.js Setup
Install dependencies:

> **Note:** Node.js BLE packages may require additional system dependencies:

#### Linux (not tested):
```bash
sudo apt-get install bluetooth bluez libbluetooth-dev libudev-dev
```

#### macOS:
- Xcode Command Line Tools

---

### Python Setup
Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Applications

### Node.js Implementation
Start the IoT device simulator (in one terminal):

```bash
node iot-device.js
```

### Python Implementation
Start the customer setup app (in another terminal):

```bash
python customer-app.py
```

---

## Architecture

### Service & Characteristic UUIDs
- **Service UUID:** `12345678-1234-5678-1234-56789abcdef0`
- **Characteristic UUID:** `12345678-1234-5678-1234-56789abcdef1`


---

## Communication Flow

1. IoT device advertises its presence with a specific service UUID
2. Customer app scans for devices with that service UUID
3. Customer app connects to the IoT device
4. Customer app writes configuration data (as JSON) to the characteristic
5. IoT device receives and processes the configuration

---

## Troubleshooting

- Ensure Bluetooth is enabled on your system
- Check that your Bluetooth adapter supports BLE
- Run the applications with elevated permissions if needed (e.g., `sudo` on Linux)
- Make sure no other applications are using the Bluetooth adapter
- Verify that the device is discoverable with a Bluetooth scanner app

---

## License

ISC License
