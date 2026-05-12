
import time
import pandas as pd 
from pathlib import Path 


def time_stats(data):
    """Displays statistics on the most frequent times of travel."""
    if data.empty:
       print("No data available.")
       print('-'*40)
       return
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # extract month and which month appears the most
    data['month'] = data['Start Time'].dt.month
    data['day_of_week'] = data['Start Time'].dt.day_name()
    data['hour'] = data['Start Time'].dt.hour

    months = ['january', 'february', 'march', 'april', 'may', 'june']
    most_frequent_month = data['month'].value_counts().idxmax()
    print('Most Common Month: ', months[most_frequent_month - 1].title())

    # display the most common day of week
    top_day = data['day_of_week'].value_counts().idxmax()
    print('common Day:   ', top_day)

    # display the most common start hour
    peak_hour = data['hour'].value_counts().idxmax()
    print('Common Hour:  ', peak_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    

def station_usage(data):
    """Displays statistics on the most popular stations and trip."""
    if data.empty:
        print("No data available.")
        print('-'*40)
        return
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start = data['Start Station'].value_counts().idxmax()
    print('Common Start Station: ', common_start)

    # display most commonly used end station
    common_end = data['End Station'].value_counts().idxmax()
    print('Common End Station:   ', common_end)

    # display most frequent combination of start and end station
    common_trip = data.groupby(['Start Station', 'End Station']).size().idxmax()
    print('Common Trip:          ', common_trip[0], ' → ', common_trip[1])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration(data):
    """Displays statistics on the total and average trip duration."""
    if data.empty:
        print("No data available.")
        print('-'*40)
        return
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = data['Trip Duration'].sum()
    minutes, seconds = divmod(total_time, 60)
    hours, minutes   = divmod(minutes, 60)
    print(f'Total Travel Time:  {int(hours)}h {int(minutes)}m {int(seconds)}s')

    # display mean travel time
    mean_time = data['Trip Duration'].mean()
    minutes, seconds = divmod(mean_time, 60)
    print(f'Mean Travel Time:   {int(minutes)}m {int(seconds)}s')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_data(data):
    """Displays statistics on bikeshare users."""
    if data.empty:
        print("No data available.")
        print('-'*40)
        return
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # display counts of user types
    user_types = data['User Type'].value_counts()
    print('User Types:\n', user_types.to_string())

    # display counts of gender
    if 'Gender' in data.columns:
        gender_counts = data['Gender'].value_counts()
        print('\nGender Counts:\n', gender_counts.to_string())
    else:
        print('\nGender data not available for this city.')

    # display earliest, most recent, and most common year of birth
    if 'Birth Year' in data.columns:
        earliest    = int(data['Birth Year'].min())
        most_recent = int(data['Birth Year'].max())
        most_common = int(data['Birth Year'].value_counts().idxmax())
        print(f'\nEarliest Year of Birth:    {earliest}')
        print(f'Most Recent Year of Birth: {most_recent}')
        print(f'Most Common Year of Birth: {most_common}')
    else:
        print('\nBirth Year data not available for this city.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def get_filters():

    print('Hello! Let\'s explore some US bikeshare data!')
    valid_cities = ['chicago', 'new york city', 'washington']
    valid_months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    valid_days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

    while True:
        city = input("Enter the city (chicago, new york city, washington): ").strip().lower()
        if city in valid_cities:
            break
        else:
            print("Invalid city. Please choose from chicago, new york city, or washington.")

    while True:
        month = input("Enter the month (all, january, february, ..., june): ").strip().lower()
        if month in valid_months:
            break
        else:
            print("Invalid month. Please choose from all, january, february, march, april, may, or june.")

    while True:
        day = input("Enter the day (all, monday, tuesday, ..., sunday): ").strip().lower()
        if day in valid_days:
            break
        else:
            print("Invalid day. Please choose a valid day of the week or 'all'.")

    print('-'*40)
    return city, month, day
def load_data(city, month, day):
    base_dir = Path(__file__).resolve().parent
    city_data = {
        'chicago': base_dir / 'chicago.csv',
        'new york city': base_dir / 'new_york_city.csv',
        'washington': base_dir / 'washington.csv'
    }

    df = pd.read_csv(city_data[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    months = ['january', 'february', 'march', 'april', 'may', 'june']

    if month != 'all':
        month_index = months.index(month) + 1
        df = df[df['month'] == month_index]

    if day != 'all':
        df = df[df['day_of_week'].str.lower() == day]

    return df

def display_raw_data(df):
    start_loc = 0

    while True:
        show_data = input('\nWould you like to see 5 lines of raw data? Enter yes or no.\n').strip().lower()

        while show_data not in ['yes', 'no']:
            print("Please enter yes or no.")
            show_data = input('\nWould you like to see 5 lines of raw data? Enter yes or no.\n').strip().lower()

        if show_data == 'no':
            break

        print(df.iloc[start_loc:start_loc + 5])
        start_loc += 5

        if start_loc >= len(df):
            print("No more raw data to display.")
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        if df.empty:
            print("No data found for the selected filters. Please try different filters.\n")
        else:
            time_stats(df)
            station_usage(df)
            trip_duration(df)
            user_data(df)
            display_raw_data(df)
        
        while True:
            restart = input('\nWould you like to restart? Enter yes or no.\n').strip().lower()
            if restart in ['yes', 'no']:
                break
            print("Please enter yes or no.")

        if restart != 'yes':
            break

        


if __name__ == "__main__":
    main()

