import tkinter as tk
from tkinter import ttk

from utils.config import config


class PreferUI:
    def init_ui(self, root=None):
        """
        Init prefer UI
        """
        config_options = [
            {"label_text": f"结果来源优先{i + 1}:", "combo_box_value": value}
            for i, value in enumerate(self.get_origin_type_prefer_index(config.origin_type_prefer))
        ]
        self.origin_type_prefer_options = []
        for config_option in config_options:
            option = ConfigOption(root, **config_option)
            option.combo_box.bind(
                "<<ComboboxSelected>>",
                option.update_select,
            )
            option.entry.bind("<KeyRelease>", option.update_input)
            self.origin_type_prefer_options.append(option)

        frame_prefer_ipv_type = tk.Frame(root)
        frame_prefer_ipv_type.pack(fill=tk.X)
        self.prefer_ipv_type_label = tk.Label(
            frame_prefer_ipv_type, text="结果协议优先:", width=12
        )
        self.prefer_ipv_type_label.pack(side=tk.LEFT, padx=4, pady=8)
        self.prefer_ipv_type_combo = ttk.Combobox(frame_prefer_ipv_type)
        self.prefer_ipv_type_combo.pack(side=tk.LEFT, padx=4, pady=8)
        self.prefer_ipv_type_combo["values"] = ("IPv4", "IPv6", "自动")
        ipv_type_prefer = config.ipv_type_prefer
        if ipv_type_prefer[0] == "ipv4":
            self.prefer_ipv_type_combo.current(0)
        elif ipv_type_prefer[0] == "ipv6":
            self.prefer_ipv_type_combo.current(1)
        else:
            self.prefer_ipv_type_combo.current(2)
        self.prefer_ipv_type_combo.bind(
            "<<ComboboxSelected>>", self.update_ipv_type_prefer
        )
        self.ipv_type_input = []
        for ipv_type in ["ipv4", "ipv6"]:
            input = IpvNumInput(root, ipv_type)
            input.entry.bind("<KeyRelease>", input.update_input)
            self.ipv_type_input.append(input)

        frame_prefer_open_supply = tk.Frame(root)
        frame_prefer_open_supply.pack(fill=tk.X)
        self.open_supply_label = tk.Label(
            frame_prefer_open_supply, text="开启补偿模式:", width=12
        )
        self.open_supply_label.pack(side=tk.LEFT, padx=4, pady=8)
        self.open_supply_var = tk.BooleanVar(value=config.open_supply)
        self.open_supply_checkbutton = ttk.Checkbutton(
            frame_prefer_open_supply,
            variable=self.open_supply_var,
            onvalue=True,
            offvalue=False,
            command=self.update_open_supply,
        )
        self.open_supply_checkbutton.pack(side=tk.LEFT, padx=4, pady=8)

    def get_origin_type_prefer_index(self, origin_type_prefer):
        index_list = [None, None, None, None]
        origin_type_prefer_obj = {
            "hotel": 0,
            "multicast": 1,
            "subscribe": 2,
            "online_search": 3,
        }
        for i, item in enumerate(origin_type_prefer):
            index_list[i] = origin_type_prefer_obj[item]
        return index_list

    def update_ipv_type_prefer(self, event):
        config.set(
            "Settings",
            "ipv_type_prefer",
            self.prefer_ipv_type_combo.get(),
        )

    def update_open_supply(self):
        config.set("Settings", "open_supply", str(self.open_supply_var.get()))

    def change_entry_state(self, state):
        for option in self.origin_type_prefer_options:
            option.change_state(state)
        self.prefer_ipv_type_combo.config(state=state)
        for input in self.ipv_type_input:
            input.change_state(state)
        self.open_supply_checkbutton.config(state=state)


class IpvNumInput:
    def __init__(self, master, ipv_type):
        self.master = master
        self.ipv_type = ipv_type
        self.frame = tk.Frame(master)
        self.frame.pack(fill=tk.X)
        self.frame_column1 = tk.Frame(self.frame)
        self.frame_column1.pack(side=tk.LEFT, fill=tk.Y)
        self.frame_column2 = tk.Frame(self.frame)
        self.frame_column2.pack(side=tk.RIGHT, fill=tk.Y)

        ipv_type_text = "IPv4" if ipv_type == "ipv4" else "IPv6"
        self.entry_label = tk.Label(
            self.frame_column1, text=f"{ipv_type_text}数量:", width=12
        )
        self.entry_label.pack(side=tk.LEFT, padx=4, pady=8)

        self.entry = tk.Entry(self.frame_column1)
        self.entry.insert(0, config.ipv_limit[ipv_type])
        self.entry.pack(side=tk.LEFT, padx=4, pady=8)

    def update_input(self, event):
        config.set(
            "Settings",
            f"{self.ipv_type}_num",
            self.entry.get(),
        )

    def change_state(self, state):
        self.entry.config(state=state)


class ConfigOption:
    def __init__(self, master, label_text, combo_box_value):
        self.master = master
        self.label_text = label_text
        self.combo_box_value = combo_box_value

        self.frame = tk.Frame(master)
        self.frame.pack(fill=tk.X)

        self.column1 = tk.Frame(self.frame)
        self.column1.pack(side=tk.LEFT, fill=tk.Y)

        self.column2 = tk.Frame(self.frame)
        self.column2.pack(side=tk.RIGHT, fill=tk.Y)

        self.label = tk.Label(self.column1, text=label_text, width=12)
        self.label.pack(side=tk.LEFT, padx=4, pady=8)

        self.combo_box = ttk.Combobox(self.column1)
        self.origin_type_prefer_obj = {
            "酒店源": "hotel",
            "组播源": "multicast",
            "订阅源": "subscribe",
            "关键字搜索": "online_search",
        }
        combo_box_values_name = list(self.origin_type_prefer_obj.keys())
        self.combo_box["values"] = combo_box_values_name
        self.combo_box.pack(side=tk.LEFT, padx=4, pady=8)
        origin_type_prefer = config.origin_type_prefer
        if not origin_type_prefer or combo_box_value is None:
            self.combo_box.current(None)
        else:
            self.combo_box.current(combo_box_value)

        self.entry_label = tk.Label(self.column2, text="数量:", width=12)
        self.entry_label.pack(side=tk.LEFT, padx=4, pady=8)

        self.entry = tk.Entry(self.column2)
        if origin_type_prefer and combo_box_value is not None:
            self.entry.insert(
                0,
                config.source_limits[self.origin_type_prefer_obj[self.combo_box.get()]],
            )
        self.entry.pack(side=tk.LEFT, padx=4, pady=8)

    def update_select(self, key):
        origin_type_prefer_list = [item.lower() for item in config.origin_type_prefer]
        select_value = self.origin_type_prefer_obj[
            self.combo_box.get()
        ]
        if self.combo_box_value < len(origin_type_prefer_list):
            origin_type_prefer_list[self.combo_box_value] = select_value
        else:
            origin_type_prefer_list.append(select_value)
        config.set(
            "Settings",
            "origin_type_prefer",
            ",".join(origin_type_prefer_list),
        )

    def update_input(self, event):
        config.set(
            "Settings",
            f"{self.origin_type_prefer_obj[self.combo_box.get()]}_num",
            self.entry.get(),
        )

    def change_state(self, state):
        self.combo_box.config(state=state)
        self.entry.config(state=state)
