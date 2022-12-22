import time
import pandas as pd


CITY_DATA = {'chicago': 'chicago.csv',
             'new york': 'new_york_city.csv',
             'washington': 'washington.csv'}

DATA = {
    "city": ['chicago', 'new york', 'washington'],

    "month": ['january', 'february', 'march', 'april', 'may', 'june', 'all'],

    "day": ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all']

}


def get_city():
    city = input("choose a city (chicago, new york, washington)\n").lower()
    while city not in DATA['city']:
        city = input("try again \nchoose a city (chicago, new york city, washington)\n").lower()
    return city


def get_day():
    day = input("choose a day\n").lower()
    while day not in DATA['day']:
        day = input("try again \nchoose a day\n").lower()

    return day


def get_month():
    month = input("choose a month, from january till june\n").lower()
    while month not in DATA['month']:
        month = input("try again \nchoose a month, from january till june\n").lower()

    return month


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bike-share data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = get_city()

    choose = input("choose a month or a day or both, type none to apply no filter\n").lower()
    # default values
    month = "all"
    day = "all"
    # TO DO: get user input for month (all, january, february, ... , june)
    if choose == "month":
        month = get_month()

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    elif choose == "day":
        day = get_day()

    elif choose == "both":
        month = get_month()
        day = get_day()

    print('-' * 40)
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

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = DATA.get("month").index(month) + 1

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
    print(f"Most Popular Start Hour: {df['month'].mode()[0]}")

    # TO DO: display the most common day of week

    print(f"Most Popular Start Hour: {df['day_of_week'].mode()[0]}")

    # TO DO: display the most common start hour
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['hour'] = df['Start Time'].dt.hour  # we need to extract hours first
    print(f"Most Popular Start Hour: {df['hour'].mode()[0]}")

    print(f"\nThis took {(time.time() - start_time)} seconds.")

    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print(f"The most common start station is:\n\t\t{df['Start Station'].mode()[0]}")

    # TO DO: display most commonly used end station
    print(f"The most common end station is:\n\t\t{df['End Station'].mode()[0]}")

    # TO DO: display most frequent combination of start station and end station trip
    common_combination = (df['Start Station'] + df['End Station']).mode()[0]
    print(f"The  most frequent combination of start station and end station trip is:\n\t\t{common_combination}")

    print(f"\nThis took {(time.time() - start_time)} seconds.")
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    print(f"Total travel time :{df['Trip Duration'].sum()}")

    # TO DO: display mean travel time
    print(f"Total travel time :{df['Trip Duration'].mean()}")

    print(f"\nThis took {(time.time() - start_time)} seconds.")
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print("Counts of user types:")
    user_counts = df['User Type'].value_counts()
    for index, user_count in enumerate(user_counts):
        print(f"\t{user_counts.index[index]}: {user_count}")
    # TO DO: Display counts of gender
    try:
        print("Counts of user Gender:")
        gender_counts = df['Gender'].value_counts()
        for index, gender_count in enumerate(gender_counts):
            print(f"\t{gender_counts.index[index]}: {gender_count}")
        # TO DO: Display earliest, most recent, and most common year of birth
        birth_year = df['Birth Year']
        print(f"""
    The most common birth year: {int(birth_year.value_counts().idxmax())}
    The most recent birth year: {int(birth_year.max())}
    The most earliest birth year: {int(birth_year.min())}
    """)
    except KeyError:
        print("\nNo data available for this month.")

    print(f"\nThis took {(time.time() - start_time)} seconds.")
    print('-' * 40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n').lower()
        if restart != "yes":
            break


if __name__ == "__main__":
    main()
