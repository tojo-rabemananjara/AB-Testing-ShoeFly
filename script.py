import pandas as pd

#read csv file
ad_clicks = pd.read_csv('ad_clicks.csv')
print(ad_clicks.head())

#view clicks by source
view_counts = ad_clicks.groupby('utm_source').user_id.count().reset_index()
print(view_counts)

#view clicks by source : #clicked & #not clicked
ad_clicks['is_click'] = ~ad_clicks.ad_click_timestamp.isnull()
clicks_by_source = ad_clicks.groupby(['utm_source', 'is_click']).user_id.count().reset_index().rename(columns = {'user_id': 'count'})
clicks_pivot = clicks_by_source.pivot(
  columns = 'is_click',
  index = 'utm_source',
  values = 'count'
)
print(clicks_pivot)

#view percent clicked by source
clicks_pivot['percent_clicked'] = (clicks_pivot[True] / (clicks_pivot[True] + clicks_pivot[False]) * 100).round(2)
print(clicks_pivot)

#view percent clicks by experiment (A/B)
clicks_by_exp = ad_clicks.groupby(['experimental_group', 'is_click']).user_id.count().reset_index().rename(columns = {'user_id': 'count'})
clicks_by_exp_piv = clicks_by_exp.pivot(
  columns = 'is_click',
  index = 'experimental_group',
  values = 'count'
)
clicks_by_exp_piv['percent_clicked'] = ((clicks_by_exp_piv[True]/(clicks_by_exp_piv[True] + clicks_by_exp_piv[False])) * 100).round(2)
print(clicks_by_exp_piv)

#view A percent clicked by day
a_clicks = ad_clicks[ad_clicks.experimental_group == 'A']
a_clicks_by_day = a_clicks.groupby(['day','is_click']).user_id.count().reset_index().rename(columns={'user_id': 'a_clicks_by_day'})
a_clicks_pivot = a_clicks_by_day.pivot(
  columns = 'is_click',
  index = 'day',
  values = 'a_clicks_by_day'
)
a_clicks_pivot['percent_clicked'] = ((a_clicks_pivot[True]/(a_clicks_pivot[True] + a_clicks_pivot[False])) * 100).round(2)
print(a_clicks_pivot)

#view B percent clicked by day
b_clicks = ad_clicks[ad_clicks.experimental_group == 'B']
b_clicks_by_day = b_clicks.groupby(['day','is_click']).user_id.count().reset_index().rename(columns={'user_id': 'b_clicks_by_day'})
b_clicks_pivot = b_clicks_by_day.pivot(
  columns = 'is_click',
  index = 'day',
  values = 'b_clicks_by_day'
)
b_clicks_pivot['percent_clicked'] = ((b_clicks_pivot[True]/(b_clicks_pivot[True] + b_clicks_pivot[False])) * 100).round(2)
print(b_clicks_pivot)

#The percent click for A is 37.48% compared to 30.83% for B. Overall use ad A. This pattern of A performing better than B is further
# evidenced in the distribution of A/B ad clicks by day where A has more %clicked for every day except Tuesday.
