
% Facts and dynamic declarations
% Enable these predicates to be dynamically updated as users input their daily data
:- dynamic daily_water_intake/1.
:- dynamic daily_sleep_hours/1.
:- dynamic skin_condition/1.
:- dynamic count_days_with/3.
:- dynamic count_days_without/3.
:- dynamic find_optimal_sleep_hours/2.
:- dynamic max_good_skin_condition/2.

% Counts the number of logged days
logged_days_count(Count) :-
    findall(Date, daily_data_logged(Date), Dates),
    sort(Dates, UniqueDates),
    length(UniqueDates, Count).

% Check if data is logged for a given day (Placeholder)
daily_data_logged(Date) :-
    ( daily_water_intake(Date, _)
    ; daily_sleep_hours(Date, _)
    ; skin_condition(Date, _)
    ).

% Rule 1: DAILY REMINDER --> Water Intake Reminder
daily_reminder(drink_more_water) :-
    daily_water_intake(Liters),
    Liters < 2.

% Rule 2: DAILY REMINDER --> Sleep Duration Reminder
daily_reminder(need_more_sleep) :-
    daily_sleep_hours(Hours),
    Hours < 6.

% Rule 3: TREND ANALYSIS --> Periods Influence on Skin Condition - needs minimum 10 days of data
conclusion(periods_influence_bad_skin) :-
    logged_days_count(Count),
    Count >= 10,
    count_days_with(periods_yes, bad_skin, CountPeriodsBad),
    count_days_with(periods_no, bad_skin, CountNoPeriodsBad),
    CountPeriodsBad > CountNoPeriodsBad.

% Rule 4: TREND ANALYSIS --> Sleep Duration and Skin Condition Analysis - needs minimum 10 days of data
conclusion(bad_sleep_schedule_affects_skin) :-
    logged_days_count(Count),
    Count >= 10,
    daily_sleep_hours(Hours),
    skin_condition(bad),
    (Hours < 6; Hours > 10).

% Rule 5: TREND ANALYSIS --> Positive Sleep Duration Influence - needs minimum 10 days of data
conclusion(optimal_sleep_for_good_skin) :-
    logged_days_count(Count),
    Count >= 10,
    find_optimal_sleep_hours(Hours, CountGood),
    max_good_skin_condition(OtherHours, OtherCountGood),
    Hours \= OtherHours,
    CountGood > OtherCountGood.


% Counts the days with a specific condition combination
count_days_with(Condition1, Condition2, Count) :-
    findall(Date, 
            (daily_data(Date, condition, Condition1), 
             daily_data(Date, skin_condition, Condition2)), 
            Dates),
    length(Dates, Count).

% Finds the sleep duration with the most days of good skin
find_optimal_sleep_hours(OptimalHours, MaxCountGood) :-
    setof(Count/Hours, CountGood^
          (aggregate(count, Date, 
                     (daily_data(Date, sleep_hours, Hours), 
                      daily_data(Date, skin_condition, good)), CountGood),
           CountGood = Count/Hours),
          CountsHours),
    last(CountsHours, MaxCountGood/OptimalHours).

% Finds the maximum good skin conditions for comparison
max_good_skin_condition(Hours, CountGood) :-
    find_optimal_sleep_hours(Hours, CountGood).

