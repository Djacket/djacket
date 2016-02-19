GIT_ACTION_RESULT = 'result'
GIT_ACTION_ADVERTISEMENT = 'advertisement'
GIT_ACTIONS = [GIT_ACTION_ADVERTISEMENT, GIT_ACTION_RESULT]


def is_valid_git_action(action):
    """
        Returns true if the given action is one of git valid actions.
    """

    return action in GIT_ACTIONS
