class DocPicture:

    def init_attr(self, fig_num: int):
        self.width = 2.36 * fig_num

    def __init__(self, path_or_stream, fig_num: int = 1, width: float = None) -> None:
        self.path_or_stream = path_or_stream
        if width == None:
            self.init_attr(fig_num)
        else:
            self.width = width / 6 * 2.36
