import argparse
from main import CampaignDataAggregator

def main():
    revenue_file = 'revenue_1.csv'
    cost_file = 'cost_1.csv'
    output_file = 'aggregated_campaign_data.csv'
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Aggregate campaign data with optional date filtering.")
    parser.add_argument("--date_from", help="Start date for filtering (e.g., 2018-12-31)")
    parser.add_argument("--date_to", help="End date for filtering (e.g., 2019-01-01)")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Create an instance of CampaignDataAggregator
    aggregator = CampaignDataAggregator(revenue_file, cost_file)

    # Run the aggregation with optional date filtering
    aggregator.run(date_from=args.date_from, date_to=args.date_to, output_file=output_file)

if __name__ == "__main__":
    main()
