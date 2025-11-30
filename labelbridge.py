import wx
import os
import ctypes
import numpy as np
import math
import sys


class Colors:
    """
    Ultralytics color palette for visualization and plotting.

    This class provides methods to work with the Ultralytics color palette, including converting hex color codes to
    RGB values and accessing predefined color schemes for object detection and pose estimation.

    Attributes:
        palette (List[tuple]): List of RGB color tuples for general use.
        n (int): The number of colors in the palette.
        pose_palette (np.ndarray): A specific color palette array for pose estimation with dtype np.uint8.

    Examples:
        >>> from ultralytics.utils.plotting import Colors
        >>> colors = Colors()
        >>> colors(5, True)  # Returns BGR format: (221, 111, 255)
        >>> colors(5, False)  # Returns RGB format: (255, 111, 221)

    ## Ultralytics Color Palette

    | Index | Color                                                             | HEX       | RGB               |
    |-------|-------------------------------------------------------------------|-----------|-------------------|
    | 0     | <i class="fa-solid fa-square fa-2xl" style="color: #042aff;"></i> | `#042aff` | (4, 42, 255)      |
    | 1     | <i class="fa-solid fa-square fa-2xl" style="color: #0bdbeb;"></i> | `#0bdbeb` | (11, 219, 235)    |
    | 2     | <i class="fa-solid fa-square fa-2xl" style="color: #f3f3f3;"></i> | `#f3f3f3` | (243, 243, 243)   |
    | 3     | <i class="fa-solid fa-square fa-2xl" style="color: #00dfb7;"></i> | `#00dfb7` | (0, 223, 183)     |
    | 4     | <i class="fa-solid fa-square fa-2xl" style="color: #111f68;"></i> | `#111f68` | (17, 31, 104)     |
    | 5     | <i class="fa-solid fa-square fa-2xl" style="color: #ff6fdd;"></i> | `#ff6fdd` | (255, 111, 221)   |
    | 6     | <i class="fa-solid fa-square fa-2xl" style="color: #ff444f;"></i> | `#ff444f` | (255, 68, 79)     |
    | 7     | <i class="fa-solid fa-square fa-2xl" style="color: #cced00;"></i> | `#cced00` | (204, 237, 0)     |
    | 8     | <i class="fa-solid fa-square fa-2xl" style="color: #00f344;"></i> | `#00f344` | (0, 243, 68)      |
    | 9     | <i class="fa-solid fa-square fa-2xl" style="color: #bd00ff;"></i> | `#bd00ff` | (189, 0, 255)     |
    | 10    | <i class="fa-solid fa-square fa-2xl" style="color: #00b4ff;"></i> | `#00b4ff` | (0, 180, 255)     |
    | 11    | <i class="fa-solid fa-square fa-2xl" style="color: #dd00ba;"></i> | `#dd00ba` | (221, 0, 186)     |
    | 12    | <i class="fa-solid fa-square fa-2xl" style="color: #00ffff;"></i> | `#00ffff` | (0, 255, 255)     |
    | 13    | <i class="fa-solid fa-square fa-2xl" style="color: #26c000;"></i> | `#26c000` | (38, 192, 0)      |
    | 14    | <i class="fa-solid fa-square fa-2xl" style="color: #01ffb3;"></i> | `#01ffb3` | (1, 255, 179)     |
    | 15    | <i class="fa-solid fa-square fa-2xl" style="color: #7d24ff;"></i> | `#7d24ff` | (125, 36, 255)    |
    | 16    | <i class="fa-solid fa-square fa-2xl" style="color: #7b0068;"></i> | `#7b0068` | (123, 0, 104)     |
    | 17    | <i class="fa-solid fa-square fa-2xl" style="color: #ff1b6c;"></i> | `#ff1b6c` | (255, 27, 108)    |
    | 18    | <i class="fa-solid fa-square fa-2xl" style="color: #fc6d2f;"></i> | `#fc6d2f` | (252, 109, 47)    |
    | 19    | <i class="fa-solid fa-square fa-2xl" style="color: #a2ff0b;"></i> | `#a2ff0b` | (162, 255, 11)    |

    ## Pose Color Palette

    | Index | Color                                                             | HEX       | RGB               |
    |-------|-------------------------------------------------------------------|-----------|-------------------|
    | 0     | <i class="fa-solid fa-square fa-2xl" style="color: #ff8000;"></i> | `#ff8000` | (255, 128, 0)     |
    | 1     | <i class="fa-solid fa-square fa-2xl" style="color: #ff9933;"></i> | `#ff9933` | (255, 153, 51)    |
    | 2     | <i class="fa-solid fa-square fa-2xl" style="color: #ffb266;"></i> | `#ffb266` | (255, 178, 102)   |
    | 3     | <i class="fa-solid fa-square fa-2xl" style="color: #e6e600;"></i> | `#e6e600` | (230, 230, 0)     |
    | 4     | <i class="fa-solid fa-square fa-2xl" style="color: #ff99ff;"></i> | `#ff99ff` | (255, 153, 255)   |
    | 5     | <i class="fa-solid fa-square fa-2xl" style="color: #99ccff;"></i> | `#99ccff` | (153, 204, 255)   |
    | 6     | <i class="fa-solid fa-square fa-2xl" style="color: #ff66ff;"></i> | `#ff66ff` | (255, 102, 255)   |
    | 7     | <i class="fa-solid fa-square fa-2xl" style="color: #ff33ff;"></i> | `#ff33ff` | (255, 51, 255)    |
    | 8     | <i class="fa-solid fa-square fa-2xl" style="color: #66b2ff;"></i> | `#66b2ff` | (102, 178, 255)   |
    | 9     | <i class="fa-solid fa-square fa-2xl" style="color: #3399ff;"></i> | `#3399ff` | (51, 153, 255)    |
    | 10    | <i class="fa-solid fa-square fa-2xl" style="color: #ff9999;"></i> | `#ff9999` | (255, 153, 153)   |
    | 11    | <i class="fa-solid fa-square fa-2xl" style="color: #ff6666;"></i> | `#ff6666` | (255, 102, 102)   |
    | 12    | <i class="fa-solid fa-square fa-2xl" style="color: #ff3333;"></i> | `#ff3333` | (255, 51, 51)     |
    | 13    | <i class="fa-solid fa-square fa-2xl" style="color: #99ff99;"></i> | `#99ff99` | (153, 255, 153)   |
    | 14    | <i class="fa-solid fa-square fa-2xl" style="color: #66ff66;"></i> | `#66ff66` | (102, 255, 102)   |
    | 15    | <i class="fa-solid fa-square fa-2xl" style="color: #33ff33;"></i> | `#33ff33` | (51, 255, 51)     |
    | 16    | <i class="fa-solid fa-square fa-2xl" style="color: #00ff00;"></i> | `#00ff00` | (0, 255, 0)       |
    | 17    | <i class="fa-solid fa-square fa-2xl" style="color: #0000ff;"></i> | `#0000ff` | (0, 0, 255)       |
    | 18    | <i class="fa-solid fa-square fa-2xl" style="color: #ff0000;"></i> | `#ff0000` | (255, 0, 0)       |
    | 19    | <i class="fa-solid fa-square fa-2xl" style="color: #ffffff;"></i> | `#ffffff` | (255, 255, 255)   |

    !!! note "Ultralytics Brand Colors"

        For Ultralytics brand colors see [https://www.ultralytics.com/brand](https://www.ultralytics.com/brand).
        Please use the official Ultralytics colors for all marketing materials.
    """

    def __init__(self):
        """Initialize colors as hex = matplotlib.colors.TABLEAU_COLORS.values()."""
        hexs = (
            "042AFF",
            "0BDBEB",
            "F3F3F3",
            "00DFB7",
            "111F68",
            "FF6FDD",
            "FF444F",
            "CCED00",
            "00F344",
            "BD00FF",
            "00B4FF",
            "DD00BA",
            "00FFFF",
            "26C000",
            "01FFB3",
            "7D24FF",
            "7B0068",
            "FF1B6C",
            "FC6D2F",
            "A2FF0B",
        )
        self.palette = [self.hex2rgb(f"#{c}") for c in hexs]
        self.n = len(self.palette)
        self.pose_palette = np.array(
            [
                [255, 128, 0],
                [255, 153, 51],
                [255, 178, 102],
                [230, 230, 0],
                [255, 153, 255],
                [153, 204, 255],
                [255, 102, 255],
                [255, 51, 255],
                [102, 178, 255],
                [51, 153, 255],
                [255, 153, 153],
                [255, 102, 102],
                [255, 51, 51],
                [153, 255, 153],
                [102, 255, 102],
                [51, 255, 51],
                [0, 255, 0],
                [0, 0, 255],
                [255, 0, 0],
                [255, 255, 255],
            ],
            dtype=np.uint8,
        )

    def __call__(self, i: int, bgr: bool = False) -> tuple:
        """
        Convert hex color codes to RGB values.

        Args:
            i (int): Color index.
            bgr (bool, optional): Whether to return BGR format instead of RGB.

        Returns:
            (tuple): RGB or BGR color tuple.
        """
        c = self.palette[int(i) % self.n]
        return (c[2], c[1], c[0]) if bgr else c

    @staticmethod
    def hex2rgb(h: str) -> tuple:
        """Convert hex color codes to RGB values (i.e. default PIL order)."""
        return tuple(int(h[1 + i: 1 + i + 2], 16) for i in (0, 2, 4))


colors = Colors()  # create instance for 'from utils.plots import colors'


class AnnotationPanel(wx.Panel):
    def __init__(self, parent, main_frame):
        super().__init__(parent)

        self.parent = parent
        self.main_frame = main_frame
        self.image = None
        self.image_path = None
        self.image_size = None
        self.scale_factor = 1.0
        self.offset_x = 0
        self.offset_y = 0

        # 标注相关
        self.annotations = []
        self.current_box = None
        self.drawing = False
        self.start_pos = None

        # 新增：框选中和编辑相关
        self.selected_annotation_index = -1
        self.editing_mode = None  # None, 'move', 'resize'
        self.resize_handle = None  # 'tl', 'tr', 'bl', 'br', 't', 'b', 'l', 'r'
        self.edit_start_pos = None
        self.original_bbox = None
        self.handle_size = 8  # 调整手柄大小

        # self.rotation_angle = 0.0     # 当前画框的角度（度）
        self.rotation_step = 1.0  # 每次按键调整角度的步长
        self.rotate_mode = False  # 是否正在画旋转框（区分普通YOLO）

        self.cross_angle = 0.0  # 十字辅助线角度（度）
        self.rotation_step = 1.0  # 每次调整角度步长

        self.current_obb_box = None

        # 缓存的背景图片
        self.background_bitmap = None

        self.SetBackgroundColour(wx.Colour(240, 240, 240))

        self.buffer = wx.Bitmap(self.GetSize().width, self.GetSize().height)  # 画布缓存

        # 十字辅助线相关
        self.show_crosshair = True  # 是否显示十字辅助线（可用界面开关）
        self.cross_pos = None  # 当前鼠标位置（wx.Point），用于画十字

        # 绑定事件
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
        self.Bind(wx.EVT_RIGHT_UP, self.OnRightUp)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        self.Bind(wx.EVT_MOTION, self.OnMouseMove)
        self.Bind(wx.EVT_ENTER_WINDOW, self.OnMouseEnter)

        # 把 offset_x/offset_y 定义改为 float（替换原来的 int 初始化）
        self.scale_factor = 1.0
        self.offset_x = 0.0
        self.offset_y = 0.0

        # 平移（中键拖动）相关
        self.panning = False
        self.pan_last_pos = None

        # 缓存一个缩放后的 bitmap（不包含偏移）
        self.scaled_bitmap = None

        # 调节角度相关
        self.adjusting = False

        # 绑定鼠标滚轮和中键事件（你原来绑定了 EVT_MOTION 等，这里补充）
        self.Bind(wx.EVT_MOUSEWHEEL, self.OnMouseWheel)
        self.Bind(wx.EVT_MIDDLE_DOWN, self.OnMiddleDown)
        self.Bind(wx.EVT_MIDDLE_UP, self.OnMiddleUp)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnMouseLeave)  # 防止 capture 卡死

        try:
            hwnd = self.GetHandle()
            # 0 代表关闭输入法（IME）
            ctypes.windll.imm32.ImmAssociateContext(hwnd, 0)
        except Exception:
            pass  # 在非 Windows 环境下忽略

        # 设置焦点以接收键盘事件
        self.SetCanFocus(True)

    def LoadImage(self, image_path):
        """加载图片"""
        try:
            self.image_path = image_path
            self.image = wx.Image(image_path)
            self.image_size = (self.image.GetWidth(), self.image.GetHeight())
            self.FitImageToPanel()
            size = self.GetClientSize()
            self.buffer = wx.Bitmap(size.width, size.height)
            self.LoadAnnotations()
            self.selected_annotation_index = -1  # 重置选择
            self.Refresh(False)  # 刷新，不擦背景，减少闪烁
            return True
        except Exception as e:
            wx.MessageBox(f"无法加载图片: {str(e)}", "错误", wx.OK | wx.ICON_ERROR)
            return False

    def FitImageToPanel(self):
        """调整图片大小以适应面板"""
        if not self.image:
            return

        panel_size = self.GetSize()
        if panel_size.width <= 0 or panel_size.height <= 0:
            return

        # 计算缩放比例
        scale_x = panel_size.width / self.image_size[0]
        scale_y = panel_size.height / self.image_size[1]
        self.scale_factor = min(scale_x, scale_y)

        # 计算偏移量以居中显示
        scaled_width = self.image_size[0] * self.scale_factor
        scaled_height = self.image_size[1] * self.scale_factor
        self.offset_x = (panel_size.width - scaled_width) // 2
        self.offset_y = (panel_size.height - scaled_height) // 2
        print("FitImageToPanel")

        # self.UpdateScaledBitmap()
        # self.ClampOffset()

        # 重新创建背景图片缓存
        if self.image:
            self.CreateBackgroundBitmap()

    def UpdateScaledBitmap(self):
        """根据 self.scale_factor 生成并缓存缩放后的 bitmap（不包含偏移）。"""
        if not self.image:
            self.scaled_bitmap = None
            return

        pw, ph = self.GetClientSize().width, self.GetClientSize().height

        # 原图像像素大小
        img_w, img_h = self.image.GetWidth(), self.image.GetHeight()

        # 放大后整张图像尺寸（像素）
        full_scaled_w = round(img_w * self.scale_factor)
        full_scaled_h = round(img_h * self.scale_factor)

        # 一个可调阈值：如果整张图缩放后不比面板大很多，就直接缩整张图。
        # ratio = allowed / 面板；例如 1.2 表示放大后宽高都 <= 1.2 * 面板尺寸时直接缩整张。
        full_image_ratio = getattr(self, "full_image_ratio", 2)

        try:
            key = ("full", self.scale_factor, img_w, img_h)

            if getattr(self, "_last_scaled_key", None) == key and getattr(self, "scaled_bitmap", None):
                return

            # 当整张图缩放后在面板上不比面板大很多 -> 缩整张图
            if full_scaled_w <= round(pw * full_image_ratio) and full_scaled_h <= round(ph * full_image_ratio):
                # 目标尺寸至少为1
                tw = max(1, full_scaled_w)
                th = max(1, full_scaled_h)
                # 直接对整张图做 Scale
                scaled_img = self.image.Scale(tw, th, wx.IMAGE_QUALITY_NEAREST)
                self.scaled_bitmap = wx.Bitmap(scaled_img)
                self._last_scaled_key = key
                self._scaled_is_full = True
                print("UpdateScaledBitmap: 缩整张图")
                return
            key = (
                "sub",
                self.scale_factor,
                img_w, img_h,
                pw, ph,
                round(self.offset_x), round(self.offset_y)
            )

            if getattr(self, "_last_scaled_key", None) == key and getattr(self, "scaled_bitmap", None):
                return
            image_rect = wx.Rect(0, 0, self.image.GetWidth(), self.image.GetHeight())
            selection_rect = wx.Rect(round(-self.offset_x / self.scale_factor),
                                     round(-self.offset_y / self.scale_factor),
                                     round(pw / self.scale_factor), round(ph / self.scale_factor))
            valid_rect = selection_rect.Intersect(image_rect)
            sub = self.image.GetSubImage(valid_rect)
            # 缩放这块到屏幕像素大小（近似为 vis_w * scale_factor）
            target_w = min(round(self.image.GetWidth() * self.scale_factor), round(pw), round(pw - self.offset_x),
                           round(self.image.GetWidth() * self.scale_factor + self.offset_x))
            target_h = min(round(self.image.GetHeight() * self.scale_factor), round(ph), round(ph - self.offset_y),
                           round(self.image.GetHeight() * self.scale_factor + self.offset_y))

            # 使用最近邻以保持像素感并提高速度
            scaled_sub = sub.Scale(target_w, target_h, wx.IMAGE_QUALITY_NEAREST)
            self.scaled_bitmap = wx.Bitmap(scaled_sub)
            self._last_scaled_key = key
            self._scaled_is_full = False

        except Exception as e:
            print("UpdateScaledBitmap 缩放出错:", e)
            self.scaled_bitmap = None
            self.scaled_bitmap = None
            self._last_scaled_key = None
            self._scaled_is_full = False

    def CreateBackgroundBitmap(self):
        """
        兼容旧接口：不再把图片烙进 panel 大小的 bitmap 中。
        改为更新 scaled_bitmap（用于绘制），方便平移时只需改变 offset。
        """
        # 现在 CreateBackgroundBitmap 的职责变为：确保 scaled_bitmap 就绪
        self.UpdateScaledBitmap()

    # def CreateBackgroundBitmap(self):
    #     """创建背景图片缓存"""
    #     print("CreateBackgroundBitmap")
    #     if not self.image:
    #         return

    #     panel_size = self.GetSize()
    #     if panel_size.width <= 0 or panel_size.height <= 0:
    #         return

    #     # 创建背景缓存位图
    #     self.background_bitmap = wx.Bitmap(panel_size.width, panel_size.height)

    #     # 在背景位图上绘制图片
    #     dc = wx.MemoryDC()
    #     dc.SelectObject(self.background_bitmap)
    #     dc.SetBackground(wx.Brush(wx.Colour(240, 240, 240)))
    #     dc.Clear()

    #     # 计算缩放后的尺寸，确保至少为1
    #     scaled_width = max(1, int(self.image_size[0] * self.scale_factor))
    #     scaled_height = max(1, int(self.image_size[1] * self.scale_factor))

    #     # 只有当缩放后的尺寸足够大时才绘制图片
    #     if scaled_width > 1 and scaled_height > 1:
    #         try:
    #             # 绘制缩放后的图片
    #             scaled_image = self.image.Scale(scaled_width, scaled_height)
    #             bitmap = wx.Bitmap(scaled_image)
    #             dc.DrawBitmap(bitmap, int(self.offset_x), int(self.offset_y))
    #         except Exception as e:
    #             print(f"绘制图片时出错: {e}")

    #     dc.SelectObject(wx.NullBitmap)

    def ClampPositionToImage(self, pos):
        """将位置限制在图片区域内"""
        if not self.image:
            return pos

        # 计算图片在面板中的边界
        scaled_width = self.image_size[0] * self.scale_factor
        scaled_height = self.image_size[1] * self.scale_factor

        min_x = int(self.offset_x)
        max_x = int(self.offset_x + scaled_width)
        min_y = int(self.offset_y)
        max_y = int(self.offset_y + scaled_height)

        # 限制位置
        clamped_x = max(min_x, min(max_x, pos.x))
        clamped_y = max(min_y, min(max_y, pos.y))

        return wx.Point(clamped_x, clamped_y)

    def OnSize(self, event):
        """面板大小改变事件"""
        if self.image:
            size = self.GetClientSize()
            self.buffer = wx.Bitmap(size.width, size.height)
            self.FitImageToPanel()
            self.Refresh(False)  # 刷新，不擦背景，减少闪烁
        event.Skip()

    def DrawToBuffer(self):
        """在内存 bitmap 上绘制内容"""
        dc = wx.MemoryDC(self.buffer)  # 绘制到缓存位图
        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        dc.Clear()

        if getattr(self, "scaled_bitmap", None):
            if getattr(self, "_scaled_is_full", False):
                # 整张图模式
                dc.DrawBitmap(self.scaled_bitmap, round(self.offset_x), round(self.offset_y))
            else:
                # 局部裁剪模式
                x = max(0, round(self.offset_x))
                y = max(0, round(self.offset_y))
                dc.DrawBitmap(self.scaled_bitmap, x, y)
            # # 绘制缓存的背景图片
            # dc.DrawBitmap(self.background_bitmap, 0, 0)

            # 绘制所有标注框
            self.DrawAllAnnotations(dc)

            # 绘制当前正在画的框
            if self.current_box and self.drawing and self.main_frame.mode == "YOLO":
                current_class = self.main_frame.GetCurrentClass()
                rgb_color = colors(current_class)
                color = wx.Colour(rgb_color[0], rgb_color[1], rgb_color[2])
                self.DrawBox(dc, self.current_box, color, 2)

            elif self.current_obb_box and self.drawing and self.main_frame.mode == "YOLO-OBB":
                current_class = self.main_frame.GetCurrentClass()
                rgb_color = colors(current_class)
                color = wx.Colour(rgb_color[0], rgb_color[1], rgb_color[2])
                self.DrawObbBox(dc, self.current_obb_box, color, 2)

            # 绘制十字（在最后，覆盖在其它内容之上）
            if self.show_crosshair and self.cross_pos:
                # 鼠标十字（颜色：浅灰）
                self.DrawCrosshair(dc, self.cross_pos, wx.Colour(0, 255, 0), style=wx.PENSTYLE_DOT,
                                   angle_deg=self.cross_angle)
        else:
            dc.Clear()
            pass

        dc.SelectObject(wx.NullBitmap)  # 解除绑定

    def OnPaint(self, event):
        # 显示缓存位图
        # tracer = VizTracer()
        # tracer.start()
        if getattr(self, "panning", False):
            self.CreateBackgroundBitmap()
        self.DrawToBuffer()
        dc = wx.PaintDC(self)
        dc.DrawBitmap(self.buffer, 0, 0)
        print("OnPaint")
        # tracer.stop()
        # tracer.save()

    # def OnPaint(self, event):
    #     """绘制事件"""
    #     dc = wx.BufferedPaintDC(self)
    #     # dc = wx.PaintDC(self)

    #     if self.background_bitmap:
    #         # 绘制缓存的背景图片
    #         dc.DrawBitmap(self.background_bitmap, 0, 0)

    #         # 绘制所有标注框
    #         self.DrawAllAnnotations(dc)

    #         # 绘制当前正在画的框
    #         if self.current_box and self.drawing:
    #             current_class = self.main_frame.GetCurrentClass()
    #             rgb_color = colors(current_class)
    #             color = wx.Colour(rgb_color[0], rgb_color[1], rgb_color[2])
    #             self.DrawBox(dc, self.current_box, color, 2)
    #         # 绘制十字（在最后，覆盖在其它内容之上）
    #         if self.show_crosshair and self.cross_pos:
    #             # 鼠标十字（颜色：浅灰）
    #             self.DrawCrosshair(dc, self.cross_pos, wx.Colour(0, 255, 0), style=wx.PENSTYLE_DOT)
    #     else:
    #         dc.Clear()

    def DrawAllAnnotations(self, dc):
        """绘制所有标注框"""
        for i, ann in enumerate(self.annotations):
            if self.main_frame.mode == "YOLO":

                # 转换坐标
                x, y, w, h = self.YoloToPixel(ann['bbox'])
                box = (x, y, x + w, y + h)

                # 绘制类别标签
                class_name = self.main_frame.class_names[ann['class']] if ann['class'] < len(
                    self.main_frame.class_names) else f"Class {ann['class']}"
                rgb_color = colors(ann['class'])
                color = wx.Colour(rgb_color[0], rgb_color[1], rgb_color[2])

                # 选中的框用不同颜色
                if i == self.selected_annotation_index:
                    # 选中框：更亮的颜色和更粗的线条
                    selected_color = wx.Colour(
                        min(255, color.Red() + 50),
                        min(255, color.Green() + 50),
                        min(255, color.Blue() + 50)
                    )
                    # self.DrawBox(dc, box, selected_color, 3)

                    self.DrawBox(dc, box, selected_color, 3)
                    # 绘制调整手柄
                    self.DrawResizeHandles(dc, box, selected_color)
                else:
                    self.DrawBox(dc, box, color, 2)
                dc.SetTextForeground(color)
                dc.DrawText(class_name, x, max(0, y - 20))
            else:
                # 转换坐标
                obb_box = self.ObbYoloToPixel(ann['bbox'])
                # box = (x, y, x + w, y + h)

                # 绘制类别标签
                class_name = self.main_frame.class_names[ann['class']] if ann['class'] < len(
                    self.main_frame.class_names) else f"Class {ann['class']}"
                rgb_color = colors(ann['class'])
                color = wx.Colour(rgb_color[0], rgb_color[1], rgb_color[2])

                # 选中的框用不同颜色
                if i == self.selected_annotation_index:
                    # 选中框：更亮的颜色和更粗的线条
                    selected_color = wx.Colour(
                        min(255, color.Red() + 50),
                        min(255, color.Green() + 50),
                        min(255, color.Blue() + 50)
                    )
                    # self.DrawBox(dc, box, selected_color, 3)

                    self.DrawObbBox(dc, obb_box, selected_color, 3)

                    # 绘制调整手柄
                    self.DrawObbResizeHandles(dc, obb_box, selected_color)
                else:
                    self.DrawObbBox(dc, obb_box, color, 2)

                dc.SetTextForeground(color)
                dc.DrawText(class_name, obb_box[0], max(0, obb_box[1] - 20))

    def DrawBox(self, dc, box, color, width):
        """绘制矩形框"""
        pen = wx.Pen(color, width)
        dc.SetPen(pen)
        dc.SetBrush(wx.Brush(color, wx.BRUSHSTYLE_TRANSPARENT))

        x1, y1, x2, y2 = box
        dc.DrawRectangle(x1, y1, x2 - x1, y2 - y1)

    def rectangle_corners_from_diagonal(self, p1, p2, theta_deg):
        """
        给定对角线两个点 p1, p2（tuple/list/np.array 长度 2）和矩形旋转角度 theta_deg（度）
        返回矩形四个顶点（按顺时针或逆时针顺序）。
        说明：角度 theta 是矩形一条边（宽向量）相对于 x 轴的旋转角（度）。
        计算思路：
        - 设单位向量 u 表示矩形宽方向（角度 theta），v 为其垂直方向。
        - 对角线向量 d = p2 - p1，可表示为 d = w * u + h * v，
            因此 w = d·u，h = d·v（取绝对值为边长）。
        - 中心 O = (p1 + p2) / 2，四个角为 O ± (w/2) * u ± (h/2) * v。
        """
        p1 = np.asarray(p1, dtype=float)
        p2 = np.asarray(p2, dtype=float)
        theta = np.deg2rad(theta_deg)
        u = np.array([np.cos(theta), np.sin(theta)])  # 矩形宽方向单位向量
        v = np.array([-np.sin(theta), np.cos(theta)])  # 矩形高方向单位向量 (u 逆时针转 90°)
        d = p2 - p1
        w = abs(np.dot(d, u))
        h = abs(np.dot(d, v))
        O = (p1 + p2) / 2.0

        # 生成四个角（未排序）
        corners = []
        for sx in [1, -1]:
            for sy in [1, -1]:
                corner = O + (sx * w / 2.0) * u + (sy * h / 2.0) * v
                corners.append(corner)
        corners = np.array(corners)

        # 将角点按极角排序以便连成多边形（顺时针或逆时针）
        centroid = corners.mean(axis=0)
        angles = np.arctan2(corners[:, 1] - centroid[1], corners[:, 0] - centroid[0])
        order = np.argsort(angles)
        corners = corners[order]
        return corners

    def DrawObbBox(self, dc, box, color, width=2):
        """根据角度绘制旋转矩形，从 start_pos 到 end_pos"""
        gc = wx.GraphicsContext.Create(dc)
        gc.SetPen(wx.Pen(color, width))
        gc.SetBrush(wx.Brush(wx.Colour(color[0], color[1], color[2], 50)))
        # 准备多边形点
        points = [wx.Point2D(x, y) for x, y in zip(box[::2], box[1::2])]
        # 绘制多边形
        gc.DrawLines(points + [points[0]])  # 添加第一个点到最后以闭合图形

    def DrawResizeHandles(self, dc, box, color):
        """绘制调整手柄"""
        x1, y1, x2, y2 = box
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2

        # 设置手柄样式
        dc.SetPen(wx.Pen(color, 1))
        dc.SetBrush(wx.Brush(wx.Colour(255, 255, 255)))

        half_size = self.handle_size // 2

        # 八个调整手柄的位置
        handles = [
            (x1 - half_size, y1 - half_size),  # 左上 (tl)
            (x2 - half_size, y1 - half_size),  # 右上 (tr)
            (x1 - half_size, y2 - half_size),  # 左下 (bl)
            (x2 - half_size, y2 - half_size),  # 右下 (br)
            (cx - half_size, y1 - half_size),  # 上中 (t)
            (cx - half_size, y2 - half_size),  # 下中 (b)
            (x1 - half_size, cy - half_size),  # 左中 (l)
            (x2 - half_size, cy - half_size),  # 右中 (r)
        ]

        for hx, hy in handles:
            dc.DrawRectangle(hx, hy, self.handle_size, self.handle_size)

    def DrawObbResizeHandles(self, dc, obb_box, color):
        """绘制有向边界框的旋转调整手柄（自动获取角度）"""

        gdc = wx.GCDC(dc)
        pen = wx.Pen(wx.Colour(color[0], color[1], color[2]), 1, wx.PENSTYLE_SOLID)
        brush = wx.Brush(wx.Colour(255, 255, 255, 255))
        gdc.SetPen(pen)
        gdc.SetBrush(brush)

        half_handle_size = self.handle_size / 2

        # 从左上角 -> 右上角计算 OBB 的旋转角度
        dx = obb_box[2] - obb_box[0]
        dy = obb_box[3] - obb_box[1]
        theta = math.atan2(dy, dx)  # 弧度制

        # 计算8个手柄位置
        handle_positions = [
            (obb_box[0], obb_box[1]),  # 左上
            (obb_box[2], obb_box[3]),  # 右上
            (obb_box[4], obb_box[5]),  # 右下
            (obb_box[6], obb_box[7]),  # 左下
            ((obb_box[0] + obb_box[2]) / 2, (obb_box[1] + obb_box[3]) / 2),  # 上中
            ((obb_box[4] + obb_box[6]) / 2, (obb_box[5] + obb_box[7]) / 2),  # 下中
            ((obb_box[0] + obb_box[6]) / 2, (obb_box[1] + obb_box[7]) / 2),  # 左中
            ((obb_box[2] + obb_box[4]) / 2, (obb_box[3] + obb_box[5]) / 2),  # 右中
        ]

        # 绘制每个旋转手柄
        for hx, hy in handle_positions:
            # 手柄局部四点（未旋转）
            pts = [
                (-half_handle_size, -half_handle_size),
                (half_handle_size, -half_handle_size),
                (half_handle_size, half_handle_size),
                (-half_handle_size, half_handle_size),
            ]

            # 绕 (hx, hy) 旋转
            rotated_pts = []
            for x, y in pts:
                rx = hx + x * math.cos(theta) - y * math.sin(theta)
                ry = hy + x * math.sin(theta) + y * math.cos(theta)
                rotated_pts.append((rx, ry))
            # print("rotated_pts:", rotated_pts)
            rotated_pts = [(int(x), int(y)) for x, y in rotated_pts]

            gdc.DrawPolygon(rotated_pts)

    # def DrawCrosshair(self, dc, pos, color=wx.Colour(200, 200, 200), style=wx.PENSTYLE_DOT):
    #     """
    #     在图片区域绘制十字（水平 + 垂直线）。pos: wx.Point（面板坐标）。
    #     style: wx pen style 如 wx.PENSTYLE_DOT, wx.PENSTYLE_SHORT_DASH 等。
    #     """
    #     if not self.image:
    #         return

    #     # 计算图片显示的边界（面板坐标）
    #     img_x1 = int(self.offset_x)
    #     img_y1 = int(self.offset_y)
    #     img_x2 = int(self.offset_x + self.image_size[0] * self.scale_factor)
    #     img_y2 = int(self.offset_y + self.image_size[1] * self.scale_factor)

    #     # 限制 pos 在图片范围内
    #     px = max(img_x1, min(img_x2, pos.x))
    #     py = max(img_y1, min(img_y2, pos.y))

    #     # 画线（水平 + 垂直），使用虚线或点线
    #     pen = wx.Pen(color, 3, style)
    #     dc.SetPen(pen)

    #     # 有时候画整条线会穿过 UI 元素，会显得突兀，可以只画在图片内：
    #     dc.DrawLine(px, img_y1, px, img_y2)  # 垂直线：x 固定，y 从 img_y1 到 img_y2
    #     dc.DrawLine(img_x1, py, img_x2, py)  # 水平线：y 固定，x 从 img_x1 到 img_x2

    #     # 画一个小十字中心点（便于视觉对齐）
    #     small_pen = wx.Pen(color, 5)
    #     dc.SetPen(small_pen)
    #     s = 7
    #     dc.DrawLine(px - s, py, px + s, py)
    #     dc.DrawLine(px, py - s, px, py + s)

    def _line_rect_intersections(self, px, py, dx, dy, x_min, y_min, x_max, y_max, eps=1e-9):
        """返回直线 (px,py) + t*(dx,dy) 与矩形边界的交点列表。
        结果为 [(x,y,t), ...]，t 是参数值（用于排序）。
        """
        pts = []

        # 与垂直边 x = x_min / x_max 相交（如果 dx != 0）
        if abs(dx) > eps:
            for x_edge in (x_min, x_max):
                t = (x_edge - px) / dx
                y = py + t * dy
                if y_min - eps <= y <= y_max + eps:
                    pts.append((x_edge, y, t))

        # 与水平边 y = y_min / y_max 相交（如果 dy != 0）
        if abs(dy) > eps:
            for y_edge in (y_min, y_max):
                t = (y_edge - py) / dy
                x = px + t * dx
                if x_min - eps <= x <= x_max + eps:
                    pts.append((x, y_edge, t))

        # 去重（有可能重复出现同一个角点），按 t 排序
        unique = []
        seen = set()
        for x, y, t in pts:
            key = (round(x, 9), round(y, 9))
            if key not in seen:
                seen.add(key)
                unique.append((x, y, t))
        unique.sort(key=lambda e: e[2])
        return unique

    def cross_segment_endpoints(self, img_x1, img_y1, img_x2, img_y2, px, py, angle_deg):
        """
        返回两个互相垂直线段的四个端点：
        ((ax1,ay1),(ax2,ay2)), ((bx1,by1),(bx2,by2))
        其中第一对是角度为 angle_deg 的线段端点，第二对是垂直（angle_deg+90°）的线段端点。
        要求交点(px,py) 在矩形内且端点在矩形边上。
        """
        # 规范化矩形（支持任意顺序传入的边界）
        x_min = min(img_x1, img_x2)
        x_max = max(img_x1, img_x2)
        y_min = min(img_y1, img_y2)
        y_max = max(img_y1, img_y2)

        # 检查 px,py 是否在矩形内（包含边界）
        if not (x_min <= px <= x_max and y_min <= py <= y_max):
            raise ValueError("交点(px,py) 必须在图像边界内")

        def endpoints_for_angle(angle_deg):
            theta = math.radians(angle_deg)
            dx = math.cos(theta)
            dy = math.sin(theta)
            inters = self._line_rect_intersections(px, py, dx, dy, x_min, y_min, x_max, y_max)
            # 对于无限直线与矩形，应该得到 2 个不同的交点
            if len(inters) < 2:
                # 有极少数数值/退化情况，尝试容忍返回已有点
                if len(inters) == 1:
                    x, y, t = inters[0]
                    return (x, y), (x, y)
                raise RuntimeError(f"未能找到足够的交点（angle={angle_deg}），交点数={len(inters)}")
            # 取 t 最小和最大的两个（分别对应线的两端）
            p1 = (inters[0][0], inters[0][1])
            p2 = (inters[-1][0], inters[-1][1])
            return p1, p2

        a1, a2 = endpoints_for_angle(angle_deg)
        b1, b2 = endpoints_for_angle(angle_deg + 90.0)

        return (a1, a2), (b1, b2)

    def DrawCrosshair(
            self, dc, pos,
            color=wx.Colour(200, 200, 200),
            style=wx.PENSTYLE_DOT,
            angle_deg=0.0
    ):
        """
        在图片区域绘制十字辅助线（支持旋转）。
        使用 GraphicsContext 实现平滑抗锯齿。
        """
        if not self.image:
            return

        # 计算图片显示边界（面板坐标）
        img_x1 = int(self.offset_x)
        img_y1 = int(self.offset_y)
        img_x2 = int(self.offset_x + self.image_size[0] * self.scale_factor)
        img_y2 = int(self.offset_y + self.image_size[1] * self.scale_factor)

        # 限制 pos 在图片范围内
        px = max(img_x1, min(img_x2, pos.x))
        py = max(img_y1, min(img_y2, pos.y))

        (a1, a2), (b1, b2) = self.cross_segment_endpoints(
            img_x1, img_y1, img_x2, img_y2, px, py, angle_deg
        )

        # --- GraphicsContext ---
        gc = wx.GraphicsContext.Create(dc)

        gc.SetAntialiasMode(wx.ANTIALIAS_DEFAULT)

        # ---- 主十字线条 ----
        pen_info = wx.GraphicsPenInfo(color).Width(2)

        gc.SetPen(gc.CreatePen(pen_info))

        # 绘制两条旋转线
        gc.StrokeLine(a1[0], a1[1], a2[0], a2[1])
        gc.StrokeLine(b1[0], b1[1], b2[0], b2[1])

        # ---- 中心点小十字（总是实线）----
        small_pen = gc.CreatePen(wx.GraphicsPenInfo(color).Width(4))
        gc.SetPen(small_pen)

        s = 6
        gc.StrokeLine(px - s, py, px + s, py)
        gc.StrokeLine(px, py - s, px, py + s)
        if self.main_frame.mode == "YOLO-OBB" and getattr(self, "adjusting", False):
            self.DrawAnchor(gc, self.adjust_last_pos[0], self.adjust_last_pos[1])

    def DrawAnchor(self, gc, x, y, outer_radius=6, inner_radius=3):
        """
        使用 wx.GraphicsContext 绘制一个绿色锚点（外围绿色圆，中间白色）
        """
        # 抗锯齿
        gc.SetAntialiasMode(wx.ANTIALIAS_DEFAULT)

        # ---- 外圆（绿色） ----
        outer_brush = gc.CreateBrush(wx.Brush(wx.Colour(0, 255, 0)))  # 亮绿色
        outer_pen = gc.CreatePen(wx.Pen(wx.Colour(0, 255, 0), 1))

        gc.SetBrush(outer_brush)
        gc.SetPen(outer_pen)
        gc.DrawEllipse(x - outer_radius, y - outer_radius,
                       outer_radius * 2, outer_radius * 2)

        # ---- 内圆（白色） ----
        inner_brush = gc.CreateBrush(wx.Brush(wx.Colour(255, 255, 255)))
        inner_pen = gc.CreatePen(wx.Pen(wx.Colour(255, 255, 255), 1))

        gc.SetBrush(inner_brush)
        gc.SetPen(inner_pen)
        gc.DrawEllipse(x - inner_radius, y - inner_radius,
                       inner_radius * 2, inner_radius * 2)

    def GetResizeHandle(self, pos, box):
        """获取鼠标位置对应的调整手柄"""
        x1, y1, x2, y2 = box
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2

        half_size = self.handle_size // 2

        # 检查各个手柄
        handles = {
            'tl': (x1 - half_size, y1 - half_size, x1 + half_size, y1 + half_size),
            'tr': (x2 - half_size, y1 - half_size, x2 + half_size, y1 + half_size),
            'bl': (x1 - half_size, y2 - half_size, x1 + half_size, y2 + half_size),
            'br': (x2 - half_size, y2 - half_size, x2 + half_size, y2 + half_size),
            't': (cx - half_size, y1 - half_size, cx + half_size, y1 + half_size),
            'b': (cx - half_size, y2 - half_size, cx + half_size, y2 + half_size),
            'l': (x1 - half_size, cy - half_size, x1 + half_size, cy + half_size),
            'r': (x2 - half_size, cy - half_size, x2 + half_size, cy + half_size),
        }

        for handle_name, (hx1, hy1, hx2, hy2) in handles.items():
            if hx1 <= pos.x <= hx2 and hy1 <= pos.y <= hy2:
                return handle_name

        return None

    def GetObbResizeHandle(self, pos, obb_box):
        """检测鼠标是否点中了旋转矩形的调整手柄"""
        # 计算8个手柄中心点
        handle_positions = {
            'tl': (obb_box[0], obb_box[1]),  # 左上
            'tr': (obb_box[2], obb_box[3]),  # 右上
            'br': (obb_box[4], obb_box[5]),  # 右下
            'bl': (obb_box[6], obb_box[7]),  # 左下
            't': ((obb_box[0] + obb_box[2]) / 2, (obb_box[1] + obb_box[3]) / 2),  # 上中
            'r': ((obb_box[2] + obb_box[4]) / 2, (obb_box[3] + obb_box[5]) / 2),  # 右中
            'b': ((obb_box[4] + obb_box[6]) / 2, (obb_box[5] + obb_box[7]) / 2),  # 下中
            'l': ((obb_box[6] + obb_box[0]) / 2, (obb_box[7] + obb_box[1]) / 2),  # 左中
        }

        # 鼠标点击位置
        px, py = pos.x, pos.y
        threshold = self.handle_size * 1.2  # 判定半径（可调）
        min_dist = float('inf')
        selected_handle = None

        # 遍历所有手柄，计算距离
        for name, (hx, hy) in handle_positions.items():
            dist = math.hypot(px - hx, py - hy)
            if dist < threshold and dist < min_dist:
                min_dist = dist
                selected_handle = name

        return selected_handle  # 没有命中则返回 None

    def GetAnnotationAt(self, pos):
        """获取指定位置的标注索引"""
        if self.main_frame.mode == "YOLO":
            for i, ann in enumerate(self.annotations):
                x, y, w, h = self.YoloToPixel(ann['bbox'])
                if x <= pos.x <= x + w and y <= pos.y <= y + h:
                    return i
        else:
            def point_in_polygon(px, py, poly):
                """射线法判断点是否在多边形内，poly 是 [(x1,y1), (x2,y2), ...]"""
                n = len(poly)
                inside = False
                p1x, p1y = poly[0]
                for i in range(1, n + 1):
                    p2x, p2y = poly[i % n]
                    if py > min(p1y, p2y):
                        if py <= max(p1y, p2y):
                            if px <= max(p1x, p2x):
                                if p1y != p2y:
                                    xinters = (py - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                                if p1x == p2x or px <= xinters:
                                    inside = not inside
                    p1x, p1y = p2x, p2y
                return inside

            for i, ann in enumerate(self.annotations):
                coords = self.ObbYoloToPixel(ann['bbox'])  # 返回 (x1, y1, x2, y2, x3, y3, x4, y4)
                polygon = [(coords[j], coords[j + 1]) for j in range(0, 8, 2)]
                if point_in_polygon(pos.x, pos.y, polygon):
                    return i
        return -1

    def OnLeftDown(self, event):
        """鼠标左键按下"""
        if not self.image:
            return

        self.SetFocus()  # 获取焦点以接收键盘事件
        pos = event.GetPosition()

        if not self.IsInImageArea(pos):
            return

        # 检查是否点击了选中标注的调整手柄
        if self.main_frame.mode == "YOLO":
            if self.selected_annotation_index >= 0:
                ann = self.annotations[self.selected_annotation_index]
                x, y, w, h = self.YoloToPixel(ann['bbox'])
                box = (x, y, x + w, y + h)

                handle = self.GetResizeHandle(pos, box)
                if handle:
                    # 开始调整大小
                    self.editing_mode = 'resize'
                    self.resize_handle = handle
                    self.edit_start_pos = pos
                    self.original_bbox = ann['bbox'][:]
                    return
        else:  # self.main_frame.mode == "YOLO_OBB":

            if self.selected_annotation_index >= 0:
                ann = self.annotations[self.selected_annotation_index]
                handle = self.GetObbResizeHandle(pos, self.ObbYoloToPixel(ann['bbox']))
                if handle:
                    self.editing_mode = 'resize'
                    self.resize_handle = handle
                    self.edit_start_pos = pos
                    self.original_obb = ann['bbox'][:]
                    return

        # 检查是否点击了标注框
        clicked_index = self.GetAnnotationAt(pos)

        if clicked_index >= 0:
            # 如果点击的是已选中的框，开始移动
            if clicked_index == self.selected_annotation_index:
                self.editing_mode = 'move'
                self.edit_start_pos = pos
                self.original_bbox = self.annotations[clicked_index]['bbox'][:]
                print(self.original_bbox)
            else:
                # 选中新的框
                self.selected_annotation_index = clicked_index
                self.Refresh(False)  # 刷新，不擦背景，减少闪烁
        else:
            # 取消选择，开始画新框
            self.selected_annotation_index = -1

            # 检查是否有可用的类别
            if not self.main_frame.class_names:
                # 提示新建类别
                dlg = wx.MessageDialog(self, "没有可用的类别，是否要添加新类别？", "提示",
                                       wx.YES_NO | wx.ICON_QUESTION)
                if dlg.ShowModal() == wx.ID_YES:
                    self.main_frame.OnAddClass(None)
                dlg.Destroy()

                # 如果添加类别后仍然没有类别，则不开始绘制
                if not self.main_frame.class_names:
                    return

            self.drawing = True
            # 限制起始位置在图片内
            clamped_pos = self.ClampPositionToImage(pos)
            self.start_pos = clamped_pos
            self.current_box = (clamped_pos.x, clamped_pos.y, clamped_pos.x, clamped_pos.y)
            self.current_obb_box = (clamped_pos.x, clamped_pos.y, clamped_pos.x, clamped_pos.y,
                                    clamped_pos.x, clamped_pos.y, clamped_pos.x, clamped_pos.y)
            print(self.current_box)
            self.Refresh(False)  # 刷新，不擦背景，减少闪烁

    def OnLeftUp(self, event):
        """鼠标左键释放"""
        pos = event.GetPosition()

        if self.editing_mode == 'move':
            # 结束移动
            self.editing_mode = None
            self.edit_start_pos = None
            self.original_bbox = None

        elif self.editing_mode == 'resize':
            # 结束调整大小
            self.editing_mode = None
            self.resize_handle = None
            self.edit_start_pos = None
            self.original_bbox = None

        elif self.drawing:
            # 结束画框
            self.drawing = False
            if self.current_box:
                x1, y1, x2, y2 = self.current_box

                # 确保框有一定大小
                if abs(x2 - x1) > 5 and abs(y2 - y1) > 5:
                    # 转换为YOLO格式并添加标注
                    yolo_bbox = self.PixelToYolo((min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1)))
                    obb_yolo_bbox = self.PixelToObbYolo(self.current_obb_box)

                    # 获取当前选择的类别
                    current_class = self.main_frame.GetCurrentClass()

                    if self.main_frame.mode == "YOLO-OBB":
                        annotation = {
                            'class': current_class,
                            'bbox': obb_yolo_bbox,
                            # 'angle': self.cross_angle   # 新增角度信息
                        }
                    else:
                        annotation = {
                            'class': current_class,
                            'bbox': yolo_bbox
                        }
                    self.annotations.append(annotation)
                    print(self.annotations)
                    self.main_frame.UpdateAnnotationList()

                    # 选中新创建的标注
                    self.selected_annotation_index = len(self.annotations) - 1

                self.current_box = None
            self.Refresh(False)  # 刷新，不擦背景，减少闪烁

    def ClampOffset(self):
        """
        保证图片不会被拖得完全离开面板视野：
        - 如果图片比 panel 小，则保持居中
        - 如果图片比 panel 大，则允许拖动但不能把图片整张移出（即至少有一像素可见）
        """
        if not self.scaled_bitmap:
            return

        sw = self.scaled_bitmap.GetWidth()
        sh = self.scaled_bitmap.GetHeight()
        pw, ph = self.GetClientSize().width, self.GetClientSize().height

        if sw <= pw:
            min_x = max_x = (pw - sw) / 2.0
        else:
            min_x = pw - sw
            max_x = 0.0

        if sh <= ph:
            min_y = max_y = (ph - sh) / 2.0
        else:
            min_y = ph - sh
            max_y = 0.0

        # clamp
        # self.offset_x = max(min_x, min(max_x, self.offset_x))
        # self.offset_y = max(min_y, min(max_y, self.offset_y))

    def OnMouseWheel(self, event):
        """Ctrl + 滚轮 缩放（以鼠标为中心）"""
        if not self.image:
            return

        if not event.ControlDown():
            return  # 你可以改成不按 ctrl 时滚动页面行为

        rotation = event.GetWheelRotation()
        # 简单做法：正/负决定放大或缩小
        zoom_step = 1.1 if rotation > 0 else (1.0 / 1.1)

        old_scale = self.scale_factor
        new_scale = max(0.05, min(20.0, old_scale * zoom_step))
        if abs(new_scale - old_scale) < 1e-9:
            return

        mouse = event.GetPosition()  # 鼠标在 panel 坐标系
        ratio = new_scale / old_scale

        # 保持鼠标处为缩放中心
        self.offset_x = mouse.x - (mouse.x - self.offset_x) * ratio
        self.offset_y = mouse.y - (mouse.y - self.offset_y) * ratio

        self.scale_factor = new_scale
        self.UpdateScaledBitmap()
        self.ClampOffset()
        self.Refresh(False)

    def OnMiddleDown(self, event):
        """开始平移"""
        if not self.image:
            return
        self.panning = True
        self.pan_last_pos = event.GetPosition()
        try:
            self.CaptureMouse()
        except Exception:
            pass
        # 改变光标为抓手
        self.SetCursor(wx.Cursor(wx.CURSOR_SIZING))

    def OnMiddleUp(self, event):
        """结束平移"""
        if self.panning:
            self.panning = False
            self.pan_last_pos = None
            try:
                if self.HasCapture():
                    self.ReleaseMouse()
            except Exception:
                pass
            # 恢复默认光标
            self.SetCursor(wx.NullCursor)
            # 最后 clamp 并刷新
            self.ClampOffset()
            self.Refresh(False)

    def OnMouseLeave(self, event):
        """防止 mouse capture 卡死（离开时释放）"""
        if self.panning:
            self.panning = False
            try:
                if self.HasCapture():
                    self.ReleaseMouse()
            except Exception:
                pass
            self.SetCursor(wx.NullCursor)
            self.pan_last_pos = None
            self.Refresh(False)

        if self.adjusting:
            self.adjusting = False
            try:
                if self.HasCapture():
                    self.ReleaseMouse()
            except Exception:
                pass
            self.SetCursor(wx.NullCursor)
            self.adjust_last_pos = None
            self.Refresh(False)

    def OnMouseMove(self, event):
        """鼠标移动"""
        pos = event.GetPosition()

        if getattr(self, "panning", False):
            pos = event.GetPosition()
            dx = pos.x - self.pan_last_pos.x
            dy = pos.y - self.pan_last_pos.y
            # 直接移动 offset（float）
            self.offset_x += dx
            self.offset_y += dy
            self.pan_last_pos = pos
            # 不需要重建 scaled_bitmap，仅刷新绘制位置
            # self.UpdateScaledBitmap()
            # self.ClampOffset()
            self.Refresh(False)
            print("panning")
            print(pos)

        if self.main_frame.mode == "YOLO-OBB" and getattr(self, "adjusting", False):
            pos = event.GetPosition()
            self.cross_angle = math.degrees(
                math.atan2(pos.y - self.adjust_last_pos.y, pos.x - self.adjust_last_pos.x))  # 注意顺序是 (y, x)

        # 每次移动都更新 cross_pos（但限制到图片区域）
        if self.image and self.IsInImageArea(pos):
            self.cross_pos = self.ClampPositionToImage(pos)
        else:
            self.cross_pos = None

        if self.editing_mode == 'move' and self.selected_annotation_index >= 0:

            if self.main_frame.mode == "YOLO":
                # 移动标注框
                dx = pos.x - self.edit_start_pos.x
                dy = pos.y - self.edit_start_pos.y

                # 将像素偏移转换为YOLO格式偏移
                dx_yolo = dx / (self.scale_factor * self.image_size[0])
                dy_yolo = dy / (self.scale_factor * self.image_size[1])

                # 更新标注位置
                new_bbox = list(self.original_bbox)
                new_bbox[0] += dx_yolo  # 中心点x
                new_bbox[1] += dy_yolo  # 中心点y

                # 确保标注框不超出图片边界
                half_w = new_bbox[2] / 2
                half_h = new_bbox[3] / 2
                new_bbox[0] = max(half_w, min(1 - half_w, new_bbox[0]))
                new_bbox[1] = max(half_h, min(1 - half_h, new_bbox[1]))

                self.annotations[self.selected_annotation_index]['bbox'] = new_bbox
                self.main_frame.UpdateAnnotationList()
                # self.main_frame.UpdateAnnotationListItem(self.selected_annotation_index)

                self.Refresh(False)  # 刷新，不擦背景，减少闪烁
            else:
                # OBB 模式：移动整个四边形，但如果会越界，则把该方向的移动限制到不会越界（即移动到边界为止）
                dx = pos.x - self.edit_start_pos.x
                dy = pos.y - self.edit_start_pos.y

                # 将像素偏移转换为归一化坐标偏移（相对于图像宽高）
                dx_norm = dx / (self.scale_factor * self.image_size[0])
                dy_norm = dy / (self.scale_factor * self.image_size[1])

                # original_bbox 假定是归一化的 8 个坐标 [x1,y1,x2,y2,...]
                orig = list(self.original_bbox)  # 复制一份以免修改原始数据

                # 计算当前 bbox 的 min/max（归一化坐标）
                xs = [orig[i] for i in range(0, 8, 2)]
                ys = [orig[i + 1] for i in range(0, 8, 2)]
                min_x, max_x = min(xs), max(xs)
                min_y, max_y = min(ys), max(ys)

                # 允许的 dx_norm 范围：保证所有点在 [0,1]
                # 例如向右移动限制为 dx_norm <= 1 - max_x；向左限制为 dx_norm >= -min_x
                allowed_dx_min = -min_x
                allowed_dx_max = 1.0 - max_x
                # 把请求的 dx_norm 限制到允许范围
                dx_norm_clamped = max(allowed_dx_min, min(allowed_dx_max, dx_norm))

                # 同理处理 dy_norm
                allowed_dy_min = -min_y
                allowed_dy_max = 1.0 - max_y
                dy_norm_clamped = max(allowed_dy_min, min(allowed_dy_max, dy_norm))

                # 将被允许的偏移同时应用到四个顶点（保持形状）
                final_bbox = []
                for i in range(0, 8, 2):
                    nx = orig[i] + dx_norm_clamped
                    ny = orig[i + 1] + dy_norm_clamped
                    # 作为保险再 clamp 到 [0,1]
                    nx = max(0.0, min(1.0, nx))
                    ny = max(0.0, min(1.0, ny))
                    final_bbox.extend([nx, ny])

                self.annotations[self.selected_annotation_index]['bbox'] = final_bbox
                self.main_frame.UpdateAnnotationList()
                # self.main_frame.UpdateAnnotationListItem(self.selected_annotation_index)

                self.Refresh(False)

        elif self.editing_mode == 'resize' and self.selected_annotation_index >= 0:

            # 调整标注框大小
            if self.main_frame.mode == "YOLO":
                self.ResizeAnnotation(pos)
            else:
                self.ResizeObbAnnotation(pos)
            self.main_frame.UpdateAnnotationList()
            # self.main_frame.UpdateAnnotationListItem(self.selected_annotation_index)
            self.Refresh(False)  # 刷新，不擦背景，减少闪烁

        elif self.drawing and self.start_pos:
            # 画新框
            clamped_pos = self.ClampPositionToImage(pos)
            self.current_box = (self.start_pos.x, self.start_pos.y, clamped_pos.x, clamped_pos.y)
            rotated_pts = self.rectangle_corners_from_diagonal((self.start_pos.x, self.start_pos.y),
                                                               (clamped_pos.x, clamped_pos.y), self.cross_angle)

            self.current_obb_box = tuple(x for pair in rotated_pts for x in pair)
            self.Refresh(False)  # 刷新，不擦背景，减少闪烁
        else:
            # 更新鼠标光标
            self.UpdateCursor(pos)

        self.Refresh(False)  # 刷新，不擦背景，减少闪烁

    def ResizeAnnotation(self, pos):
        """调整标注框大小"""
        if not self.original_bbox or not self.edit_start_pos:
            return

        # 获取原始框的像素坐标
        orig_x, orig_y, orig_w, orig_h = self.YoloToPixel(self.original_bbox)
        orig_x1, orig_y1 = orig_x, orig_y
        orig_x2, orig_y2 = orig_x + orig_w, orig_y + orig_h

        # 计算鼠标移动距离
        dx = pos.x - self.edit_start_pos.x
        dy = pos.y - self.edit_start_pos.y

        # 根据调整手柄类型计算新的边界
        new_x1, new_y1, new_x2, new_y2 = orig_x1, orig_y1, orig_x2, orig_y2

        if 'l' in self.resize_handle:  # 左边
            new_x1 = orig_x1 + dx
        if 'r' in self.resize_handle:  # 右边
            new_x2 = orig_x2 + dx
        if 't' in self.resize_handle:  # 上边
            new_y1 = orig_y1 + dy
        if 'b' in self.resize_handle:  # 下边
            new_y2 = orig_y2 + dy

        # 确保最小大小
        min_size = 10
        if new_x2 - new_x1 < min_size:
            if 'l' in self.resize_handle:
                new_x1 = new_x2 - min_size
            else:
                new_x2 = new_x1 + min_size

        if new_y2 - new_y1 < min_size:
            if 't' in self.resize_handle:
                new_y1 = new_y2 - min_size
            else:
                new_y2 = new_y1 + min_size

        # 限制在图片范围内
        img_x1 = self.offset_x
        img_y1 = self.offset_y
        img_x2 = self.offset_x + self.image_size[0] * self.scale_factor
        img_y2 = self.offset_y + self.image_size[1] * self.scale_factor

        new_x1 = max(img_x1, min(img_x2, new_x1))
        new_y1 = max(img_y1, min(img_y2, new_y1))
        new_x2 = max(img_x1, min(img_x2, new_x2))
        new_y2 = max(img_y1, min(img_y2, new_y2))

        # 转换回YOLO格式
        new_bbox = self.PixelToYolo((min(new_x1, new_x2), min(new_y1, new_y2),
                                     abs(new_x2 - new_x1), abs(new_y2 - new_y1)))

        self.annotations[self.selected_annotation_index]['bbox'] = new_bbox

    def ResizeObbAnnotation(self, pos):
        """改进的 OBB 尺寸调整：支持边界自动截断并反推坐标"""
        if not getattr(self, 'original_obb', None) or not getattr(self, 'edit_start_pos', None):
            return

        orig_pts = np.array(self.ObbYoloToPixel(self.original_obb), dtype=float).reshape(4, 2)
        p0, p1, p2, p3 = orig_pts.copy()

        img_x1 = self.offset_x
        img_y1 = self.offset_y
        img_x2 = self.offset_x + self.image_size[0] * self.scale_factor
        img_y2 = self.offset_y + self.image_size[1] * self.scale_factor

        u = p1 - p0
        u_norm = np.linalg.norm(u)
        if u_norm == 0:
            return
        u = u / u_norm

        v = p3 - p0
        v_norm = np.linalg.norm(v)
        if v_norm == 0:
            return
        v = v / v_norm

        dx = pos.x - self.edit_start_pos.x
        dy = pos.y - self.edit_start_pos.y
        move_vec = np.array([dx, dy], dtype=float)

        comp_u = np.dot(move_vec, u) * u
        comp_v = np.dot(move_vec, v) * v

        def clamp_movement(base_pts, pts_indices, movement):
            if np.allclose(movement, 0):
                return movement

            max_t = 1.0
            for idx in pts_indices:
                pt = base_pts[idx]
                new_pt = pt + movement

                if movement[0] > 0:
                    if new_pt[0] > img_x2:
                        t = (img_x2 - pt[0]) / movement[0]
                        max_t = min(max_t, t)
                elif movement[0] < 0:
                    if new_pt[0] < img_x1:
                        t = (img_x1 - pt[0]) / movement[0]
                        max_t = min(max_t, t)

                if movement[1] > 0:
                    if new_pt[1] > img_y2:
                        t = (img_y2 - pt[1]) / movement[1]
                        max_t = min(max_t, t)
                elif movement[1] < 0:
                    if new_pt[1] < img_y1:
                        t = (img_y1 - pt[1]) / movement[1]
                        max_t = min(max_t, t)

            max_t = max(0.0, max_t)
            return movement * max_t

        def dxdy_from_a_and_u_np(a, u, d=10.0, eps=1e-12):
            u = np.asarray(u, dtype=float)
            norm = np.linalg.norm(u)
            if norm < eps:
                raise ValueError("direction vector u is zero")
            u_unit = u / norm
            return d * u_unit  # 返回 (dx,dy)

        def signed_distance_along_u(a, b, u, eps=1e-12):
            """
            a, b: array-like (x,y)
            u: array-like direction vector (preferably unit). If not unit, function normalizes it.
            返回: 带符号距离 s（从 a 指向 b 的方向为正）
            """
            a = np.asarray(a, dtype=float)
            b = np.asarray(b, dtype=float)
            u = np.asarray(u, dtype=float)

            v = b - a  # ab 向量
            norm_u = np.linalg.norm(u)
            if norm_u < eps:
                raise ValueError("direction u is zero vector")
            u_unit = u / norm_u

            s = float(np.dot(v, u_unit))
            return s

        new_pts = orig_pts.copy()

        # 注意这里用 new_pts 作为基准（顺序：先 u 再 v），这样角点会按期望顺序钳制
        if 'l' in self.resize_handle:  # 左边 (p0, p3) 沿 u
            clamped_u = clamp_movement(new_pts, [0, 3], comp_u)
            new_pts[0] = new_pts[0] + clamped_u
            new_pts[3] = new_pts[3] + clamped_u
        if 'r' in self.resize_handle:  # 右边 (p1, p2) 沿 u
            clamped_u = clamp_movement(new_pts, [1, 2], comp_u)
            new_pts[1] = new_pts[1] + clamped_u
            new_pts[2] = new_pts[2] + clamped_u
        if 't' in self.resize_handle:  # 上边 (p0, p1) 沿 v
            clamped_v = clamp_movement(new_pts, [0, 1], comp_v)
            new_pts[0] = new_pts[0] + clamped_v
            new_pts[1] = new_pts[1] + clamped_v
        if 'b' in self.resize_handle:  # 下边 (p3, p2) 沿 v
            clamped_v = clamp_movement(new_pts, [3, 2], comp_v)
            new_pts[3] = new_pts[3] + clamped_v
            new_pts[2] = new_pts[2] + clamped_v

        # 确保最小大小
        min_size = 10.0
        if signed_distance_along_u(new_pts[0], new_pts[1], u) < min_size:
            if 'l' in self.resize_handle:
                new_pts[0] = new_pts[1] + dxdy_from_a_and_u_np(orig_pts[1], u, -min_size)
                new_pts[3] = new_pts[2] + dxdy_from_a_and_u_np(orig_pts[2], u, -min_size)
            else:
                new_pts[1] = new_pts[0] + dxdy_from_a_and_u_np(orig_pts[0], u, min_size)
                new_pts[2] = new_pts[3] + dxdy_from_a_and_u_np(orig_pts[3], u, min_size)
        if signed_distance_along_u(new_pts[0], new_pts[3], v) < min_size:
            if 't' in self.resize_handle:
                new_pts[0] = new_pts[3] + dxdy_from_a_and_u_np(orig_pts[3], v, -min_size)
                new_pts[1] = new_pts[2] + dxdy_from_a_and_u_np(orig_pts[2], v, -min_size)
            else:
                new_pts[2] = new_pts[1] + dxdy_from_a_and_u_np(orig_pts[1], v, min_size)
                new_pts[3] = new_pts[0] + dxdy_from_a_and_u_np(orig_pts[0], v, min_size)

        final_pts = new_pts.copy()
        final_pts[:, 0] = np.clip(final_pts[:, 0], img_x1, img_x2)
        final_pts[:, 1] = np.clip(final_pts[:, 1], img_y1, img_y2)

        final_pts_flat = final_pts.reshape(-1).tolist()
        new_obb_yolo = self.PixelToObbYolo(tuple(final_pts_flat))
        self.annotations[self.selected_annotation_index]['bbox'] = new_obb_yolo

        self.main_frame.UpdateAnnotationList()
        self.Refresh(False)

    def UpdateCursor(self, pos):
        """更新鼠标光标"""

        if self.selected_annotation_index >= 0:
            ann = self.annotations[self.selected_annotation_index]
            if self.main_frame.mode == "YOLO":
                x, y, w, h = self.YoloToPixel(ann['bbox'])
                box = (x, y, x + w, y + h)

                handle = self.GetResizeHandle(pos, box)
            else:
                handle = self.GetObbResizeHandle(pos, self.ObbYoloToPixel(ann['bbox']))
            if handle:
                # 设置调整大小光标
                cursor_map = {
                    'tl': wx.CURSOR_SIZENWSE, 'br': wx.CURSOR_SIZENWSE,
                    'tr': wx.CURSOR_SIZENESW, 'bl': wx.CURSOR_SIZENESW,
                    't': wx.CURSOR_SIZENS, 'b': wx.CURSOR_SIZENS,
                    'l': wx.CURSOR_SIZEWE, 'r': wx.CURSOR_SIZEWE,
                }
                self.SetCursor(wx.Cursor(cursor_map.get(handle, wx.CURSOR_DEFAULT)))
                return
            else:
                if self.main_frame.mode == "YOLO" and x <= pos.x <= x + w and y <= pos.y <= y + h:
                    # 在选中框内，设置移动光标
                    self.SetCursor(wx.Cursor(wx.CURSOR_SIZING))
                    return
                elif self.main_frame.mode == "YOLO-OBB" and self.GetAnnotationAt(pos) != -1:
                    # 在选中框内，设置移动光标
                    self.SetCursor(wx.Cursor(wx.CURSOR_SIZING))
                    return
        if getattr(self, "panning", False):
            self.SetCursor(wx.Cursor(wx.CURSOR_SIZING))
            return

        # 默认光标
        self.SetCursor(wx.Cursor(wx.CURSOR_BLANK))
        # self.SetCursor(wx.Cursor(wx.CURSOR_DEFAULT))

    def OnMouseEnter(self, event):
        """鼠标进入时自动获取焦点"""
        self.SetFocus()
        event.Skip()

    def OnKeyDown(self, event):
        """键盘事件"""
        key_code = event.GetKeyCode()

        if key_code == wx.WXK_DELETE or key_code == wx.WXK_BACK:
            # 删除选中的标注
            if self.selected_annotation_index >= 0:
                del self.annotations[self.selected_annotation_index]
                self.selected_annotation_index = -1
                self.main_frame.UpdateAnnotationList()
                self.Refresh(False)  # 刷新，不擦背景，减少闪烁
                return
        elif key_code == wx.WXK_ESCAPE:
            # 取消选择
            self.selected_annotation_index = -1
            self.drawing = False
            self.current_box = None
            self.editing_mode = None
            self.Refresh(False)  # 刷新，不擦背景，减少闪烁s
            return

        if self.main_frame.mode == "YOLO-OBB":
            if key_code == ord('Z'):
                self.cross_angle -= 5 * self.rotation_step
            elif key_code == ord('X'):
                self.cross_angle -= self.rotation_step
            elif key_code == ord('C'):
                self.cross_angle += self.rotation_step
            elif key_code == ord('V'):
                self.cross_angle += 5 * self.rotation_step
            self.cross_angle %= 360
            # print(f"十字角度: {self.cross_angle:.1f}°")
            self.Refresh(False)
            return

        event.Skip()

    def OnRightDown(self, event):
        """右键调节角度"""
        self.adjusting = True
        self.adjust_last_pos = event.GetPosition()
        try:
            self.CaptureMouse()
        except Exception:
            pass

    def OnRightUp(self, event):
        """结束调节角度"""
        if self.adjusting:
            self.adjusting = False
            try:
                if self.HasCapture():
                    self.ReleaseMouse()
            except Exception:
                pass
            self.SetCursor(wx.NullCursor)
            self.adjust_last_pos = None
            self.Refresh(False)

    def IsInImageArea(self, pos):
        """检查位置是否在图片区域内"""
        if not self.image:
            return False

        scaled_width = self.image_size[0] * self.scale_factor
        scaled_height = self.image_size[1] * self.scale_factor

        return (self.offset_x <= pos.x <= self.offset_x + scaled_width and
                self.offset_y <= pos.y <= self.offset_y + scaled_height)

    def PixelToYolo(self, pixel_bbox):
        """像素坐标转YOLO格式"""
        px, py, pw, ph = pixel_bbox

        # 转换为相对于图片的坐标
        img_x = (px - self.offset_x) / self.scale_factor
        img_y = (py - self.offset_y) / self.scale_factor
        img_w = pw / self.scale_factor
        img_h = ph / self.scale_factor

        # 转换为YOLO格式 (中心点坐标 + 相对宽高)
        center_x = (img_x + img_w / 2) / self.image_size[0]
        center_y = (img_y + img_h / 2) / self.image_size[1]
        rel_w = img_w / self.image_size[0]
        rel_h = img_h / self.image_size[1]

        return center_x, center_y, rel_w, rel_h

    def PixelToObbYolo(self, pixel_bbox):
        """像素坐标转OBB_YOLO格式"""
        x1, y1, x2, y2, x3, y3, x4, y4 = pixel_bbox

        # 转换为相对于图片的坐标
        img_x1 = (x1 - self.offset_x) / self.scale_factor
        img_y1 = (y1 - self.offset_y) / self.scale_factor
        img_x2 = (x2 - self.offset_x) / self.scale_factor
        img_y2 = (y2 - self.offset_y) / self.scale_factor
        img_x3 = (x3 - self.offset_x) / self.scale_factor
        img_y3 = (y3 - self.offset_y) / self.scale_factor
        img_x4 = (x4 - self.offset_x) / self.scale_factor
        img_y4 = (y4 - self.offset_y) / self.scale_factor

        # 转换为YOLO格式 (中心点坐标 + 相对宽高)
        obb_x1 = img_x1 / self.image_size[0]
        obb_y1 = img_y1 / self.image_size[1]
        obb_x2 = img_x2 / self.image_size[0]
        obb_y2 = img_y2 / self.image_size[1]
        obb_x3 = img_x3 / self.image_size[0]
        obb_y3 = img_y3 / self.image_size[1]
        obb_x4 = img_x4 / self.image_size[0]
        obb_y4 = img_y4 / self.image_size[1]

        return obb_x1, obb_y1, obb_x2, obb_y2, obb_x3, obb_y3, obb_x4, obb_y4

    def YoloToPixel(self, yolo_bbox):
        """YOLO格式转像素坐标"""
        center_x, center_y, rel_w, rel_h = yolo_bbox

        # 转换为图片坐标
        img_w = rel_w * self.image_size[0]
        img_h = rel_h * self.image_size[1]
        img_x = center_x * self.image_size[0] - img_w / 2
        img_y = center_y * self.image_size[1] - img_h / 2

        # 转换为面板坐标
        px = img_x * self.scale_factor + self.offset_x
        py = img_y * self.scale_factor + self.offset_y
        pw = img_w * self.scale_factor
        ph = img_h * self.scale_factor

        # return int(px), int(py), int(pw), int(ph)
        return round(px), round(py), round(pw), round(ph)

    def ObbYoloToPixel(self, yolo_bbox):
        """YOLO格式转像素坐标"""
        obb_x1, obb_y1, obb_x2, obb_y2, obb_x3, obb_y3, obb_x4, obb_y4 = yolo_bbox

        # 转换为图片坐标
        img_x1 = obb_x1 * self.image_size[0]
        img_y1 = obb_y1 * self.image_size[1]
        img_x2 = obb_x2 * self.image_size[0]
        img_y2 = obb_y2 * self.image_size[1]
        img_x3 = obb_x3 * self.image_size[0]
        img_y3 = obb_y3 * self.image_size[1]
        img_x4 = obb_x4 * self.image_size[0]
        img_y4 = obb_y4 * self.image_size[1]

        # 转换为面板坐标

        x1 = img_x1 * self.scale_factor + self.offset_x
        y1 = img_y1 * self.scale_factor + self.offset_y
        x2 = img_x2 * self.scale_factor + self.offset_x
        y2 = img_y2 * self.scale_factor + self.offset_y
        x3 = img_x3 * self.scale_factor + self.offset_x
        y3 = img_y3 * self.scale_factor + self.offset_y
        x4 = img_x4 * self.scale_factor + self.offset_x
        y4 = img_y4 * self.scale_factor + self.offset_y
        # return int(px), int(py), int(pw), int(ph)
        return round(x1), round(y1), round(x2), round(y2), round(x3), round(y3), round(x4), round(y4)

    def LoadAnnotations(self):
        """加载标注文件"""
        if not self.image_path:
            return

        # 根据图片路径生成标注文件路径
        base_name = os.path.splitext(os.path.basename(self.image_path))[0]
        txt_path = os.path.join(os.path.dirname(self.image_path), f"{base_name}.txt")

        self.annotations = []
        if os.path.exists(txt_path):
            try:
                with open(txt_path, 'r') as f:
                    for line in f:
                        parts = line.strip().split()
                        if self.main_frame.mode == "YOLO":
                            if len(parts) == 5:
                                class_id = int(parts[0])
                                bbox = [float(x) for x in parts[1:]]
                                self.annotations.append({
                                    'class': class_id,
                                    'bbox': bbox
                                })
                        else:
                            if len(parts) == 9:
                                class_id = int(parts[0])
                                bbox = [float(x) for x in parts[1:]]
                                self.annotations.append({
                                    'class': class_id,
                                    'bbox': bbox
                                })
            except Exception as e:
                wx.MessageBox(f"加载标注文件失败: {str(e)}", "错误", wx.OK | wx.ICON_ERROR)

    def SaveAnnotations(self):
        """保存标注文件"""
        print("SaveAnnotations")
        if not self.image_path:
            return

        base_name = os.path.splitext(os.path.basename(self.image_path))[0]
        txt_path = os.path.join(os.path.dirname(self.image_path), f"{base_name}.txt")

        try:
            if not self.annotations:
                # 如果没有标注，删除标注文件（如果存在）
                if os.path.exists(txt_path):
                    os.remove(txt_path)
            else:
                if self.main_frame.mode == "YOLO":
                    # 有标注时正常保存
                    with open(txt_path, 'w') as f:
                        for ann in self.annotations:
                            bbox = ann['bbox']
                            f.write(f"{ann['class']} {bbox[0]:.6f} {bbox[1]:.6f} {bbox[2]:.6f} {bbox[3]:.6f}\n")
                else:
                    # 有标注时正常保存
                    with open(txt_path, 'w') as f:
                        for ann in self.annotations:
                            bbox = ann['bbox']
                            f.write(
                                f"{ann['class']} {bbox[0]:.6f} {bbox[1]:.6f} {bbox[2]:.6f} {bbox[3]:.6f} {bbox[4]:.6f} {bbox[5]:.6f} {bbox[6]:.6f} {bbox[7]:.6f}\n")
        except Exception as e:
            wx.MessageBox(f"保存标注文件失败: {str(e)}", "错误", wx.OK | wx.ICON_ERROR)


class YoloLabelingTool(wx.Frame):
    def __init__(self):
        super().__init__(None, title="labelbridge", size=wx.Size(1200, 800))

        self.image_list = None
        self.current_class_label = None
        self.annotation_list = None
        self.annotation_panel = None
        self.image_files = []
        self.current_image_index = -1
        self.class_names = []  # 初始为空
        self.current_folder = None

        self.InitUI()
        self.Centre()

    def InitUI(self):
        """初始化用户界面"""
        panel = wx.Panel(self)
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # 左侧面板
        left_panel = wx.Panel(panel)
        left_sizer = wx.BoxSizer(wx.VERTICAL)

        mode_box = wx.StaticBox(left_panel, label="模式选择")
        mode_sizer = wx.StaticBoxSizer(mode_box, wx.VERTICAL)

        mode_choice = wx.Choice(left_panel, choices=["YOLO", "YOLO-OBB"])
        mode_choice.Bind(wx.EVT_CHOICE, self.on_switch_mode)

        # 设置默认选择为 "YOLO"
        mode_choice.SetSelection(0)
        self.mode = "YOLO"

        mode_sizer.Add(mode_choice, 0, wx.EXPAND | wx.ALL, 5)
        left_sizer.Insert(0, mode_sizer, 0, wx.EXPAND | wx.ALL, 5)

        # 文件操作按钮
        file_box = wx.StaticBox(left_panel, label="文件操作")
        file_sizer = wx.StaticBoxSizer(file_box, wx.VERTICAL)

        load_btn = wx.Button(left_panel, label="导入图片文件夹")
        load_btn.Bind(wx.EVT_BUTTON, self.OnLoadFolder)
        file_sizer.Add(load_btn, 0, wx.EXPAND | wx.ALL, 5)

        save_btn = wx.Button(left_panel, label="保存当前标注")
        save_btn.Bind(wx.EVT_BUTTON, self.OnSave)
        file_sizer.Add(save_btn, 0, wx.EXPAND | wx.ALL, 5)

        export_btn = wx.Button(left_panel, label="导出所有标注")
        export_btn.Bind(wx.EVT_BUTTON, self.OnExportAll)
        file_sizer.Add(export_btn, 0, wx.EXPAND | wx.ALL, 5)

        left_sizer.Add(file_sizer, 0, wx.EXPAND | wx.ALL, 5)

        # 图片列表
        list_box = wx.StaticBox(left_panel, label="图片列表")
        list_sizer = wx.StaticBoxSizer(list_box, wx.VERTICAL)

        self.image_list = wx.ListBox(left_panel)
        self.image_list.Bind(wx.EVT_LISTBOX, self.OnImageSelect)
        list_sizer.Add(self.image_list, 1, wx.EXPAND | wx.ALL, 5)

        # 导航按钮
        nav_sizer = wx.BoxSizer(wx.HORIZONTAL)
        prev_btn = wx.Button(left_panel, label="上一张")
        prev_btn.Bind(wx.EVT_BUTTON, self.OnPrevImage)
        nav_sizer.Add(prev_btn, 1, wx.EXPAND | wx.RIGHT, 2)

        next_btn = wx.Button(left_panel, label="下一张")
        next_btn.Bind(wx.EVT_BUTTON, self.OnNextImage)
        nav_sizer.Add(next_btn, 1, wx.EXPAND | wx.LEFT, 2)

        list_sizer.Add(nav_sizer, 0, wx.EXPAND | wx.ALL, 5)

        left_sizer.Add(list_sizer, 1, wx.EXPAND | wx.ALL, 5)

        # 类别选择 - 改为列表框形式
        class_box = wx.StaticBox(left_panel, label="类别管理")
        class_sizer = wx.StaticBoxSizer(class_box, wx.VERTICAL)

        # 当前选择的类别显示
        current_class_sizer = wx.BoxSizer(wx.HORIZONTAL)
        current_class_sizer.Add(wx.StaticText(left_panel, label="当前类别:"), 0,
                                wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        self.current_class_label = wx.StaticText(left_panel, label="无")
        self.current_class_label.SetForegroundColour(wx.Colour(255, 0, 0))
        current_class_sizer.Add(self.current_class_label, 1, wx.ALIGN_CENTER_VERTICAL)
        class_sizer.Add(current_class_sizer, 0, wx.EXPAND | wx.ALL, 5)

        # 类别列表
        self.class_list = wx.ListBox(left_panel, style=wx.LB_SINGLE)
        self.class_list.Bind(wx.EVT_LISTBOX, self.OnClassSelect)
        class_sizer.Add(self.class_list, 1, wx.EXPAND | wx.ALL, 5)

        # 类别操作按钮
        class_btn_sizer = wx.BoxSizer(wx.HORIZONTAL)

        add_class_btn = wx.Button(left_panel, label="添加")
        add_class_btn.Bind(wx.EVT_BUTTON, self.OnAddClass)
        class_btn_sizer.Add(add_class_btn, 1, wx.EXPAND | wx.RIGHT, 2)

        edit_class_btn = wx.Button(left_panel, label="编辑")
        edit_class_btn.Bind(wx.EVT_BUTTON, self.OnEditClass)
        class_btn_sizer.Add(edit_class_btn, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 2)

        del_class_btn = wx.Button(left_panel, label="删除")
        del_class_btn.Bind(wx.EVT_BUTTON, self.OnDeleteClass)
        class_btn_sizer.Add(del_class_btn, 1, wx.EXPAND | wx.LEFT, 2)

        class_sizer.Add(class_btn_sizer, 0, wx.EXPAND | wx.ALL, 5)

        # 排序按钮
        sort_btn_sizer = wx.BoxSizer(wx.HORIZONTAL)

        up_btn = wx.Button(left_panel, label="上移")
        up_btn.Bind(wx.EVT_BUTTON, self.OnMoveUp)
        sort_btn_sizer.Add(up_btn, 1, wx.EXPAND | wx.RIGHT, 2)

        down_btn = wx.Button(left_panel, label="下移")
        down_btn.Bind(wx.EVT_BUTTON, self.OnMoveDown)
        sort_btn_sizer.Add(down_btn, 1, wx.EXPAND | wx.LEFT, 2)

        class_sizer.Add(sort_btn_sizer, 0, wx.EXPAND | wx.ALL, 5)

        left_sizer.Add(class_sizer, 1, wx.EXPAND | wx.ALL, 5)

        # 标注列表
        ann_box = wx.StaticBox(left_panel, label="当前标注")
        ann_sizer = wx.StaticBoxSizer(ann_box, wx.VERTICAL)

        # self.annotation_list = wx.ListBox(left_panel)
        # self.annotation_list.Bind(wx.EVT_LISTBOX, self.OnAnnotationSelect)

        self.annotation_list = wx.ListCtrl(left_panel, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        self.annotation_list.InsertColumn(0, "选择", width=40)
        self.annotation_list.InsertColumn(1, "序号", width=50)
        self.annotation_list.InsertColumn(2, "类别", width=80)
        self.annotation_list.InsertColumn(3, "边界框", width=200)
        # 在初始化时
        # self.annotation_list = wx.ListCtrl(self, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        # self.annotation_list.EnableAlternateRowColours(True)
        # 启用双缓冲
        # if hasattr(self.annotation_list, 'SetDoubleBuffered'):
        #     self.annotation_list.SetDoubleBuffered(True)

        ann_sizer.Add(self.annotation_list, 1, wx.EXPAND | wx.ALL, 5)

        del_ann_btn = wx.Button(left_panel, label="删除选中标注")
        del_ann_btn.Bind(wx.EVT_BUTTON, self.OnDeleteAnnotation)
        ann_sizer.Add(del_ann_btn, 0, wx.EXPAND | wx.ALL, 5)

        left_sizer.Add(ann_sizer, 1, wx.EXPAND | wx.ALL, 5)

        left_panel.SetSizer(left_sizer)

        # 右侧图片显示区域
        self.annotation_panel = AnnotationPanel(panel, self)

        # 布局
        main_sizer.Add(left_panel, 0, wx.EXPAND | wx.ALL, 5)
        main_sizer.Add(self.annotation_panel, 1, wx.EXPAND | wx.ALL, 5)

        panel.SetSizer(main_sizer)

        # 创建菜单栏
        self.CreateMenuBar()

        # 创建状态栏
        self.CreateStatusBar()
        self.SetStatusText("就绪 - 左键拖拽创建框，单击选中，拖拽移动/调整大小")

    def CreateMenuBar(self):
        """创建菜单栏"""
        menubar = wx.MenuBar()

        # 文件菜单
        file_menu = wx.Menu()
        file_menu.Append(wx.ID_OPEN, "打开文件夹\tCtrl+O")
        file_menu.Append(wx.ID_SAVE, "保存\tCtrl+S")
        file_menu.AppendSeparator()
        file_menu.Append(wx.ID_EXIT, "退出\tCtrl+Q")

        menubar.Append(file_menu, "文件")

        # 导航菜单
        nav_menu = wx.Menu()
        nav_menu.Append(101, "上一张\tLeft")
        nav_menu.Append(102, "下一张\tRight")

        menubar.Append(nav_menu, "导航")

        # 帮助菜单
        help_menu = wx.Menu()
        help_menu.Append(wx.ID_ABOUT, "关于")

        menubar.Append(help_menu, "帮助")

        self.SetMenuBar(menubar)

        # 绑定菜单事件
        self.Bind(wx.EVT_MENU, self.OnLoadFolder, id=wx.ID_OPEN)
        self.Bind(wx.EVT_MENU, self.OnSave, id=wx.ID_SAVE)
        self.Bind(wx.EVT_MENU, self.OnExit, id=wx.ID_EXIT)
        self.Bind(wx.EVT_MENU, self.OnAbout, id=wx.ID_ABOUT)
        self.Bind(wx.EVT_MENU, self.OnPrevImage, id=101)
        self.Bind(wx.EVT_MENU, self.OnNextImage, id=102)
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        # 绑定快捷键
        accel_tbl = wx.AcceleratorTable([
            (wx.ACCEL_CTRL, ord('O'), wx.ID_OPEN),
            (wx.ACCEL_CTRL, ord('S'), wx.ID_SAVE),
            (wx.ACCEL_CTRL, ord('Q'), wx.ID_EXIT),
            (wx.ACCEL_NORMAL, wx.WXK_LEFT, 101),
            (wx.ACCEL_NORMAL, wx.WXK_RIGHT, 102),
        ])
        self.SetAcceleratorTable(accel_tbl)

    def on_switch_mode(self, event):
        """切换标注模式（YOLO / YOLO-OBB）"""
        choice = event.GetEventObject()
        mode = choice.GetStringSelection()
        self.mode = mode  # 保存当前模式

        # 可选：打印或日志输出，方便调试
        print(f"切换到模式: {self.mode}")

    def OnPrevImage(self, event):
        """上一张图片"""
        if self.image_files and self.current_image_index > 0:
            self.image_list.SetSelection(self.current_image_index - 1)
            self.OnImageSelect(None)

    def OnNextImage(self, event):
        """下一张图片"""
        if self.image_files and self.current_image_index < len(self.image_files) - 1:
            self.image_list.SetSelection(self.current_image_index + 1)
            self.OnImageSelect(None)

    def OnAnnotationSelect(self, event):
        """选择标注列表中的项目"""
        selection = self.annotation_list.GetSelection()
        if selection != wx.NOT_FOUND:
            # 在画板上选中对应的标注
            self.annotation_panel.selected_annotation_index = selection
            self.annotation_panel.Refresh()

    def LoadClassesFromFile(self, folder_path):
        """从classes.txt文件加载类别"""
        classes_path = os.path.join(folder_path, "classes.txt")
        if os.path.exists(classes_path):
            try:
                with open(classes_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    self.class_names = []
                    for i, line in enumerate(lines):
                        class_name = line.strip()
                        if class_name:
                            self.class_names.append(class_name)
                return True
            except Exception as e:
                wx.MessageBox(f"读取classes.txt失败: {str(e)}", "错误", wx.OK | wx.ICON_ERROR)
                return False
        return False

    def OnLoadFolder(self, event):
        """加载图片文件夹"""
        dlg = wx.DirDialog(self, "选择图片文件夹")
        if dlg.ShowModal() == wx.ID_OK:
            folder_path = dlg.GetPath()
            self.current_folder = folder_path
            # 先尝试加载类别文件
            self.LoadClassesFromFile(folder_path)
            self.UpdateClassList()
            self.LoadImageFolder(folder_path)
        dlg.Destroy()

    def LoadImageFolder(self, folder_path):
        """加载文件夹中的所有图片"""
        image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
        self.image_files = []

        for file_name in os.listdir(folder_path):
            if any(file_name.lower().endswith(ext) for ext in image_extensions):
                self.image_files.append(os.path.join(folder_path, file_name))

        self.image_files.sort()

        # 更新图片列表
        self.image_list.Clear()
        for img_path in self.image_files:
            self.image_list.Append(os.path.basename(img_path))

        if self.image_files:
            self.image_list.SetSelection(0)
            self.OnImageSelect(None)

        self.SetStatusText(f"加载了 {len(self.image_files)} 张图片")

    def OnImageSelect(self, event):
        """选择图片"""
        selection = self.image_list.GetSelection()
        if selection != wx.NOT_FOUND:
            self.current_image_index = selection
            image_path = self.image_files[selection]

            # 保存之前图片的标注
            if hasattr(self, 'annotation_panel') and self.annotation_panel.image_path:
                self.annotation_panel.SaveAnnotations()

            # 加载新图片
            if self.annotation_panel.LoadImage(image_path):
                self.UpdateAnnotationList()
                self.SetStatusText(
                    f"当前图片: {os.path.basename(image_path)} ({selection + 1}/{len(self.image_files)})")

    def OnSave(self, event):
        """保存当前标注"""
        if self.annotation_panel.image_path:
            self.annotation_panel.SaveAnnotations()
            self.SetStatusText("标注已保存")
        else:
            wx.MessageBox("没有图片需要保存", "提示", wx.OK | wx.ICON_INFORMATION)

    def OnExportAll(self, event):
        """导出所有标注"""
        if not self.image_files:
            wx.MessageBox("没有图片需要导出", "提示", wx.OK | wx.ICON_INFORMATION)
            return

        # 保存当前标注
        if self.annotation_panel.image_path:
            self.annotation_panel.SaveAnnotations()

        # 创建classes.txt文件
        if self.image_files and self.class_names:
            folder_path = os.path.dirname(self.image_files[0])
            classes_path = os.path.join(folder_path, "classes.txt")

            try:
                with open(classes_path, 'w', encoding='utf-8') as f:
                    for class_id in range(len(self.class_names)):
                        f.write(f"{self.class_names[class_id]}\n")

                wx.MessageBox(f"导出完成！\n类别文件: {classes_path}", "导出成功", wx.OK | wx.ICON_INFORMATION)
            except Exception as e:
                wx.MessageBox(f"导出失败: {str(e)}", "错误", wx.OK | wx.ICON_ERROR)

    def OnAddClass(self, event):
        """添加新类别"""
        dlg = wx.TextEntryDialog(self, "输入新类别名称:", "添加类别")
        if dlg.ShowModal() == wx.ID_OK:
            class_name = dlg.GetValue().strip()
            if class_name:
                # 找到下一个可用的类别ID
                max_id = len(self.class_names) if self.class_names else -1
                new_id = max_id + 1
                self.class_names.append(class_name)
                self.UpdateClassList()
                # 自动选择新添加的类别
                self.class_list.SetSelection(self.class_list.GetCount() - 1)
                self.OnClassSelect(None)
        dlg.Destroy()

    def OnEditClass(self, event):
        """编辑类别"""
        selection = self.class_list.GetSelection()
        if selection == wx.NOT_FOUND:
            wx.MessageBox("请先选择要编辑的类别", "提示", wx.OK | wx.ICON_INFORMATION)
            return

        current_name = self.class_names[selection]

        dlg = wx.TextEntryDialog(self, "编辑类别名称:", "编辑类别", current_name)
        if dlg.ShowModal() == wx.ID_OK:
            new_name = dlg.GetValue().strip()
            if new_name and new_name != current_name:
                self.class_names[selection] = new_name
                self.UpdateClassList()
                self.class_list.SetSelection(selection)
                self.OnClassSelect(None)
                # 刷新显示
                self.annotation_panel.Refresh()
                self.UpdateAnnotationList()
        dlg.Destroy()

    def UpdateAllAnnotationFiles(self, id_mapping):
        """更新所有标注文件中的类别ID"""
        if not self.image_files:
            return

        for image_path in self.image_files:
            # 生成对应的标注文件路径
            base_name = os.path.splitext(os.path.basename(image_path))[0]
            txt_path = os.path.join(os.path.dirname(image_path), f"{base_name}.txt")

            if os.path.exists(txt_path):
                try:
                    # 读取标注文件
                    annotations = []
                    with open(txt_path, 'r') as f:
                        for line in f:
                            parts = line.strip().split()
                            if len(parts) == 5:
                                class_id = int(parts[0])
                                bbox = [float(x) for x in parts[1:]]
                                # 更新类别ID
                                if class_id in id_mapping:
                                    new_class_id = id_mapping[class_id]
                                    annotations.append((new_class_id, bbox))
                    # 写回文件
                    if annotations:
                        with open(txt_path, 'w') as f:
                            for class_id, bbox in annotations:
                                f.write(f"{class_id} {bbox[0]:.6f} {bbox[1]:.6f} {bbox[2]:.6f} {bbox[3]:.6f}\n")
                    else:
                        # 如果没有标注了，删除标注文件
                        os.remove(txt_path)

                except Exception as e:
                    print(f"更新标注文件 {txt_path} 失败: {e}")

    def OnDeleteClass(self, event):
        """删除类别"""
        selection = self.class_list.GetSelection()
        if selection == wx.NOT_FOUND:
            wx.MessageBox("请先选择要删除的类别", "提示", wx.OK | wx.ICON_INFORMATION)
            return

        class_name = self.class_names[selection]

        dlg = wx.MessageDialog(self, f"确定要删除类别 '{class_name}' 吗？\n注意：这将删除所有图片中使用该类别的标注框！",
                               "确认删除", wx.YES_NO | wx.ICON_QUESTION)
        if dlg.ShowModal() == wx.ID_YES:
            # 先保存当前图片的标注
            if self.annotation_panel.image_path:
                self.annotation_panel.SaveAnnotations()

            # 删除当前图片中所有使用该类别的标注
            self.annotation_panel.annotations = [
                ann for ann in self.annotation_panel.annotations
                if ann['class'] != selection
            ]

            # 重新构建类别字典，确保ID连续
            new_class_names = []
            id_mapping = {}  # 旧ID到新ID的映射

            new_id = 0
            for old_id in range(len(self.class_names)):
                if old_id != selection:
                    new_class_names.append(self.class_names[old_id])
                    id_mapping[old_id] = new_id
                    new_id += 1

            self.class_names = new_class_names

            # 更新当前图片中所有标注的类别ID
            for ann in self.annotation_panel.annotations:
                old_class_id = ann['class']
                if old_class_id in id_mapping:
                    ann['class'] = id_mapping[old_class_id]

            # 更新所有标注文件
            self.UpdateAllAnnotationFiles(id_mapping)

            self.UpdateClassList()

            # 如果删除后没有类别了，清空当前类别选择
            if not self.class_names:
                self.current_class_label.SetLabel("无")
            else:
                # 选择合适的类别（如果删除的是最后一个，选择前一个；否则选择当前位置）
                new_selection = min(selection, self.class_list.GetCount() - 1)
                self.class_list.SetSelection(new_selection)
                self.OnClassSelect(None)

            self.annotation_panel.selected_annotation_index = -1

            # 刷新显示
            self.annotation_panel.Refresh()
            self.UpdateAnnotationList()
        dlg.Destroy()

    def OnMoveUp(self, event):
        """上移类别"""
        selection = self.class_list.GetSelection()
        if selection == wx.NOT_FOUND or selection == 0:
            return

        # 先保存当前图片的标注
        if self.annotation_panel.image_path:
            self.annotation_panel.SaveAnnotations()

        # 获取排序后的类别列表
        sorted_items = [(class_id, class_name) for class_id, class_name in enumerate(self.class_names)]

        # 交换位置
        sorted_items[selection], sorted_items[selection - 1] = sorted_items[selection - 1], sorted_items[selection]

        # 重新分配ID并更新标注
        id_mapping = self.ReassignClassIds(sorted_items)

        # 更新所有标注文件
        self.UpdateAllAnnotationFiles(id_mapping)

        self.UpdateClassList()
        self.class_list.SetSelection(selection - 1)
        self.OnClassSelect(None)

        # 刷新显示
        self.annotation_panel.Refresh()
        self.UpdateAnnotationList()

    def OnMoveDown(self, event):
        """下移类别"""
        selection = self.class_list.GetSelection()
        if selection == wx.NOT_FOUND or selection == self.class_list.GetCount() - 1:
            return

        # 先保存当前图片的标注
        if self.annotation_panel.image_path:
            self.annotation_panel.SaveAnnotations()

        # 获取排序后的类别列表
        sorted_items = [(class_id, class_name) for class_id, class_name in enumerate(self.class_names)]

        # 交换位置
        sorted_items[selection], sorted_items[selection + 1] = sorted_items[selection + 1], sorted_items[selection]

        # 重新分配ID并更新标注
        id_mapping = self.ReassignClassIds(sorted_items)

        # 更新所有标注文件
        self.UpdateAllAnnotationFiles(id_mapping)

        self.UpdateClassList()
        self.class_list.SetSelection(selection + 1)
        self.OnClassSelect(None)

        # 刷新显示
        self.annotation_panel.Refresh()
        self.UpdateAnnotationList()

    def ReassignClassIds(self, sorted_items):
        """重新分配类别ID并更新所有标注"""
        # 创建旧ID到新ID的映射
        old_to_new_mapping = {}

        # 重新构建class_names字典，使用连续的ID
        new_class_names = self.class_names
        for new_id, (old_id, class_name) in enumerate(sorted_items):
            new_class_names[new_id] = class_name
            old_to_new_mapping[old_id] = new_id

        self.class_names = new_class_names

        # 更新当前图片中所有标注的类别ID
        for ann in self.annotation_panel.annotations:
            old_class_id = ann['class']
            if old_class_id in old_to_new_mapping:
                ann['class'] = old_to_new_mapping[old_class_id]

        return old_to_new_mapping

    def OnClassSelect(self, event):
        """选择类别"""
        selection = self.class_list.GetSelection()
        if selection != wx.NOT_FOUND:
            class_name = self.class_names[selection]
            self.current_class_label.SetLabel(f"{selection}: {class_name}")
        else:
            self.current_class_label.SetLabel("无")

    def UpdateClassList(self):
        """更新类别列表显示"""
        self.class_list.Clear()
        for class_id in range(len(self.class_names)):
            self.class_list.Append(f"{class_id}: {self.class_names[class_id]}")

        # 如果有类别，默认选择第一个
        if self.class_list.GetCount() > 0:
            self.class_list.SetSelection(0)
            self.OnClassSelect(None)
        else:
            self.current_class_label.SetLabel("无")

    def GetCurrentClass(self):
        """获取当前选择的类别ID"""
        selection = self.class_list.GetSelection()
        if selection != wx.NOT_FOUND and self.class_names:
            return selection
        return 0  # 如果没有选择或没有类别，返回0

    # def UpdateAnnotationList(self):
    #     """更新标注列表显示"""
    #     self.annotation_list.Freeze()
    #     self.annotation_list.Clear()
    #     for i, ann in enumerate(self.annotation_panel.annotations):
    #         if ann['class'] < len(self.class_names):
    #             class_name = self.class_names[ann['class']]
    #         else:
    #             class_name = f"Class {ann['class']}"
    #         bbox = ann['bbox']
    #
    #         # 如果是选中的标注，添加标记
    #         prefix = "► " if i == self.annotation_panel.selected_annotation_index else "  "
    #         self.annotation_list.Append(
    #             f"{prefix}{i + 1}. {class_name} ({bbox[0]:.3f}, {bbox[1]:.3f}, {bbox[2]:.3f}, {bbox[3]:.3f})")
    #     self.annotation_list.Thaw()
    def UpdateAnnotationList(self):
        """更新标注列表显示"""
        self.annotation_list.Freeze()
        self.annotation_list.DeleteAllItems()

        for i, ann in enumerate(self.annotation_panel.annotations):
            if ann['class'] < len(self.class_names):
                class_name = self.class_names[ann['class']]
            else:
                class_name = f"Class {ann['class']}"
            bbox = ann['bbox']

            index = self.annotation_list.InsertItem(i,
                                                    "►" if i == self.annotation_panel.selected_annotation_index else "")
            self.annotation_list.SetItem(index, 1, str(i + 1))
            self.annotation_list.SetItem(index, 2, class_name)
            self.annotation_list.SetItem(index, 3, f"({bbox[0]:.3f}, {bbox[1]:.3f}, {bbox[2]:.3f}, {bbox[3]:.3f})")

        self.annotation_list.Thaw()

    def UpdateAnnotationListItem(self, index):
        """仅更新指定索引的标注列表项"""
        if index < 0 or index >= self.annotation_list.GetCount():
            return

        ann = self.annotation_panel.annotations[index]
        if ann['class'] < len(self.class_names):
            class_name = self.class_names[ann['class']]
        else:
            class_name = f"Class {ann['class']}"
        bbox = ann['bbox']
        prefix = "► " if index == self.annotation_panel.selected_annotation_index else "  "
        new_text = f"{prefix}{index + 1}. {class_name} ({bbox[0]:.3f}, {bbox[1]:.3f}, {bbox[2]:.3f}, {bbox[3]:.3f})"
        self.annotation_list.SetString(index, new_text)

    def OnDeleteAnnotation(self, event):
        """删除选中的标注"""
        selection = self.annotation_list.GetFirstSelected()  # ← 改这里
        if selection != wx.NOT_FOUND:
            del self.annotation_panel.annotations[selection]

            # 更新选中索引
            if self.annotation_panel.selected_annotation_index == selection:
                self.annotation_panel.selected_annotation_index = -1
            elif self.annotation_panel.selected_annotation_index > selection:
                self.annotation_panel.selected_annotation_index -= 1

            self.UpdateAnnotationList()
            self.annotation_panel.Refresh()

    def OnExit(self, event):
        """退出程序"""
        # 保存当前标注
        print("onexit")
        if hasattr(self, 'annotation_panel') and self.annotation_panel.image_path:
            self.annotation_panel.SaveAnnotations()
        self.Close()

    def OnClose(self, event):
        """处理窗口关闭事件"""
        # 执行你的退出逻辑
        # 保存当前标注
        print("onexit")
        if hasattr(self, 'annotation_panel') and self.annotation_panel.image_path:
            self.annotation_panel.SaveAnnotations()

        # 确保窗口真正关闭（调用 Destroy）
        self.Destroy()

    def OnAbout(self, event):
        import wx.adv
        """关于对话框"""
        info = wx.adv.AboutDialogInfo()
        info.SetName("YOLO标注工具 - 增强版")
        info.SetVersion("2.0")
        info.SetDescription(
            "用于YOLO目标检测的图片标注工具 - 增强版\n\n"
            "新功能：\n"
            "• 框选中和编辑：单击选中标注框\n"
            "• 拖拽移动：选中框后可拖拽移动位置\n"
            "• 调整大小：拖拽框的角点或边缘调整大小\n"
            "• 键盘快捷键：Delete删除，ESC取消选择\n"
            "• 导航快捷键：左右箭头键切换图片\n\n"
            "使用说明:\n"
            "1. 导入图片文件夹\n"
            "2. 添加或选择类别\n"
            "3. 左键拖拽创建新标注框\n"
            "4. 单击框选中，拖拽移动或调整大小\n"
            "5. 右键或Delete键删除标注框\n"
            "6. 保存并导出标注\n"
            "• 左键拖拽：创建新框\n"
            "• 单击框：选中标注\n"
            "• 拖拽框：移动标注\n"
            "• 拖拽角点/边：调整大小\n"
            "• 右键框：删除标注\n"
            "• Delete键：删除选中标注\n"
            "• ESC键：取消选择"
        )
        info.SetCopyright("(C) 2025")

        wx.adv.AboutBox(info)


class YoloApp(wx.App):
    def OnInit(self):
        frame = YoloLabelingTool()
        frame.Show()
        return True


if __name__ == '__main__':
    # 设置 DPI 感知
    if sys.platform.startswith('win'):
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(1)  # 1: 系统 DPI 感知, 2: 每个监视器 DPI 感知
        except Exception:
            ctypes.windll.user32.SetProcessDPIAware()  # 备用方法
    app = YoloApp()
    app.MainLoop()
