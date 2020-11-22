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
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    
    correct_city = True
    while correct_city:
        city = input('Would you like to see data for Chicago, New York City or Washington?')
        city = city.lower()
        #get user input for month & day
        if city in CITY_DATA:
            correct_city = False
            time_filter = input('Would you like to filter data by month,'+
            'day, both, or not at all? Type "none" for no time filter.')
            if time_filter == 'month': 
                month = input('Which month? January, February, March, April, May or June?').title()
                day = "none"
            elif time_filter == 'day':
                month = "none"
                day = input('Which day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday')
            elif time_filter == 'both':
                month = input('Which month? January, February, March, April, May or June?').title()
                day = input('Which day? Please type your response as an integer (e.g. 1 = Monday)')
            else:
                print('Your input is not valid. Please try again.')

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
    df = pd.read_csv(CITY_DATA[city]).rename(columns={'Unnamed: 0': 'ID'})
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    df['month'] = df['Start Time'].dt.month
    df['day']= df['Start Time'].dt.weekday
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'none':
        # use the index of the months list to get the corresponding int
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'none':
        # filter by day of week to create the new dataframe
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 
        'Friday', 'Saturday', 'Sunday']
        day = days.index(day) + 1
        df = df[df['day'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    month_int = int(df['month'].mode().to_string(index=False))
    # display the most common day of week
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 
        'Friday', 'Saturday', 'Sunday']
    day_int = int(df['day'].mode().to_string(index=False))
    # display the most common start hour
    common_hour = int(df['hour'].mode())
    print('Most Popular Month is {}'.format(months[month_int-1].title()))
    print('Most Popular Day is {}'.format(days[day_int-1].title()))
    print('Most Popular Hour is {}'.format(common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('The most commonly used start station:')
    start_station_count = df['Start Station'].value_counts()
    print('Start Station: ' +str(start_station_count.keys()[0]) + ' Count: '+str(start_station_count[0]))
    # display most commonly used end station
    print('The most commonly used end station:')
    end_station_count = df['End Station'].value_counts()
    print('End Station: ' + str(end_station_count.keys()[0])+ ' Count: ' + str(end_station_count[0]))
    # display most frequent combination of start station and end station trip
    print("The most popular trip for Travellers: ")
    start_end_count = df.groupby(['Start Station', 'End Station']).size().nlargest(1)
    for i, value in start_end_count.iteritems():
        print('Start Station: ' + str(i[0]) + ' End Station: ' + str(i[1]) + ' Count: ' + str(value))
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = round(df['Trip Duration'].sum(),4)
    # display mean travel time
    average_travel_time = round(np.mean(df['Trip Duration']),4)
    trip_count = df['Trip Duration'].count()
    print('Total Trip Duration: {:4f} Average Trip Duration: {:4f} Count: {}'
    .format(total_travel_time, average_travel_time,trip_count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("User Types Breakdown:")
    user_types = df['User Type'].value_counts()
    print("Subscribers: " + str(user_types['Subscriber']) + 
    "\nCustomers: " + str(user_types['Customer']))
    

    # Display counts of gender
    if city != 'Washington':
        print("Gender Breakdown:")
        gender_count = df['Gender'].value_counts()
        print("Male: "+ str(gender_count['Male'])+ 
        "\nFemale: "+str(gender_count['Female']))

        # Display earliest, most recent, and most common year of birth
        print("Birth Year Breakdown:")
        oldest_dob = int(df['Birth Year'].min())
        youngest_dob = int(df['Birth Year'].max())
        common_dob = int(df['Birth Year'].mode())

        print("Earliest Birth Year: {}\nMost Recent Birth Year: {}\nMost Common Birth Year: {}"
        .format(oldest_dob,youngest_dob,common_dob))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def main():
    
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
    

if __name__ == "__main__":
    main()
