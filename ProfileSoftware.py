import csv
import json
from datetime import datetime, timedelta

schedule = {}


# 1 make a reservation
def make_reservation(name=None):
    """
    User should be prompted to give his full name, and date of a reservation
    this should fail if:
    User has more than 2 reservations already this week
    Court is already reserved for the time user specified
    The date user gives is less than one hour from now

    If the court is reserved the system should suggest the user to make a reservation on the closest possible time.
    """
    if not name:
        name = input("What's your Name?: ")
    while True:
        try:
            date = input("When would you like to book? Enter datetime in format DD.MM.YYYY HH:MM: ")
            if datetime.strptime(date, "%d.%m.%Y %H:%M"):
                break
        except ValueError:
            print("Format is DD.MM.YYYY HH:MM: ")
    date_entered = datetime.strptime(date, "%d.%m.%Y %H:%M")
    days_count = datetime.strptime(date, "%d.%m.%Y %H:%M")
    count = 0
    for i in range(7 - date_entered.weekday()):
        for j in schedule.get(days_count.strftime("%d.%m.%Y")[:10], range(0)):
            count += list(j.values()).count(name)
            if count > 2:
                break
        if count > 2:
            print("too many reservations")
            return
        days_count += timedelta(days=1)

    if (datetime.today() - date_entered) < timedelta(minutes=60):
        print("The time is less than one hour from now")

    for i in schedule.get(date_entered.date().strftime("%d.%m.%Y"), range(0)):
        if i['start_date'] == date_entered.strftime("%d.%m.%Y %H:%M"):
            print("Time is not available")

    if schedule.get(date_entered.date().strftime("%d.%m.%Y")) is None:
        schedule[date_entered.date().strftime("%d.%m.%Y")] = [
            {"name": f"{name}", "start_date": date_entered.strftime("%d.%m.%Y %H:%M"),
             "end_date": (date_entered + timedelta(minutes=get_duration_empty())).strftime("%d.%m.%Y %H:%M")}]

    elif schedule.get(date_entered.date().strftime("%d.%m.%Y")):
        init_date = schedule.get(date_entered.date().strftime("%d.%m.%Y"))
        print(init_date)
        for i in range(len(init_date)):
            start = init_date[0]['start_date']
            print(start)
            if date_entered < datetime.strptime(start, "%d.%m.%Y %H:%M"):
                duration = get_duration(datetime.strptime(start, "%d.%m.%Y %H:%M"), date_entered)
                init_date.insert(i, {"name": f"{name}",
                                     "start_date": date_entered.strftime("%d.%m.%Y %H:%M"),
                                     "end_date": (date_entered + timedelta(minutes=duration)).strftime(
                                         "%d.%m.%Y %H:%M")})
                return

            elif datetime.strptime(init_date[i]['start_date'], "%d.%m.%Y %H:%M") <= date_entered < datetime.strptime(
                    init_date[i]['end_date'], "%d.%m.%Y %H:%M"):
                if i == len(init_date) - 1:
                    decision = get_decision(init_date[i]['end_date'][11:], name)
                    if decision:
                        init_date.append({"name": f"{name}", "start_date": init_date[i]['end_date'],
                                          "end_date": (datetime.strptime(init_date[i]['end_date'],
                                                                         "%d.%m.%Y %H:%M") + timedelta(
                                              minutes=decision)).strftime(
                                              "%d.%m.%Y %H:%M")})
                        break
                    break
                for j in (i, len(init_date) - 1):
                    if j == len(init_date) - 1:
                        decision = get_decision(init_date[j]['end_date'][11:], name)
                        if decision:
                            init_date.append({"name": f"{name}", "start_date": init_date[j]['end_date'],
                                              "end_date": (datetime.strptime(init_date[j]['end_date'],
                                                                             "%d.%m.%Y %H:%M") + timedelta(
                                                  minutes=decision)).strftime(
                                                  "%d.%m.%Y %H:%M")})
                        break
                    elif datetime.strptime(init_date[j]['end_date'], "%d.%m.%Y %H:%M") != datetime.strptime(
                            init_date[j + 1]['start_date'], "%d.%m.%Y %H:%M"):
                        duration = get_duration(
                            datetime.strptime(init_date[j + 1]['start_date'], "%d.%m.%Y %H:%M"),
                            datetime.strptime(init_date[j]['end_date'], "%d.%m.%Y %H:%M"))
                        init_date.insert(j + 1,
                                         {"name": f"{name}", "start_date": init_date[j]['end_date'],
                                          "end_date": (datetime.strptime(init_date[j]['end_date'],
                                                                         "%d.%m.%Y %H:%M") + timedelta(
                                              minutes=duration)).strftime(
                                              "%d.%m.%Y %H:%M")})
                        break
                break

            elif date_entered == datetime.strptime(init_date[i]['end_date'], "%d.%m.%Y %H:%M"):
                for j in (i, len(init_date) - 1):
                    if i == len(init_date) - 1:
                        decision = get_decision(date_entered.strftime("%d.%m.%Y %H:%M"), name)
                        if decision:
                            init_date.append(
                                {"name": f"{name}",
                                 "start_date": date_entered.strftime("%d.%m.%Y %H:%M"),
                                 "end_date": (date_entered + timedelta(minutes=decision)).strftime(
                                     "%d.%m.%Y %H:%M")})
                            break
                        break
                    if datetime.strptime(init_date[j]['end_date'], "%d.%m.%Y %H:%M") != datetime.strptime(
                            init_date[j + 1]['start_date'], "%d.%m.%Y %H:%M"):
                        duration = get_duration(
                            datetime.strptime(init_date[j + 1]['start_date'], "%d.%m.%Y %H:%M"),
                            datetime.strptime(init_date[j]['end_date'], "%d.%m.%Y %H:%M"))
                        init_date.insert(j + 1,
                                         {"name": f"{name}", "start_date": init_date[j]['end_date'],
                                          "end_date": (datetime.strptime(init_date[j]['end_date'],
                                                                         "%d.%m.%Y %H:%M") + timedelta(
                                              minutes=duration)).strftime(
                                              "%d.%m.%Y %H:%M")})
                        break
                break

            elif date_entered > datetime.strptime(init_date[i]['end_date'], "%d.%m.%Y %H:%M"):
                if i == len(init_date) - 1:
                    decision = get_decision(date_entered.strftime("%d.%m.%Y %H:%M"), name)
                    if decision:
                        init_date.append(
                            {"name": f"{name}",
                             "start_date": date_entered.strftime("%d.%m.%Y %H:%M"),
                             "end_date": (date_entered + timedelta(minutes=decision)).strftime(
                                 "%d.%m.%Y %H:%M")})
                        break
                    break

                elif date_entered < datetime.strptime(init_date[i + 1]['start_date'], "%d.%m.%Y %H:%M"):
                    duration = get_duration(
                        datetime.strptime(init_date[i + 1]['start_date'], "%d.%m.%Y %H:%M"), date_entered)
                    init_date.insert(i + 1,
                                     {"name": f"{name}",
                                      "start_date": date_entered.strftime("%d.%m.%Y %H:%M"),
                                      "end_date": (date_entered + timedelta(minutes=duration)).strftime(
                                          "%d.%m.%Y %H:%M")})
                    break


def get_decision(available_date: str, name: str):
    """
    Give a choice of time if reservation is the last one in the schedule list.
    """
    decision = input(
        f"Next available time is {available_date}. Would you like to make a reservation (yes/no): ")
    if decision.lower() == "yes":
        print(
            "How long would you like to book court?\n",
            "1) 30 Minutes\n",
            "2) 60 Minutes\n",
            "3) 90 Minutes",
        )
        duration = int(input())
        return duration
    elif decision.lower() == "no":
        make_reservation(name)


def get_duration_empty():
    """
    Give a choice of time if available time is at the beginning or at the end of the schedule list.
    """
    while True:
        print(
            "How long would you like to book court? Enter a number of minutes: \n",
            "1) 30 Minutes\n",
            "2) 60 Minutes\n",
            "3) 90 Minutes",
        )

        try:
            duration = int(input())
            return duration
        except ValueError:
            print("Enter an integer!")


def get_duration(end: datetime, start: datetime) -> int:
    """
    Give a choice of time if available time is in the middle of the schedule list.
    """
    dif = end - start
    available_duration = 3 if dif.seconds / 1800 >= 3 else dif.seconds / 1800
    print(f"Time {start} is available. How long would you like to book court?")
    while True:
        try:
            for i in range(1, int(available_duration) + 1):
                print(f"{i}) {i * 30} minutes")
            duration = int(input())
            return duration
        except ValueError:
            print("Enter an integer!")


# 2 cancel reservation
def cansel_reservation():
    """
    User should be prompted to give his full name, and date of a reservation
    this should fail if:
    There is no reservation for this user on specified date
    The date user gives is less than one hour from now
    """
    name = input("What's your Name?: ")
    date = input("Enter a date for cancellation in format DD.MM.YYYY HH:MM: ")
    day_reservations = schedule.get(date[:10])
    if day_reservations:
        for index, column in enumerate(day_reservations):
            if column.get('name') == name and column.get('start_date') == date:
                if datetime.strptime(column.get('start_date'), "%d.%m.%Y %H:%M") + timedelta(
                        minutes=60) > datetime.today():
                    print("You cannot cancel a reservation. Its too late")
                    break
                else:
                    day_reservations.pop(index)
                    break
    else:
        print(f"No such reservation.")


# 3 print schedule
def print_schedule():
    """
    The user is prompted to enter a start and end date, then the schedule for the specified period is printed.
    """
    while True:
        try:
            start_print = datetime.strptime(input("Enter a date for start in format DD.MM.YYYY: "), "%d.%m.%Y")
            end_print = datetime.strptime(input("Enter a date for finish in format DD.MM.YYYY: "), "%d.%m.%Y")
            if start_print and end_print:
                break
        except ValueError:
            print("Format is DD.MM.YYYY")

    print("-" * 60)
    while True:
        if start_print > end_print:
            break
        if schedule.get(start_print.strftime("%d.%m.%Y")):
            print(start_print.strftime("%d.%m.%Y"))
            for reserve in schedule[start_print.strftime("%d.%m.%Y")]:
                print("\t", reserve['name'], reserve['start_date'], "-", reserve['end_date'])
        else:
            print(start_print.strftime("%d.%m.%Y"), "\n", "Not reserved", sep="")
        start_print += timedelta(days=1)
    print("-" * 60)


# 4 write to file:
def save_schedule():
    """
    The user is prompted to enter the start date, end date, file format (csv or json) and file name, and then
    The schedule should be saved to a file in a format of the user's choice.
    Examples are provided in this repository
    """
    while True:
        try:
            start = input("Enter a date for start in format DD.MM.YYYY: ")
            end = input("Enter a date for finish in format DD.MM.YYYY: ")
            if datetime.strptime(start, "%d.%m.%Y") and datetime.strptime(end, "%d.%m.%Y"):
                break
        except ValueError:
            print("Format is DD.MM.YYYY")
    fileformat = input("Enter a format (json/csv): ")
    filename = input("Enter a filename: ")
    if fileformat == "json":
        with open(f"{filename}.json", mode="w", encoding="UTF-8", newline="") as file:
            table_to_write = dict(filter(
                lambda one: datetime.strptime(start, "%d.%m.%Y") <= datetime.strptime(one[0],
                                                                                      "%d.%m.%Y") <= datetime.strptime(
                    end, "%d.%m.%Y"), schedule.items()))
            sorted_table = dict(
                sorted(table_to_write.items(), key=lambda one: datetime.strptime(one[0], "%d.%m.%Y")))
            json.dump(sorted_table, file, indent=2)
    else:
        with open(f"{filename}.csv", mode="w", encoding="UTF-8", newline="") as file:
            sorted_table = dict(
                sorted(schedule.items(), key=lambda one: datetime.strptime(one[0], "%d.%m.%Y")))
            columns = ['name', 'start_date', 'end_date']
            writer = csv.DictWriter(file, fieldnames=columns, delimiter=',')
            writer.writeheader()
            for k, v in sorted_table.items():
                if datetime.strptime(start, "%d.%m.%Y") <= \
                        datetime.strptime(k, "%d.%m.%Y") <= datetime.strptime(end, "%d.%m.%Y"):
                    writer.writerows(v)


while True:
    print(
        " Enter 1 to Make a reservation\n",
        "Enter 2 to Cancel a reservation\n",
        "Enter 3 to Print schedule\n",
        "Enter 4 to Save schedule to a file\n",
        "Enter 5 to Exit\n",
    )
    try:
        choice = int(input("Enter the choice: "))
        if choice == 5:
            break
    except ValueError:
        print("Use a number!")

    else:
        {1: make_reservation, 2: cansel_reservation, 3: print_schedule, 4: save_schedule}.get(choice)()
