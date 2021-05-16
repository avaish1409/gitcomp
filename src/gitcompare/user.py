class User:
    login: str
    followers: int
    following: int
    site_admin: bool
    name: str
    company: str
    blog: str
    location: str
    public_repos: int
    public_gists: int

    def __init__(self, user_data: dict):
        """
        setup a user object containing a user's vital stats, equivalent to using the CLI tool with the -u flag
        :param user_data: the json dictionary we get from calling the GitHub API
        """
        self.login = user_data['login']
        self.followers = user_data['followers']
        self.following = user_data['following']
        self.site_admin = user_data['site_admin']
        self.name = user_data['name']
        self.company = user_data['company']
        self.blog = user_data['blog']
        self.location = user_data['location']
        self.public_repos = user_data['public_repos']
        self.public_gists = user_data['public_gists']
