import time
import pandas as pd
import numpy as np
from scipy import stats

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
   
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    print('Hello! Let\'s explore some US bikeshare data!')
    print('Which city would you like to see data for ? Chicago, New York or Washington.')
    while True:
        city = input('City Name: ').lower()
        cities = ['chicago','new york city','washington']
        if city not in cities:
          print("Sorry, please enter one of this cities Chicago,New York or Washigton")
          continue
        else:
          print('\n')
          break

    # TO DO: get user input for month (all, january, february, ... , june)
    print('Which month ? January, February, March, April, May, June or all')
    while True:
        month = input('Enter month: ').lower()
        months = ['january','february','march','april','may','june','all']
        if month not in months:
          print("Sorry, invalid month, try again \n")
          continue;
        else:
          print('\n')
          break; 

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    print('Which day? all, Monday, Tuesday, Wednesday, Thusday, Friday, Saturday or Sunday')
    while True:
        day = input('Enter day: ').title()
        days_of_the_week = ['Monday','Tuesday','Wednesday','Thusday','Friday','Saturday','Sunday','All']
        if day not in days_of_the_week:
          print("Sorry, invalid day, try again \n")
          continue;
        else:
          print('\n')
          break; 
    
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df0 = pd.read_csv(CITY_DATA[city])
    
    # We drop any rows with NaN values
    df=df0.dropna(axis = 0)

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    months = df['month'].values
    month_mode = stats.mode(months)
    most_common_month_int = month_mode[0][0]
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    common_month = months[most_common_month_int - 1]
    print("Most common month is", common_month)

    # TO DO: display the most common day of week
    common_day_series = df.loc[:,"day_of_week"].mode()
    common_day = common_day_series.values[0]
    print("Most common day is", common_day)
    
    # TO DO: display the most common start hour
    hours = np.array(df['Start Time'].dt.hour)
    hours_mode = stats.mode(hours)
    common_hour = hours_mode[0][0]
    print("Most common start hour is", common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    
    # Function to display most common start and end station
    def Common_used_start_end_station(station_input):
        station = df[station_input].values
        station_mode = stats.mode(station)
        Common_used_station = station_mode[0][0]
        print(f"Most commonly used {station_input} is:", Common_used_station)

    # TO DO: display most commonly used start station
    Common_used_start_end_station('Start Station')
    
    # TO DO: display most commonly used end station
    Common_used_start_end_station('End Station')

    # TO DO: display most frequent combination of start station and end station trip
    df['start_end_station']= df['Start Station'] + ' + ' + df['End Station']
    start_end_stations = df['start_end_station'].values
    Start_end_stations_mode = stats.mode(start_end_stations)
    frequent_combination = Start_end_stations_mode[0][0]
    print("Most frequent combination of start station and end station trip is:", frequent_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    travel_duration_array = df['Trip Duration'].values
    total_travel_time = sum(travel_duration_array)
    print('Total travel time is:', total_travel_time)

    # TO DO: display mean travel time
    travel_duration_array = df['Trip Duration'].values
    mean_travel_time = np.mean(travel_duration_array)
    print('Mean travel time is:', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""
    print(df.info())

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types_count = df['User Type'].value_counts()
    print(user_types_count)

    # TO DO: Display counts of gender
    try:
        gender_count = df['Gender'].value_counts()
        print(gender_count)
    except: 
        print('dataframe has no "Gender column')
    
    # TO DO: Display earliest, most recent, and most common year of birth
    
    try:
        earliest_birth_year = df['Birth Year'].min()
        most_recent = df['Birth Year'].max()
        birth_years = df['Birth Year'].values
        birth_years_mode = stats.mode(birth_years)
        common_birth_year = birth_years_mode[0][0]
        print("The earliest year of birth is:", earliest_birth_year)
        print("The most recent year of birth is:", most_recent)
        print("The most common year of birth is:", common_birth_year)
    except: 
        print('dataframe has no "Birth Year')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    """Displays data row as per user input Yes or No"""
    
    # Get user input "Yes" or "No"
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower()
    start_loc = 0
    row_count = 5
    while (view_data == 'yes'):
        print(df.iloc[start_loc:row_count])
        start_loc += 5
        row_count += 5
        view_data = input("Do you wish to continue?: ").lower()

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
