# this is a script for scraping planning applications from the London Planning Datahub. 

import requests
import pandas as pd
import json
from datetime import datetime, timedelta
import pyarrow as pa
import pyarrow.parquet as pq
from pyarrow import csv
import os
import time
from tqdm import tqdm
import argparse
import calendar

# Configuration
url = "https://planningdata.london.gov.uk/api-guest/applications/_search"
headers = {
    "X-API-AllowRequests": "X-API-AllowRequest",
    "Content-Type": "application/json"
}
DEFAULT_START_DATE = "01/01/2020"  # DD/MM/YYYY format
output_dir = "planning_data"
page_size = 1000  # Number of records per request
max_retries = 5
retry_delay = 3  # seconds
max_records_per_chunk = 9000  # Safety margin below the 10,000 limit

# Create output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def parse_date(date_str):
    """Parse date from DD/MM/YYYY format to datetime object"""
    return datetime.strptime(date_str, "%d/%m/%Y")

def format_date(date_obj):
    """Format datetime object to DD/MM/YYYY format"""
    return date_obj.strftime("%d/%m/%Y")

def get_date_chunks(start_date_str, end_date_str=None, chunk_size="month"):
    """Generate date chunks from start date to end date"""
    start_date = parse_date(start_date_str)
    
    if end_date_str:
        end_date = parse_date(end_date_str)
    else:
        end_date = datetime.now()
    
    chunks = []
    
    if chunk_size == "month":
        current_date = start_date.replace(day=1)  # Start at beginning of month
        
        while current_date <= end_date:
            # Calculate last day of current month
            if current_date.month == 12:
                next_month = current_date.replace(year=current_date.year + 1, month=1)
            else:
                next_month = current_date.replace(month=current_date.month + 1)
            
            last_day = next_month - timedelta(days=1)
            
            # Ensure we don't go beyond end_date
            if last_day > end_date:
                last_day = end_date
                
            chunks.append((format_date(current_date), format_date(last_day)))
            current_date = next_month
    
    elif chunk_size == "week":
        current_date = start_date
        
        while current_date <= end_date:
            next_date = current_date + timedelta(days=6)
            
            # Ensure we don't go beyond end_date
            if next_date > end_date:
                next_date = end_date
                
            chunks.append((format_date(current_date), format_date(next_date)))
            current_date = next_date + timedelta(days=1)
    
    elif chunk_size == "day":
        current_date = start_date
        
        while current_date <= end_date:
            chunks.append((format_date(current_date), format_date(current_date)))
            current_date += timedelta(days=1)
    
    return chunks

def fetch_data(from_date, to_date, from_idx=0, size=page_size):
    """Fetch data from the Elasticsearch API with date range and pagination"""
    query = {
        "query": {
            "bool": {
                "must": [
                    {
                        "range": {
                            "valid_date": {
                                "gte": from_date,
                                "lte": to_date
                            }
                        }
                    }
                ]
            }
        },
        "from": from_idx,
        "size": size
    }
    
    for attempt in range(max_retries):
        try:
            response = requests.post(url, headers=headers, json=query)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Request failed (attempt {attempt+1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                raise Exception(f"Failed to fetch data after {max_retries} attempts")

def get_total_records(from_date, to_date):
    """Get total number of records for a date range"""
    response_data = fetch_data(from_date, to_date, 0, 1)
    return response_data["hits"]["total"]["value"]

def fetch_all_for_date_range(from_date, to_date, progress_bar=None):
    """Fetch all records for a specific date range"""
    total_records = get_total_records(from_date, to_date)
    
    if total_records == 0:
        return []
    
    if total_records > max_records_per_chunk:
        print(f"\nDate range {from_date} to {to_date} has {total_records} records (exceeds limit).")
        print("Subdividing into smaller chunks...")
        
        # Try weekly chunks first
        weekly_chunks = get_date_chunks(from_date, to_date, "week")
        all_records = []
        
        for week_from, week_to in weekly_chunks:
            week_total = get_total_records(week_from, week_to)
            
            if week_total > max_records_per_chunk:
                # If weekly is still too large, go to daily
                print(f"  Weekly chunk {week_from} to {week_to} has {week_total} records (exceeds limit).")
                print("  Further subdividing into daily chunks...")
                
                daily_chunks = get_date_chunks(week_from, week_to, "day")
                
                for day_from, day_to in daily_chunks:
                    day_records = fetch_all_for_date_range(day_from, day_to, progress_bar)
                    all_records.extend(day_records)
            else:
                # Weekly chunk is manageable
                print(f"  Fetching weekly chunk {week_from} to {week_to} ({week_total} records)...")
                week_records = fetch_chunk_with_pagination(week_from, week_to, week_total, progress_bar)
                all_records.extend(week_records)
        
        return all_records
    else:
        # Date range is manageable, fetch with standard pagination
        return fetch_chunk_with_pagination(from_date, to_date, total_records, progress_bar)

def fetch_chunk_with_pagination(from_date, to_date, total_records, progress_bar=None):
    """Fetch all records for a date range using pagination"""
    all_records = []
    from_idx = 0
    
    while from_idx < total_records:
        batch_size = min(page_size, total_records - from_idx)
        response_data = fetch_data(from_date, to_date, from_idx, batch_size)
        hits = response_data["hits"]["hits"]
        batch_records = [hit["_source"] for hit in hits]
        all_records.extend(batch_records)
        
        # Update progress bar if provided
        if progress_bar:
            progress_bar.update(len(batch_records))
        
        from_idx += batch_size
    
    return all_records

def preview_data(start_date_str, sample_size=10):
    """Fetch a small sample of data to preview"""
    print(f"Fetching {sample_size} records for preview...")
    
    # Get today's date in required format
    today = format_date(datetime.now())
    
    response_data = fetch_data(start_date_str, today, 0, sample_size)
    total_records = response_data["hits"]["total"]["value"]
    hits = response_data["hits"]["hits"]
    records = [hit["_source"] for hit in hits]
    
    print(f"Total records available: {total_records}")
    
    # Convert to DataFrame
    df = pd.DataFrame(records)
    
    # Save sample data
    sample_csv_path = os.path.join(output_dir, "sample_data.csv")
    df.to_csv(sample_csv_path, index=False)
    
    # Display sample info
    print("\n===== DATA PREVIEW =====")
    print(f"Sample size: {len(df)} records")
    print(f"Columns ({len(df.columns)}): {', '.join(df.columns)}")
    print("\nFirst 5 rows:")
    print(df.head().to_string())
    print("\nData types:")
    print(df.dtypes)
    print(f"\nSample saved to: {sample_csv_path}")
    print("========================\n")
    
    return total_records

def clean_dataframe(df):
    """Clean and prepare DataFrame for saving to various formats"""
    # Convert all columns to string to avoid type issues
    for col in df.columns:
        if df[col].dtype == 'object':
            # Handle nested dictionaries/lists by converting to JSON strings
            df[col] = df[col].apply(
                lambda x: json.dumps(x) if isinstance(x, (dict, list)) else str(x) if x is not None else None
            )
    
    # Remove problematic characters from column names
    df.columns = [col.replace('.', '_').replace(' ', '_') for col in df.columns]
    
    return df

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Elastic database scraper')
    parser.add_argument('--test', action='store_true', help='Run in test mode to preview data')
    parser.add_argument('--sample-size', type=int, default=10, help='Number of records to fetch in test mode')
    parser.add_argument('--debug', action='store_true', help='Print debug information')
    parser.add_argument('--start-date', type=str, default=DEFAULT_START_DATE, 
                        help=f'Start date in DD/MM/YYYY format (default: {DEFAULT_START_DATE})')
    parser.add_argument('--end-date', type=str, default=None, 
                        help='End date in DD/MM/YYYY format (default: today)')
    parser.add_argument('--chunk-size', type=str, default='month', choices=['month', 'week', 'day'],
                        help='Initial time chunk size (default: month)')
    args = parser.parse_args()
    
    # Set start and end dates
    start_date_str = args.start_date
    end_date_str = args.end_date if args.end_date else format_date(datetime.now())
    
    if args.debug:
        # Print the actual query that will be sent
        test_query = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "range": {
                                "valid_date": {
                                    "gte": start_date_str,
                                    "lte": end_date_str
                                }
                            }
                        }
                    ]
                }
            },
            "from": 0,
            "size": 1
        }
        print("Debug - Query to be sent:")
        print(json.dumps(test_query, indent=2))
        print("\n")
    
    if args.test:
        preview_data(start_date_str, args.sample_size)
        return
    
    print(f"Starting data extraction from {start_date_str} to {end_date_str}...")
    
    # Get total count first to set up progress bar
    total_count = get_total_records(start_date_str, end_date_str)
    print(f"Found {total_count} total records across the entire date range.")
    
    # Generate date chunks
    date_chunks = get_date_chunks(start_date_str, end_date_str, args.chunk_size)
    print(f"Split into {len(date_chunks)} {args.chunk_size}ly chunks for processing.")
    
    # Set up progress bar
    progress_bar = tqdm(total=total_count, desc="Fetching records", unit="record")
    
    # Process each date chunk
    all_records = []
    for chunk_idx, (from_date, to_date) in enumerate(date_chunks):
        print(f"\nProcessing chunk {chunk_idx+1}/{len(date_chunks)}: {from_date} to {to_date}")
        chunk_records = fetch_all_for_date_range(from_date, to_date, progress_bar)
        all_records.extend(chunk_records)
    
    progress_bar.close()
    
    print(f"\nSuccessfully fetched {len(all_records)} records.")
    
    # Convert to DataFrame
    df = pd.DataFrame(all_records)
    
    # Clean DataFrame for saving
    print("Processing data for saving...")
    df_clean = clean_dataframe(df)
    
    # Save as CSV
    csv_path = os.path.join(output_dir, "planning_data.csv")
    df_clean.to_csv(csv_path, index=False)
    print(f"Data saved as CSV: {csv_path}")
    
    try:
        # Save as Parquet
        parquet_path = os.path.join(output_dir, "planning_data.parquet")
        df_clean.to_parquet(parquet_path, index=False)
        print(f"Data saved as Parquet: {parquet_path}")
        
        # Save as Arrow
        arrow_path = os.path.join(output_dir, "planning_data.arrow")
        table = pa.Table.from_pandas(df_clean)
        with pa.OSFile(arrow_path, 'wb') as sink:
            with pa.RecordBatchFileWriter(sink, table.schema) as writer:
                writer.write_table(table)
        print(f"Data saved as Arrow: {arrow_path}")
    
    except Exception as e:
        print(f"Error saving to Parquet/Arrow: {e}")
        print("Saving only raw data as JSON as fallback...")
        # Save raw data as JSON as fallback
        json_path = os.path.join(output_dir, "planning_data.json")
        with open(json_path, 'w') as f:
            json.dump(all_records, f)
        print(f"Raw data saved as JSON: {json_path}")
    
    print("Data extraction and saving completed!")

if __name__ == "__main__":
    main()
