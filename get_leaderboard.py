import requests
import argparse
import time
import os
from rich import print as rprint
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel


def main():
    def get_leaderboard():
        layout = Layout()
        layout.split_column(Layout(name="upper"))
        if args.display:
            layout.split_column(
                Layout(name="upper"),
                Layout(name="lower")
            )
            layout["lower"].split_row(
                *(Layout(name=group) for group in groups_list)
            )
            for num, group in enumerate(groups_list):
                color = int((num + 1) * (200/len(groups_list)))
                table = Table(title=f"[u]{group}", show_edge=False, show_lines=True, expand=True, title_style=f"color({color})")
                table.add_column("Rank", ratio=3, style="blue")
                table.add_column("User", ratio=20, style="green")
                table.add_column("Honor", ratio=6, style="magenta", justify="right")
                group_rank = {user:user_ranking[user] for user in groups if groups[user] == group and (user in user_ranking)}
                for rank, user in enumerate(reversed(sorted(group_rank, key=group_rank.get))):
                    table.add_row(str(rank + 1), user, str(user_ranking[user]))
                layout["lower"][group].update(Panel(table, border_style=f"color({255 - color})", padding=1))
        table = Table(title="[deep_pink3 b]LEADERBOARD", show_edge=False, show_lines=True, expand=True)
        table.add_column("Rank", ratio=3, style="blue")
        table.add_column("User", ratio=20, style="green")
        table.add_column("Group", ratio=10, style="cyan")
        table.add_column("Honor", ratio=6, style="magenta", justify="right")
        for rank, user in enumerate(reversed(sorted(user_ranking, key=user_ranking.get))):
            table.add_row(str(rank + 1), user, groups.get(user, ""), str(user_ranking[user]))
        layout["upper"].update(Panel(table, border_style="red", padding=1))
        if not args.surpress:
            [rprint(error) for error in errors]
        return layout


    parser = argparse.ArgumentParser(description="Takes a list of usernames and returns the codewars leaderboard with those users")
    parser.add_argument("input", nargs="*", help="Usernames or files of usernames. If the input is a filepath, the program will use ach line in the file as a username. If it is not a valid file path, the program will interpret it as a username. To force the program to interpret your input as a username or file, use -u or -f respectuively")
    parser.add_argument("-f", "--file", action="append", help="The program will use this as a file path to get usernames from")
    parser.add_argument("-u", "--username", action="append", help="The program will use this as a username to rank")
    parser.add_argument("-t", "--time", type=int, help="Sets the program to run every x minutes")
    parser.add_argument("-s", "--surpress", action="store_true", help="Supresses any error messages from missing usernames. Note: Does not supress any file-related errors")
    parser.add_argument("-g", "--group", nargs="+", action="append", default=[], help="Add a group of users. The first argument is the name of the group, and anything after that is either files or usernames")
    parser.add_argument("-d", "--display", action="store_true", help="Displays individual group leaderboards in addition to the overall leaderboard")
    args = parser.parse_args()

    usernames = []

    if args.username:
        usernames.extend[args.username]

    if args.file:
        with Progress(transient=True) as progress:
            get_files = progress.add_task("[cyan]Parsing files...", total=len(args.file))
            for i in args.file: # Gets all the usernames provided directly by the user or in any user-provided files
                usernames.extend(parse_file(i))
                progress.update(get_files, advance=1)
    
    for i in args.input:
        if os.path.isfile(i):
            usernames.extend(parse_file(i))
        else:
            usernames.append(i)

    groups = {}
    groups_list = {}

    for group in args.group:
        group_name = group[0]
        groups_list[group_name] = []
        group.pop(0)
        for user in group:
            if os.path.isfile(user):
                parsed = parse_file(user)
                usernames.extend(parsed)
                for username in parse_file(user):
                    groups[username] = group_name
                    groups_list[group_name].append(username)
            else:
                usernames.append(user)
                groups[user] = group_name
                groups_list[group_name].append(user)

    user_ranking = {}
    errors = ["\n"]
    with Progress("{task.description}", SpinnerColumn(), BarColumn(), TextColumn("[progress.percentage]{task.percentage:>3.0f}%"), transient=True) as progress:
            leaderboard = progress.add_task("[cyan]Getting leaderboard...", total=len(usernames))
            for username in usernames: # Gets the ranking for each username from codewars
                if username not in user_ranking:
                    user = requests.get(f"https://www.codewars.com/api/v1/users/{username}")
                    if user.ok:
                        user_ranking[username] = user.json()["honor"]
                    else:
                        errors.append(f"[red]{username} could not be found")
                progress.update(leaderboard, advance=1)
    if args.time:
        with Live(get_leaderboard(), screen=True) as live:      
            try:
                while True:
                    user_ranking = {}
                    errors = ["\n"]
                    for username in usernames: # Gets the ranking for each username from codewars
                        if username not in user_ranking:
                            user = requests.get(f"https://www.codewars.com/api/v1/users/{username}")
                            if user.ok:
                                user_ranking[username] = user.json()["honor"]
                            else:
                                errors.append(f"[red]{username} could not be found")
                    live.update(get_leaderboard())
                    time.sleep(args.time * 60)
            except KeyboardInterrupt:
                live.stop()
    else:
        rprint(get_leaderboard())

def parse_file(path):
    try:
        file = open(path, "r")
        parsed = [j.strip() for j in file.readlines()]
        file.close()
        return parsed
    except FileNotFoundError:
        rprint(f"[red]Cannot find {path}")
        return []
    except PermissionError:
        rprint(f"[red]You do not have permission to view {path}")
        return []
    except IsADirectoryError:
        rprint(f"[red]{path} is a directory")
        return []

if __name__ == "__main__":
    main()