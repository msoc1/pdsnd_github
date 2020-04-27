import time
import pandas as pd
import numpy as np
import datetime as dt

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTHS_DATA = ('january', 'february', 'march', 'april', 'may', 'june')
WEEKDAYS_DATA = ('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday')
OPTIONS_DATA = ("yes", "no", "finish")
SORT_DATA = ('start time', 'end time', 'trip duration', 'start station', 'end station', '')

day = 86400
hour = 3600
minute = 60

def user_selection(message, selections):
        #This function returns input from user from list of answers

        while True:
            temp = input(message).strip().lower()

            if temp == OPTIONS_DATA[2]:
                print("\nEnding Program.")
                exit()
                break
            elif ',' not in selections:
                if temp in selections:
                    selection = temp
                    break
            elif ',' in temp:
                temp = [x.strip().lower() for x in temp.split(',')]
                if list(filter(lambda x: x in selections, temp)) == temp:
                    selection = temp
                    break

            message = "Please input valid option: \
                        \nPossible options " + str(selections)
        return selection.lower()


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    while True:
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
        city = user_selection("Which city or cities to display?\n"
                            "Chicago, New York City, Washington?\n", CITY_DATA.keys())

    # get user input for month (all, january, february, ... , june)
        month = user_selection("Which months to display?\n"
                            "January, February, March, April, May, June?\n", MONTHS_DATA)

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
        day = user_selection("Which days to display?\n"
                         "Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday?\n", WEEKDAYS_DATA)

    #display confirmation to the user
        print("Is it correct?" +
              "\nCity = {0} ".format(city) +
              "\nMonth = {0} ".format(month) +
              "\nDay = {0}".format(day))
        confirm = user_selection("Yes or No to confirm ", OPTIONS_DATA[0:2])

        if confirm.lower() == OPTIONS_DATA[0]:
            break
        elif confirm.lower() == OPTIONS_DATA[1]:
            get_filters()
            break
        else:
            print("please give Yes or No")
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
    print("Loading filters")
    start_time = time.time()

    # filter the data
    if isinstance(city, list):
        df = pd.concat(map(lambda city: pd.read_csv(CITY_DATA[city]), city), sort=True)
        # reindex DataFrame columns
        try:
            df = df.reindex(columns=["Unnamed: 0", "Start Time", "End Time",
                                     "Trip Duration", "Start Station",
                                     "End Station", "User Type", "Gender",
                                     "Birth Year"])
        except:
            pass
    else:
        df = pd.read_csv(CITY_DATA[city])

    # columns for statistics
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Weekday'] = df['Start Time'].dt.day_name()
    df['Start Hour'] = df['Start Time'].dt.hour

    #filter the data according by month & weekday
    if isinstance(month, list):
        df = pd.concat(map(lambda month: df[df['Month'] == (MONTHS_DATA.index(month)+1)], month))
    else:
        df = df[df['Month'] == (MONTHS_DATA.index(month)+1)]

    if isinstance(day, list):
        df = pd.concat(map(lambda day: df[df['Weekday'] == (day.title())], day))
    else:
        df = df[df['Weekday'] == day.title()]

    print("\nTask was completed in {:.3f} seconds.".format(round((time.time() - start_time),3)))
    print('-'*40)

    return df


def time_stats(df):
    """Display statistics on the most frequent times of travel."""

    print("\nCalculating The Most Frequent Times of Travel...\n")
    start_time = time.time()

    #display the most common month
    cmn_month = df['Month'].mode()[0]
    print("Most common month: " + str(MONTHS_DATA[cmn_month-1]))

    #display the most common day of week
    cmn_day = df['Weekday'].mode()[0]
    print("Most common day of week: " + str(cmn_day))

    #display the most common start hour
    cmn_hour = df['Start Hour'].mode()[0]
    print("Most common hour of day: " + str(cmn_hour))

    print("\nTask was completed in {:.3f} seconds.".format(round((time.time() - start_time),3)))
    print('-'*40)


def station_stats(df):
    """Display statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #display most commonly used start station
    start_station = str(df['Start Station'].mode()[0])
    print("Most common start station is: " + start_station)

    #display most commonly used end station
    end_station = str(df['End Station'].mode()[0])
    print("Most common start end is: " + end_station)

    #display most frequent combination of start station and
    #end station trip
    df['Start-End Combination'] = (df['Start Station'] + ' - ' + df['End Station'])
    start_end = str(df['Start-End Combination'].mode()[0])
    print("Most common start-end combination of stations is: " + start_end)
    print("\nTask was completed in {:.3f} seconds.".format(round((time.time() - start_time),3)))
    print('-'*40)


def trip_duration_stats(df):
    """Display statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #display total travel time
    total_time = df['Trip Duration'].sum()
    total_time = (str(int(total_time//day)) + "d " +
                         str(int((total_time % day)//hour)) + "h " +
                         str(int(((total_time % day) % hour)//minute)) + "m " +
                         str(int(((total_time % day) % hour) % minute)) + "s")
    print('Total travel time is : ' + total_time)

    #display mean travel time
    average_time = df['Trip Duration'].mean()
    average_time = (str(int(average_time//minute)) + "m " + str(int(average_time % minute)) + "s")

    print("Average travel time is : " + average_time + ".")
    print("\nTask was completed in {:.3f} seconds.".format(round((time.time() - start_time),3)))
    print('-'*40)


def user_stats(df, city):
    """Display statistics on bikeshare users."""
    start_time = time.time()
    user_types = df['User Type'].value_counts().to_string()
    print("User types:")
    print(user_types)

    #display counts of gender
    try:
        gender_distribution = df['Gender'].value_counts().to_string()
        print("\Gener breakthrough:")
        print(gender_distribution)
    except KeyError:
        print("No data for genders in Washington ")

    #display earliest, most recent, and most common year of birth
    try:
        oldest_person = str(int(df['Birth Year'].min()))
        print("\nOldest person to rent: {}".format(oldest_person))
        youngest_person = str(int(df['Birth Year'].max()))
        print("Youngest person to rent: {}".format(youngest_person))
        median_person = str(int(df['Birth Year'].mode()[0]))
        print("Most common birth year: {}".format(median_person))
    except:
        print("No data for birth data for Washington")

    print("\nTask was completed in {:.3f} seconds.".format(round((time.time() - start_time),3)))
    print('-'*40)


def raw_data(df, position):
    """Display 5 line of sorted raw data each time."""

    print("\nShowing raw data")

    if position != 0:
        position_finished = user_selection("\nWould you like to continue from where you stopped last time?" , OPTIONS_DATA[0:2])
        if position_finished == 'no':
            position = 0

    if position == 0:
        df_sorting = user_selection("\nHow to sort data displayed in the dataframe? Press Enter to see not sorted.\n"
                                "start time, end time, trip duration, start station, end station \n>",SORT_DATA)

        ascending_descending = user_selection("\nData should be ascending or descending? \n",
                             ('ascending', 'descending'))

        if ascending_descending == 'ascending':
            ascending_descending = True
        elif ascending_descending == 'descending':
            ascending_descending = False

        if df_sorting == 'start time':
            df = df.sort_values(['Start Time'], ascending=ascending_descending)
        elif df_sorting == 'end time':
            df = df.sort_values(['End Time'], ascending=ascending_descending)
        elif df_sorting == 'trip duration':
            df = df.sort_values(['Trip Duration'], ascending=ascending_descending)
        elif df_sorting == 'start station':
            df = df.sort_values(['Start Station'], ascending=ascending_descending)
        elif df_sorting == 'end station':
            df = df.sort_values(['End Station'], ascending=ascending_descending)
        elif df_sorting == '':
            pass

    #5 lines raw data displayed after each loop
    while True:
        for position in range(position, len(df.index)):
            print(df.iloc[position:position+5].to_string())
            position += 5

            if user_selection("\nPrint more raw data? Yes or No\n\n", OPTIONS_DATA[0:2]) == 'yes':
                continue
            else:
                break
        break
    return position


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        position = 0
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        restart = input("\nWould you like to restart or see raw data? Enter 'restart' or 'raw data'.\n")
        if restart.lower() == "raw data":
            position = raw_data(df, position)
        elif restart.lower() != 'restart':
            break


if __name__ == "__main__":
    main()
