import requests
import argparse
import schedule
import time
from functools import partial
from rich import print as rprint
from rich.progress import Progress
from rich.table import Table


def main():
    parser = argparse.ArgumentParser(description="Takes a list of usernames and returns the codewars leaderboard with those users")
    parser.add_argument("usernames", nargs="*", help="Users to rank")
    parser.add_argument("-f", "--file", nargs="*", help="Files that contain users to rank")
    parser.add_argument("-t", "--time", type=int,  help="Sets the program to run every x minutes")
    args = parser.parse_args()
    
    
    
    if args.file:
        with Progress(transient=True) as progress:
            get_files = progress.add_task("[cyan]Parsing files...", total=len(args.file))
            for i in args.file: # Gets all the usernames provided directly by the user or in any user-provided files
                try:
                    file = open(i)
                    args.usernames.extend([j.strip() for j in file.readlines()])
                    file.close()
                except FileNotFoundError:
                    rprint(f"[red]Cannot find {file}")
                except PermissionError:
                    rprint(f"[red]You do not have permission to view {file}")
                except IsADirectoryError:
                    rprint(f"[red]{file} is a directory")
                progress.update(get_files, advance=1)
    
    if args.time:
            schedule.every(args.time).minutes.do(partial(get_leaderboard, args.usernames))
    
    get_leaderboard(args.usernames)

def get_leaderboard(usernames):
    user_ranking = {}
    output = ["\n"]
    errors = ["\n"]
    with Progress(transient=True) as progress:
        leaderboard = progress.add_task("[cyan]Getting leaderboard...", total=len(usernames))
        for username in usernames: # Gets the ranking for each username from codewars
            if username not in user_ranking:
                user = requests.get(f"https://www.codewars.com/api/v1/users/{username}")
                if user.ok:
                    user_ranking[username] = user.json()["honor"]
                else:
                    errors.append(f"[red]{username} could not be found")
            progress.update(leaderboard, advance=1)
    
    table = Table(title="Leaderboard", show_edge=False, show_lines=True, expand=True)
    table.add_column("Rank", ratio=3, style="blue")
    table.add_column("User", ratio=20, style="green")
    table.add_column("Honor", ratio=6, style="magenta", justify="right")
    for rank, user in enumerate(reversed(sorted(user_ranking, key=user_ranking.get))):
        table.add_row(str(rank + 1), user, str(user_ranking[user]))
    output.append(table)
    output.extend(errors)
    for message in output:
        rprint(message)


if __name__ == "__main__":
    main()
    while True:
        schedule.run_pending()
        time.sleep(1)