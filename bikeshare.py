#!/usr/bin/env python
# coding: utf-8

import time
import pandas as pd
import numpy as np

CITY_DATA = { 
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv' 
}

def get_valid_input(prompt, valid_options):
    """
    Prompts the user for input and ensures it matches one of the valid options.

    Args:
        prompt (str): The message displayed to the user.
        valid_options (list): A list of valid options.

    Returns:
        str: The user's valid input.
    """
    while True:
        user_input = input(prompt).lower()
        if user_input in valid_options:
            return user_input
        print(f"Invalid input. Please enter one of the following: {', '.join(valid_options)}")

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print("Hello! Let's explore some US bikeshare data!")

    city = get_valid_input("Enter city name (chicago, new york city, washington): ", CITY_DATA.keys())
    month = get_valid_input("Enter month (january to june) or 'all': ", 
                            ['january', 'february', 'march', 'april', 'may', 'june', 'all'])
    day = get_valid_input("Enter day of week or 'all': ", 
                          ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all'])

    print('-'*40)
    return city, month, day

def load_bikeshare_data(city, month, day):
    """
    Loads bikeshare data for the specified city, filtering by month and day if applicable.

    Args:
        city (str): The name of the city dataset to analyze.
        month (str): The name of the month to filter by, or "all" for no filter.
        day (str): The name of the day to filter by, or "all" for no filter.

    Returns:
        df (DataFrame): The filtered bikeshare data.
    """
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month_name().str.lower()
    df['Day of Week'] = df['Start Time'].dt.day_name().str.lower()
    df['Hour'] = df['Start Time'].dt.hour

    if month != 'all':
        df = df[df['Month'] == month]
    if day != 'all':
        df = df[df['Day of Week'] == day]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    print(f"Most common month: {df['Month'].mode()[0]}")
    print(f"Most common day of week: {df['Day of Week'].mode()[0]}")
    print(f"Most common start hour: {df['Hour'].mode()[0]}")
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    print(f"Most common start station: {df['Start Station'].mode()[0]}")
    print(f"Most common end station: {df['End Station'].mode()[0]}")
    most_common_trip = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print(f"Most common trip: {most_common_trip[0]} -> {most_common_trip[1]}")
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    print(f"Total travel time: {df['Trip Duration'].sum()} seconds")
    print(f"Average travel time: {df['Trip Duration'].mean()} seconds")
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    print("User Type Counts:")
    print(df['User Type'].value_counts())

    if 'Gender' in df:
        print("\nGender Counts:")
        print(df['Gender'].value_counts(dropna=True))

    if 'Birth Year' in df:
        print("\nEarliest birth year:", int(df['Birth Year'].min()))
        print("Most recent birth year:", int(df['Birth Year'].max()))
        print("Most common birth year:", int(df['Birth Year'].mode()[0]))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_bikeshare_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()
