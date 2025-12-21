# DailyLogs

## Project Overview

DailyLogs is a system designed to automate the process of keeping a daily journal. It allows you to send casual messages to a Discord bot throughout the day. These messages are stored and then processed to generate a structured daily log.

The workflow is as follows:

1.  **Input**: You send messages to a Discord bot.
2.  **Storage**: The bot saves these messages and their timestamps to Supabase.
3.  **Processing**: A daily script retrieves the day's messages (based on JST).
4.  **Enrichment**: The script creates a summary of your most played track on Spotify for that day. (Data source: [save-spotify-logs](https://github.com/k4nkan/save-spotify-logs))
5.  **Output**: The messages and song summary are formatted and pushed to Notion.

## How to Run

### Prerequisites

- Python 3.13 or higher
- Supabase project set up with a `logs` table.
- Notion Integration set up.

### Environment Variables

You need to set up `.env` files in both `bot/` and `script/` directories.

**`bot/.env`**:

```
DISCORD_TOKEN=your_discord_token
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

**`script/.env`**:

```
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
NOTION_API_KEY=your_notion_api_key
NOTION_DATASOURCE_ID=your_notion_database_id
SONG_SUPABASE_URL=your_song_supabase_url
SONG_SUPABASE_KEY=your_song_supabase_key
```

### 1. Run the Discord Bot

Start the bot to begin collecting messages.

```bash
cd bot
pip install -r requirements.txt
python main.py
```

### 2. Generate Daily Log

Run the script to fetch logs for the current day (JST) and push to Notion.

```bash
cd script
pip install -r requirements.txt
python main.py
```

## Architecture

The project is structured into two main components:

- **`bot/`**: Contains the Discord bot logic.
  - `main.py`: Handles Discord events and saves messages to Supabase.
- **`script/`**: Contains the daily processing logic.
  - `main.py`: Fetches logs from Supabase, formats them, and syncs to Notion.
  - `music/spotify_summary.py`: Fetches top track data from Supabase.
