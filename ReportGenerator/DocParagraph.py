

class DocParagraph:
    def init_attr(self):
        self.style = None
        self.font_size = 11
        self.first_line_indent = None
        self.space_before = None
        self.space_after = None
        self.line_spacing = None
        self.is_bold = None
        self.alignment = None
        self.par_level = None
    
    def __init__(self,context):
        self.context = context
        self.init_attr()