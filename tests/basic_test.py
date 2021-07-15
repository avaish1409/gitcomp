import gitcomp

"""
Baisc test cases dependent on GitComp class output (as caputured in capsys)
- usernames
- reponames
- null args
"""


def test_user(capsys):
    gitcomp.GitComp(['avaish1409'])

    out, err = capsys.readouterr()
    print(out)
    assert err == ''


def test_repo(capsys):
    gitcomp.GitComp(repos=['avaish1409/VideoChatBot'])

    out, err = capsys.readouterr()
    assert err == ''


def test_null(capsys):
    gitcomp.GitComp()

    out, err = capsys.readouterr()
    assert err == ''
