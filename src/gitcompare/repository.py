from datetime import datetime


class Repository:
    name: str
    full_name: str
    private: bool
    web_url: str
    description: str
    forked: str
    created_at: datetime
    updated_at: datetime
    pushed_at: datetime
    clone_url: str
    stars: int
    watches: int
    language: str
    forks: int
    license: str
    archived: bool
    owner: str

    def __init__(self, repo_data: dict):
        self.name = repo_data['name']
        self.full_name = repo_data['full_name']
        self.private = repo_data['private']
        self.web_url = repo_data['html_url']
        self.description = repo_data['description']
        self.forked = repo_data['fork']
        self.created_at = repo_data['created_at']
        self.updated_at = repo_data['updated_at']
        self.pushed_at = repo_data['pushed_at']
        self.clone_url = repo_data['clone_url']
        self.stars = repo_data['stargazers_count']
        self.watches = repo_data['watchers_count']
        self.language = repo_data['language']
        self.forks = repo_data['forks_count']
        self.license = repo_data['license']
        self.archived = repo_data['archives']
        self.owner = repo_data['owner']['login']
