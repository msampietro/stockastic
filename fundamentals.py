import json
import os

from datetime import datetime, timedelta
from stockapi import get_earnings_calendar

def update_earnings_calendar(future_days, filename):
    # Determine the date range
    current_date = datetime.now().date()
    end_date = (current_date + timedelta(days=future_days))

    # Check if the file exists and is not empty
    if os.path.exists(filename) and os.path.getsize(filename) > 0:
        with open(filename, 'r') as json_file:
            earnings_data = json.load(json_file)

        existing_dates = sorted(
            datetime.strptime(date, '%Y-%m-%d').date() for date in earnings_data.keys()
        )

        new_dates = set()

        # Find the latest existing date
        latest_existing_date = existing_dates[-1] if existing_dates else current_date - timedelta(days=1)

        # Determine the new date range to query
        for day in range((end_date - latest_existing_date).days):
            query_date = latest_existing_date + timedelta(days=day + 1)
            if query_date not in existing_dates:
                new_dates.add(query_date)
        
        if new_dates:
            # Query the missing date range in one go
            new_start_date = min(new_dates).strftime('%Y-%m-%d 00:00:00')
            new_end_date = max(new_dates).strftime('%Y-%m-%d 23:59:59')
            earnings_calendar = get_earnings_calendar(new_start_date, new_end_date)

            # Update earnings_data with the new earnings
            for date in new_dates:
                date_str = date.strftime('%Y-%m-%d')
                earnings_list = earnings_calendar.get(date_str)
                if earnings_list is not None:
                    earnings_data[date_str] = earnings_list

            # Remove outdated entries
            cutoff_date = end_date.strftime('%Y-%m-%d')
            earnings_data = {date: data for date, data in earnings_data.items() if date <= cutoff_date}

            # Save the updated earnings data to the file
            with open(filename, 'w', encoding='utf-8') as json_file:
                json.dump(earnings_data, json_file, ensure_ascii=False, indent=4)
            print(f"Earnings calendar updated successfully in {filename}")
        else:
            print("Earnings calendar is already up to date.")
    else:
        # If the file does not exist or is empty, fetch the full range of data
        earnings_calendar = get_earnings_calendar(current_date.strftime('%Y-%m-%d 00:00:00'), end_date.strftime('%Y-%m-%d 23:59:59'))
        with open(filename, 'w', encoding='utf-8') as json_file:
            json.dump(earnings_calendar, json_file, ensure_ascii=False, indent=4)
        print(f"Earnings calendar saved successfully in {filename}")