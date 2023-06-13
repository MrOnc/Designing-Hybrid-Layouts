#derecelerin yazıldığı yer değiştirilmeli (1. iterasyon)
import tkinter as tk
from tkinter import ttk


class TesisPlanlama(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry("800x800")
        self.title("Tesis Planlama Hesaplama")

        self.mezun_duzenler = tk.Button(self, text="Melez Düzenlerin Tasarlanması", command=self.open_mezun_duzenler)
        self.mezun_duzenler.pack(pady=20)

    def open_mezun_duzenler(self):
        MezunDuzenler(self)


class MezunDuzenler(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)

        self.title("Melez Düzenlerin Tasarlanması")
        self.geometry("1400x800")

        self.table_frame = tk.Frame(self)
        self.table_frame.pack(side="left", padx=10, pady=10)

        self.column_count = 10
        self.row_count = 10
        self.create_table()

        self.adjust_buttons_frame = tk.Frame(self)
        self.adjust_buttons_frame.pack(side="left", padx=10, pady=10)

        self.add_row_button = tk.Button(self.adjust_buttons_frame, text="Satır Ekle", command=self.add_row)
        self.add_row_button.pack(side="top", pady=5)

        self.add_column_button = tk.Button(self.adjust_buttons_frame, text="Sütun Ekle", command=self.add_column)
        self.add_column_button.pack(side="top", pady=5)
        self.calculate_button = tk.Button(self.adjust_buttons_frame, text="Hesapla", command=self.calculate)
        self.calculate_button.pack(side="top", pady=5)
        self.remove_row_button = tk.Button(self.adjust_buttons_frame, text="Satır Sil", command=self.remove_row)
        self.remove_row_button.pack(side="top", pady=5)

        self.remove_column_button = tk.Button(self.adjust_buttons_frame, text="Sütun Sil", command=self.remove_column)
        self.remove_column_button.pack(side="top", pady=5)


    def create_table(self):
        self.entries = []
        for i in range(self.row_count):
            row = []
            for j in range(self.column_count):
                entry = tk.Entry(self.table_frame, width=10)
                entry.grid(row=i + 1, column=j + 2)
                row.append(entry)
            self.entries.append(row)
        for i in range(self.row_count):
            label = tk.Label(self.table_frame, text=f"Makine {i + 1}")
            label.grid(row=i + 1, column=0)
            label.bind("<Button-1>", lambda e, i=i: self.edit_label(e, i))
        for j in range(self.column_count):
            label = tk.Label(self.table_frame, text=f"Parça {j + 1}")
            label.grid(row=0, column=j + 2)
            label.bind("<Button-1>", lambda e, j=j: self.edit_label(e, j, is_row=False))
        self.create_two_pow_i_column()

    def create_two_pow_i_column(self):
        two_pow_i_label = tk.Label(self.table_frame, text="2^i")
        two_pow_i_label.grid(row=0, column=1)
        self.two_pow_i_entries = []
        for i in range(self.row_count):
            entry = tk.Entry(self.table_frame, width=10, bg="yellow")
            entry.grid(row=i + 1, column=1)
            self.two_pow_i_entries.append(entry)

    def edit_label(self, event, index, is_row=True):
            label = event.widget
            current_text = label["text"]
            new_text = tk.simpledialog.askstring("Düzenle", f"{current_text} adını girin:")
            if new_text:
                label["text"] = new_text

    def add_row(self):
            self.row_count += 1
            row = []
            for j in range(self.column_count):
                entry = tk.Entry(self.table_frame, width=10)
                entry.grid(row=self.row_count, column=j + 1)
                row.append(entry)
            self.entries.append(row)

            label = tk.Label(self.table_frame, text=f"Makine {self.row_count}")
            label.grid(row=self.row_count, column=0)
            label.bind("<Button-1>", lambda e, i=self.row_count - 1: self.edit_label(e, i))

            entry = tk.Entry(self.table_frame, width=10, bg="yellow")
            entry.grid(row=self.row_count, column=self.column_count + 1)
            self.two_pow_i_entries.append(entry)

    def add_column(self):
        self.column_count += 1
        for i, row in enumerate(self.entries):
            entry = tk.Entry(self.table_frame, width=10)
            entry.grid(row=i + 1, column=self.column_count)
            row.insert(-1, entry)
        label = tk.Label(self.table_frame, text=f"Parça {self.column_count}")
        label.grid(row=0, column=self.column_count)
        label.bind("<Button-1>", lambda e, j=self.column_count - 1: self.edit_label(e, j, is_row=False))
    def calculate(self):
        wj_values = self.calculate_wj_values()
        self.display_wj_values(wj_values)  # wj değerlerini göster
        degrees = self.calculate_degrees(wj_values)
        self.display_degrees(degrees)
        self.open_iteration(degrees)
    def calculate_wj_values(self):
        wj_values = [0] * self.column_count
        for j in range(self.column_count):
            for i in range(self.row_count):
                cell_value = int(self.entries[i][j].get()) if self.entries[i][j].get() else 0
                two_pow_i_value = int(self.two_pow_i_entries[i].get()) if self.two_pow_i_entries[i].get() else 0
                wj_values[j] += cell_value * two_pow_i_value
        return wj_values
    def calculate_degrees(self, wj_values):
        sorted_wj_values = sorted(set(wj_values))
        degrees = [sorted_wj_values.index(wj_value) + 1 for wj_value in wj_values]
        return degrees
    def display_wj_values(self, wj_values):
        wj_label = tk.Label(self.table_frame, text="Wj")
        wj_label.grid(row=self.row_count + 1, column=0)

        for j, wj_value in enumerate(wj_values):
            label = tk.Label(self.table_frame, text=str(wj_value))
            label.grid(row=self.row_count + 1, column=j + 1)
    def calculate_degrees(self, wj_values):
        sorted_wj_values = sorted(wj_values)
        degrees = [sorted_wj_values.index(wj_value) + 1 for wj_value in wj_values]
        return degrees
    def display_degrees(self, degrees):
        degree_label = tk.Label(self.table_frame, text="Derece")
        degree_label.grid(row=self.row_count + 2, column=0)

        for j, degree in enumerate(degrees):
            label = tk.Label(self.table_frame, text=str(degree))
            label.grid(row=self.row_count + 2, column=j + 1)
    def remove_row(self):
        if self.row_count > 1:
            for entry in self.entries[-1]:
                entry.destroy()
            self.entries.pop()

            self.two_pow_i_entries[-1].destroy()
            self.two_pow_i_entries.pop()

            label = self.table_frame.grid_slaves(row=self.row_count, column=0)[0]
            label.destroy()

            self.row_count -= 1

    def remove_column(self):
        if self.column_count > 1:
            for row in self.entries:
                row[-1].destroy()
                row.pop()

            label = self.table_frame.grid_slaves(row=0, column=self.column_count)[0]
            label.destroy()

            self.column_count -= 1
    def open_iteration(self, degrees):
        Iteration(self, degrees)
class Iteration(tk.Toplevel):
    def __init__(self, master, degrees):
        super().__init__(master)
        self.title("1. İterasyon")
        self.geometry("1400x1400")
        self.table_frame = tk.Frame(self)
        self.table_frame.pack(side="left", padx=10, pady=10)
        self.row_count = master.row_count
        self.column_count = master.column_count
        self.entries = []
        for i in range(self.row_count):
            row = []
            for j in range(self.column_count):
                entry = tk.Entry(self.table_frame, width=10)
                entry.grid(row=i + 2, column=j + 2)  
                row.append(entry)
            self.entries.append(row)
        for i in range(self.row_count):
            label = tk.Label(self.table_frame, text=f"Makine {i + 1}")
            label.grid(row=i + 2, column=0)  
        degree_sorted_indexes = sorted(range(len(degrees)), key=lambda k: degrees[k])
        for j, index in enumerate(degree_sorted_indexes):
            label = tk.Label(self.table_frame, text=master.table_frame.grid_slaves(row=0, column=index + 2)[0]["text"])
            label.grid(row=0, column=j + 2)
            for i in range(self.row_count):
                self.entries[i][j].insert(0, master.entries[i][index].get())
        two_pow_j_label = tk.Label(self.table_frame, text="2^j")
        two_pow_j_label.grid(row=1, column=1)  
        self.two_pow_j_entries = []
        for j in range(self.column_count):
            entry = tk.Entry(self.table_frame, width=10, bg="yellow")
            entry.grid(row=1, column=j + 2)  
            entry.insert(0, 2**(j + 1))
            self.two_pow_j_entries.append(entry)   
        self.calculate_button = tk.Button(self.table_frame, text="Hesapla", command=self.open_second_iteration)
        self.calculate_button.grid(row=self.row_count + 3, column=self.column_count + 2)

        self.calculate_wi_values()
        self.display_wi_values()
        self.machine_degrees = self.calculate_machine_degrees()
        self.display_machine_degrees()
    def calculate_wi_values(self):
        self.wi_values = [0] * self.row_count
        for i in range(self.row_count):
            for j in range(self.column_count):
                cell_value = int(self.entries[i][j].get()) if self.entries[i][j].get() else 0
                two_pow_j_value = int(self.two_pow_j_entries[j].get()) if self.two_pow_j_entries[j].get() else 0
                self.wi_values[i] += cell_value * two_pow_j_value
    def display_wi_values(self):
        wi_label = tk.Label(self.table_frame, text="Wi")
        wi_label.grid(row=0, column=self.column_count + 2)        
        for i, wi_value in enumerate(self.wi_values):
            entry = tk.Entry(self.table_frame, width=10)
            entry.grid(row=i + 2, column=self.column_count + 2)
            entry.insert(0, wi_value)
    def calculate_machine_degrees(self):
        sorted_wi_values = sorted(self.wi_values)
        machine_degrees = [sorted_wi_values.index(wi_value) + 1 for wi_value in self.wi_values]
        return machine_degrees
    def display_machine_degrees(self):
        degree_label = tk.Label(self.table_frame, text="Derece")
        degree_label.grid(row=1, column=self.column_count + 3)  
        for i, degree in enumerate(self.machine_degrees):
            label = tk.Label(self.table_frame, text=str(degree))
            label.grid(row=i + 2, column=self.column_count + 3)  
    def open_second_iteration(self):
        second_iteration = SecondIteration(self)
        second_iteration.mainloop()
class SecondIteration(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("2. İterasyon-Sütun")
        self.geometry("1400x1400")
        self.table_frame = tk.Frame(self)
        self.table_frame.pack(side="left", padx=10, pady=10)
        self.row_count = master.row_count
        self.column_count = master.column_count
        self.entries = []
        self.calculate_button = tk.Button(self.table_frame, text="Hesapla", command=self.open_third_iteration)
        self.calculate_button.grid(row=self.row_count + 4, column=self.column_count + 3)
       

        # Reorder the machines based on their degree
        self.degree_machine_order = sorted(range(len(master.machine_degrees)), key=lambda k: master.machine_degrees[k])

        for i in range(self.row_count):
            row = []
            for j in range(self.column_count):
                entry = tk.Entry(self.table_frame, width=10)
                entry.grid(row=i + 2, column=j + 3)  # Update the column index
                row.append(entry)
            self.entries.append(row)

        for i, machine_index in enumerate(self.degree_machine_order):
            label = tk.Label(self.table_frame, text=f"Makine {machine_index + 1}")
            label.grid(row=i + 2, column=0)

        for j in range(self.column_count):
            label = tk.Label(self.table_frame, text=master.table_frame.grid_slaves(row=0, column=j + 2)[0]["text"])
            label.grid(row=0, column=j + 3)  # Update the column index
            for i, machine_index in enumerate(self.degree_machine_order):
                self.entries[i][j].insert(0, master.entries[machine_index][j].get())

        # Add the "2^i" label and fill the column with 2's powers
        two_pow_i_label = tk.Label(self.table_frame, text="2^i")
        two_pow_i_label.grid(row=1, column=1)
        self.two_pow_i_entries = []
        for i in range(self.row_count):
            entry = tk.Entry(self.table_frame, width=10, bg="yellow")
            entry.grid(row=i + 2, column=1)
            entry.insert(0, 2**(i + 1))
            self.two_pow_i_entries.append(entry)
        self.calculate_wj_values()
        self.display_wj_values()
        self.part_degrees = self.calculate_part_degrees()
        self.display_part_degrees()
    def open_third_iteration(self):
        third_iteration = ThirdIteration(self)
        third_iteration.mainloop()
    def calculate_wj_values(self):
        self.wj_values = [0] * self.column_count
        for j in range(self.column_count):
            for i in range(self.row_count):
                cell_value = int(self.entries[i][j].get()) if self.entries[i][j].get() else 0
                two_pow_i_value = int(self.two_pow_i_entries[i].get()) if self.two_pow_i_entries[i].get() else 0
                self.wj_values[j] += cell_value * two_pow_i_value


    def display_wj_values(self):
        wj_label = tk.Label(self.table_frame, text="Wj")
        wj_label.grid(row=self.row_count + 2, column=0)
        for j, wj_value in enumerate(self.wj_values):
            entry = tk.Entry(self.table_frame, width=10)
            entry.grid(row=self.row_count + 2, column=j + 3)
            entry.insert(0, wj_value)

    def calculate_part_degrees(self):
        sorted_wj_values = sorted(self.wj_values)
        part_degrees = [sorted_wj_values.index(wj_value) + 1 for wj_value in self.wj_values]
        return part_degrees

    def display_part_degrees(self):
        degree_label = tk.Label(self.table_frame, text="Derece")
        degree_label.grid(row=self.row_count + 3, column=0)
        for j, degree in enumerate(self.part_degrees):
            label = tk.Label(self.table_frame, text=str(degree))
            label.grid(row=self.row_count + 3, column=j + 3)
        # Rest of the code should be similar to the `Iteration` class
class ThirdIteration(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("2. İterasyon - Satır")
        self.geometry("1400x1400")
        self.table_frame = tk.Frame(self)
        self.table_frame.pack(side="left", padx=10, pady=10)
        self.row_count = master.row_count
        self.column_count = master.column_count
        self.entries = []

        # Use the same machine order as in SecondIteration
        degree_machine_order = master.degree_machine_order

        for i in range(self.row_count):
            row = []
            for j in range(self.column_count):
                entry = tk.Entry(self.table_frame, width=10)
                entry.grid(row=i + 2, column=j + 3)
                row.append(entry)
            self.entries.append(row)

        for i, machine_index in enumerate(degree_machine_order):
            label = tk.Label(self.table_frame, text=f"Makine {machine_index + 1}")
            label.grid(row=i + 2, column=0)

        # Reorder the parts based on their degree
        degree_part_order = sorted(range(len(master.part_degrees)), key=lambda k: master.part_degrees[k])

        for j, part_index in enumerate(degree_part_order):
            label = tk.Label(self.table_frame, text=master.table_frame.grid_slaves(row=0, column=part_index + 3)[0]["text"])
            label.grid(row=0, column=j + 3)
            for i, machine_index in enumerate(degree_machine_order):
                self.entries[i][j].insert(0, master.entries[machine_index][part_index].get())

        # Add the "2^j" row and fill the row with 2's powers
        two_pow_j_label = tk.Label(self.table_frame, text="2^j")
        two_pow_j_label.grid(row=self.row_count + 2, column=1)
        self.two_pow_j_entries = []
        for j in range(self.column_count):
            entry = tk.Entry(self.table_frame, width=10, bg="yellow")
            entry.grid(row=self.row_count + 2, column=j + 3)
            entry.insert(0, 2**(j + 1))
            self.two_pow_j_entries.append(entry)

        self.calculate_wi_values()
        self.display_wi_values()
        self.machine_degrees = self.calculate_machine_degrees()
        self.display_machine_degrees()



if __name__ == "__main__":
    app = TesisPlanlama()
    app.mainloop()

