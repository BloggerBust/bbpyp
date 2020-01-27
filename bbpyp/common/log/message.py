class Message:
    def __init__(self, format_string, args):
        self.format_string = format_string
        self.args = args

    def __str__(self):
        return self.format_string.format(*self.args)
