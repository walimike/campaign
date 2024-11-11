import pandas as pd

class CampaignDataAggregator:
  def __init__(self, revenue_file, cost_file):
    self.revenue_file = revenue_file
    self.cost_file = cost_file

  def load_data(self):
    self.revenue_df = pd.read_csv(self.revenue_file)
    self.cost_df = pd.read_csv(self.cost_file)

    self.revenue_df['data_date'] = pd.to_datetime(self.revenue_df['data_date'], format='%m/%d/%y %H:%M').dt.tz_localize('America/New_York').dt.tz_convert('UTC')
    self.cost_df['data_date'] = pd.to_datetime(self.cost_df['data_date'], format='%m/%d/%y %H:%M').dt.tz_localize('America/New_York').dt.tz_convert('UTC')

  def merge_data(self):
    self.merged_df = pd.merge(self.revenue_df, self.cost_df, on=['data_date', 'campaign_id'], how='inner')

  def filter_data(self, date_from=None, date_to=None):
    if date_from:
        date_from = pd.to_datetime(date_from).tz_localize('UTC')
        self.merged_df = self.merged_df[self.merged_df['data_date'] >= date_from]
    if date_to:
        date_to = pd.to_datetime(date_to).tz_localize('UTC')
        self.merged_df = self.merged_df[self.merged_df['data_date'] <= date_to]

  def calculate_metrics(self):
    self.merged_df['date'] = self.merged_df['data_date'].dt.strftime('%Y/%m/%d')
    self.merged_df['total_profit'] = self.merged_df['revenue'] - self.merged_df['cost']
    self.merged_df['UV'] = self.merged_df['revenue'] / self.merged_df['clicks']
    self.merged_df['CPC'] = self.merged_df['cost'] / self.merged_df['clicks']
    self.merged_df['ROI'] = self.merged_df['UV'] / self.merged_df['CPC']

  def aggregate_data(self):
    self.aggregated_df = self.merged_df.groupby(['date', 'campaign_id', 'campaign_name']).agg(
        total_revenue=('revenue', 'sum'),
        total_cost=('cost', 'sum'),
        total_profit=('total_profit', 'sum'),
        total_clicks=('clicks', 'sum'),
        avg_cpc=('CPC', 'mean'),
        total_roi=('ROI', 'mean'),
        hourly_avg_revenue=('revenue', 'mean')  # Assuming hourly average over multiple rows in a day
    ).reset_index()

  def save_data(self, output_file):
    self.aggregated_df.to_csv(output_file, index=False)
    print(f"Aggregated data saved to {output_file}")

  def run(self, date_from=None, date_to=None, output_file='aggregated_campaign_data.csv'):
    self.load_data()
    self.merge_data()
    self.filter_data(date_from, date_to)
    self.calculate_metrics()
    self.aggregate_data()
    self.save_data(output_file)
