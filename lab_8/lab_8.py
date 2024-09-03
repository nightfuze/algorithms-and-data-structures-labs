"""
Требуется написать объектно-ориентированную программу с графическим интерфейсом в соответствии со своим вариантом.
В программе должны быть реализованы минимум один класс, три атрибута, четыре метода (функции).
Ввод данных из файла с контролем правильности ввода.
Базы данных использовать нельзя. При необходимости сохранять информацию в виде файлов, разделяя значения запятыми или пробелами.
Для GUI использовать библиотеку tkinter.

Вариант - 6

Объекты:
    + треугольники
Функции:
    + проверка пересечения
    + визуализация
    + раскраска
    + поворот вокруг одной из вершин
"""

import csv
import math
import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox
from dataclasses import dataclass
from tkinter import ttk, colorchooser
from typing import Optional, List, Tuple, Callable, Dict, Literal


@dataclass
class RotationControlState:
    default_angle: int
    default_point: int
    set_rotation: Callable[[int], None]
    set_point: Callable[[int], None]


@dataclass
class ColorControlState:
    color: str
    set_color: Callable[[str], None]


class Vec2:
    def __init__(self, x: int or float, y: int or float):
        self._x = float(x)
        self._y = float(y)

    def __repr__(self):
        return f'Vec2({self._x}, {self._y})'

    def __eq__(self, other):
        if isinstance(other, Vec2):
            return self._x == other.x and self._y == other.y

    def __add__(self, other):
        if isinstance(other, Vec2):
            return Vec2(self._x + other.x, self._y + other.y)

    def __sub__(self, other):
        if isinstance(other, Vec2):
            return Vec2(self._x - other.x, self._y - other.y)

    def __mul__(self, other):
        if isinstance(other, Vec2):
            return Vec2(self._x * other.x, self._y * other.y)
        return Vec2(self._x * other, self._y * other)

    def data(self) -> Tuple[float, float]:
        return self._x, self._y

    @property
    def x(self) -> float:
        return self._x

    @property
    def y(self) -> float:
        return self._y

    @x.setter
    def x(self, value: float):
        self._x = value

    @y.setter
    def y(self, value: float):
        self._y = value


class Path2D:
    def __init__(self, path: List[Vec2]):
        self._data = path

    @classmethod
    def from_array(cls, path: List[float]):
        data = []
        for i in range(0, len(path), 2):
            data.append(Vec2(path[i], path[i + 1]))
        return cls(data)

    def __str__(self):
        return str(self._data)

    def __len__(self):
        return len(self._data)

    def __eq__(self, other):
        return self._data == other

    def __getitem__(self, item):
        return self._data[item]

    def __iter__(self):
        for item in self._data:
            yield item

    def toarray(self):
        data = []
        for p in self._data:
            data.append(p.x)
            data.append(p.y)
        return data


class Util:

    @staticmethod
    def intersection_lines(x1: float, y1: float, x2: float, y2: float, x3: float, y3: float, x4: float, y4: float) -> \
            Optional[Vec2]:
        d = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

        if d == 0:
            return

        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / d
        u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / d

        if not (0 <= t <= 1 and 0 <= u <= 1):
            return

        x = x1 + t * (x2 - x1)
        y = y1 + t * (y2 - y1)

        return Vec2(x, y)

    @staticmethod
    def lines_from_path(path: Path2D) -> List[Tuple[Vec2, Vec2]]:
        lines = []
        for i in range(len(path) - 1):
            lines.append((path[i], path[i + 1]))
        lines.append((path[-1], path[0]))
        return lines


class CanvasObject:
    canvas: Optional[tk.Canvas] = None

    def __init__(self, object_id: int, position: Vec2, path: Path2D, width, height):
        self._position = Vec2(position.x - width / 2, position.y - height / 2)
        self._width = width
        self._height = height
        self.path = path
        self.id = object_id

    @staticmethod
    def bind_canvas(canvas: tk.Canvas):
        CanvasObject.canvas = canvas

    def destroy(self):
        CanvasObject.canvas.delete(self.id)

    def set_coords(self, path: List[float]):
        self.set_path(path)
        CanvasObject.canvas.coords(self.id, path)

    def set_path(self, path: List[float]):
        self.path = Path2D.from_array(path)

    def get_coords(self) -> List[float]:
        return CanvasObject.canvas.coords(self.id)

    def get_width(self) -> float:
        return self._width

    def get_height(self) -> float:
        return self._height

    def get_tags(self) -> Tuple[str, ...]:
        return CanvasObject.canvas.gettags(self.id)

    def set_fill(self, color: str):
        CanvasObject.canvas.itemconfig(self.id, fill=color)

    def get_fill(self) -> str:
        return CanvasObject.canvas.itemcget(self.id, "fill")

    def set_outline(self, color: str):
        CanvasObject.canvas.itemconfig(self.id, outline=color)

    def set_thickness(self, thickness: float):
        CanvasObject.canvas.itemconfig(self.id, width=thickness)

    def select(self):
        self.set_outline("blue")
        self.set_thickness(2)

    def unselect(self):
        self.set_outline("black")
        self.set_thickness(1)

    def show(self):
        CanvasObject.canvas.itemconfig(self.id, state="normal")

    def hide(self):
        CanvasObject.canvas.itemconfig(self.id, state="hidden")

    def get_center(self):
        return Vec2(self._position.x + self._width / 2,
                    self._position.y + self._height / 2)

    def set_position(self, position: Vec2):
        self._position = Vec2(position.x - self._width / 2,
                              position.y - self._height / 2)
        center = self.get_center()
        self.path = Path2D.from_array(self.get_coords())
        CanvasObject.canvas.moveto(self.id, center.x, center.y)

    def get_position(self) -> Vec2:
        return self._position


class Point(CanvasObject):
    def __init__(self, x, y, size=10, tags: str = "point", variant: str = "rect"):
        size /= 2
        top = Vec2(x - size, y - size)
        bottom = Vec2(x + size, y + size)
        path = Path2D([top, bottom])

        if variant == "rect":
            object_id = self.canvas.create_rectangle(path.toarray(), fill='white', outline='black', tags=tags)

        else:
            object_id = self.canvas.create_oval(path.toarray(), fill='white', outline='black', tags=tags)

        position = Vec2(x, y)
        super().__init__(object_id, position, path, size, size)


class Shape(CanvasObject):
    def __init__(self, position: Vec2, path: Path2D, width, height, tags):
        object_id = self.canvas.create_polygon(*path.toarray(), fill='white', outline='black', tags=tags)
        # print("Created:", object_id)
        super().__init__(object_id, position, path, width, height)
        # self.rotation_point: Point = Point(*self.path[0].data())
        self.rotation_point: Optional[Point] = None
        # print(self.rotation_point.get_position())
        self.rotation_point_index = 0
        # self.rotation_point.hide()

    def rotate(self, radians):
        if self.rotation_point is None:
            self.rotation_point = Point(*self.path[0].data())
        c = self.rotation_point.get_center()
        for p in self.path:
            if p == c:
                continue
            dx = p.x - c.x
            dy = p.y - c.y
            p.x = c.x + dx * math.cos(radians) - dy * math.sin(radians)
            p.y = c.y + dx * math.sin(radians) + dy * math.cos(radians)
        # print(self.path.toarray())
        self.set_coords(self.path.toarray())
        # print("Rotate:", math.degrees(radians), "degrees")

    # def set_coords(self, path: List[float]):
    #     super().set_coords(path)
    #     self.rotation_point.destroy()
    #     self.rotation_point = Point(*self.path[self.rotation_point_index].data())

    # def set_path(self, path: List[float]):
    #     super().set_path(path)
    #     w = self.rotation_point.get_width()
    #     h = self.rotation_point.get_height()
    #     pos = self.path[self.rotation_point_index] - Vec2(w / 2, h / 2)
    #     self.rotation_point.set_position(pos)

    def select(self):
        super().select()
        if self.rotation_point is None:
            self.rotation_point = Point(*self.path[0].data())
        self.rotation_point.show()

    def unselect(self):
        super().unselect()
        if self.rotation_point is None:
            self.rotation_point = Point(*self.path[0].data())
        self.rotation_point.hide()

    def select_rotation_point(self, index: int):
        if index >= len(self.path):
            return
        self.rotation_point.destroy()
        self.rotation_point_index = index
        self.rotation_point = Point(*self.path[index].data())

    def set_position(self, position: Vec2):
        super().set_position(position)
        self.rotation_point.destroy()
        self.rotation_point = Point(*self.path[self.rotation_point_index].data())


class Triangle(Shape):
    def __init__(self, x, y, width=100, height=100):
        top = Vec2(x, y - height / 2)
        left = Vec2(x - width / 2, y + height / 2)
        right = Vec2(x + width / 2, y + height / 2)
        path = Path2D([top, left, right])
        position = Vec2(x, y)
        # print("Created triangle: ", path.toarray())
        super().__init__(position, path, width, height, tags="triangle")


class RotationControlFrame(ttk.Frame):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.label = ttk.LabelFrame(self, text="Управление поворотом")
        self.label.pack(fill="both", pady=5)

        self.label_point = ttk.Label(self.label, text="Выбрать вершину")
        self.label_point.pack(fill="x")

        self.state = AppContext.get_instance().rotation_control_state

        self.angle = tk.IntVar(value=self.state.default_angle)
        self.point = tk.IntVar(value=self.state.default_point)

        for i in range(3):
            ttk.Radiobutton(self.label, text=str(i), value=i, variable=self.point, command=self._point_change).pack(
                fill="x")

        self.label_rotate = ttk.Label(self.label, text="Угол поворота")
        self.label_rotate.pack(fill="x")

        ttk.Entry(self.label, textvariable=self.angle).pack(fill="x")

        self.scale_angle = ttk.Scale(self.label, orient="horizontal", from_=-180, to=180, variable=self.angle,
                                     command=self._scale_change)
        self.scale_angle.pack(fill="x", pady=5)

        self.btn_rotate = ttk.Button(self.label, text="Повернуть", command=self._rotate)
        self.btn_rotate.pack(pady=5)

    def _scale_change(self, value):
        value = int(float(value))
        self.angle.set(value)

    def _rotate(self):
        self.state.set_rotation(self.angle.get())

    def _point_change(self):
        self.state.set_point(self.point.get())

    def _reset(self):
        self.angle.set(0)


class Sidebar(ttk.Frame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.configure(padding=10)
        RotationControlFrame(self).pack()


class ToolControlFrame(ttk.Frame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.configure(padding=10)
        self.btn_create = ttk.Button(self, text="Создать", command=self._create)
        self.btn_create.pack(side="left", padx=5)
        self.btn_select = ttk.Button(self, text="Выбрать", command=self._select)
        self.btn_select.pack(side="left", padx=5)
        self.btn_select = ttk.Button(self, text="Цвет", command=self._color)
        self.btn_select.pack(side="left", padx=5)
        self.app_ctx = AppContext.get_instance()

    def _create(self):
        self.app_ctx.tool_mode = "create"

    def _select(self):
        self.app_ctx.tool_mode = "select"

    def _color(self):
        init_color = self.app_ctx.color_control_state.color
        selected_color = colorchooser.askcolor(title='Выберите цвет', initialcolor=init_color)
        if selected_color[1]:
            self.app_ctx.color_control_state.set_color(str(selected_color[1]))


class Toolbar(ttk.Frame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.pack(side="top", fill="x")
        ToolControlFrame(self).pack()


class AppContext:
    _instance = None

    def __init__(self):
        self.rotation_control_state: Optional[RotationControlState] = None
        self.tool_mode: Literal["select", "rotate"] = "select"
        self.selected_triangle: Optional[int] = None
        self.dragging_triangle: bool = False
        self.color_control_state: Optional[ColorControlState] = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = AppContext()
        return cls._instance


class TriangleManager:
    _instance = None

    def __init__(self):
        self.data: Dict[int, Triangle] = {}

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = TriangleManager()
        return cls._instance

    def create(self, position: Vec2):
        triangle = Triangle(position.x, position.y)
        self.data[triangle.id] = triangle

    def add(self, triangle: Triangle):
        self.data[triangle.id] = triangle

    def get(self, triangle_id: int):
        return self.data.get(triangle_id)

    def all(self):
        return self.data

    def remove(self, triangle_id: int):
        self.data.pop(triangle_id).destroy()

    def clear(self):
        ids = list(self.data.keys())
        for i in ids:
            self.remove(i)


class App(ttk.Frame):
    def __init__(self, root: tk.Tk):
        super().__init__(root)
        self.pack()
        self.root = root

        self.main_menu = tk.Menu(tearoff=0)

        self.file_menu = tk.Menu(tearoff=0)
        self.file_menu.add_command(label="Открыть...", command=self.load)
        self.file_menu.add_command(label="Сохранить", command=self.save)
        self.file_menu.add_command(label="Сохранить как...", command=self.save_as)
        self.file_menu.add_command(label="Новый", command=self.new)

        self.main_menu.add_cascade(label="Файл", menu=self.file_menu)

        root.config(menu=self.main_menu)

        self.filename = None

        self.toolbar = Toolbar(self)
        self.toolbar.pack(side="top", fill="x")

        rotation_control_state = RotationControlState(45, 0, self.rotate_triangle, self.select_rotation_point)
        color_control_state = ColorControlState('white', self.change_color)

        self.context = AppContext.get_instance()
        self.context.rotation_control_state = rotation_control_state
        self.context.color_control_state = color_control_state

        self.sidebar = Sidebar(self)
        self.sidebar.pack(side="right", fill="y")

        self.canvas = tk.Canvas(self, width=800, height=600, bg="white")
        self.canvas.pack()
        CanvasObject.bind_canvas(self.canvas)

        self.canvas.bind("<Button-1>", self.on_left_click)
        self.canvas.bind("<B1-Motion>", self.on_left_motion)
        self.canvas.bind("<ButtonRelease-1>", self.on_left_release)
        # self.canvas.bind("<Button-3>", self.on_right_click)

        self.triangle_manager = TriangleManager.get_instance()
        # self.triangle_manager.create(Vec2(400, 150))
        # self.triangle_manager.create(Vec2(150, 350))
        # self.triangle_manager.create(Vec2(450, 150))

    def new(self):
        self.clear_canvas()
        self.filename = None

    def load(self):
        self.filename = tkinter.filedialog.askopenfilename(filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*")))
        if not self.filename:
            return
        try:
            with open(self.filename, newline='') as csvfile:
                self.clear_canvas()

                reader = csv.DictReader(csvfile)
                for row in reader:
                    coords = list(map(float, row["coords"].split(',')))
                    pos = Vec2(float(row['position_x']), float(row['position_y']))
                    t = Triangle(pos.x, pos.y)
                    t.set_coords(coords)
                    t.set_fill(row['color'])
                    TriangleManager.get_instance().add(t)
        except Exception:
            tkinter.messagebox.showwarning("Невозможно открыть файл!", "Файл поврежден или отсутствует.")

    def save(self):
        if not self.filename:
            self.save_as()
            return

        with open(self.filename, 'w', newline='') as csvfile:
            fieldnames = ['coords', 'position_x', 'position_y', 'color']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            triangles = TriangleManager.get_instance().all()
            for _, item in triangles.items():
                writer.writerow(
                    {'coords': ", ".join(map(str, item.get_coords())),
                     'position_x': item.get_center().x,
                     'position_y': item.get_center().y,
                     'color': item.get_fill()
                     })

    def save_as(self):
        try:
            self.filename = tkinter.filedialog.asksaveasfilename(
                filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*")))
            if not self.filename:
                return
            ext = self.filename[-4:]
            if ext != ".csv":
                self.filename = None
                raise ValueError("Неверное расширение файла")
        except ValueError:
            tkinter.messagebox.showwarning("Невозможно сохранить файл!", "Неверное расширение файла")
        self.save()

    def draw_intersections(self):
        triangle = self.triangle_manager.get(self.context.selected_triangle)
        if triangle:
            triangles = [v for k, v in self.triangle_manager.all().items() if k != self.context.selected_triangle]
            current_lines = Util.lines_from_path(triangle.path)
            intersection_points = []
            for p1, p2 in current_lines:
                for t in triangles:
                    other_lines = Util.lines_from_path(t.path)
                    for p3, p4 in other_lines:
                        intersection = Util.intersection_lines(*p1.data(), *p2.data(), *p3.data(), *p4.data())
                        if intersection is not None:
                            intersection_points.append(intersection)

            self.canvas.delete("intersection")
            for p in intersection_points:
                Point(p.x, p.y, variant="circle", tags="intersection")

    def clear_canvas(self):
        self.triangle_manager.clear()
        self.canvas.delete("all")

    def change_color(self, color: str):
        triangle = self.triangle_manager.get(self.context.selected_triangle)
        if triangle:
            triangle.set_fill(color)

    def rotate_triangle(self, angle):
        radians = math.radians(angle)
        triangle = self.triangle_manager.get(self.context.selected_triangle)
        if triangle:
            triangle.rotate(radians)
            self.draw_intersections()

    def select_rotation_point(self, point):
        triangle = self.triangle_manager.get(self.context.selected_triangle)
        if triangle:
            triangle.select_rotation_point(point)

    def select_triangle(self, triangle_id):
        if self.context.selected_triangle != triangle_id:
            triangle = self.triangle_manager.get(self.context.selected_triangle)
            if triangle:
                triangle.unselect()
            self.context.selected_triangle = triangle_id
        triangle = self.triangle_manager.get(triangle_id)
        triangle.select()
        self.draw_intersections()
        self.context.color_control_state.color = triangle.get_fill()

    def on_left_click(self, event):
        # print(event.x, event.y)
        if self.context.tool_mode == "create":
            triangle = Triangle(*Vec2(event.x, event.y).data())
            self.triangle_manager.add(triangle)
            self.context.tool_mode = "select"
            self.select_triangle(triangle.id)

        elif self.context.tool_mode == "select":
            ids = list(self.canvas.find_overlapping(event.x, event.y, event.x,
                                                    event.y))
            for i in range(len(ids) - 1, -1, -1):
                triangle = self.triangle_manager.get(ids[i])
                if triangle:
                    if ids[i] == self.context.selected_triangle:
                        self.context.dragging_triangle = True
                        self.select_triangle(triangle.id)
                        return
                    self.select_triangle(triangle.id)
                    # print("Coords", triangle.get_coords())
                    self.context.selected_triangle = ids[i]
                    break
            else:
                triangle = self.triangle_manager.get(
                    self.context.selected_triangle)
                if triangle:
                    triangle.unselect()
                self.context.selected_triangle = None

            # print("Select", self.context.selected_triangle)

    def on_left_motion(self, event):
        if self.context.dragging_triangle:
            triangle = self.triangle_manager.get(self.context.selected_triangle)
            width = triangle.get_width()
            height = triangle.get_height()
            triangle.set_position(
                Vec2(event.x - width / 2, event.y - height / 2))

            self.draw_intersections()

    def on_left_release(self, event):
        if self.context.dragging_triangle:
            self.context.dragging_triangle = False


class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Треугольники')
        self.geometry('800x600')


def main():
    root = Window()
    app = App(root)
    app.mainloop()


if __name__ == '__main__':
    main()
