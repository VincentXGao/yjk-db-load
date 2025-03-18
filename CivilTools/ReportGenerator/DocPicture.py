class DocPicture:

    def init_attr(self, fig_num: int):
        self.width = 2.36 * fig_num

    def __init__(self, path_or_stream, fig_num: int = 1) -> None:
        self.path_or_stream = path_or_stream
        self.init_attr(fig_num)
