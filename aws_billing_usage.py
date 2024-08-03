import boto3
import argparse
from datetime import datetime

def get_cost_and_usage(start_date, end_date, profile_name):
    session = boto3.Session(profile_name=profile_name)
    client = session.client('ce')

    response = client.get_cost_and_usage(
        TimePeriod={
            'Start': start_date,
            'End': end_date
        },
        Granularity='MONTHLY',
        Metrics=['BlendedCost'],
        GroupBy=[
            {
                'Type': 'DIMENSION',
                'Key': 'SERVICE'
            }
        ]
    )

    return response

def main():
    parser = argparse.ArgumentParser(description='Fetch AWS costs for a specified date range.')
    parser.add_argument('from_date', type=str, help='The start date for the cost retrieval in YYYY-MM-DD format.')
    parser.add_argument('to_date', type=str, help='The end date for the cost retrieval in YYYY-MM-DD format.')
    parser.add_argument('--profile', type=str, default='default', help='The AWS CLI profile to use.')

    args = parser.parse_args()

    # Validate date format
    try:
        datetime.strptime(args.from_date, '%Y-%m-%d')
        datetime.strptime(args.to_date, '%Y-%m-%d')
    except ValueError:
        print("Error: Dates must be in YYYY-MM-DD format.")
        return

    print(f"Fetching AWS costs from {args.from_date} to {args.to_date} using profile {args.profile}...")

    cost_response = get_cost_and_usage(args.from_date, args.to_date, args.profile)

    if 'ResultsByTime' in cost_response and cost_response['ResultsByTime']:
        results = cost_response['ResultsByTime'][0]
        groups = results.get('Groups', [])

        total_cost = 0.0
        unit = "USD"  # Default unit, assuming all costs are in the same unit

        print("AWS Services and their costs for the specified date range:")
        for group in groups:
            service = group['Keys'][0]
            amount = float(group['Metrics']['BlendedCost']['Amount'])
            unit = group['Metrics']['BlendedCost']['Unit']
            total_cost += amount
            print(f"{service}: {amount:.2f} {unit}")

        print(f"Total cost: {total_cost:.2f} {unit}")
    else:
        print("No cost data available for the specified period.")

if __name__ == "__main__":
    main()

