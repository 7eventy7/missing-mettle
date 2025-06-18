<div align="center">
  
# Missing Mettle

### Track your missing Team Fortress 2 weapons.

[![GitHub issues](https://img.shields.io/github/issues/7eventy7/missing-mettle.svg)](https://github.com/7eventy7/missing-mettle/issues)
[![License](https://img.shields.io/github/license/7eventy7/missing-mettle.svg)](https://github.com/7eventy7/missing-mettle/blob/main/LICENSE)

A modern, dark-themed desktop application for Team Fortress 2 players to track missing unlockable weapons in their Steam inventory.

</div>

## Features

- **Comprehensive Weapon Tracking**: Automatically detects all weapon qualities
- **Smart Name Matching**: Removes quality prefixes to accurately match weapons
- **Dual Display**: Side-by-side view of missing weapons and obtained weapons
- **Advanced Filtering**: Filter missing weapons by class, slot, and type
- **Dark Theme UI**: Modern, easy-on-the-eyes dark themed interface 
- **Steam Integration**: Works with SteamID64, custom URLs, or profile URLs
- **Real-time Status**: Live updates during inventory scanning with pagination support

## Installation

1. **Install Python** (if not already installed)
   - Download from [python.org](https://www.python.org/downloads/)

2. **Install required dependencies**
   ```bash
   pip install requests
   ```

3. **Download the application files**
   - Download the latest release and unzip it
   - Run `main.pyw` to start the application

## Setup Instructions

### 1. Steam Profile Configuration
- Set your Steam profile to **PUBLIC**
- Ensure your inventory is set to **PUBLIC**
- Note your Steam profile information (SteamID64 or custom URL)

### 2. Finding Your Steam ID
You can use any of these formats:

**SteamID64** (17 digits starting with 7656119):
```
76561198123456789
```

**Custom URL** (just the username):
```
your_username
```

**Profile URLs**:
```
https://steamcommunity.com/id/your_username
https://steamcommunity.com/profiles/76561198123456789
```

### 3. Get Steam API Key
   - Visit [Steam Web API Key Registration](https://steamcommunity.com/dev/apikey)
   - Register with any domain name (e.g., "localhost")
   - Copy your API key

## Troubleshooting

**"Steam inventory is private" (403 Error)**
- Set your Steam profile to PUBLIC
- Set your inventory to PUBLIC in privacy settings

**"Steam profile not found" (404 Error)**
- Verify the Steam ID format is correct
- Ensure the profile exists and is spelled correctly

**"No weapons found"**
- Check if you have TF2 items in your Steam inventory
- Verify your Steam profile has TF2 in the game library
- Some items might not be recognized as weapons

**"list.json not found"**
- Ensure `list.json` is in the same folder as `main.py`
- Check file name spelling and case sensitivity

**API Key Issues**
- Verify your Steam API key is correct
- Ensure you're not hitting Steam API rate limits (wait a few minutes)

## License

This project is provided as-is for personal use. Steam, Team Fortress 2, and related trademarks are property of Valve Corporation.
