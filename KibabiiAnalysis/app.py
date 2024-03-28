import streamlit as st
import pandas as pd
import plotly.express as px

# Function to add date features
def add_date_features(df, date_column_name):
    df["Day"] = df[date_column_name].dt.dayofweek
    df["Month"] = df[date_column_name].dt.month
    df["Year"] = df[date_column_name].dt.year
    df["Q"] = df[date_column_name].dt.quarter
    df["Dayofyear"] = df[date_column_name].dt.dayofyear
    df["Dayofmonth"] = df[date_column_name].dt.day
    df["Weekofyear"] = df[date_column_name].dt.isocalendar().week
    df["Season"] = df["Month"].apply(categorize_season)
    return df

# Function to categorize seasons
def categorize_season(month):
    # Define a mapping of months to seasons
    season_mapping = {
        1: 1,
        2: 1,
        3: 2,
        4: 2,
        5: 2,
        6: 3,
        7: 3,
        8: 3,
        9: 4,
        10: 4,
        11: 4,
        12: 1
    }

    # Return the corresponding season based on the month
    return season_mapping[month]

# Function to load rainfall data
def load_rainfall_data():
    rainfall_df = pd.read_csv(r"KibabiiAnalysis\Kibabii University data.xlsx - Rainfall.csv")
    rainfall_df['ID'] = pd.to_datetime(rainfall_df['ID'], format='%Y%m%d')
    rainfall_df = add_date_features(rainfall_df, 'ID')
    rainfall_df.set_index('ID', inplace=True)
    return rainfall_df

# Function to load temperature max data
def load_temp_max_data():
    temp_max_df = pd.read_csv(r"KibabiiAnalysis\Kibabii University data.xlsx - Tmax.csv")
    temp_max_df['ID'] = pd.to_datetime(temp_max_df['ID'], format='%Y%m%d')
    temp_max_df = add_date_features(temp_max_df, 'ID')
    temp_max_df.set_index('ID', inplace=True)
    return temp_max_df

# Function to load temperature min data
def load_temp_min_data():
    temp_min_df = pd.read_csv(r"KibabiiAnalysis\Kibabii University data.xlsx - Tmin.csv")
    temp_min_df['ID'] = pd.to_datetime(temp_min_df['ID'], format='%Y%m%d')
    temp_min_df = add_date_features(temp_min_df, 'ID')
    temp_min_df.set_index('ID', inplace=True)
    return temp_min_df

# Plot yearly averages
def plot_yearly_averages(data, column):
    yearly_averages = data.groupby("Year")[column].mean()
    fig = px.line(yearly_averages, x=yearly_averages.index, y=yearly_averages.values, title=f"Yearly Average {column}")
    st.plotly_chart(fig)

# Plot monthly averages
def plot_monthly_averages(data, column):
    monthly_averages = data.groupby("Month")[column].mean()
    # Rename index to month names
    monthly_averages.index = pd.date_range(start='2022-01-01', periods=12, freq='M').month_name()
    fig = px.line(monthly_averages, x=monthly_averages.index, y=monthly_averages.values, title=f"Monthly Average {column}")
    st.plotly_chart(fig)

# Plot seasonal averages
def plot_seasonal_averages(data, column):
    seasonal_averages = data.groupby("Season")[column].mean()
    season_names = {1: "Hot and Dry_Season", 2: "Long Rains", 3: "Dry Season", 4: "Short Rains"}
    seasonal_averages.index = seasonal_averages.index.map(season_names)
    fig = px.bar(seasonal_averages, x=seasonal_averages.index, y=seasonal_averages.values, title=f"Seasonal Average {column}")
    st.plotly_chart(fig)
    
# Plot quarterly averages
def plot_quarterly_averages(data, column, year, quarter):
    quarterly_data = data[(data["Year"] == year) & (data["Q"] == quarter)]
    quarterly_averages = quarterly_data.groupby("Month")[column].mean()
    
    # Determine the correct month labels for the selected quarter
    if quarter == 1:
        month_labels = ["Jan", "Feb", "Mar"]
    elif quarter == 2:
        month_labels = ["Apr", "May", "Jun"]
    elif quarter == 3:
        month_labels = ["Jul", "Aug", "Sep"]
    else:
        month_labels = ["Oct", "Nov", "Dec"]
        
    quarterly_averages.index = month_labels
    
    fig = px.line(quarterly_averages, x=quarterly_averages.index, y=quarterly_averages.values, title=f"Quarterly Average {column} - Q{quarter} {year}")
    st.plotly_chart(fig)


# Page: Home
def page_home():
    st.title("Welcome to Your Weather Data App!")
    st.write("This app allows you to explore rainfall and temperature data.")
    st.write("Please use the sidebar to navigate to different pages.")

# Page 1: Rainfall Data
def page_rainfall():
    st.title("Rainfall Data in mm")
    rainfall_data = load_rainfall_data()
    show_data = st.checkbox("Show Data")
    if show_data:
        st.write(rainfall_data)
    st.write(rainfall_data.describe())

    # Plotting section
    st.subheader("Plot Rainfall Data")
    selected_column = st.selectbox("Select Column", rainfall_data.columns)
    plot_type = st.selectbox("Select Plot Type", ["Yearly", "Monthly", "Seasonal", "Quarterly"])
    if plot_type == "Yearly":
        plot_yearly_averages(rainfall_data, selected_column)
    elif plot_type == "Monthly":
        plot_monthly_averages(rainfall_data, selected_column)
    elif plot_type == "Quarterly":
        selected_year = st.selectbox("Select Year", sorted(rainfall_data["Year"].unique()))
        selected_quarter = st.selectbox("Select Quarter", [1, 2, 3, 4])
        plot_quarterly_averages(rainfall_data, selected_column, selected_year, selected_quarter)
    else:
        plot_seasonal_averages(rainfall_data, selected_column)

# Page 2: Temperature Max Data
def page_temp_max():
    st.title(u'Temperature Max Data (\u2103)')
    temp_max_data = load_temp_max_data()
    show_data = st.checkbox("Show Data")
    if show_data:
        st.write(temp_max_data)
    st.write(temp_max_data.describe())

    # Plotting section
    st.subheader("Plot Temperature Max Data")
    selected_column = st.selectbox("Select Column", temp_max_data.columns)
    plot_type = st.selectbox("Select Plot Type", ["Yearly", "Monthly", "Seasonal", "Quarterly"])
    if plot_type == "Yearly":
        plot_yearly_averages(temp_max_data, selected_column)
    elif plot_type == "Monthly":
        plot_monthly_averages(temp_max_data, selected_column)
    elif plot_type == "Quarterly":
        selected_year = st.selectbox("Select Year", sorted(temp_max_data["Year"].unique()))
        selected_quarter = st.selectbox("Select Quarter", [1, 2, 3, 4])
        plot_quarterly_averages(temp_max_data, selected_column, selected_year, selected_quarter)
    else:
        plot_seasonal_averages(temp_max_data, selected_column)

# Page 3: Temperature Min Data
def page_temp_min():
    st.title(u"Temperature Min Data (\u2103)")
    temp_min_data = load_temp_min_data()
    show_data = st.checkbox("Show Data")
    if show_data:
        st.write(temp_min_data)
    st.write(temp_min_data.describe())

    # Plotting section
    st.subheader("Plot Temperature Min Data")
    selected_column = st.selectbox("Select Column", temp_min_data.columns)
    plot_type = st.selectbox("Select Plot Type", ["Yearly", "Monthly", "Seasonal", "Quarterly"])
    if plot_type == "Yearly":
        plot_yearly_averages(temp_min_data, selected_column)
    elif plot_type == "Monthly":
        plot_monthly_averages(temp_min_data, selected_column)
    elif plot_type == "Quarterly":
        selected_year = st.selectbox("Select Year", sorted(temp_min_data["Year"].unique()))
        selected_quarter = st.selectbox("Select Quarter", [1, 2, 3, 4])
        plot_quarterly_averages(temp_min_data, selected_column, selected_year, selected_quarter)
    else:
        plot_seasonal_averages(temp_min_data, selected_column)

# Main function to run the app
def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Go to", ["Home", "Rainfall Data", "Temperature Max Data", "Temperature Min Data"])

    if page == "Home":
        page_home()
    elif page == "Rainfall Data":
        page_rainfall()
    elif page == "Temperature Max Data":
        page_temp_max()
    elif page == "Temperature Min Data":
        page_temp_min()

if __name__ == "__main__":
    main()
