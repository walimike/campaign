from main import CampaignDataAggregator

def main():
    revenue_file = 'revenue_1.csv'
    cost_file = 'cost_1.csv'
    output_file = 'aggregated_campaign_data.csv'

    aggregator = CampaignDataAggregator(revenue_file, cost_file)

    # Run the aggregation with optional date filtering
    date_from = '2018-12-31'
    date_to = '2019-01-01'
    aggregator.run(date_from=date_from, date_to=date_to, output_file=output_file)

if __name__ == "__main__":
    main()
