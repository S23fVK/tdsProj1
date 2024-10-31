import requests
import csv
import pandas as pd
from time import sleep

TOKEN = "<inserted github token here>"
HEADERS = {"Authorization": f"token {TOKEN}"}

def fetch_users_in_seattle(min_followers=200):
    url = f"https://api.github.com/search/users?q=location:seattle+followers:>{min_followers}&per_page=100"
    users = []
    page = 1
    while True:
        response = requests.get(f"{url}&page={page}", headers=HEADERS)
        if response.status_code != 200:
            print(f"Error fetching users: {response.status_code}")
            break
        data = response.json()
        items = data.get('items', [])
        if not items:
            break
        for item in items:
            username = item['login']
            user_info = fetch_user_details(username)
            if user_info:
                users.append(user_info)
        page += 1
        sleep(1)
    return users

def fetch_user_details(username):
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        user_data = response.json()
        user_data['company'] = clean_company_name(user_data.get('company', ""))
        return {"login": user_data.get("login", ""),
            "name": user_data.get("name", ""),
            "company": user_data.get("company", ""),
            "location": user_data.get("location", ""),
            "email": user_data.get("email", ""),
            "hireable": user_data.get("hireable", ""),
            "bio": user_data.get("bio", ""),
            "public_repos": user_data.get("public_repos", 0),
            "followers": user_data.get("followers", 0),
            "following": user_data.get("following", 0),
            "created_at": user_data.get("created_at", "")}
    return None

def clean_company_name(company):
    if company:
        return company.lstrip('@').strip().upper()
    return ""

def fetch_repositories(username, max_repos=500):
    repos = []
    url = f"https://api.github.com/users/{username}/repos?sort=pushed&per_page=100"
    page = 1
    while len(repos) < max_repos:
        response = requests.get(f"{url}&page={page}", headers=HEADERS)
        if response.status_code != 200:
            print(f"Error fetching repos for {username}: {response.status_code}")
            break
        data = response.json()
        if not data:
            break
        for repo in data:
            repos.append({"login": username,
                "full_name": repo.get("full_name", ""),
                "created_at": repo.get("created_at", ""),
                "stargazers_count": repo.get("stargazers_count", 0),
                "watchers_count": repo.get("watchers_count", 0),
                "language": repo.get("language", ""),
                "has_projects": repo.get("has_projects", False),
                "has_wiki": repo.get("has_wiki", False),
                "license_name": repo.get("license", {}).get("key", "") if repo.get("license") else ""})
        page += 1
        sleep(1)
    return repos[:max_repos]

def save_users_to_csv(users, filename="users.csv"):
    fieldnames = ["login", "name", "company", "location", "email", "hireable", "bio", "public_repos", "followers", "following", "created_at"]
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for user in users:
            writer.writerow(user)

def save_repositories_to_csv(repos, filename="repositories.csv"):
    fieldnames = ["login", "full_name", "created_at", "stargazers_count", "watchers_count", "language", "has_projects", "has_wiki", "license_name"]
    with open(filename, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for repo in repos:
            writer.writerow(repo)

if __name__ == "__main__":
    users = fetch_users_in_seattle()
    save_users_to_csv(users)
    all_repos = []
    for user in users:
        username = user["login"]
        repos = fetch_repositories(username)
        all_repos.extend(repos)
    save_repositories_to_csv(all_repos)
    print("Data collection complete.")
