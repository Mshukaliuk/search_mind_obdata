import pandas as pd
from tabulate import tabulate
from datetime import datetime

# ADD right path!
fileinput = '/Users/mariashukaliuk/Downloads/Maria_report_for_Aske.csv'
save_path = '/Users/mariashukaliuk/Downloads'



# DONT CHANGE ANYTHING BELOW

df = pd.read_csv(fileinput)

df['Clicks'] = df['Clicks'].astype(str).str.replace(',', '').astype(float).astype(int).round()
df['Impr.'] = df['Impr.'].astype(str).str.replace(',', '').astype(float).astype(int).round()
df['Conversions'] = df['Conversions'].astype(str).str.replace(',', '').astype(float)

search_brand_df = df[(df['Campaign type'] == 'Search') & (df['Campaign'].str.contains('brand', case=False))]
search_non_brand_df = df[(df['Campaign type'] == 'Search') & (~df['Campaign'].str.contains('brand', case=False))]
yt_dg_df = df[df['Campaign type'].isin(['Demand Gen', 'Video'])]
display_df = df[df['Campaign type'] == 'Display']
pmax_df = df[df['Campaign type'] == 'Performance Max']
shop_df = df[df['Campaign type'] == 'Shopping']

# Cost amount
curr_num = int(input('How many currencies are you working with: ').strip())

currency_to_report = 0
curlist = []

while curr_num > currency_to_report:
    cur = input('Insert currency code: ').strip()
    currency_to_report = currency_to_report + 1
    curlist.append(cur)

def calculate_total_cost(df, curlist, exchange_rates):
    total_cost_df = 0
    cost_sums = {}

    for df_name, df_data in df:
        cost_sum_0 = df_data[df_data['Currency code'] == curlist[0]]['Cost'].sum()
        cost_sums[f"cost_sum_{curlist[0]}"] = float(cost_sum_0)

        for i in range(1, len(curlist)):
            if (curlist[i], curlist[0]) in exchange_rates:
                rate = exchange_rates[(curlist[i], curlist[0])]
            else:
                rate = float(input(f"Enter the exchange rate from {curlist[i]} to {curlist[0]}: ").strip())
                exchange_rates[(curlist[i], curlist[0])] = rate

            cost_sum_i = df_data[df_data['Currency code'] == curlist[i]]['Cost'].sum()
            cost_sum_i_in_0 = cost_sum_i * rate
            cost_sums[f"cost_sum_{curlist[i]}_in_{curlist[0]}"] = round(float(cost_sum_i_in_0), 2)

        total_cost_df += sum(float(value) for value in cost_sums.values())

    # print("Total Cost for", df_name, ":", round(total_cost_df, 2))

    return total_cost_df


def calculate_total_conv(df, curlist, exchange_rates):
    total_conv_df = 0
    conv_sums = {}

    for df_name, df_data in df:
        conv_sum_0 = df_data[df_data['Currency code'] == curlist[0]]['Conv. value'].sum()
        conv_sums[f"conv_sum_{curlist[0]}"] = float(conv_sum_0)

        for i in range(1, len(curlist)):
            if (curlist[i], curlist[0]) in exchange_rates:
                rate = exchange_rates[(curlist[i], curlist[0])]
            else:
                rate = float(input(f"Enter the exchange rate from {curlist[i]} to {curlist[0]}: ").strip())
                exchange_rates[(curlist[i], curlist[0])] = rate

            conv_sum_i = df_data[df_data['Currency code'] == curlist[i]]['Conv. value'].sum()
            conv_sum_i_in_0 = conv_sum_i * rate
            conv_sums[f"conv_sum_{curlist[i]}_in_{curlist[0]}"] = round(float(conv_sum_i_in_0), 2)

        total_conv_df += sum(float(value) for value in conv_sums.values())

    # print("Total Revenue for", df_name, ":", round(total_conv_df, 2))

    return total_conv_df

print('\n Type your exchange rates__________________________________________\n')
df_list = [("Search (Generic)", search_non_brand_df),
           ("Brand (Core)", search_brand_df),
           ("Youtube/demand gen", yt_dg_df),
           ("Display", display_df),
           ("Performance Max", pmax_df),
           ("Shopping", shop_df)]

exchange_rates = {}  # Dictionary to store exchange rates

for df_name, df_data in df_list:
    total_cost = calculate_total_cost([(df_name, df_data)], curlist, exchange_rates)
    total_conv = calculate_total_conv([(df_name, df_data)], curlist, exchange_rates)

# Clicks amount
clicks_non_brand_sum = search_non_brand_df['Clicks'].sum()
clicks_brand_sum = search_brand_df['Clicks'].sum()

clicks_yt_dg_sum = yt_dg_df['Clicks'].sum()
clicks_display_sum = display_df['Clicks'].sum()
clicks_pmax_sum = pmax_df['Clicks'].sum()
clicks_shop_sum = shop_df['Clicks'].sum()

# print('\n Print CLICKS results__________________________________________\n')
# print("clicks_NON_brand_sum", clicks_non_brand_sum)

# Impr amount
impr_brand_sum = search_brand_df['Impr.'].sum()
impr_non_brand_sum = search_non_brand_df['Impr.'].sum()
impr_yt_dg_sum = yt_dg_df['Impr.'].sum()
impr_display_sum = display_df['Impr.'].sum()
impr_pmax_sum = pmax_df['Impr.'].sum()
impr_shop_sum = shop_df['Impr.'].sum()

# print('\n Print IMPRESSIONS results__________________________________________\n')
# print("impr_brand_sum", impr_brand_sum)

# Conv amount
conv_brand_sum = search_brand_df['Conversions'].sum()
conv_non_brand_sum = search_non_brand_df['Conversions'].sum()
conv_yt_dg_sum = yt_dg_df['Conversions'].sum()
conv_display_sum = display_df['Conversions'].sum()
conv_pmax_sum = pmax_df['Conversions'].sum()
conv_shop_sum = shop_df['Conversions'].sum()

# print('\n Print CONVERSION results__________________________________________\n')
# print("conv_brand_sum ", conv_brand_sum )

# Define columns
columns = ['Conversions', 'Clicks', 'Impr.', 'Revenue', 'Spend', 'AOV', 'CPC', 'ROAS', 'CPM']
"""
'Conversions', 'Clicks', 'Impr.' - getting from file
'Revenue' - conversion value based metrics -calculate_total_conv
'Spend' - cost - calculate_total_cost
'AOV' = Revenue/Clicks
'CPC' = Spend/Clicks
'ROAS' = Spend/Revenue
'CPM' = Spend/Impr.*1000
"""

# Define rows
rows = [
    ("Search (Generic)", search_non_brand_df),
    ("Brand (Core)", search_brand_df),
    ("Youtube/demand gen", yt_dg_df),
    ("Display", display_df),
    ("Performance Max", pmax_df),
    ("Shopping", shop_df)
]

table_list = []

for row_name, df_row in rows:
    data = []
    for col_name in columns:
        if col_name == 'Revenue':
            revenue = calculate_total_conv([(row_name, df_row)], curlist, exchange_rates)
            data.append(round(revenue, 2))

        elif col_name == 'Spend':
            spend = calculate_total_cost([(row_name, df_row)], curlist, exchange_rates)
            data.append(round(spend, 2))

        elif col_name == 'AOV':
            conversions = df_row['Conversions'].sum()
            if conversions != 0:
                aov = calculate_total_conv([(row_name, df_row)], curlist, exchange_rates) / conversions
                data.append(round(aov, 2))
            else:
                data.append(0)

        elif col_name == 'CPC':
            conversions = df_row['Clicks'].sum()
            if conversions != 0:
                cpc = calculate_total_cost([(row_name, df_row)], curlist, exchange_rates) / conversions
                data.append(round(cpc, 2))
            else:
                data.append(0)

        elif col_name == 'ROAS':
            spend = calculate_total_cost([(row_name, df_row)], curlist, exchange_rates)
            revenue = calculate_total_conv([(row_name, df_row)], curlist, exchange_rates)
            if spend != 0:
                roas = spend / revenue
                data.append(round(roas, 2))
            else:
                data.append(0)

        elif col_name == 'CPM':
            spend = calculate_total_cost([(row_name, df_row)], curlist, exchange_rates)
            impr = df_row['Impr.'].sum()
            if spend != 0:
                cpm = spend / impr *1000
                data.append(round(cpm, 2))
            else:
                data.append(0)

        else:
            impr_sum = '{:.0f}'.format(df_row[col_name].sum())
            data.append(impr_sum)

    # Додавання даних до списку
    table_list.append([row_name] + data)

# Друк таблиці
print(tabulate(table_list, headers=[''] + columns, tablefmt='grid'))

# Збереження результатів у файл Excel
timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
filename = timestamp + 'GoogleAds_ExportReport.xlsx'  # Назва файлу
with pd.ExcelWriter(filename, engine='openpyxl') as writer:
    pd.DataFrame(table_list, columns=[''] + columns).to_excel(writer, index=False, sheet_name='Results')