import ctypes
import math
import os
import sys

import numpy as np
import wx


class I18N:
    """International text management"""
    TEXTS = {
        'en': {
            # Window
            'app_title': 'labelbridge',
            'ready_status': 'Ready - Left-click drag to create box, click to select, drag to move/resize',

            # Mode
            'mode_select': 'Mode Selection',
            'mode_yolo': 'YOLO',
            'mode_yolo_obb': 'YOLO-OBB',

            # File Operations
            'file_ops': 'File Operations',
            'load_folder': 'Load Image Folder',
            'export_all': 'Export All Annotations',

            # Image List
            'image_list': 'Image List',
            'prev_image': 'Previous',
            'next_image': 'Next',

            # Class Management
            'class_manage': 'Class Management',
            'current_class': 'Current Class:',
            'no_class': 'None',
            'add_class': 'Add',
            'edit_class': 'Edit',
            'delete_class': 'Delete',
            'move_up': 'Move Up',
            'move_down': 'Move Down',

            # Annotation List
            'current_annotations': 'Current Annotations',
            'delete_annotation': 'Delete Selected',
            'col_select': 'Select',
            'col_index': 'Index',
            'col_class': 'Class',
            'col_bbox': 'Bounding Box',

            # Menu Bar
            'menu_file': 'File',
            'menu_open': 'Open Folder\tCtrl+O',
            'menu_save': 'Save\tCtrl+S',
            'menu_exit': 'Exit\tCtrl+Q',
            'menu_nav': 'Navigation',
            'menu_prev': 'Previous\tLeft',
            'menu_next': 'Next\tRight',
            'menu_help': 'Help',
            'menu_about': 'About',
            'menu_language': 'Language',
            'menu_english': 'English',
            'menu_chinese': '中文',

            # Dialogs
            'add_class_title': 'Add Class',
            'add_class_prompt': 'Enter new class name:',
            'edit_class_title': 'Edit Class',
            'edit_class_prompt': 'Edit class name:',
            'delete_class_title': 'Confirm Delete',
            'delete_class_msg': "Are you sure you want to delete class '{}'?\nNote: This will delete all annotation boxes using this class in all images!",
            'select_class_first': 'Please select a class first',
            'info': 'Info',
            'error': 'Error',
            'success': 'Success',

            # Messages
            'loaded_images': 'Loaded {} images',
            'current_image': 'Current image: {} ({}/{})',
            'annotation_saved': 'Annotations saved',
            'no_image_to_save': 'No image to save',
            'export_complete': 'Export complete!\nClass file: {}',
            'export_failed': 'Export failed: {}',
            'read_classes_failed': 'Failed to read classes.txt: {}',

            # About Dialog
            'about_description': (
                "labelbridge - Efficient Image Annotation Tool\n\n"
                "Supports YOLO and YOLO-OBB (rotated box) annotation modes\n\n"
                "Usage:\n"
                "1. Load Image Folder: Load images to annotate\n"
                "2. Class Management: Add, edit, sort class list\n"
                "3. Select Current Class: Choose annotation class from left list\n"
                "4. Image Annotation:\n"
                "   • Normal Rectangle (YOLO mode):\n"
                "     - Left-click drag: Create new annotation box\n"
                "     - Click box: Select annotation box\n"
                "     - Drag box: Move selected box\n"
                "     - Drag handles: Resize box\n"
                "   • Rotated Rectangle (YOLO-OBB mode):\n"
                "     - Z/X/C/V keys: Adjust crosshair angle\n"
                "     - Right-click drag: Real-time rotation adjustment\n"
                "     - Other operations same as normal box\n"
                "5. Image Navigation:\n"
                "   • Left/Right arrow keys: Switch images\n"
                "   • Image list: Direct image selection\n"
                "6. Annotation Editing:\n"
                "   • Delete key: Delete selected annotation\n"
                "   • ESC key: Cancel selection\n"
                "7. Pan & Zoom:\n"
                "   • Middle-click drag: Pan image\n"
                "   • Ctrl+Wheel: Zoom centered on mouse\n"
                "8. Save Annotations:\n"
                "   • Auto-save: Automatically saves when switching images\n"
                "   • Manual save: Click export button to save\n\n"
                "Export Format:\n"
                "• YOLO format: class_id x_center y_center width height\n"
                "• YOLO-OBB format: class_id x1 y1 x2 y2 x3 y3 x4 y4\n"
                "• Class file: Automatically generates classes.txt"
            ),
        },
        'zh': {
            # Window
            'app_title': 'labelbridge',
            'ready_status': '就绪 - 左键拖拽创建框，单击选中，拖拽移动/调整大小',

            # Mode
            'mode_select': '模式选择',
            'mode_yolo': 'YOLO',
            'mode_yolo_obb': 'YOLO-OBB',

            # File Operations
            'file_ops': '文件操作',
            'load_folder': '导入图片文件夹',
            'export_all': '导出所有标注',

            # Image List
            'image_list': '图片列表',
            'prev_image': '上一张',
            'next_image': '下一张',

            # Class Management
            'class_manage': '类别管理',
            'current_class': '当前类别:',
            'no_class': '无',
            'add_class': '添加',
            'edit_class': '编辑',
            'delete_class': '删除',
            'move_up': '上移',
            'move_down': '下移',

            # Annotation List
            'current_annotations': '当前标注',
            'delete_annotation': '删除选中标注',
            'col_select': '选择',
            'col_index': '序号',
            'col_class': '类别',
            'col_bbox': '边界框',

            # Menu Bar
            'menu_file': '文件',
            'menu_open': '打开文件夹\tCtrl+O',
            'menu_save': '保存\tCtrl+S',
            'menu_exit': '退出\tCtrl+Q',
            'menu_nav': '导航',
            'menu_prev': '上一张\tLeft',
            'menu_next': '下一张\tRight',
            'menu_help': '帮助',
            'menu_about': '关于',
            'menu_language': '语言',
            'menu_english': 'English',
            'menu_chinese': '中文',

            # Dialogs
            'add_class_title': '添加类别',
            'add_class_prompt': '输入新类别名称:',
            'edit_class_title': '编辑类别',
            'edit_class_prompt': '编辑类别名称:',
            'delete_class_title': '确认删除',
            'delete_class_msg': "确定要删除类别 '{}' 吗？\n注意：这将删除所有图片中使用该类别的标注框！",
            'select_class_first': '请先选择要编辑的类别',
            'info': '提示',
            'error': '错误',
            'success': '导出成功',

            # Messages
            'loaded_images': '加载了 {} 张图片',
            'current_image': '当前图片: {} ({}/{})',
            'annotation_saved': '标注已保存',
            'no_image_to_save': '没有图片需要保存',
            'export_complete': '导出完成！\n类别文件: {}',
            'export_failed': '导出失败: {}',
            'read_classes_failed': '读取classes.txt失败: {}',

            # About Dialog
            'about_description': (
                "labelbridge - 高效便捷的图像标注工具\n\n"
                "支持 YOLO 和 YOLO-OBB（旋转框）两种标注模式\n\n"
                "使用说明:\n"
                "1. 导入图片文件夹：加载需要标注的图片\n"
                "2. 类别管理：添加、编辑、排序类别列表\n"
                "3. 选择当前类别：在左侧列表中选择标注类别\n"
                "4. 图像标注：\n"
                "   • 普通矩形框（YOLO模式）：\n"
                "     - 左键拖拽：创建新标注框\n"
                "     - 单击框：选中标注框\n"
                "     - 拖拽框：移动选中框\n"
                "     - 拖拽手柄：调整框大小\n"
                "   • 旋转矩形框（YOLO-OBB模式）：\n"
                "     - Z/X/C/V键：调整十字辅助线角度\n"
                "     - 右键拖动：实时调整旋转角度\n"
                "     - 其他操作同普通框\n"
                "5. 图像导航：\n"
                "   • 左右箭头键：切换图片\n"
                "   • 图片列表：直接选择图片\n"
                "6. 标注编辑：\n"
                "   • Delete键：删除选中标注\n"
                "   • ESC键：取消选择\n"
                "7. 平移缩放：\n"
                "   • 中键拖动：平移图像\n"
                "   • Ctrl+滚轮：以鼠标为中心缩放\n"
                "8. 保存标注：\n"
                "   • 自动保存：切换图片时自动保存\n"
                "   • 手动保存：点击导出按钮保存\n\n"
                "导出格式：\n"
                "• YOLO格式：class_id x_center y_center width height\n"
                "• YOLO-OBB格式：class_id x1 y1 x2 y2 x3 y3 x4 y4\n"
                "• 类别文件：自动生成 classes.txt"
            ),
        }
    }

    def __init__(self, lang='en'):
        self.current_lang = lang

    def t(self, key):
        """Get translated text"""
        return self.TEXTS.get(self.current_lang, {}).get(key, key)

    def set_language(self, lang):
        """Set language"""
        if lang in self.TEXTS:
            self.current_lang = lang


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

        # === References ===
        self.parent = parent
        self.main_frame = main_frame

        # === Image State ===
        self.image = None
        self.image_path = None
        self.image_size = None
        self.buffer = wx.Bitmap(self.GetSize().width, self.GetSize().height)
        self.scaled_bitmap = None  # Cached scaled bitmap (without offset)

        # === View Transform (Pan & Zoom) ===
        self.scale_factor = 1.0
        self.offset_x = 0.0
        self.offset_y = 0.0
        self.panning = False
        self.pan_last_pos = None

        # === Annotation Data ===
        self.annotations = []
        self.selected_annotation_index = -1

        # === Drawing State (Standard YOLO) ===
        self.current_box = None
        self.drawing = False
        self.start_pos = None

        # === Editing State (Selection & Manipulation) ===
        self.editing_mode = None  # None, 'move', 'resize'
        self.resize_handle = None  # 'tl', 'tr', 'bl', 'br', 't', 'b', 'l', 'r'
        self.edit_start_pos = None
        self.original_bbox = None
        self.handle_size = 8  # Resize handle size in pixels

        # === Rotation & OBB (Oriented Bounding Box) ===
        self.rotate_mode = False  # Whether drawing rotated box
        self.current_obb_box = None
        self.cross_angle = 0.0  # Crosshair/rotation angle (degrees)
        self.rotation_step = 1.0  # Angle adjustment per key press
        self.adjusting = False  # Angle adjustment mode active

        # === Crosshair Display ===
        self.show_crosshair = True
        self.cross_pos = None  # Current mouse position (wx.Point)

        # === UI Setup ===
        self.SetBackgroundColour(wx.Colour(240, 240, 240))
        self.SetCanFocus(True)  # Enable keyboard events

        # === Event Bindings ===
        # Paint & Size
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_SIZE, self.on_size)

        # Mouse Events
        self.Bind(wx.EVT_LEFT_DOWN, self.on_left_down)
        self.Bind(wx.EVT_LEFT_UP, self.on_left_up)
        self.Bind(wx.EVT_RIGHT_DOWN, self.on_right_down)
        self.Bind(wx.EVT_RIGHT_UP, self.on_right_up)
        self.Bind(wx.EVT_MIDDLE_DOWN, self.on_middle_down)
        self.Bind(wx.EVT_MIDDLE_UP, self.on_middle_up)
        self.Bind(wx.EVT_MOTION, self.on_mouse_move)
        self.Bind(wx.EVT_MOUSEWHEEL, self.on_mouse_wheel)
        self.Bind(wx.EVT_ENTER_WINDOW, self.on_mouse_enter)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.on_mouse_leave)

        # Keyboard Events
        self.Bind(wx.EVT_KEY_DOWN, self.on_key_down)

        # === Platform-Specific Setup (Windows IME) ===
        try:
            hwnd = self.GetHandle()
            ctypes.windll.imm32.ImmAssociateContext(hwnd, 0)  # Disable IME
        except Exception:
            pass  # Ignore on non-Windows systems

    def load_image(self, image_path):
        """Load image"""
        try:
            self.image_path = image_path
            self.image = wx.Image(image_path)
            self.image_size = (self.image.GetWidth(), self.image.GetHeight())
            self._last_scaled_key = None
            self.fit_image_to_panel()
            size = self.GetClientSize()
            self.buffer = wx.Bitmap(size.width, size.height)
            self.load_annotations()
            self.selected_annotation_index = -1  # Reset selection
            self.Refresh(False)  # Refresh without clearing background to reduce flicker
            return True
        except Exception as e:
            wx.MessageBox(f"Failed to load image: {str(e)}", "Error", wx.OK | wx.ICON_ERROR)
            return False

    def fit_image_to_panel(self):
        """Adjust image size to fit panel"""
        if not self.image:
            return

        panel_size = self.GetSize()
        if panel_size.width <= 0 or panel_size.height <= 0:
            return

        # Calculate scale factors
        scale_x = panel_size.width / self.image_size[0]
        scale_y = panel_size.height / self.image_size[1]
        self.scale_factor = min(scale_x, scale_y)

        # Calculate offset to center image
        scaled_width = self.image_size[0] * self.scale_factor
        scaled_height = self.image_size[1] * self.scale_factor
        self.offset_x = (panel_size.width - scaled_width) // 2
        self.offset_y = (panel_size.height - scaled_height) // 2
        # print("fit_image_to_panel")

        # self.clamp_offset()

        # Recreate background image cache
        if self.image:
            self.create_background_bitmap()

    def create_background_bitmap(self):
        """Generate and cache scaled bitmap based on self.scale_factor (without offset)."""
        if not self.image:
            self.scaled_bitmap = None
            return

        pw, ph = self.GetClientSize().width, self.GetClientSize().height

        # Original image pixel size
        img_w, img_h = self.image.GetWidth(), self.image.GetHeight()

        # Full scaled image dimensions (pixels)
        full_scaled_w = round(img_w * self.scale_factor)
        full_scaled_h = round(img_h * self.scale_factor)

        # Adjustable threshold: if full scaled image is not much larger than panel, scale entire image directly.
        # ratio = allowed / panel; e.g., 1.2 means if scaled width/height <= 1.2 * panel size, scale entire image.
        full_image_ratio = getattr(self, "full_image_ratio", 2)

        try:
            key = ("full", self.scale_factor, img_w, img_h)

            if getattr(self, "_last_scaled_key", None) == key and getattr(self, "scaled_bitmap", None):
                return

            # When full scaled image is not much larger than panel -> scale entire image
            if full_scaled_w <= round(pw * full_image_ratio) and full_scaled_h <= round(ph * full_image_ratio):
                # Target size at least 1
                tw = max(1, full_scaled_w)
                th = max(1, full_scaled_h)
                # Scale entire image directly
                scaled_img = self.image.Scale(tw, th, wx.IMAGE_QUALITY_NEAREST)
                self.scaled_bitmap = wx.Bitmap(scaled_img)
                self._last_scaled_key = key
                self._scaled_is_full = True
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
            # Scale this region to screen pixel size (approximately vis_w * scale_factor)
            target_w = min(round(self.image.GetWidth() * self.scale_factor), round(pw), round(pw - self.offset_x),
                           round(self.image.GetWidth() * self.scale_factor + self.offset_x))
            target_h = min(round(self.image.GetHeight() * self.scale_factor), round(ph), round(ph - self.offset_y),
                           round(self.image.GetHeight() * self.scale_factor + self.offset_y))

            # Use nearest neighbor for pixelated effect and better performance
            scaled_sub = sub.Scale(target_w, target_h, wx.IMAGE_QUALITY_NEAREST)
            self.scaled_bitmap = wx.Bitmap(scaled_sub)
            self._last_scaled_key = key
            self._scaled_is_full = False

        except Exception as e:
            print("create_background_bitmap scaling error:", e)
            self.scaled_bitmap = None
            self.scaled_bitmap = None
            self._last_scaled_key = None
            self._scaled_is_full = False

    def clamp_position_to_image(self, pos):
        """Clamp position to image area"""
        if not self.image:
            return pos

        # Calculate image boundaries in panel
        scaled_width = self.image_size[0] * self.scale_factor
        scaled_height = self.image_size[1] * self.scale_factor

        min_x = int(self.offset_x)
        max_x = int(self.offset_x + scaled_width)
        min_y = int(self.offset_y)
        max_y = int(self.offset_y + scaled_height)

        # Clamp position
        clamped_x = max(min_x, min(max_x, pos.x))
        clamped_y = max(min_y, min(max_y, pos.y))

        return wx.Point(clamped_x, clamped_y)

    def on_size(self, event):
        """Panel resize event"""
        if self.image:
            size = self.GetClientSize()
            self.buffer = wx.Bitmap(size.width, size.height)
            self.fit_image_to_panel()
            self.Refresh(False)  # Refresh without clearing background to reduce flicker
        event.Skip()

    def draw_to_buffer(self):
        """rraw content to memory bitmap"""
        dc = wx.MemoryDC(self.buffer)  # Draw to cached bitmap
        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        dc.Clear()

        if getattr(self, "scaled_bitmap", None):
            if getattr(self, "_scaled_is_full", False):
                # Full image mode
                dc.DrawBitmap(self.scaled_bitmap, round(self.offset_x), round(self.offset_y))
            else:
                # Partial crop mode
                x = max(0, round(self.offset_x))
                y = max(0, round(self.offset_y))
                dc.DrawBitmap(self.scaled_bitmap, x, y)
            # # Draw cached background image
            # dc.DrawBitmap(self.background_bitmap, 0, 0)

            # Draw all annotation boxes
            self.draw_all_annotations(dc)

            # Draw currently drawing box
            if self.current_box and self.drawing and self.main_frame.mode == "YOLO":
                current_class = self.main_frame.get_current_class()
                rgb_color = colors(current_class)
                color = wx.Colour(rgb_color[0], rgb_color[1], rgb_color[2])
                self.draw_box(dc, self.current_box, color, 2)

            elif self.current_obb_box and self.drawing and self.main_frame.mode == "YOLO-OBB":
                current_class = self.main_frame.get_current_class()
                rgb_color = colors(current_class)
                color = wx.Colour(rgb_color[0], rgb_color[1], rgb_color[2])
                self.draw_obb_box(dc, self.current_obb_box, color, 2)

            # Draw crosshair (on top of other content)
            if self.show_crosshair and self.cross_pos:
                # Mouse crosshair (color: white)
                self.draw_crosshair(dc, self.cross_pos, wx.Colour(255, 255, 255), style=wx.PENSTYLE_DOT,
                                    angle_deg=self.cross_angle)
        else:
            dc.Clear()
            pass

        dc.SelectObject(wx.NullBitmap)  # Unbind

    def on_paint(self, event):
        # Display cached bitmap
        # tracer = VizTracer()
        # tracer.start()
        if getattr(self, "panning", False):
            self.create_background_bitmap()
        self.draw_to_buffer()
        dc = wx.PaintDC(self)
        dc.DrawBitmap(self.buffer, 0, 0)
        # print("on_paint")
        # tracer.stop()
        # tracer.save()

    def draw_all_annotations(self, dc):
        """Draw all annotation boxes"""
        for i, ann in enumerate(self.annotations):
            if self.main_frame.mode == "YOLO":
                # Convert coordinates
                x, y, w, h = self.yolo_to_pixel(ann['bbox'])
                box = (x, y, x + w, y + h)

                # Draw class label
                class_name = self.main_frame.class_names[ann['class']] if ann['class'] < len(
                    self.main_frame.class_names) else f"Class {ann['class']}"
                rgb_color = colors(ann['class'])
                color = wx.Colour(rgb_color[0], rgb_color[1], rgb_color[2])

                # Selected box uses different color
                if i == self.selected_annotation_index:
                    # Selected box: brighter color and thicker line
                    selected_color = wx.Colour(
                        min(255, color.Red() + 50),
                        min(255, color.Green() + 50),
                        min(255, color.Blue() + 50)
                    )
                    # self.draw_box(dc, box, selected_color, 3)

                    self.draw_box(dc, box, selected_color, 3)
                    # Draw resize handles
                    self.draw_resize_handles(dc, box, selected_color)
                else:
                    self.draw_box(dc, box, color, 2)
                dc.SetTextForeground(color)
                dc.DrawText(class_name, x, max(0, y - 20))
            else:
                # Convert coordinates
                obb_box = self.obb_yolo_to_pixel(ann['bbox'])
                # box = (x, y, x + w, y + h)

                # Draw class label
                class_name = self.main_frame.class_names[ann['class']] if ann['class'] < len(
                    self.main_frame.class_names) else f"Class {ann['class']}"
                rgb_color = colors(ann['class'])
                color = wx.Colour(rgb_color[0], rgb_color[1], rgb_color[2])

                # Selected box uses different color
                if i == self.selected_annotation_index:
                    # Selected box: brighter color and thicker line
                    selected_color = wx.Colour(
                        min(255, color.Red() + 50),
                        min(255, color.Green() + 50),
                        min(255, color.Blue() + 50)
                    )
                    # self.draw_box(dc, box, selected_color, 3)

                    self.draw_obb_box(dc, obb_box, selected_color, 3)

                    # Draw resize handles
                    self.draw_obb_resize_handles(dc, obb_box, selected_color)
                else:
                    self.draw_obb_box(dc, obb_box, color, 2)

                dc.SetTextForeground(color)
                dc.DrawText(class_name, obb_box[0], max(0, obb_box[1] - 20))

    def draw_box(self, dc, box, color, width):
        """Draw rectangle box"""
        gc = wx.GraphicsContext.Create(dc)
        gc.SetPen(wx.Pen(color, width))
        gc.SetBrush(wx.Brush(wx.Colour(color[0], color[1], color[2], 50)))
        x1, y1, x2, y2 = box
        gc.DrawRectangle(x1, y1, x2 - x1, y2 - y1)

    def rectangle_corners_from_diagonal(self, p1, p2, theta_deg):
        """
        Given diagonal points p1, p2 (tuple/list/np.array length 2) and rectangle rotation angle theta_deg (degrees)
        Return rectangle four vertices (clockwise or counterclockwise order).
        Explanation: angle theta is the rotation angle of one rectangle side (width vector) relative to x-axis.
        Calculation approach:
        - Let unit vector u represent rectangle width direction (angle theta), v be its perpendicular direction.
        - Diagonal vector d = p2 - p1, can be expressed as d = w * u + h * v,
            so w = d·u, h = d·v (take absolute value as side lengths).
        - Center O = (p1 + p2) / 2, four corners are O ± (w/2) * u ± (h/2) * v.
        """
        p1 = np.asarray(p1, dtype=float)
        p2 = np.asarray(p2, dtype=float)
        theta = np.deg2rad(theta_deg)
        u = np.array([np.cos(theta), np.sin(theta)])  # Rectangle width direction unit vector
        v = np.array([-np.sin(theta), np.cos(theta)])  # Rectangle height direction unit vector (u rotated 90° CCW)
        d = p2 - p1
        w = abs(np.dot(d, u))
        h = abs(np.dot(d, v))
        O = (p1 + p2) / 2.0

        # Generate four corners (unsorted)
        corners = []
        for sx in [1, -1]:
            for sy in [1, -1]:
                corner = O + (sx * w / 2.0) * u + (sy * h / 2.0) * v
                corners.append(corner)
        corners = np.array(corners)

        # Sort corners by polar angle to form polygon (clockwise or CCW)
        centroid = corners.mean(axis=0)
        angles = np.arctan2(corners[:, 1] - centroid[1], corners[:, 0] - centroid[0])
        order = np.argsort(angles)
        corners = corners[order]
        return corners

    def draw_obb_box(self, dc, box, color, width=2):
        """Draw rotated rectangle from start_pos to end_pos"""
        gc = wx.GraphicsContext.Create(dc)
        gc.SetPen(wx.Pen(color, width))
        gc.SetBrush(wx.Brush(wx.Colour(color[0], color[1], color[2], 50)))
        # Prepare polygon points
        points = [wx.Point2D(x, y) for x, y in zip(box[::2], box[1::2])]
        # Draw polygon
        gc.DrawLines(points + [points[0]])  # Add first point to end to close shape

    def draw_resize_handles(self, dc, box, color):
        """Draw resize handles"""
        x1, y1, x2, y2 = box
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2

        # Set handle style
        dc.SetPen(wx.Pen(color, 1))
        dc.SetBrush(wx.Brush(wx.Colour(255, 255, 255)))

        half_size = self.handle_size // 2

        # Eight resize handle positions
        handles = [
            (x1 - half_size, y1 - half_size),  # Top-left (tl)
            (x2 - half_size, y1 - half_size),  # Top-right (tr)
            (x1 - half_size, y2 - half_size),  # Bottom-left (bl)
            (x2 - half_size, y2 - half_size),  # Bottom-right (br)
            (cx - half_size, y1 - half_size),  # Top-center (t)
            (cx - half_size, y2 - half_size),  # Bottom-center (b)
            (x1 - half_size, cy - half_size),  # Left-center (l)
            (x2 - half_size, cy - half_size),  # Right-center (r)
        ]

        for hx, hy in handles:
            dc.DrawRectangle(hx, hy, self.handle_size, self.handle_size)

    def draw_obb_resize_handles(self, dc, obb_box, color):
        """Draw rotation adjustment handles for oriented bounding boxes (automatically get angle)"""

        gdc = wx.GCDC(dc)
        pen = wx.Pen(wx.Colour(color[0], color[1], color[2]), 1, wx.PENSTYLE_SOLID)
        brush = wx.Brush(wx.Colour(255, 255, 255, 255))
        gdc.SetPen(pen)
        gdc.SetBrush(brush)

        half_handle_size = self.handle_size / 2

        # Calculate OBB rotation angle from top-left -> top-right
        dx = obb_box[2] - obb_box[0]
        dy = obb_box[3] - obb_box[1]
        theta = math.atan2(dy, dx)  # Radians

        # Calculate 8 handle positions
        handle_positions = [
            (obb_box[0], obb_box[1]),  # Top-left
            (obb_box[2], obb_box[3]),  # Top-right
            (obb_box[4], obb_box[5]),  # Bottom-right
            (obb_box[6], obb_box[7]),  # Bottom-left
            ((obb_box[0] + obb_box[2]) / 2, (obb_box[1] + obb_box[3]) / 2),  # Top-center
            ((obb_box[4] + obb_box[6]) / 2, (obb_box[5] + obb_box[7]) / 2),  # Bottom-center
            ((obb_box[0] + obb_box[6]) / 2, (obb_box[1] + obb_box[7]) / 2),  # Left-center
            ((obb_box[2] + obb_box[4]) / 2, (obb_box[3] + obb_box[5]) / 2),  # Right-center
        ]

        # Draw each rotation handle
        for hx, hy in handle_positions:
            # Handle local four points (unrotated)
            pts = [
                (-half_handle_size, -half_handle_size),
                (half_handle_size, -half_handle_size),
                (half_handle_size, half_handle_size),
                (-half_handle_size, half_handle_size),
            ]

            # Rotate around (hx, hy)
            rotated_pts = []
            for x, y in pts:
                rx = hx + x * math.cos(theta) - y * math.sin(theta)
                ry = hy + x * math.sin(theta) + y * math.cos(theta)
                rotated_pts.append((rx, ry))
            rotated_pts = [(int(x), int(y)) for x, y in rotated_pts]

            gdc.DrawPolygon(rotated_pts)

    def _line_rect_intersections(self, px, py, dx, dy, x_min, y_min, x_max, y_max, eps=1e-9):
        """Return intersection points of line (px,py) + t*(dx,dy) with rectangle boundaries.
        Result is [(x,y,t), ...], where t is parameter value (for sorting).
        """
        pts = []

        # Intersect with vertical edges x = x_min / x_max (if dx != 0)
        if abs(dx) > eps:
            for x_edge in (x_min, x_max):
                t = (x_edge - px) / dx
                y = py + t * dy
                if y_min - eps <= y <= y_max + eps:
                    pts.append((x_edge, y, t))

        # Intersect with horizontal edges y = y_min / y_max (if dy != 0)
        if abs(dy) > eps:
            for y_edge in (y_min, y_max):
                t = (y_edge - py) / dy
                x = px + t * dx
                if x_min - eps <= x <= x_max + eps:
                    pts.append((x, y_edge, t))

        # Deduplicate (corner points might appear twice), sort by t
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
        Return endpoints of two perpendicular line segments:
        ((ax1,ay1),(ax2,ay2)), ((bx1,by1),(bx2,by2))
        First pair is line segment with angle angle_deg, second pair is perpendicular (angle_deg+90°).
        Intersection point (px,py) must be inside rectangle and endpoints on rectangle edges.
        """
        # Normalize rectangle (support any boundary input order)
        x_min = min(img_x1, img_x2)
        x_max = max(img_x1, img_x2)
        y_min = min(img_y1, img_y2)
        y_max = max(img_y1, img_y2)

        # Check if px,py is within rectangle (including edges)
        if not (x_min <= px <= x_max and y_min <= py <= y_max):
            raise ValueError("Intersection point (px,py) must be within image boundaries")

        def endpoints_for_angle(angle_deg):
            theta = math.radians(angle_deg)
            dx = math.cos(theta)
            dy = math.sin(theta)
            inters = self._line_rect_intersections(px, py, dx, dy, x_min, y_min, x_max, y_max)
            # For infinite line intersecting rectangle, should get 2 distinct intersection points
            if len(inters) < 2:
                # Handle rare numerical/degenerate cases, try to return existing points
                if len(inters) == 1:
                    x, y, t = inters[0]
                    return (x, y), (x, y)
                raise RuntimeError(
                    f"Failed to find enough intersection points (angle={angle_deg}), intersection count={len(inters)}")
            # Take two points with minimum and maximum t (corresponding to line ends)
            p1 = (inters[0][0], inters[0][1])
            p2 = (inters[-1][0], inters[-1][1])
            return p1, p2

        a1, a2 = endpoints_for_angle(angle_deg)
        b1, b2 = endpoints_for_angle(angle_deg + 90.0)

        return (a1, a2), (b1, b2)

    def draw_crosshair(
            self, dc, pos,
            color=wx.Colour(200, 200, 200),
            style=wx.PENSTYLE_DOT,
            angle_deg=0.0
    ):
        """
        Draw crosshair in image area (supports rotation).
        Uses GraphicsContext for smooth anti-aliasing.
        """
        if not self.image:
            return

        # Calculate image display boundaries (panel coordinates)
        img_x1 = int(self.offset_x)
        img_y1 = int(self.offset_y)
        img_x2 = int(self.offset_x + self.image_size[0] * self.scale_factor)
        img_y2 = int(self.offset_y + self.image_size[1] * self.scale_factor)

        # Clamp pos to image area
        px = max(img_x1, min(img_x2, pos.x))
        py = max(img_y1, min(img_y2, pos.y))

        (a1, a2), (b1, b2) = self.cross_segment_endpoints(
            img_x1, img_y1, img_x2, img_y2, px, py, angle_deg
        )

        # === Create GraphicsContext ===
        gc = wx.GraphicsContext.Create(dc)
        gc.SetAntialiasMode(wx.ANTIALIAS_DEFAULT)

        # =============================
        # 1️⃣ Center point: small dot
        # =============================
        dot_radius = 2  # Small dot radius
        blank_radius = 15  # Radius without line

        brush = wx.Brush(color)
        gc.SetBrush(brush)
        gc.SetPen(wx.NullPen)  # No border needed

        gc.DrawEllipse(px - dot_radius, py - dot_radius,
                       dot_radius * 2, dot_radius * 2)

        # =============================
        # 2️⃣ Crosshair with blank area
        # =============================
        # Main line pen
        pen_info = wx.GraphicsPenInfo(color).Width(2)
        gc.SetPen(gc.CreatePen(pen_info))

        # --- Calculate trimmed segments ---
        def trim_segment(p1, p2):
            """Cut out parts of segment p1→p2 within blank_radius distance from center"""
            import math

            x1, y1 = p1
            x2, y2 = p2

            # Vector
            vx = x2 - x1
            vy = y2 - y1

            length = math.hypot(vx, vy)
            if length == 0:
                return None

            # Unit vector
            ux = vx / length
            uy = vy / length

            # Vector from p1 to center
            wx_ = px - x1
            wy_ = py - y1

            # Projection length (position of p1->center projection on p1->p2, parameter t)
            t_center = wx_ * ux + wy_ * uy

            # Cut out [t_center - R, t_center + R]
            t1 = t_center - blank_radius
            t2 = t_center + blank_radius

            # Entire segment within blank area
            if t2 <= 0 or t1 >= length:
                return [(x1, y1), (x2, y2)]  # No trimming needed

            segments = []

            # Left segment preserved (p1 → t1)
            if t1 > 0:
                segments.append(((x1, y1), (x1 + ux * t1, y1 + uy * t1)))

            # Right segment preserved (t2 → p2)
            if t2 < length:
                segments.append(((x1 + ux * t2, y1 + uy * t2), (x2, y2)))

            return segments

        # Process two line segments
        for seg in trim_segment(a1, a2) or []:
            gc.StrokeLine(seg[0][0], seg[0][1], seg[1][0], seg[1][1])

        for seg in trim_segment(b1, b2) or []:
            gc.StrokeLine(seg[0][0], seg[0][1], seg[1][0], seg[1][1])

        # =============================
        # 3️⃣ OBB adjustment point
        # =============================
        if self.main_frame.mode == "YOLO-OBB" and getattr(self, "adjusting", False):
            self.draw_anchor(gc, self.adjust_last_pos[0], self.adjust_last_pos[1])

    def draw_anchor(self, gc, x, y, outer_radius=6, inner_radius=3):
        """
        Draw white anchor point using wx.GraphicsContext (outer white circle, inner black)
        """
        # Anti-aliasing
        gc.SetAntialiasMode(wx.ANTIALIAS_DEFAULT)

        # ---- Outer circle (white) ----
        outer_brush = gc.CreateBrush(wx.Brush(wx.Colour(255, 255, 255)))  # white
        outer_pen = gc.CreatePen(wx.Pen(wx.Colour(255, 255, 255), 1))

        gc.SetBrush(outer_brush)
        gc.SetPen(outer_pen)
        gc.DrawEllipse(x - outer_radius, y - outer_radius,
                       outer_radius * 2, outer_radius * 2)

        # ---- Inner circle (black) ----
        inner_brush = gc.CreateBrush(wx.Brush(wx.Colour(0, 0, 0)))
        inner_pen = gc.CreatePen(wx.Pen(wx.Colour(0, 0, 0), 1))

        gc.SetBrush(inner_brush)
        gc.SetPen(inner_pen)
        gc.DrawEllipse(x - inner_radius, y - inner_radius,
                       inner_radius * 2, inner_radius * 2)

    def get_resize_handle(self, pos, box):
        """Get resize handle at mouse position"""
        x1, y1, x2, y2 = box
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2

        half_size = self.handle_size // 2

        # Check each handle
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

    def get_obb_resize_handle(self, pos, obb_box):
        """Check if mouse clicked on OBB resize handle"""
        # Calculate 8 handle center points
        handle_positions = {
            'tl': (obb_box[0], obb_box[1]),  # Top-left
            'tr': (obb_box[2], obb_box[3]),  # Top-right
            'br': (obb_box[4], obb_box[5]),  # Bottom-right
            'bl': (obb_box[6], obb_box[7]),  # Bottom-left
            't': ((obb_box[0] + obb_box[2]) / 2, (obb_box[1] + obb_box[3]) / 2),  # Top-center
            'r': ((obb_box[2] + obb_box[4]) / 2, (obb_box[3] + obb_box[5]) / 2),  # Right-center
            'b': ((obb_box[4] + obb_box[6]) / 2, (obb_box[5] + obb_box[7]) / 2),  # Bottom-center
            'l': ((obb_box[6] + obb_box[0]) / 2, (obb_box[7] + obb_box[1]) / 2),  # Left-center
        }

        # Mouse click position
        px, py = pos.x, pos.y
        threshold = self.handle_size * 1.2  # Detection radius (adjustable)
        min_dist = float('inf')
        selected_handle = None

        # Iterate through all handles, calculate distance
        for name, (hx, hy) in handle_positions.items():
            dist = math.hypot(px - hx, py - hy)
            if dist < threshold and dist < min_dist:
                min_dist = dist
                selected_handle = name

        return selected_handle  # Returns None if not hit

    def get_annotation_at(self, pos):
        """Get annotation index at specified position"""
        if self.main_frame.mode == "YOLO":
            for i, ann in enumerate(self.annotations):
                x, y, w, h = self.yolo_to_pixel(ann['bbox'])
                if x <= pos.x <= x + w and y <= pos.y <= y + h:
                    return i
        else:
            def point_in_polygon(px, py, poly):
                """Ray casting algorithm to check if point is inside polygon, poly is [(x1,y1), (x2,y2), ...]"""
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
                coords = self.obb_yolo_to_pixel(ann['bbox'])  # Returns (x1, y1, x2, y2, x3, y3, x4, y4)
                polygon = [(coords[j], coords[j + 1]) for j in range(0, 8, 2)]
                if point_in_polygon(pos.x, pos.y, polygon):
                    return i
        return -1

    def on_left_down(self, event):
        """Mouse left button down"""
        if not self.image:
            return

        self.SetFocus()  # Get focus to receive keyboard events
        pos = event.GetPosition()

        if not self.is_in_image_area(pos):
            return

        # Check if clicked on selected annotation's resize handle
        if self.main_frame.mode == "YOLO":
            if self.selected_annotation_index >= 0:
                ann = self.annotations[self.selected_annotation_index]
                x, y, w, h = self.yolo_to_pixel(ann['bbox'])
                box = (x, y, x + w, y + h)

                handle = self.get_resize_handle(pos, box)
                if handle:
                    # Start resizing
                    self.editing_mode = 'resize'
                    self.resize_handle = handle
                    self.edit_start_pos = pos
                    self.original_bbox = ann['bbox'][:]
                    return
        else:  # self.main_frame.mode == "YOLO_OBB":

            if self.selected_annotation_index >= 0:
                ann = self.annotations[self.selected_annotation_index]
                handle = self.get_obb_resize_handle(pos, self.obb_yolo_to_pixel(ann['bbox']))
                if handle:
                    self.editing_mode = 'resize'
                    self.resize_handle = handle
                    self.edit_start_pos = pos
                    self.original_obb = ann['bbox'][:]
                    return

        # Check if clicked on annotation box
        clicked_index = self.get_annotation_at(pos)

        if clicked_index >= 0:
            # Clicked selected box, start moving
            self.editing_mode = 'move'
            self.edit_start_pos = pos
            self.original_bbox = self.annotations[clicked_index]['bbox'][:]
            self.selected_annotation_index = clicked_index
            self.Refresh(False)  # Refresh without clearing background to reduce flicker
        else:
            # Deselect, start drawing new box
            self.selected_annotation_index = -1

            # Check if any class is available
            if not self.main_frame.class_names:
                # Prompt to create new class
                dlg = wx.MessageDialog(self, "No classes available. Would you like to add a new class?", "Info",
                                       wx.YES_NO | wx.ICON_QUESTION)
                if dlg.ShowModal() == wx.ID_YES:
                    self.main_frame.on_add_class(None)
                dlg.Destroy()
                return

            self.drawing = True
            # Clamp start position to image area
            clamped_pos = self.clamp_position_to_image(pos)
            self.start_pos = clamped_pos
            self.current_box = (clamped_pos.x, clamped_pos.y, clamped_pos.x, clamped_pos.y)
            self.current_obb_box = (clamped_pos.x, clamped_pos.y, clamped_pos.x, clamped_pos.y,
                                    clamped_pos.x, clamped_pos.y, clamped_pos.x, clamped_pos.y)
            self.Refresh(False)  # Refresh without clearing background to reduce flicker

    def on_left_up(self, event):
        """Mouse left button release"""
        pos = event.GetPosition()

        if self.editing_mode == 'move':
            # End moving
            self.editing_mode = None
            self.edit_start_pos = None
            self.original_bbox = None

        elif self.editing_mode == 'resize':
            # End resizing
            self.editing_mode = None
            self.resize_handle = None
            self.edit_start_pos = None
            self.original_bbox = None

        elif self.drawing:
            # End drawing box
            self.drawing = False
            if self.current_box:
                x1, y1, x2, y2 = self.current_box

                # Ensure box has reasonable size
                if abs(x2 - x1) > 5 and abs(y2 - y1) > 5:
                    # Convert to YOLO format and add annotation
                    yolo_bbox = self.pixel_to_yolo((min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1)))
                    obb_yolo_bbox = self.pixel_to_obb_yolo(self.current_obb_box)

                    # Get currently selected class
                    current_class = self.main_frame.get_current_class()

                    if self.main_frame.mode == "YOLO-OBB":
                        annotation = {
                            'class': current_class,
                            'bbox': obb_yolo_bbox,
                            # 'angle': self.cross_angle   # Add angle information
                        }
                    else:
                        annotation = {
                            'class': current_class,
                            'bbox': yolo_bbox
                        }
                    self.annotations.append(annotation)
                    self.main_frame.update_annotation_list()

                    # Select newly created annotation
                    self.selected_annotation_index = len(self.annotations) - 1

                self.current_box = None
            self.Refresh(False)  # Refresh without clearing background to reduce flicker

    def clamp_offset(self):
        """
        Ensure image doesn't get dragged completely out of panel view:
        - If image is smaller than panel, keep it centered
        - If image is larger than panel, allow dragging but keep at least one pixel visible
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

    def on_mouse_wheel(self, event):
        """Ctrl + wheel zoom (centered on mouse)"""
        if not self.image:
            return

        if not event.ControlDown():
            return  # Can change to page scrolling when Ctrl not pressed

        rotation = event.GetWheelRotation()
        # Simple approach: positive/negative determines zoom in/out
        zoom_step = 1.1 if rotation > 0 else (1.0 / 1.1)

        old_scale = self.scale_factor
        new_scale = max(0.05, min(20.0, old_scale * zoom_step))
        if abs(new_scale - old_scale) < 1e-9:
            return

        mouse = event.GetPosition()  # Mouse position in panel coordinates
        ratio = new_scale / old_scale

        # Keep mouse position as zoom center
        self.offset_x = mouse.x - (mouse.x - self.offset_x) * ratio
        self.offset_y = mouse.y - (mouse.y - self.offset_y) * ratio

        self.scale_factor = new_scale
        self.create_background_bitmap()
        self.clamp_offset()
        self.Refresh(False)

    def on_middle_down(self, event):
        """Start panning"""
        if not self.image:
            return
        self.panning = True
        self.pan_last_pos = event.GetPosition()
        try:
            self.CaptureMouse()
        except Exception:
            pass
        # Change cursor to hand
        self.SetCursor(wx.Cursor(wx.CURSOR_SIZING))

    def on_middle_up(self, event):
        """End panning"""
        if self.panning:
            self.panning = False
            self.pan_last_pos = None
            try:
                if self.HasCapture():
                    self.ReleaseMouse()
            except Exception:
                pass
            # Restore default cursor
            self.SetCursor(wx.NullCursor)
            # Final clamp and refresh
            self.clamp_offset()
            self.Refresh(False)

    def on_mouse_leave(self, event):
        """Prevent mouse capture from getting stuck (release when leaving)"""
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

    def on_mouse_move(self, event):
        """Mouse movement"""
        pos = event.GetPosition()

        if getattr(self, "panning", False):
            pos = event.GetPosition()
            dx = pos.x - self.pan_last_pos.x
            dy = pos.y - self.pan_last_pos.y
            # Directly move offset (float)
            self.offset_x += dx
            self.offset_y += dy
            self.pan_last_pos = pos
            # No need to rebuild scaled_bitmap, just refresh drawing position
            # self.clamp_offset()
            self.Refresh(False)

        if self.main_frame.mode == "YOLO-OBB" and getattr(self, "adjusting", False):
            pos = event.GetPosition()
            self.cross_angle = math.degrees(
                math.atan2(pos.y - self.adjust_last_pos.y, pos.x - self.adjust_last_pos.x))  # Note order is (y, x)

        # Update cross_pos on every move (but clamp to image area)
        if self.image and self.is_in_image_area(pos):
            self.cross_pos = self.clamp_position_to_image(pos)
        else:
            self.cross_pos = None

        if self.editing_mode == 'move' and self.selected_annotation_index >= 0:

            if self.main_frame.mode == "YOLO":
                # Move annotation box
                dx = pos.x - self.edit_start_pos.x
                dy = pos.y - self.edit_start_pos.y

                # Convert pixel offset to YOLO format offset
                dx_yolo = dx / (self.scale_factor * self.image_size[0])
                dy_yolo = dy / (self.scale_factor * self.image_size[1])

                # Update annotation position
                new_bbox = list(self.original_bbox)
                new_bbox[0] += dx_yolo  # Center point x
                new_bbox[1] += dy_yolo  # Center point y

                # Ensure annotation doesn't go beyond image boundaries
                half_w = new_bbox[2] / 2
                half_h = new_bbox[3] / 2
                new_bbox[0] = max(half_w, min(1 - half_w, new_bbox[0]))
                new_bbox[1] = max(half_h, min(1 - half_h, new_bbox[1]))

                self.annotations[self.selected_annotation_index]['bbox'] = new_bbox
                self.main_frame.update_annotation_list()

                self.Refresh(False)  # Refresh without clearing background to reduce flicker
            else:
                # OBB mode: Move entire quadrilateral, but restrict movement if it would go out of bounds
                dx = pos.x - self.edit_start_pos.x
                dy = pos.y - self.edit_start_pos.y

                # Convert pixel offset to normalized coordinate offset (relative to image width/height)
                dx_norm = dx / (self.scale_factor * self.image_size[0])
                dy_norm = dy / (self.scale_factor * self.image_size[1])

                # original_bbox assumed to be normalized 8 coordinates [x1,y1,x2,y2,...]
                orig = list(self.original_bbox)  # Copy to avoid modifying original data

                # Calculate current bbox min/max (normalized coordinates)
                xs = [orig[i] for i in range(0, 8, 2)]
                ys = [orig[i + 1] for i in range(0, 8, 2)]
                min_x, max_x = min(xs), max(xs)
                min_y, max_y = min(ys), max(ys)

                # Allowed dx_norm range: ensure all points stay in [0,1]
                # e.g., right movement limited to dx_norm <= 1 - max_x; left limited to dx_norm >= -min_x
                allowed_dx_min = -min_x
                allowed_dx_max = 1.0 - max_x
                # Clamp requested dx_norm to allowed range
                dx_norm_clamped = max(allowed_dx_min, min(allowed_dx_max, dx_norm))

                # Similarly handle dy_norm
                allowed_dy_min = -min_y
                allowed_dy_max = 1.0 - max_y
                dy_norm_clamped = max(allowed_dy_min, min(allowed_dy_max, dy_norm))

                # Apply allowed offset to all four vertices (preserve shape)
                final_bbox = []
                for i in range(0, 8, 2):
                    nx = orig[i] + dx_norm_clamped
                    ny = orig[i + 1] + dy_norm_clamped
                    # Clamp to [0,1] as additional safety
                    nx = max(0.0, min(1.0, nx))
                    ny = max(0.0, min(1.0, ny))
                    final_bbox.extend([nx, ny])

                self.annotations[self.selected_annotation_index]['bbox'] = final_bbox
                self.main_frame.update_annotation_list()

                self.Refresh(False)

        elif self.editing_mode == 'resize' and self.selected_annotation_index >= 0:

            # Resize annotation box
            if self.main_frame.mode == "YOLO":
                self.resize_annotation(pos)
            else:
                self.resize_obb_annotation(pos)
            self.main_frame.update_annotation_list()
            self.Refresh(False)  # Refresh without clearing background to reduce flicker

        elif self.drawing and self.start_pos:
            # Draw new box
            clamped_pos = self.clamp_position_to_image(pos)
            self.current_box = (self.start_pos.x, self.start_pos.y, clamped_pos.x, clamped_pos.y)
            rotated_pts = self.rectangle_corners_from_diagonal((self.start_pos.x, self.start_pos.y),
                                                               (clamped_pos.x, clamped_pos.y), self.cross_angle)

            self.current_obb_box = tuple(x for pair in rotated_pts for x in pair)
            self.Refresh(False)  # Refresh without clearing background to reduce flicker
        else:
            # Update mouse cursor
            self.update_cursor(pos)

        self.Refresh(False)  # Refresh without clearing background to reduce flicker

    def resize_annotation(self, pos):
        """Resize annotation box"""
        if not self.original_bbox or not self.edit_start_pos:
            return

        # Get original box pixel coordinates
        orig_x, orig_y, orig_w, orig_h = self.yolo_to_pixel(self.original_bbox)
        orig_x1, orig_y1 = orig_x, orig_y
        orig_x2, orig_y2 = orig_x + orig_w, orig_y + orig_h

        # Calculate mouse movement distance
        dx = pos.x - self.edit_start_pos.x
        dy = pos.y - self.edit_start_pos.y

        # Calculate new boundaries based on resize handle type
        new_x1, new_y1, new_x2, new_y2 = orig_x1, orig_y1, orig_x2, orig_y2

        if 'l' in self.resize_handle:  # Left side
            new_x1 = orig_x1 + dx
        if 'r' in self.resize_handle:  # Right side
            new_x2 = orig_x2 + dx
        if 't' in self.resize_handle:  # Top side
            new_y1 = orig_y1 + dy
        if 'b' in self.resize_handle:  # Bottom side
            new_y2 = orig_y2 + dy

        # Ensure minimum size
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

        # Clamp to image boundaries
        img_x1 = self.offset_x
        img_y1 = self.offset_y
        img_x2 = self.offset_x + self.image_size[0] * self.scale_factor
        img_y2 = self.offset_y + self.image_size[1] * self.scale_factor

        new_x1 = max(img_x1, min(img_x2, new_x1))
        new_y1 = max(img_y1, min(img_y2, new_y1))
        new_x2 = max(img_x1, min(img_x2, new_x2))
        new_y2 = max(img_y1, min(img_y2, new_y2))

        # Convert back to YOLO format
        new_bbox = self.pixel_to_yolo((min(new_x1, new_x2), min(new_y1, new_y2),
                                       abs(new_x2 - new_x1), abs(new_y2 - new_y1)))

        self.annotations[self.selected_annotation_index]['bbox'] = new_bbox

    def resize_obb_annotation(self, pos):
        """Improved OBB size adjustment: supports automatic boundary clipping and coordinate recalculation"""
        if not getattr(self, 'original_obb', None) or not getattr(self, 'edit_start_pos', None):
            return

        orig_pts = np.array(self.obb_yolo_to_pixel(self.original_obb), dtype=float).reshape(4, 2)
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
            return d * u_unit  # Return (dx,dy)

        def signed_distance_along_u(a, b, u, eps=1e-12):
            """
            a, b: array-like (x,y)
            u: array-like direction vector (preferably unit). If not unit, function normalizes it.
            Returns: signed distance s (positive from a to b direction)
            """
            a = np.asarray(a, dtype=float)
            b = np.asarray(b, dtype=float)
            u = np.asarray(u, dtype=float)

            v = b - a  # ab vector
            norm_u = np.linalg.norm(u)
            if norm_u < eps:
                raise ValueError("direction u is zero vector")
            u_unit = u / norm_u

            s = float(np.dot(v, u_unit))
            return s

        new_pts = orig_pts.copy()

        # Note: use new_pts as base (order: first u then v) so corners clamp as expected
        if 'l' in self.resize_handle:  # Left side (p0, p3) along u
            clamped_u = clamp_movement(new_pts, [0, 3], comp_u)
            new_pts[0] = new_pts[0] + clamped_u
            new_pts[3] = new_pts[3] + clamped_u
        if 'r' in self.resize_handle:  # Right side (p1, p2) along u
            clamped_u = clamp_movement(new_pts, [1, 2], comp_u)
            new_pts[1] = new_pts[1] + clamped_u
            new_pts[2] = new_pts[2] + clamped_u
        if 't' in self.resize_handle:  # Top side (p0, p1) along v
            clamped_v = clamp_movement(new_pts, [0, 1], comp_v)
            new_pts[0] = new_pts[0] + clamped_v
            new_pts[1] = new_pts[1] + clamped_v
        if 'b' in self.resize_handle:  # Bottom side (p3, p2) along v
            clamped_v = clamp_movement(new_pts, [3, 2], comp_v)
            new_pts[3] = new_pts[3] + clamped_v
            new_pts[2] = new_pts[2] + clamped_v

        # Ensure minimum size
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
        new_obb_yolo = self.pixel_to_obb_yolo(tuple(final_pts_flat))
        self.annotations[self.selected_annotation_index]['bbox'] = new_obb_yolo

        self.main_frame.update_annotation_list()
        self.Refresh(False)

    def update_cursor(self, pos):
        """Update mouse cursor"""

        if self.selected_annotation_index >= 0:
            ann = self.annotations[self.selected_annotation_index]
            if self.main_frame.mode == "YOLO":
                x, y, w, h = self.yolo_to_pixel(ann['bbox'])
                box = (x, y, x + w, y + h)

                handle = self.get_resize_handle(pos, box)
            else:
                handle = self.get_obb_resize_handle(pos, self.obb_yolo_to_pixel(ann['bbox']))
            if handle:
                # Set resize cursor
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
                    # Inside selected box, set move cursor
                    self.SetCursor(wx.Cursor(wx.CURSOR_SIZING))
                    return
                elif self.main_frame.mode == "YOLO-OBB" and self.get_annotation_at(pos) != -1:
                    # Inside selected box, set move cursor
                    self.SetCursor(wx.Cursor(wx.CURSOR_SIZING))
                    return
        if getattr(self, "panning", False):
            self.SetCursor(wx.Cursor(wx.CURSOR_SIZING))
            return

        # Default cursor
        self.SetCursor(wx.Cursor(wx.CURSOR_BLANK))
        # self.SetCursor(wx.Cursor(wx.CURSOR_DEFAULT))

    def on_mouse_enter(self, event):
        """Automatically get focus when mouse enters"""
        self.SetFocus()
        event.Skip()

    def on_key_down(self, event):
        """Keyboard event"""
        key_code = event.GetKeyCode()

        if key_code == wx.WXK_DELETE or key_code == wx.WXK_BACK:
            # Delete selected annotation
            if self.selected_annotation_index >= 0:
                del self.annotations[self.selected_annotation_index]
                self.selected_annotation_index = -1
                self.main_frame.update_annotation_list()
                self.Refresh(False)  # Refresh without clearing background to reduce flicker
                return
        elif key_code == wx.WXK_ESCAPE:
            # Cancel selection
            self.selected_annotation_index = -1
            self.drawing = False
            self.current_box = None
            self.editing_mode = None
            self.Refresh(False)  # Refresh without clearing background to reduce flicker
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
            self.Refresh(False)
            return

        event.Skip()

    def on_right_down(self, event):
        """Right button for angle adjustment"""
        self.adjusting = True
        self.adjust_last_pos = event.GetPosition()
        try:
            self.CaptureMouse()
        except Exception:
            pass

    def on_right_up(self, event):
        """End angle adjustment"""
        if self.adjusting:
            self.adjusting = False
            try:
                if self.HasCapture():
                    self.ReleaseMouse()
            except Exception:
                pass
            self.adjust_last_pos = None
            self.Refresh(False)

    def is_in_image_area(self, pos):
        """Check if position is within image area"""
        if not self.image:
            return False

        scaled_width = self.image_size[0] * self.scale_factor
        scaled_height = self.image_size[1] * self.scale_factor

        return (self.offset_x <= pos.x <= self.offset_x + scaled_width and
                self.offset_y <= pos.y <= self.offset_y + scaled_height)

    def pixel_to_yolo(self, pixel_bbox):
        """Convert pixel coordinates to YOLO format"""
        px, py, pw, ph = pixel_bbox

        # Convert to image-relative coordinates
        img_x = (px - self.offset_x) / self.scale_factor
        img_y = (py - self.offset_y) / self.scale_factor
        img_w = pw / self.scale_factor
        img_h = ph / self.scale_factor

        # Convert to YOLO format (center coordinates + relative width/height)
        center_x = (img_x + img_w / 2) / self.image_size[0]
        center_y = (img_y + img_h / 2) / self.image_size[1]
        rel_w = img_w / self.image_size[0]
        rel_h = img_h / self.image_size[1]

        return center_x, center_y, rel_w, rel_h

    def pixel_to_obb_yolo(self, pixel_bbox):
        """Convert pixel coordinates to OBB_YOLO format"""
        x1, y1, x2, y2, x3, y3, x4, y4 = pixel_bbox

        # Convert to image-relative coordinates
        img_x1 = (x1 - self.offset_x) / self.scale_factor
        img_y1 = (y1 - self.offset_y) / self.scale_factor
        img_x2 = (x2 - self.offset_x) / self.scale_factor
        img_y2 = (y2 - self.offset_y) / self.scale_factor
        img_x3 = (x3 - self.offset_x) / self.scale_factor
        img_y3 = (y3 - self.offset_y) / self.scale_factor
        img_x4 = (x4 - self.offset_x) / self.scale_factor
        img_y4 = (y4 - self.offset_y) / self.scale_factor

        # Convert to YOLO format (center coordinates + relative width/height)
        obb_x1 = img_x1 / self.image_size[0]
        obb_y1 = img_y1 / self.image_size[1]
        obb_x2 = img_x2 / self.image_size[0]
        obb_y2 = img_y2 / self.image_size[1]
        obb_x3 = img_x3 / self.image_size[0]
        obb_y3 = img_y3 / self.image_size[1]
        obb_x4 = img_x4 / self.image_size[0]
        obb_y4 = img_y4 / self.image_size[1]

        return obb_x1, obb_y1, obb_x2, obb_y2, obb_x3, obb_y3, obb_x4, obb_y4

    def yolo_to_pixel(self, yolo_bbox):
        """Convert YOLO format to pixel coordinates"""
        center_x, center_y, rel_w, rel_h = yolo_bbox

        # Convert to image coordinates
        img_w = rel_w * self.image_size[0]
        img_h = rel_h * self.image_size[1]
        img_x = center_x * self.image_size[0] - img_w / 2
        img_y = center_y * self.image_size[1] - img_h / 2

        # Convert to panel coordinates
        px = img_x * self.scale_factor + self.offset_x
        py = img_y * self.scale_factor + self.offset_y
        pw = img_w * self.scale_factor
        ph = img_h * self.scale_factor

        # return int(px), int(py), int(pw), int(ph)
        return round(px), round(py), round(pw), round(ph)

    def obb_yolo_to_pixel(self, yolo_bbox):
        """Convert YOLO format to pixel coordinates"""
        obb_x1, obb_y1, obb_x2, obb_y2, obb_x3, obb_y3, obb_x4, obb_y4 = yolo_bbox

        # Convert to image coordinates
        img_x1 = obb_x1 * self.image_size[0]
        img_y1 = obb_y1 * self.image_size[1]
        img_x2 = obb_x2 * self.image_size[0]
        img_y2 = obb_y2 * self.image_size[1]
        img_x3 = obb_x3 * self.image_size[0]
        img_y3 = obb_y3 * self.image_size[1]
        img_x4 = obb_x4 * self.image_size[0]
        img_y4 = obb_y4 * self.image_size[1]

        # Convert to panel coordinates

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

    def load_annotations(self):
        """Load annotation file"""
        if not self.image_path:
            return

        # Generate annotation file path from image path
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
                wx.MessageBox(f"Failed to load annotation file: {str(e)}", "Error", wx.OK | wx.ICON_ERROR)

    def save_annotations(self):
        """Save annotation file"""
        print("save_annotations")
        if not self.image_path:
            return

        base_name = os.path.splitext(os.path.basename(self.image_path))[0]
        txt_path = os.path.join(os.path.dirname(self.image_path), f"{base_name}.txt")

        try:
            if not self.annotations:
                # If no annotations, delete annotation file (if exists)
                if os.path.exists(txt_path):
                    os.remove(txt_path)
            else:
                if self.main_frame.mode == "YOLO":
                    # Save annotations normally when they exist
                    with open(txt_path, 'w') as f:
                        for ann in self.annotations:
                            bbox = ann['bbox']
                            f.write(f"{ann['class']} {bbox[0]:.6f} {bbox[1]:.6f} {bbox[2]:.6f} {bbox[3]:.6f}\n")
                else:
                    # Save annotations normally when they exist
                    with open(txt_path, 'w') as f:
                        for ann in self.annotations:
                            bbox = ann['bbox']
                            f.write(
                                f"{ann['class']} {bbox[0]:.6f} {bbox[1]:.6f} {bbox[2]:.6f} {bbox[3]:.6f} {bbox[4]:.6f} {bbox[5]:.6f} {bbox[6]:.6f} {bbox[7]:.6f}\n")
        except Exception as e:
            wx.MessageBox(f"Failed to save annotation file: {str(e)}", "Error", wx.OK | wx.ICON_ERROR)


class YoloLabelingTool(wx.Frame):
    def __init__(self):
        self.i18n = I18N('en')  # Default English
        super().__init__(None, title=self.i18n.t('app_title'), size=wx.Size(1200, 800))

        self.image_list = None
        self.current_class_label = None
        self.annotation_list = None
        self.annotation_panel = None
        self.image_files = []
        self.current_image_index = -1
        self.class_names = []  # Initially empty
        self.current_folder = None

        self.init_ui()
        self.Centre()

    def init_ui(self):
        """Initialize user interface"""
        panel = wx.Panel(self)
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Left panel
        left_panel = wx.Panel(panel)
        left_sizer = wx.BoxSizer(wx.VERTICAL)

        # Mode selection
        mode_box = wx.StaticBox(left_panel, label=self.i18n.t('mode_select'))
        mode_sizer = wx.StaticBoxSizer(mode_box, wx.VERTICAL)

        mode_choice = wx.Choice(left_panel, choices=[
            self.i18n.t('mode_yolo'),
            self.i18n.t('mode_yolo_obb')
        ])
        mode_choice.Bind(wx.EVT_CHOICE, self.on_switch_mode)
        mode_choice.SetSelection(0)
        self.mode = "YOLO"

        mode_sizer.Add(mode_choice, 0, wx.EXPAND | wx.ALL, 5)
        left_sizer.Insert(0, mode_sizer, 0, wx.EXPAND | wx.ALL, 5)

        # File operation buttons
        file_box = wx.StaticBox(left_panel, label=self.i18n.t('file_ops'))
        file_sizer = wx.StaticBoxSizer(file_box, wx.VERTICAL)

        self.load_btn = wx.Button(left_panel, label=self.i18n.t('load_folder'))
        self.load_btn.Bind(wx.EVT_BUTTON, self.on_load_folder)
        file_sizer.Add(self.load_btn, 0, wx.EXPAND | wx.ALL, 5)

        self.save_btn = wx.Button(left_panel, label=self.i18n.t('export_all'))
        self.save_btn.Bind(wx.EVT_BUTTON, self.on_save)
        file_sizer.Add(self.save_btn, 0, wx.EXPAND | wx.ALL, 5)

        left_sizer.Add(file_sizer, 0, wx.EXPAND | wx.ALL, 5)

        # Image list
        list_box = wx.StaticBox(left_panel, label=self.i18n.t('image_list'))
        list_sizer = wx.StaticBoxSizer(list_box, wx.VERTICAL)

        self.image_list = wx.ListBox(left_panel)
        self.image_list.Bind(wx.EVT_LISTBOX, self.on_image_select)
        list_sizer.Add(self.image_list, 1, wx.EXPAND | wx.ALL, 5)

        # Navigation buttons
        nav_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.prev_btn = wx.Button(left_panel, label=self.i18n.t('prev_image'))
        self.prev_btn.Bind(wx.EVT_BUTTON, self.on_prev_image)
        nav_sizer.Add(self.prev_btn, 1, wx.EXPAND | wx.RIGHT, 2)

        self.next_btn = wx.Button(left_panel, label=self.i18n.t('next_image'))
        self.next_btn.Bind(wx.EVT_BUTTON, self.on_next_image)
        nav_sizer.Add(self.next_btn, 1, wx.EXPAND | wx.LEFT, 2)

        list_sizer.Add(nav_sizer, 0, wx.EXPAND | wx.ALL, 5)
        left_sizer.Add(list_sizer, 1, wx.EXPAND | wx.ALL, 5)

        # Class selection
        class_box = wx.StaticBox(left_panel, label=self.i18n.t('class_manage'))
        class_sizer = wx.StaticBoxSizer(class_box, wx.VERTICAL)

        # Current class display
        current_class_sizer = wx.BoxSizer(wx.HORIZONTAL)
        current_class_sizer.Add(
            wx.StaticText(left_panel, label=self.i18n.t('current_class')),
            0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5
        )
        self.current_class_label = wx.StaticText(left_panel, label=self.i18n.t('no_class'))
        self.current_class_label.SetForegroundColour(wx.Colour(255, 0, 0))
        current_class_sizer.Add(self.current_class_label, 1, wx.ALIGN_CENTER_VERTICAL)
        class_sizer.Add(current_class_sizer, 0, wx.EXPAND | wx.ALL, 5)

        # Class list
        self.class_list = wx.ListBox(left_panel, style=wx.LB_SINGLE)
        self.class_list.Bind(wx.EVT_LISTBOX, self.on_class_select)
        class_sizer.Add(self.class_list, 1, wx.EXPAND | wx.ALL, 5)

        # Class operation buttons
        class_btn_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.add_class_btn = wx.Button(left_panel, label=self.i18n.t('add_class'))
        self.add_class_btn.Bind(wx.EVT_BUTTON, self.on_add_class)
        class_btn_sizer.Add(self.add_class_btn, 1, wx.EXPAND | wx.RIGHT, 2)

        self.edit_class_btn = wx.Button(left_panel, label=self.i18n.t('edit_class'))
        self.edit_class_btn.Bind(wx.EVT_BUTTON, self.on_edit_class)
        class_btn_sizer.Add(self.edit_class_btn, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 2)

        self.del_class_btn = wx.Button(left_panel, label=self.i18n.t('delete_class'))
        self.del_class_btn.Bind(wx.EVT_BUTTON, self.on_delete_class)
        class_btn_sizer.Add(self.del_class_btn, 1, wx.EXPAND | wx.LEFT, 2)

        class_sizer.Add(class_btn_sizer, 0, wx.EXPAND | wx.ALL, 5)

        # Sort buttons
        sort_btn_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.up_btn = wx.Button(left_panel, label=self.i18n.t('move_up'))
        self.up_btn.Bind(wx.EVT_BUTTON, self.on_move_up)
        sort_btn_sizer.Add(self.up_btn, 1, wx.EXPAND | wx.RIGHT, 2)

        self.down_btn = wx.Button(left_panel, label=self.i18n.t('move_down'))
        self.down_btn.Bind(wx.EVT_BUTTON, self.on_move_down)
        sort_btn_sizer.Add(self.down_btn, 1, wx.EXPAND | wx.LEFT, 2)

        class_sizer.Add(sort_btn_sizer, 0, wx.EXPAND | wx.ALL, 5)
        left_sizer.Add(class_sizer, 1, wx.EXPAND | wx.ALL, 5)

        # Annotation list
        ann_box = wx.StaticBox(left_panel, label=self.i18n.t('current_annotations'))
        ann_sizer = wx.StaticBoxSizer(ann_box, wx.VERTICAL)

        self.annotation_list = wx.ListCtrl(left_panel, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        self.annotation_list.InsertColumn(0, self.i18n.t('col_select'), width=40)
        self.annotation_list.InsertColumn(1, self.i18n.t('col_index'), width=50)
        self.annotation_list.InsertColumn(2, self.i18n.t('col_class'), width=80)
        self.annotation_list.InsertColumn(3, self.i18n.t('col_bbox'), width=200)

        ann_sizer.Add(self.annotation_list, 1, wx.EXPAND | wx.ALL, 5)

        self.del_ann_btn = wx.Button(left_panel, label=self.i18n.t('delete_annotation'))
        self.del_ann_btn.Bind(wx.EVT_BUTTON, self.on_delete_annotation)
        ann_sizer.Add(self.del_ann_btn, 0, wx.EXPAND | wx.ALL, 5)

        left_sizer.Add(ann_sizer, 1, wx.EXPAND | wx.ALL, 5)
        left_panel.SetSizer(left_sizer)

        # Right image display area
        self.annotation_panel = AnnotationPanel(panel, self)

        # Layout
        main_sizer.Add(left_panel, 0, wx.EXPAND | wx.ALL, 5)
        main_sizer.Add(self.annotation_panel, 1, wx.EXPAND | wx.ALL, 5)
        panel.SetSizer(main_sizer)

        # Create menu bar
        self.create_menu_bar()

        # Create status bar
        self.CreateStatusBar()
        self.SetStatusText(self.i18n.t('ready_status'))

    def create_menu_bar(self):
        """Create menu bar"""
        menubar = wx.MenuBar()

        # File menu
        file_menu = wx.Menu()
        file_menu.Append(wx.ID_OPEN, self.i18n.t('menu_open'))
        file_menu.Append(wx.ID_SAVE, self.i18n.t('menu_save'))
        file_menu.AppendSeparator()
        file_menu.Append(wx.ID_EXIT, self.i18n.t('menu_exit'))
        menubar.Append(file_menu, self.i18n.t('menu_file'))

        # Navigation menu
        nav_menu = wx.Menu()
        nav_menu.Append(101, self.i18n.t('menu_prev'))
        nav_menu.Append(102, self.i18n.t('menu_next'))
        menubar.Append(nav_menu, self.i18n.t('menu_nav'))

        # Language menu
        lang_menu = wx.Menu()
        lang_menu.Append(201, self.i18n.t('menu_english'))
        lang_menu.Append(202, self.i18n.t('menu_chinese'))
        menubar.Append(lang_menu, self.i18n.t('menu_language'))

        # Help menu
        help_menu = wx.Menu()
        help_menu.Append(wx.ID_ABOUT, self.i18n.t('menu_about'))
        menubar.Append(help_menu, self.i18n.t('menu_help'))

        self.SetMenuBar(menubar)

        # Bind menu events
        self.Bind(wx.EVT_MENU, self.on_load_folder, id=wx.ID_OPEN)
        self.Bind(wx.EVT_MENU, self.on_save, id=wx.ID_SAVE)
        self.Bind(wx.EVT_MENU, self.on_exit, id=wx.ID_EXIT)
        self.Bind(wx.EVT_MENU, self.on_about, id=wx.ID_ABOUT)
        self.Bind(wx.EVT_MENU, self.on_prev_image, id=101)
        self.Bind(wx.EVT_MENU, self.on_next_image, id=102)
        self.Bind(wx.EVT_MENU, lambda e: self.switch_language('en'), id=201)
        self.Bind(wx.EVT_MENU, lambda e: self.switch_language('zh'), id=202)
        self.Bind(wx.EVT_CLOSE, self.on_close)

        # Bind keyboard shortcuts
        accel_tbl = wx.AcceleratorTable([
            (wx.ACCEL_CTRL, ord('O'), wx.ID_OPEN),
            (wx.ACCEL_CTRL, ord('S'), wx.ID_SAVE),
            (wx.ACCEL_CTRL, ord('Q'), wx.ID_EXIT),
            (wx.ACCEL_NORMAL, wx.WXK_LEFT, 101),
            (wx.ACCEL_NORMAL, wx.WXK_RIGHT, 102),
        ])
        self.SetAcceleratorTable(accel_tbl)

    def switch_language(self, lang):
        """Switch language"""
        self.i18n.set_language(lang)
        # Rebuild interface
        self.Freeze()

        # Save current state
        current_image_index = self.current_image_index

        # Destroy old interface
        for child in self.GetChildren():
            child.Destroy()

        # Reinitialize interface
        self.init_ui()

        # Restore state
        if self.image_files:
            self.image_list.Clear()
            for img_path in self.image_files:
                self.image_list.Append(os.path.basename(img_path))

            if current_image_index >= 0:
                self.image_list.SetSelection(current_image_index)
                self.on_image_select(None)

        if self.class_names:
            self.update_class_list()

        self.Thaw()
        self.Layout()

    def on_add_class(self, event):
        """Add new class"""
        dlg = wx.TextEntryDialog(
            self,
            self.i18n.t('add_class_prompt'),
            self.i18n.t('add_class_title')
        )
        if dlg.ShowModal() == wx.ID_OK:
            class_name = dlg.GetValue().strip()
            if class_name:
                self.class_names.append(class_name)
                self.update_class_list()
                self.class_list.SetSelection(self.class_list.GetCount() - 1)
                self.on_class_select(None)
        dlg.Destroy()

    def on_edit_class(self, event):
        """Edit class"""
        selection = self.class_list.GetSelection()
        if selection == wx.NOT_FOUND:
            wx.MessageBox(
                self.i18n.t('select_class_first'),
                self.i18n.t('info'),
                wx.OK | wx.ICON_INFORMATION
            )
            return

        current_name = self.class_names[selection]
        dlg = wx.TextEntryDialog(
            self,
            self.i18n.t('edit_class_prompt'),
            self.i18n.t('edit_class_title'),
            current_name
        )
        if dlg.ShowModal() == wx.ID_OK:
            new_name = dlg.GetValue().strip()
            if new_name and new_name != current_name:
                self.class_names[selection] = new_name
                self.update_class_list()
                self.class_list.SetSelection(selection)
                self.on_class_select(None)
                if hasattr(self, 'annotation_panel'):
                    self.annotation_panel.Refresh()
                    self.update_annotation_list()
        dlg.Destroy()

    def on_delete_class(self, event):
        """Delete class"""
        selection = self.class_list.GetSelection()
        if selection == wx.NOT_FOUND:
            wx.MessageBox(
                self.i18n.t('select_class_first'),
                self.i18n.t('info'),
                wx.OK | wx.ICON_INFORMATION
            )
            return

        class_name = self.class_names[selection]
        dlg = wx.MessageDialog(
            self,
            self.i18n.t('delete_class_msg').format(class_name),
            self.i18n.t('delete_class_title'),
            wx.YES_NO | wx.ICON_QUESTION
        )
        if dlg.ShowModal() == wx.ID_YES:
            # Execute deletion logic (keep original code)
            if self.annotation_panel.image_path:
                self.annotation_panel.save_annotations()

            self.annotation_panel.annotations = [
                ann for ann in self.annotation_panel.annotations
                if ann['class'] != selection
            ]

            new_class_names = []
            id_mapping = {}
            new_id = 0
            for old_id in range(len(self.class_names)):
                if old_id != selection:
                    new_class_names.append(self.class_names[old_id])
                    id_mapping[old_id] = new_id
                    new_id += 1

            self.class_names = new_class_names

            for ann in self.annotation_panel.annotations:
                old_class_id = ann['class']
                if old_class_id in id_mapping:
                    ann['class'] = id_mapping[old_class_id]

            self.update_all_annotation_files(id_mapping)
            self.update_class_list()

            if not self.class_names:
                self.current_class_label.SetLabel(self.i18n.t('no_class'))
            else:
                new_selection = min(selection, self.class_list.GetCount() - 1)
                self.class_list.SetSelection(new_selection)
                self.on_class_select(None)

            self.annotation_panel.selected_annotation_index = -1
            self.annotation_panel.Refresh()
            self.update_annotation_list()
        dlg.Destroy()

    def on_save(self, event=None):
        """Save current annotations"""
        if self.annotation_panel.image_path:
            self.annotation_panel.save_annotations()
            self.SetStatusText(self.i18n.t('annotation_saved'))
        else:
            wx.MessageBox(
                self.i18n.t('no_image_to_save'),
                self.i18n.t('info'),
                wx.OK | wx.ICON_INFORMATION
            )

        # Create classes.txt file
        if self.image_files and self.class_names:
            folder_path = os.path.dirname(self.image_files[0])
            classes_path = os.path.join(folder_path, "classes.txt")

            try:
                with open(classes_path, 'w', encoding='utf-8') as f:
                    for class_id in range(len(self.class_names)):
                        f.write(f"{self.class_names[class_id]}\n")

                wx.MessageBox(
                    self.i18n.t('export_complete').format(classes_path),
                    self.i18n.t('success'),
                    wx.OK | wx.ICON_INFORMATION
                )
            except Exception as e:
                wx.MessageBox(
                    self.i18n.t('export_failed').format(str(e)),
                    self.i18n.t('error'),
                    wx.OK | wx.ICON_ERROR
                )

    def load_classes_from_file(self, folder_path):
        """Load classes from classes.txt file"""
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
                wx.MessageBox(
                    self.i18n.t('read_classes_failed').format(str(e)),
                    self.i18n.t('error'),
                    wx.OK | wx.ICON_ERROR
                )
                return False
        return False

    def load_image_folder(self, folder_path):
        """Load all images in folder"""
        image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
        self.image_files = []

        for file_name in os.listdir(folder_path):
            if any(file_name.lower().endswith(ext) for ext in image_extensions):
                self.image_files.append(os.path.join(folder_path, file_name))

        self.image_files.sort()

        # Update image list
        self.image_list.Clear()
        for img_path in self.image_files:
            self.image_list.Append(os.path.basename(img_path))

        if self.image_files:
            self.image_list.SetSelection(0)
            self.on_image_select(None)

        self.SetStatusText(self.i18n.t('loaded_images').format(len(self.image_files)))

    def on_image_select(self, event):
        """Select image"""
        selection = self.image_list.GetSelection()
        if selection != wx.NOT_FOUND:
            self.current_image_index = selection
            image_path = self.image_files[selection]

            # Save previous image's annotations
            if hasattr(self, 'annotation_panel') and self.annotation_panel.image_path:
                self.annotation_panel.save_annotations()

            # Load new image
            if self.annotation_panel.load_image(image_path):
                self.update_annotation_list()
                self.SetStatusText(
                    self.i18n.t('current_image').format(
                        os.path.basename(image_path),
                        selection + 1,
                        len(self.image_files)
                    )
                )

    def on_load_folder(self, event):
        """Load image folder"""
        dlg = wx.DirDialog(self, self.i18n.t('load_folder'))
        if dlg.ShowModal() == wx.ID_OK:
            folder_path = dlg.GetPath()
            self.current_folder = folder_path
            # Try to load class file first
            self.load_classes_from_file(folder_path)
            self.update_class_list()
            self.load_image_folder(folder_path)
        dlg.Destroy()

    def on_switch_mode(self, event):
        """Switch annotation mode (YOLO / YOLO-OBB)"""
        choice = event.GetEventObject()
        mode = choice.GetStringSelection()
        # Determine mode based on current language
        if mode == self.i18n.t('mode_yolo'):
            self.mode = "YOLO"
        else:
            self.mode = "YOLO-OBB"
        print(f"Switched to mode: {self.mode}")

    def on_prev_image(self, event):
        """Previous image"""
        if self.image_files and self.current_image_index > 0:
            self.image_list.SetSelection(self.current_image_index - 1)
            self.on_image_select(None)

    def on_next_image(self, event):
        """Next image"""
        if self.image_files and self.current_image_index < len(self.image_files) - 1:
            self.image_list.SetSelection(self.current_image_index + 1)
            self.on_image_select(None)

    def update_all_annotation_files(self, id_mapping):
        """Update class IDs in all annotation files"""
        if not self.image_files:
            return

        for image_path in self.image_files:
            base_name = os.path.splitext(os.path.basename(image_path))[0]
            txt_path = os.path.join(os.path.dirname(image_path), f"{base_name}.txt")

            if os.path.exists(txt_path):
                try:
                    annotations = []
                    with open(txt_path, 'r') as f:
                        for line in f:
                            parts = line.strip().split()
                            if len(parts) == 5 or len(parts) == 9:
                                class_id = int(parts[0])
                                bbox = [float(x) for x in parts[1:]]
                                if class_id in id_mapping:
                                    new_class_id = id_mapping[class_id]
                                    annotations.append((new_class_id, bbox))

                    if annotations:
                        with open(txt_path, 'w') as f:
                            for class_id, bbox in annotations:
                                if len(bbox) == 8:
                                    f.write(
                                        f"{class_id} {bbox[0]:.6f} {bbox[1]:.6f} {bbox[2]:.6f} {bbox[3]:.6f} "
                                        f"{bbox[4]:.6f} {bbox[5]:.6f} {bbox[6]:.6f} {bbox[7]:.6f}\n"
                                    )
                                else:
                                    f.write(f"{class_id} {bbox[0]:.6f} {bbox[1]:.6f} {bbox[2]:.6f} {bbox[3]:.6f}\n")
                    else:
                        os.remove(txt_path)

                except Exception as e:
                    print(f"Failed to update annotation file {txt_path}: {e}")

    def on_move_up(self, event):
        """Move class up"""
        selection = self.class_list.GetSelection()
        if selection == wx.NOT_FOUND or selection == 0:
            return

        if self.annotation_panel.image_path:
            self.annotation_panel.save_annotations()

        sorted_items = [(class_id, class_name) for class_id, class_name in enumerate(self.class_names)]
        sorted_items[selection], sorted_items[selection - 1] = sorted_items[selection - 1], sorted_items[selection]

        id_mapping = self.reassign_class_ids(sorted_items)
        self.update_all_annotation_files(id_mapping)

        self.update_class_list()
        self.class_list.SetSelection(selection - 1)
        self.on_class_select(None)

        self.annotation_panel.Refresh()
        self.update_annotation_list()

    def on_move_down(self, event):
        """Move class down"""
        selection = self.class_list.GetSelection()
        if selection == wx.NOT_FOUND or selection == self.class_list.GetCount() - 1:
            return

        if self.annotation_panel.image_path:
            self.annotation_panel.save_annotations()

        sorted_items = [(class_id, class_name) for class_id, class_name in enumerate(self.class_names)]
        sorted_items[selection], sorted_items[selection + 1] = sorted_items[selection + 1], sorted_items[selection]

        id_mapping = self.reassign_class_ids(sorted_items)
        self.update_all_annotation_files(id_mapping)

        self.update_class_list()
        self.class_list.SetSelection(selection + 1)
        self.on_class_select(None)

        self.annotation_panel.Refresh()
        self.update_annotation_list()

    def reassign_class_ids(self, sorted_items):
        """Reassign class IDs and update all annotations"""
        old_to_new_mapping = {}
        new_class_names = self.class_names

        for new_id, (old_id, class_name) in enumerate(sorted_items):
            new_class_names[new_id] = class_name
            old_to_new_mapping[old_id] = new_id

        self.class_names = new_class_names

        for ann in self.annotation_panel.annotations:
            old_class_id = ann['class']
            if old_class_id in old_to_new_mapping:
                ann['class'] = old_to_new_mapping[old_class_id]

        return old_to_new_mapping

    def on_class_select(self, event):
        """Select class"""
        selection = self.class_list.GetSelection()
        if selection != wx.NOT_FOUND:
            class_name = self.class_names[selection]
            self.current_class_label.SetLabel(f"{selection}: {class_name}")
        else:
            self.current_class_label.SetLabel(self.i18n.t('no_class'))

    def update_class_list(self):
        """Update class list display"""
        self.class_list.Clear()
        for class_id in range(len(self.class_names)):
            self.class_list.Append(f"{class_id}: {self.class_names[class_id]}")

        if self.class_list.GetCount() > 0:
            self.class_list.SetSelection(0)
            self.on_class_select(None)
        else:
            self.current_class_label.SetLabel(self.i18n.t('no_class'))

    def get_current_class(self):
        """Get currently selected class ID"""
        selection = self.class_list.GetSelection()
        if selection != wx.NOT_FOUND and self.class_names:
            return selection
        return 0

    def update_annotation_list(self):
        """Incrementally update annotation list to avoid flickering"""
        anns = self.annotation_panel.annotations
        list_ctrl = self.annotation_list
        target_count = len(anns)

        while list_ctrl.GetItemCount() > target_count:
            list_ctrl.DeleteItem(list_ctrl.GetItemCount() - 1)

        while list_ctrl.GetItemCount() < target_count:
            idx = list_ctrl.GetItemCount()
            list_ctrl.InsertItem(idx, "")

        for i in range(target_count):
            ann = anns[i]
            class_name = self.class_names[ann['class']] if ann['class'] < len(
                self.class_names) else f"Class {ann['class']}"
            bbox = ann['bbox']
            prefix = "►" if i == self.annotation_panel.selected_annotation_index else ""

            list_ctrl.SetItem(i, 0, prefix)
            list_ctrl.SetItem(i, 1, str(i + 1))
            list_ctrl.SetItem(i, 2, class_name)
            list_ctrl.SetItem(i, 3, f"({bbox[0]:.3f}, {bbox[1]:.3f}, {bbox[2]:.3f}, {bbox[3]:.3f})")

    def on_delete_annotation(self, event):
        """Delete selected annotation"""
        selection = self.annotation_list.GetFirstSelected()
        if selection != wx.NOT_FOUND:
            del self.annotation_panel.annotations[selection]

            if self.annotation_panel.selected_annotation_index == selection:
                self.annotation_panel.selected_annotation_index = -1
            elif self.annotation_panel.selected_annotation_index > selection:
                self.annotation_panel.selected_annotation_index -= 1

            self.update_annotation_list()
            self.annotation_panel.Refresh()

    def on_exit(self, event):
        """Exit program"""
        print("on_exit")
        self.on_close()

    def on_close(self, event=None):
        """Handle window close event"""
        print("on_close")
        self.on_save()
        self.Destroy()

    def on_about(self, event):
        import wx.adv
        """About dialog"""
        info = wx.adv.AboutDialogInfo()
        info.SetName(self.i18n.t('app_title'))
        info.SetVersion("1.0")
        info.SetDescription(self.i18n.t('about_description'))
        info.SetCopyright("(C) 2025")
        wx.adv.AboutBox(info)


class YoloApp(wx.App):
    def OnInit(self):
        frame = YoloLabelingTool()
        frame.Show()
        return True


if __name__ == '__main__':
    # Set DPI awareness
    if sys.platform.startswith('win'):
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(1)  # 1: System DPI aware, 2: Per-monitor DPI aware
        except Exception:
            ctypes.windll.user32.SetProcessDPIAware()  # Fallback method
    app = YoloApp()
    app.MainLoop()
