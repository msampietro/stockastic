import json
import os
from datetime import datetime, timedelta
from stockapi import get_earnings_calendar

def update_earnings_calendar(future_days, filename):
    current_date = datetime.now().date()
    end_date = current_date + timedelta(days=future_days)

    # Check if the file exists and is not empty
    earnings_data = {}
    if os.path.exists(filename) and os.path.getsize(filename) > 0:
        with open(filename, 'r') as json_file:
            earnings_data = json.load(json_file)
    
    # Convert existing dates from string to date objects
    existing_dates = {datetime.strptime(date, '%Y-%m-%d').date() for date in earnings_data.keys()}
    
    # Determine new dates that need to be fetched
    all_dates = {current_date + timedelta(days=day) for day in range((end_date - current_date).days + 1)}
    new_dates = sorted(all_dates - existing_dates)

    if new_dates:
        # Fetch earnings for the new date range
        new_start_date = new_dates[0].strftime('%Y-%m-%d 00:00:00')
        new_end_date = new_dates[-1].strftime('%Y-%m-%d 23:59:59')
        earnings_calendar = get_earnings_calendar(new_start_date, new_end_date)

        # Update earnings data with new fetched data
        for date in new_dates:
            date_str = date.strftime('%Y-%m-%d')
            earnings_list = earnings_calendar.get(date_str)
            if earnings_list:
                earnings_data[date_str] = earnings_list

        # Keep only recent entries (after or on current_date)
        earnings_data = {date: data for date, data in earnings_data.items() if datetime.strptime(date, '%Y-%m-%d').date() >= current_date}

        # Write updated data back to file
        with open(filename, 'w', encoding='utf-8') as json_file:
            json.dump(earnings_data, json_file, ensure_ascii=False, indent=4)
        print(f"Earnings calendar updated successfully in {filename}")
    else:
        print("Earnings calendar is already up to date.")