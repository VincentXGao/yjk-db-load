from PIL import Image, ImageDraw, ImageFont
import warnings
import math
import io


def draw_rotated_text(
    image, text, position, rotate, font, fill, x_offset=0, y_offset=0
):
    # 创建临时透明图层
    text_layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
    text_draw = ImageDraw.Draw(text_layer)

    # 计算文字包围盒
    bbox = text_draw.textbbox((0, 0), text, font=font)
    text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]

    # 在临时图层中央绘制文字
    text_draw.text(
        (
            (text_layer.width - text_width + x_offset) / 2,
            (text_layer.height - text_height + y_offset) / 2,
        ),
        text,
        font=font,
        fill=fill,
    )

    # 绕中心点旋转
    rotated = text_layer.rotate(
        rotate, center=(text_layer.width // 2, text_layer.height // 2), expand=True
    )

    # 计算最终粘贴位置
    paste_x = position[0] - rotated.width // 2
    paste_y = position[1] - rotated.height // 2

    # 合并到原图
    image.paste(rotated, (paste_x, paste_y), rotated)


class BasicPNGPlotter:
    def __init__(self, width, height, bg=(0, 0, 0, 0)):
        self.width = width
        self.height = height
        self.image = Image.new("RGBA", (width, height), bg)
        self.draw = ImageDraw.Draw(self.image)

    def draw_horizental_line(self, s_x, s_y, length, color="black", line_width=5):
        """画一段水平线，length为长度，正代表向右"""
        self.draw_line(s_x, s_y, s_x + length, s_y, color, line_width)

    def draw_vertical_line(self, s_x, s_y, length, color="black", line_width=5):
        """画一段竖直线，length为长度，正代表向下"""
        self.draw_line(s_x, s_y, s_x + length, s_y, color, line_width)

    def draw_arc(self, start_x, start_y, width, height, start_degree, sweep_degree):
        bbox = (
            start_x,
            start_y,
            start_x + width,
            start_y + height,
        )
        self.draw.arc(bbox, start_degree, sweep_degree, fill="black", width=5)

    def draw_circle(self, start_x, start_y, diameter, line_width=5):
        bbox = (
            start_x,
            start_y,
            start_x + diameter,
            start_y + diameter,
        )
        # 绘制圆（轮廓线）
        self.draw.ellipse(bbox, outline="black", width=line_width)

    def draw_rectangle(
        self, s_x, s_y, rec_width, rec_height, color="black", line_width=2
    ):
        """画一个矩形，左上角点为s_x,s_y，width正代表向右，height正代表向下"""
        self.draw_horizental_line(s_x, s_y, rec_width, color, line_width)
        self.draw_horizental_line(s_x, s_y + rec_height, rec_width, color, line_width)
        self.draw_vertical_line(s_x, s_y, rec_height, color, line_width)
        self.draw_vertical_line(s_x + rec_width, s_y, rec_height, color, line_width)

    def draw_line(self, s_x, s_y, e_x, e_y, color="black", width=5):
        if s_x < 0 or s_x > self.width or s_y < 0 or s_y > self.height:
            warnings.warn("Start point is out of figure.")
        if e_x < 0 or e_x > self.width or e_y < 0 or e_y > self.height:
            warnings.warn("End point is out of figure.")
        self.draw.line((s_x, s_y, e_x, e_y), fill=color, width=width)

    def draw_text(
        self,
        x: int,
        y: int,
        text: str,
        font_size: int,
        degree: float,
        x_offset: float = 0,
        y_offset: float = 0,
    ):
        font = ImageFont.truetype("simhei.ttf", font_size)
        draw_rotated_text(
            self.image,
            text,
            (x, y),
            degree / math.pi * 180,
            font,
            "black",
            x_offset,
            y_offset,
        )

    def draw_png(self):
        self.draw.line((0, 0, 500, 500), fill="black", width=5)

    def save(self, path):
        self.image.save(path, "PNG")

    def to_stream(self):
        # 将图片保存到内存中的 BytesIO 对象
        img_buffer = io.BytesIO()
        self.image.save(img_buffer, "PNG")  # 保存为 PNG 格式
        del self.image
        del self.draw  # 关闭图形，释放内存
        # 将指针重置到流的开头，以便后续读取
        img_buffer.seek(0)
        return img_buffer


if __name__ == "__main__":
    p = BasicPNGPlotter(1500, 800)
    p.draw_png()
    p.save("testfiles/output.png")
