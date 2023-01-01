import requests

# Set your personal access token
personal_access_token = ""
username = ""

# Set the headers for the REST API call
headers = {
    'Authorization': 'Bearer ' + personal_access_token,
    'Content-Type': 'application/json',
    "X-GitHub-Api-Version": "2022-11-28" 
}


# Now let's define a function to delete a repository
def delete_repo(repo_name):
  # Send a DELETE request to the API to delete the repository
  response = requests.delete(f"https://api.github.com/repos/{username}/{repo_name}", headers=headers)

  # If the response status code is 204, it was successful
  if response.status_code == 204:
    print(f"Successfully deleted repository {repo_name}")
  else:
    print(f"Failed to delete repository {repo_name} with status code {response.status_code}")

# Next, let's define a function to get a list of repositories for the user
def get_repos(page=1, per_page=100):
  # Set the `page` and `per_page` parameters
  params = {
      "page": page,
      "per_page": per_page
  }

  # Send a GET request to the API to get a list of repositories for the user
  response = requests.get("https://api.github.com/user/repos", headers=headers, params=params)

  # If the response status code is 200, it was successful and we can parse the list of repositories
  if response.status_code == 200:
    repos = response.json()
    return repos
  else:
    print(f"Failed to get list of repositories with status code {response.status_code}")
    return []

# Now let's define a function to get the commit count for a repository
def get_commit_count(repo_name):
  # Send a GET request to the API to get a list of commits for the repository
  response = requests.get(f"https://api.github.com/repos/{username}/{repo_name}/commits", headers=headers)

  # If the response status code is 200, it was successful and we can return the length of the list of commits
  if response.status_code == 200:
    commits = response.json()
    return len(commits)
  else:
    print(f"Failed to get list of commits for repository {repo_name} with status code {response.status_code}")
    return 0

# Now let's put it all together

page = 2
per_page = 100

# Set a flag to keep track of whether there are more pages to retrieve
more_pages = True

while more_pages:
  if page == 5:
    break
  # Get the list of repositories for the current page
  repos = get_repos(page, per_page)
# Iterate over the list of repositories
  for repo in repos:
    # Get the commit count for the repository
    commit_count = get_commit_count(repo["name"])
    print(commit_count)
    # If the commit count is less than 3, ask the user if they want to delete the repository
    if commit_count <= 4:
      choice = input(f"Repository {repo['name']} has about {commit_count} commits. Do you want to delete it? [y/n] ")
      if choice.lower() == "y":
        delete_repo(repo["name"])
  page += 1

print("Done!")

