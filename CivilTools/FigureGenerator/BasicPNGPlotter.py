from PIL import Image, ImageDraw
import warnings


class BasicPNGPlotter:
    def __init__(self, width, height, bg=(0, 0, 0, 0)):
        self.width = width
        self.height = height
        self.image = Image.new("RGBA", (width, height), bg)
        self.draw = ImageDraw.Draw(self.image)

    def draw_horizental_line(self, s_x, s_y, length, color="black", line_width=2):
        """画一段水平线，length为长度，正代表向右"""
        self.draw_line(s_x, s_y, s_x + length, s_y, color, line_width)

    def draw_vertical_line(self, s_x, s_y, length, color="black", line_width=2):
        """画一段竖直线，length为长度，正代表向下"""
        self.draw_line(s_x, s_y, s_x + length, s_y, color, line_width)

    def draw_rectangle(
        self, s_x, s_y, rec_width, rec_height, color="black", line_width=2
    ):
        """画一个矩形，左上角点为s_x,s_y，width正代表向右，height正代表向下"""
        self.draw_horizental_line(s_x, s_y, rec_width, color, line_width)
        self.draw_horizental_line(s_x, s_y + rec_height, rec_width, color, line_width)
        self.draw_vertical_line(s_x, s_y, rec_height, color, line_width)
        self.draw_vertical_line(s_x + rec_width, s_y, rec_height, color, line_width)

    def draw_line(self, s_x, s_y, e_x, e_y, color="black", width=2):
        if s_x < 0 or s_x > self.width or s_y < 0 or s_y > self.height:
            warnings.warn("Start point is out of figure.")
        if e_x < 0 or e_x > self.width or e_y < 0 or e_y > self.height:
            warnings.warn("End point is out of figure.")
        self.draw.line((s_x, s_y, e_x, e_y), fill=color, width=width)

    def draw_png(self):
        self.draw.line((0, 0, 500, 500), fill="black", width=2)

    def save(self, path):
        self.image.save(path, "PNG")


if __name__ == "__main__":
    p = BasicPNGPlotter(1500, 800)
    p.draw_png()
    p.save("testfiles/output.png")
