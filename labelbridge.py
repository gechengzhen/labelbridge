import wx
import os
import ctypes


class AnnotationPanel(wx.Panel):
    def __init__(self, parent, main_frame):
        super().__init__(parent)
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)

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

        # 缓存的背景图片
        self.background_bitmap = None

        self.SetBackgroundColour(wx.Colour(240, 240, 240))

        # 绑定事件
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_MOTION, self.OnMouseMove)
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
        self.Bind(wx.EVT_SIZE, self.OnSize)

    def LoadImage(self, image_path):
        """加载图片"""
        try:
            self.image_path = image_path
            self.image = wx.Image(image_path)
            self.image_size = (self.image.GetWidth(), self.image.GetHeight())
            self.FitImageToPanel()
            self.LoadAnnotations()
            self.CreateBackgroundBitmap()
            self.Refresh()
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

        # 重新创建背景图片缓存
        if self.image:
            self.CreateBackgroundBitmap()

    def CreateBackgroundBitmap(self):
        """创建背景图片缓存"""
        if not self.image:
            return

        panel_size = self.GetSize()
        if panel_size.width <= 0 or panel_size.height <= 0:
            return

        # 创建背景缓存位图
        self.background_bitmap = wx.Bitmap(panel_size.width, panel_size.height)

        # 在背景位图上绘制图片和固定标注
        dc = wx.MemoryDC()
        dc.SelectObject(self.background_bitmap)
        dc.SetBackground(wx.Brush(wx.Colour(240, 240, 240)))
        dc.Clear()

        # 计算缩放后的尺寸，确保至少为1
        scaled_width = max(1, int(self.image_size[0] * self.scale_factor))
        scaled_height = max(1, int(self.image_size[1] * self.scale_factor))

        # 只有当缩放后的尺寸足够大时才绘制图片
        if scaled_width > 1 and scaled_height > 1:
            try:
                # 绘制缩放后的图片
                scaled_image = self.image.Scale(scaled_width, scaled_height)
                bitmap = wx.Bitmap(scaled_image)
                dc.DrawBitmap(bitmap, int(self.offset_x), int(self.offset_y))

                # 绘制已有的标注框
                self.DrawAnnotationsOnDC(dc)
            except Exception as e:
                print(f"绘制图片时出错: {e}")
                # 如果出错，至少保持背景色

        dc.SelectObject(wx.NullBitmap)

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
            self.FitImageToPanel()
            self.Refresh()
        event.Skip()

    def OnPaint(self, event):
        """绘制事件"""
        dc = wx.BufferedPaintDC(self)

        if self.background_bitmap:
            # 绘制缓存的背景图片（包含图片和固定标注）
            dc.DrawBitmap(self.background_bitmap, 0, 0)

            # 只绘制当前正在画的框
            if self.current_box and self.drawing:
                self.DrawBox(dc, self.current_box, wx.Colour(0, 255, 0), 2)
        else:
            dc.Clear()

    def DrawAnnotationsOnDC(self, dc):
        """在指定DC上绘制所有标注框"""
        for ann in self.annotations:
            # 转换坐标
            x, y, w, h = self.YoloToPixel(ann['bbox'])
            box = (x, y, x + w, y + h)

            # 绘制框
            color = wx.Colour(255, 0, 0) if ann == self.annotations[-1] else wx.Colour(0, 0, 255)
            self.DrawBox(dc, box, color, 2)

            # 绘制类别标签
            if ann['class'] < len(self.main_frame.class_names):
                class_name = self.main_frame.class_names[ann['class']]
            else:
                class_name = f"Class {ann['class']}"
            dc.SetTextForeground(color)
            dc.DrawText(class_name, x, max(0, y - 20))

    def DrawBox(self, dc, box, color, width):
        """绘制矩形框"""
        pen = wx.Pen(color, width)
        dc.SetPen(pen)
        dc.SetBrush(wx.Brush(color, wx.BRUSHSTYLE_TRANSPARENT))

        x1, y1, x2, y2 = box
        dc.DrawRectangle(x1, y1, x2 - x1, y2 - y1)

    def OnLeftDown(self, event):
        """鼠标左键按下"""
        if not self.image:
            return

        pos = event.GetPosition()
        if self.IsInImageArea(pos):
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

    def OnLeftUp(self, event):
        """鼠标左键释放"""
        if not self.drawing:
            return

        self.drawing = False
        if self.current_box:
            x1, y1, x2, y2 = self.current_box

            # 确保框有一定大小
            if abs(x2 - x1) > 5 and abs(y2 - y1) > 5:
                # 转换为YOLO格式并添加标注
                yolo_bbox = self.PixelToYolo((min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1)))

                # 获取当前选择的类别
                current_class = self.main_frame.GetCurrentClass()

                annotation = {
                    'class': current_class,
                    'bbox': yolo_bbox
                }
                self.annotations.append(annotation)
                self.main_frame.UpdateAnnotationList()

                # 重新创建背景缓存以包含新标注
                self.CreateBackgroundBitmap()

            self.current_box = None
            self.Refresh()

    def OnMouseMove(self, event):
        """鼠标移动"""
        if self.drawing and self.start_pos:
            pos = event.GetPosition()
            # 限制当前位置在图片内
            clamped_pos = self.ClampPositionToImage(pos)
            self.current_box = (self.start_pos.x, self.start_pos.y, clamped_pos.x, clamped_pos.y)
            self.Refresh()  # 只触发前景重绘

    def OnRightDown(self, event):
        """右键删除标注"""
        if not self.image:
            return

        pos = event.GetPosition()
        # 查找点击位置的标注
        for i, ann in enumerate(self.annotations):
            x, y, w, h = self.YoloToPixel(ann['bbox'])
            if x <= pos.x <= x + w and y <= pos.y <= y + h:
                del self.annotations[i]
                self.main_frame.UpdateAnnotationList()

                # 重新创建背景缓存
                self.CreateBackgroundBitmap()
                self.Refresh()
                break

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

        return int(px), int(py), int(pw), int(ph)

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
                        if len(parts) == 5:
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
                # 有标注时正常保存
                with open(txt_path, 'w') as f:
                    for ann in self.annotations:
                        bbox = ann['bbox']
                        f.write(f"{ann['class']} {bbox[0]:.6f} {bbox[1]:.6f} {bbox[2]:.6f} {bbox[3]:.6f}\n")
        except Exception as e:
            wx.MessageBox(f"保存标注文件失败: {str(e)}", "错误", wx.OK | wx.ICON_ERROR)


class YoloLabelingTool(wx.Frame):
    def __init__(self):
        super().__init__(None, title="YOLO标注工具", size=wx.Size(1200, 800))

        self.image_list = None
        self.current_class_label = None
        self.class_list = None
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

        self.annotation_list = wx.ListBox(left_panel)
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
        self.SetStatusText("就绪")

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
                self.SetStatusText(f"当前图片: {os.path.basename(image_path)}")

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
                self.annotation_panel.CreateBackgroundBitmap()
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

            # 刷新显示
            self.annotation_panel.CreateBackgroundBitmap()
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
        self.annotation_panel.CreateBackgroundBitmap()
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
        self.annotation_panel.CreateBackgroundBitmap()
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

    def UpdateAnnotationList(self):
        """更新标注列表显示"""
        self.annotation_list.Clear()
        for i, ann in enumerate(self.annotation_panel.annotations):
            if ann['class'] in self.class_names:
                class_name = ann['class']
            else:
                class_name = f"Class {ann['class']}"
            bbox = ann['bbox']
            self.annotation_list.Append(
                f"{i + 1}. {class_name} ({bbox[0]:.3f}, {bbox[1]:.3f}, {bbox[2]:.3f}, {bbox[3]:.3f})")

    def OnDeleteAnnotation(self, event):
        """删除选中的标注"""
        selection = self.annotation_list.GetSelection()
        if selection != wx.NOT_FOUND:
            del self.annotation_panel.annotations[selection]
            self.UpdateAnnotationList()
            # 重新创建背景缓存以移除已删除的标注
            self.annotation_panel.CreateBackgroundBitmap()
            self.annotation_panel.Refresh()

    def OnExit(self, event):
        """退出程序"""
        self.Close()

    def OnAbout(self, event):
        import wx.adv
        """关于对话框"""
        info = wx.adv.AboutDialogInfo()
        info.SetName("YOLO标注工具")
        info.SetVersion("1.0")
        info.SetDescription(
            "用于YOLO目标检测的图片标注工具\n\n使用说明:\n1. 导入图片文件夹\n2. 选择类别\n3. 在图片上拖拽鼠标画框\n4. 右键删除标注框\n5. 保存并导出标注")
        info.SetCopyright("(C) 2025")

        wx.adv.AboutBox(info)


class YoloApp(wx.App):
    def OnInit(self):
        frame = YoloLabelingTool()
        frame.Show()
        return True


if __name__ == '__main__':
    # 设置 DPI 感知
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)  # 1: 系统 DPI 感知, 2: 每个监视器 DPI 感知
    except Exception:
        ctypes.windll.user32.SetProcessDPIAware()  # 备用方法
    app = YoloApp()
    app.MainLoop()
