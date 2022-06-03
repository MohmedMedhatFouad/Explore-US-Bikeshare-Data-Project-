import time
import pandas as pd
import numpy as np

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
    
    print('Hello! Let\'s explore some US bikeshare data!')
    # list of available cites
    cites = ['chicago', 'new york city', 'washington']
    # get user input for city (chicago, new york city, washington).    
    city = input("Would you like to see data for Chicago, New york city, or Washington?\n")
    # check city while input not in cites list ask him again
    while city.lower() not in cites:
        city = input("It's not available! Would you like to see data for Chicago, New york city, or Washington?\n")
    
    #list of filterion
    filter_by_list = ['month', 'day', 'both', 'all']    
    # list of available months
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    # list of available days
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']     
    #get filtertion input
    filter_by = input("Would you like to filter the data by month, day, both, or all?\n")      
    # check filtertion input if it month ==> get which month from user & assign day to all,
    # if it day ==> get which day from user & assign month to all ,
    # if it both ==> get which month & day from user,
    # if it all ==> assign day & month to all "no filter".
    while filter_by not in filter_by_list:
        filter_by = input("It's not available! Would you like to filter the data by month, day, both, or all?\n")
    else:        
        if filter_by.lower() == filter_by_list[0]:
            # get user input for month (all, january, february, ... , june)
            month = input("which month - January, February, March,  April, May, June or All?\n")
            # check month while month input not in months list ask him again
            while month.lower() not in months:
                month = input("It's not available! which month - January, February, March,  April, May, June or All?\n")
            day = "all"  

        elif filter_by.lower() == filter_by_list[1]:
            # get user input for day of week (all, monday, tuesday, ... sunday)
            day = input("Which day -  Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday or All?\n")
            # check day while input not in days list ask him again
            while day.lower() not in days:
                day = input("It's not available! Which day -  Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or All?\n")
            month = "all"  

        elif filter_by.lower() == filter_by_list[2]:
            # get user input for month (all, january, february, ... , june)
            month = input("which month - January, February, March, April, May, June or All?\n")
            # check month while month input not in months list ask him again
            while month.lower() not in months:
                month = input("It's not available! which month - January, February, March, April, May, June or All?\n")
            # get user input for day of week (all, monday, tuesday, ... sunday)    
            day = input("Which day -  Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or All?\n")
            # check day while input not in days list ask him again
            while day.lower() not in days:
                day = input("It's not available! Which day -  Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or All?\n")

        else:
            month = "all"
            day = "all"
        
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
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

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
    
    # display the most common month
    common_month = df['month'].mode()[0]
    print('Most Common Month:', common_month)     
    
    # display the most common day of week
    common_day_week = df['day_of_week'].mode()[0]
    print('Most Common Day of Week:', common_day_week)
    
    # display the most common start hour
    common_hour = df['hour'].mode()[0]
    print('Most Common Start Hour:', common_hour)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print("Most common start station:", common_start_station)

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print("Most common end station:", common_end_station)

    # display most frequent combination of start station and end station trip
    df['Trip'] = df['Start Station'] + ' to ' + df['End Station']
    common_total_trip = df['Trip'].mode()[0]
    print("Most Common Trip: ", common_total_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)    


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum()
    print("Total Travel Time:", total_time , "Sec.")

    # display mean travel time
    average_time = df['Trip Duration'].mean()
    print("Average Travel Time:", average_time , "Sec.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    if "User Type" in df.columns:
        user_types = df['User Type'].value_counts()
        print(user_types.to_string())   
        
    # Display counts of gender
    if "Gender" in df.columns:
        gender = df['Gender'].value_counts()
        print(gender.to_string())
                      
    # Display earliest, most recent, and most common year of birth
    if "Birth Year" in df.columns:        
        print("Earliest Year of Birth:", int(df['Birth Year'].min()))
        print("Most Recent Year of Birth:", int(df['Birth Year'].max()))
        print("Most common Year of Birth:", int(df['Birth Year'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    
def display_raw_data(df):
    """Displays a 5 random sample of raw data."""
    
    # ask user if want to view a sample data
    response = input("Would you like to view individual trip data?\n")
    # check respone while it yes print 5 sample
    while response.lower() == "yes":
        print(df.head(5))
        df.drop(df.head(5).index, inplace = True)
        response = input("Would you like to view individual trip data? Enter yes or no.\n")
        

def main():
    
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
