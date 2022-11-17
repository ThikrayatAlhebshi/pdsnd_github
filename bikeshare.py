import time
import pandas as pd
import sys

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
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
    month = 'all'
    day = 'all'
    # get user input for city (chicago, new york, washington). 
    while True:
        city = input('Would you like to see data for Chicago, New York, or Washington? \n')
        if city.lower() in ['chicago', 'new york', 'washington']:
           break
        else:
           print("Wrong input please choose from the list")    
# get user choice for filter type            
    while True:
        general_filter = input('Would you like to filter the data by month, day, both, or not at all? Type "none" for no time filter.\n')
        if general_filter.lower() == 'both':
            month = get_month()
            day = get_day()
            return city.lower(),month,day
        elif general_filter.lower() == 'month':
            month = get_month()
            return city.lower(),month,day
        elif general_filter.lower() == 'day':
            day = get_day()
            return city.lower(),month,day
        elif general_filter.lower() == 'none':
            return city.lower(),month,day
        else:
            print('Wrong input! please choose from the list')
    print('-'*40)
    return city.lower(), month, day


# get user input for month (all, january, february, ... , june)
def get_month():
     while True:
        month = input('Which month? January, February, March, April, May, June?\n')
        if month.lower() in ['january','february','march','april','may','june']:
            return month
        else:
            print("Wrong input please choose from the list")  
            
            
# get user input for day of week (all, monday, tuesday, ... sunday)        
def get_day():
    while True:
        week = {1:'Sunday',2:'Monday',3:'Tuesday',4:'Wednesday',5:'Thursday',6:'Friday',7:'Saturday'}
        day = input('Which day? please type your response as an integer (e.g. 1=Sunday)\n')
        if int(day) in week.keys():
            return week.get(int(day))
        else:
            print("Wrong input please choose from the list")  
        
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
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

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
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] =  df['Start Time'].dt.month
    df['day'] =  df['Start Time'].dt.day_name()
    df['hour'] =  df['Start Time'].dt.hour

    # display the most common month

    print('{} is the most common month'.format(df['month'].mode()[0]))

    # display the most common day of week
    print('{} is the most common day of week'.format( df['day'].mode()[0]))

    # display the most common start hour
    print('{} is the most common start hour'.format(df['hour'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    
    # display most commonly used start station
    print(df['Start Station'].mode()[0])

    # display most commonly used end station
    print(df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    print(df[['Start Station','End Station']].mode())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total trip time = ',df['Trip Duration'].sum())
    # display mean travel time
    print('Average trip time = ', df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    # Display counts of user types
    print(df['User Type'].value_counts())
    # check if gender column exist
    try:
        # Display counts of gender
        print(df['Gender'].value_counts())
    except KeyError:
        print('Gender data is not available!')
        
    # check if Birth Year column exist
    try:
        # Display earliest, most recent, and most common year of birth
        print('Earliest year of birth = ', df['Birth Year'].min())
        print('Most recent year of birth = ', df['Birth Year'].max())
        print('Most common year of birth = ', df['Birth Year'].mode()[0])
    except KeyError:
        print('Birth year data is not available!')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
# Display 5 rows of data
def display_data(df):
    x = 0
    y = 5
    while True:
        choice = input('Do you want to display more data? (Yes\\No) \n')
        if choice.lower() == 'no':
            break
        elif choice.lower() == 'yes':
            for i in range(x,y):
                 print(df.iloc[i,:],'\n')
            x = y
            y += 5
        else:
            print("Wrong input! Try again.")

        
def main():
    city, month, day = get_filters()
    df = load_data(city, month, day)

    time_stats(df)
    station_stats(df)
    trip_duration_stats(df)
    user_stats(df)
    display_data(df)
    while True: 
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() == 'no':
            sys.exit('Thank you!!')
        elif restart.lower() == 'yes':
            main()
        else:
            print('Wrong input! Try again.')
            continue
        
if __name__ == "__main__":
	main()
