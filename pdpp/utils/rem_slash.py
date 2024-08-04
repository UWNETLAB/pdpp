def rem_slash(string_in):
    """
    A simple function which takes in a string and returns it stripped of
    double backslashes, single forward slashes, and spaces.
    """

    return str(string_in).replace("\\", "").replace("/", "").replace(" ", "")
