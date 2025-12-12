# Mac → Raspberry Pi Zero 2 W

## Basic Operation Flow (SSH / systemd)

This document describes the **minimal and practical workflow** to manage a Raspberry Pi Zero 2 W from a Mac using SSH.

---

## 1. Connect to Raspberry Pi via SSH

```bash
ssh kanta@kanta.local
```

## 2. Copy files from Mac to Raspberry Pi

Copy the entire bot directory. The destination `~/bot` will be overwritten.
_Version control is handled on the Mac side only._

```bash
scp -r bot kanta@kanta.local:/home/kanta/
```

## 3. Install Python packages on Raspberry Pi

Run this only on first setup or when `requirements.txt` changes.
_Note: No virtual environment is used (intentional for dedicated Pi device)._

```bash
cd ~/bot
pip3 install -r requirements.txt --break-system-packages
```

> **Note**: `--break-system-packages` is required on Raspberry Pi OS (PEP 668).

## 4. Control the systemd service

Restart the service (most common):

```bash
sudo systemctl restart dailylogs-bot
```

Stop the service:

```bash
sudo systemctl stop dailylogs-bot
```

Start the service:

```bash
sudo systemctl start dailylogs-bot
```

## 5. Check service status

```bash
systemctl status dailylogs-bot
```

**Expected state:**

```text
Active: active (running)
```

## 6. View service logs (real-time)

```bash
journalctl -u dailylogs-bot -f
```

## 7. Edit the systemd service file

```bash
sudo nano /etc/systemd/system/dailylogs-bot.service
```

**Nano key bindings:**

- Save: `Ctrl + O` → `Enter`
- Exit: `Ctrl + X`

**Apply changes:**

```bash
sudo systemctl daemon-reload
sudo systemctl restart dailylogs-bot
```

## 8. Exit SSH session

You can close your Mac terminal. The bot will continue running on Raspberry Pi.

```bash
exit
```

---

## Command Cheat Sheet

```bash
ssh kanta@kanta.local
scp -r bot kanta@kanta.local:/home/kanta/
pip3 install -r requirements.txt --break-system-packages
sudo systemctl restart dailylogs-bot
systemctl status dailylogs-bot
journalctl -u dailylogs-bot -f
exit
```
