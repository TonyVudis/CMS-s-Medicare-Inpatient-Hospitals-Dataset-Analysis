import matplotlib.pyplot as plt
import pandas as pd
import os

def load_data():
    py_path = os.getcwd()
    CMS_path = os.path.join(py_path, 'CMS.CSV')

    CMS_Data = pd.read_csv(CMS_path, encoding='utf-8')
    return CMS_Data

CMS_data = load_data()

def initial_data(data):
    #Data report
    data_report = {
        "columns": data.columns.tolist(),
        "shape": data.shape,
        "missing_values": data.isnull().sum().to_dict(),
        "duplicates": data.duplicated().sum()
    }
    #Copy to preserve original data
    data_copy = data.copy(deep=True)
    #Basic cleaning
    data_copy.dropna(inplace=True)
    data_copy.drop_duplicates(inplace=True)

    data_copy.columns = (
        data_copy.columns
        .str.lower()
        .str.strip()
        .str.replace(" ", "_")
    )
    #Adding to data report with cleaned data
    data_report["cleaned_columns"] = data_copy.columns.tolist()
    data_report['cleaned_shape'] = data_copy.shape
    data_report['cleaned_missing_values'] = data_copy.isnull().sum().to_dict()
    data_report['cleaned_duplicates'] = data_copy.duplicated().sum()

    return data_copy, data_report

CMS_data_cleaned, CMS_data_report = initial_data(CMS_data)

#Mapping states to regions for further analysis
def state_to_region(data):
    regions = {
        "New England": [
            "CT", "ME", "MA", "NH", "RI", "VT"
        ],
        "Middle Atlantic": [
            "NJ", "NY", "PA"
        ],
        "East North Central": [
            "IL", "IN", "MI", "OH", "WI"
        ],
        "West North Central": [
            "IA", "KS", "MN", "MO", "NE", "ND", "SD"
        ],
        "South Atlantic": [
            "DE", "DC", "FL", "GA", "MD", "NC", "SC", "VA", "WV"
        ],
        "East South Central": [
            "AL", "KY", "MS", "TN"
        ],
        "West South Central": [
            "AR", "LA", "OK", "TX"
        ],
        "Mountain": [
            "AZ", "CO", "ID", "MT", "NV", "NM", "UT", "WY"
        ],
        "Pacific": [
            "AK", "CA", "HI", "OR", "WA"
        ]
    }

    state_to_region = {
        state: region
        for region, states in regions.items()
        for state in states
    }

    data['region'] = data['rndrng_prvdr_state_abrvtn'].map(state_to_region)

    return data

CMS_data_regions = state_to_region(CMS_data_cleaned)

def bar_avg_tot_discharges_by_region(CMS_data_regions):

    #Scatter plot for avg total payment amount for each hospital
    fig_bar = plt.figure(figsize=(12, 6), dpi = 125)
    for region, region_data in CMS_data_regions.groupby('region'):
        plt.bar([region],
                [region_data['tot_dschrgs'].sum()/ region_data['tot_dschrgs'].count()],
                alpha=0.5,
                label=f'Region: {region}')
        
    plt.ylim(0, CMS_data_regions['tot_dschrgs'].sum()/ CMS_data_regions['tot_dschrgs'].count() *2)
    plt.xlabel('Region')
    plt.xticks(rotation=45, ha = 'right', fontsize = 7)
    plt.ylabel('Total Discharges')
    plt.title('Bar Plot for Avg Total Discharges for Each Region')
    plt.legend(fontsize = 8, ncol =2)
    plt.tight_layout(pad=2.0)
    
    discharge_insight="The region with the highest average discharges is the Midwest, while the lowest is the West."

    return fig_bar, discharge_insight

fig_bar, discharge_insight = bar_avg_tot_discharges_by_region(CMS_data_regions)

def scatter_avg_discharge_avg_payment_by_region(CMS_data_regions):
    fig_scatter = plt.figure(figsize=(12, 6), dpi = 125)
    for region, region_data in CMS_data_regions.groupby('region'):
        plt.scatter([region_data['tot_dschrgs'].sum()/ region_data['tot_dschrgs'].count()],
                 region_data['avg_tot_pymt_amt'].median(),
                 alpha=0.5,
                 label=f'Region: {region}')

    plt.xlabel('Avg Total Discharges Per Region')
    plt.ylabel('Avg Total Payment Amount Per Region')
    plt.title('Scatter Plot for Avg Total Discharges vs Avg Total Payment Amount by Region')
    plt.legend(fontsize = 8, ncol =2)
    plt.tight_layout(pad=2.0)

    payment_insight="The region with the highest average total payment amount is the Northeast, while the lowest is the South."

    return fig_scatter, payment_insight

fig_scatter, payment_insight = scatter_avg_discharge_avg_payment_by_region(CMS_data_regions)

def Overall_info(data):
    #Correlation between average covered charges and average medicare payments
    medi_cov_correlation = data['avg_submtd_cvrd_chrg'].corr(data['avg_mdcr_pymt_amt'])

    #Correlation between average medicare payments and average total payments
    medi_tot_correlation = data['avg_mdcr_pymt_amt'].corr(data['avg_tot_pymt_amt'])

    #What percent of the paid total amount is covered by Medicare payments by region
    medi_tot_percent = (
        data.assign(
            percentage=data["avg_mdcr_pymt_amt"] / data["avg_tot_pymt_amt"] * 100
        )
        .groupby("region", as_index=False)["percentage"]
        .mean()
        .round(2)
    )

    medi_tot_percent = medi_tot_percent.to_html(index=False)

    correlation_insight="There is a strong positive correlation between covered charges and Medicare payments, and a moderate positive correlation between Medicare payments and total payments."
    medi_tot_percent_insight="On average, Medicare payments cover a significant portion of the total payments."

    return medi_cov_correlation, medi_tot_correlation, medi_tot_percent, correlation_insight, medi_tot_percent_insight

medi_cov_correlation, medi_tot_correlation, medi_tot_percent, correlation_insight, medi_tot_percent_insight = Overall_info(CMS_data_cleaned)
