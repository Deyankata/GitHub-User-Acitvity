import requests
import argparse
import json

def main():
    parser = argparse.ArgumentParser(description="Fetch GitHub activity for a user")
    parser.add_argument("username", help="GitHub username")

    args = parser.parse_args()
    print(f"Fetching GitHub activity for: {args.username}")

    response = requests.get(f"https://api.github.com/users/{args.username}/events/public")

    if response.status_code != 200:
            print(f"Error: Invalid username or API rate limit exceeded (Status code: {response.status_code})")
            return

    activity = json.loads(response.text)

    if not activity:
        print(f"No activity found for user: {args.username}")
        return

    commits, issues = get_activity(activity)

    print_activity(commits, issues)

def get_activity(event_list):
    commits = {}
    issues = {}
    for event in event_list:
        if event["type"] == "PushEvent":
            repo = event["repo"]["name"]
            for payload_item in event["payload"]["commits"]:
                commit_message = payload_item["message"]
                if repo not in commits:
                    commits[repo] = [commit_message]
                else:
                    commits[repo].append(commit_message)
        elif event["type"] == "IssuesEvent":
            repo = event["repo"]["name"]
            issue = event["payload"]["issue"]["title"]
            if repo not in issues:
                issues[repo] = [issue]
            else:
                issues[repo].append(issue)

    return commits, issues

def print_activity(commits, issues):
    indent = " " * 4

    for key in commits.keys():
        print(f"-Pushed {len(commits[key])} commits to {key}")
        print("\n".join(indent + item for item in commits[key]))

    if issues:
        print("\n######\n")

    for key in issues.keys():
        print(f"-Opened new issue(s) in {key}")
        print("\n".join(indent + item for item in issues[key]))


if __name__ == "__main__":
    main()
