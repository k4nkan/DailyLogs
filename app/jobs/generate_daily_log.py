"""
Generate daily log.
"""

from datetime import datetime, timedelta, timezone
from app.services import get_daily_messages, summarize, push_daily_log


def main():
    """Main function."""
    utc_now = datetime.now(timezone.utc)
    jst_now = utc_now + timedelta(hours=9)

    date = jst_now.date().isoformat()

    msgs = get_daily_messages(utc_now)
    if not msgs:
        print(f"No messages found for {date}")
        return

    raw = "\n".join(m["content"] for m in msgs)
    summary = summarize(raw)

    print(summary)

    # push_daily_log(date, summary)


if __name__ == "__main__":
    main()
