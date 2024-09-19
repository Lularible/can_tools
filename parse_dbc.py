
from my_cantools.src import cantools
import tkinter as tk  
from tkinter import filedialog, messagebox  

class CANViewerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('CAN DBC Viewer')
        self.geometry('1000x600')

        # Load DBC file
        self.load_dbc_file()

        # Create frames
        self.create_widgets()

    def load_dbc_file(self):
        root = tk.Tk()
        root.withdraw()

        file_path = filedialog.askopenfilename(
            title="Choose a dbc file",
            filetypes=[("DBC files", "*.dbc")]
        )

        if file_path:
            self.db = cantools.database.load_file(file_path)

    def create_widgets(self):
        # Frame for Search
        self.search_frame = tk.Frame(self)
        self.search_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        # Search for Signals

        self.signal_search_label = tk.Label(self.search_frame, text="Search Signals:")
        self.signal_search_label.pack(side=tk.LEFT, padx=5)
        self.signal_search_entry = tk.Entry(self.search_frame)
        self.signal_search_entry.pack(side=tk.LEFT, fill=tk.X, padx=5, expand=True)
        self.signal_search_entry.bind('<KeyRelease>', self.update_signal_list)

        # Frame for Signal List
        self.signal_frame = tk.Frame(self)
        self.signal_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.signal_listbox = tk.Listbox(self.signal_frame)
        self.signal_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.signal_listbox.bind('<Double-1>', self.show_signal_details)

        self.update_signal_list()

    def update_signal_list(self, event=None):
        search_term = self.signal_search_entry.get().lower()
        self.signal_listbox.delete(0, tk.END)
        for message in self.db.messages:
            for signal in message.signals:
                if search_term in signal.name.lower():
                    self.signal_listbox.insert(tk.END, f"{message.name}: {signal.name}")


    def show_signal_details(self, event=None):
        selected_signal_text = self.signal_listbox.get(tk.ACTIVE)
        if selected_signal_text:
            message_name, signal_name = selected_signal_text.split(": ")
            message = next((msg for msg in self.db.messages if msg.name == message_name), None)
            if message:
                signal = next((sig for sig in message.signals if sig.name == signal_name), None)
                if signal:
                    SignalDetailsWindow(message)


class SignalDetailsWindow(tk.Toplevel):  
    def __init__(self, message):  
        super().__init__()  
        self.title("Signal Details")  
        self.geometry("1000x800")  

        # Create a canvas for scrolling  
        self.canvas = tk.Canvas(self)  
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)  

        # Create a scrollbar  
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)  
        self.scrollbar.pack(side=tk.RIGHT, fill="y")  

        # Create a frame to hold all signal details  
        self.signal_frame = tk.Frame(self.canvas)  
        self.canvas.create_window((0, 0), window=self.signal_frame, anchor='nw')  

        # Configure the scrollbar  
        self.signal_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))  
        self.canvas.configure(yscrollcommand=self.scrollbar.set)  

        # Bind mouse wheel event for scrolling within this window  
        self.bind("<MouseWheel>", self.on_mouse_wheel)  

        self.signal_entries = {}  
        self.signals = message.signals
        self.message_id = hex(message.frame_id)
        self.populate_signals(self.signals)  

        # Add button to generate hexadecimal data  
        self.generate_button = tk.Button(self.signal_frame, text="Generate Hex Data", command=self.generate_hex_data)  
        self.generate_button.grid(row=0, column=15, padx=2, pady=5, sticky='e')  

        # Text box to display generated hex data  
        self.result_text = tk.Text(self.signal_frame, height=20, width=60)  
        self.result_text.grid(row=1, column=15, padx=2, pady=5, sticky='w')

    def populate_signals(self, signals):  
        self.signal_entries.clear()  # Clear previous entries if needed  

        row = 0  
        last_end_bit = -1  

        for signal in signals:  
            start_bit = signal.start  
            length = signal.length  
            min_val = signal.minimum if signal.minimum is not None else "N/A"  
            max_val = signal.maximum if signal.maximum is not None else "N/A"  
            default_value = str(signal.raw_initial) if signal.raw_initial is not None else "0"  

            if start_bit > last_end_bit + 1:  
                reserved_start = last_end_bit + 1  
                reserved_end = start_bit - 1  
                reserved_description = f"Reserved Bits: {reserved_start} - {reserved_end}"  
                tk.Label(self.signal_frame, text=reserved_description, justify='left', font=("Arial", 10), borderwidth=1, relief="solid", anchor='w').grid(row=row, column=0, sticky='w', padx=5, pady=5, columnspan=3)  
                row += 1  

            description = f"Signal Name: {signal.name}\nMin: {min_val}\nMax: {max_val}\nBits: {start_bit} - {start_bit + length - 1}"  
            tk.Label(self.signal_frame, text=description, justify='left', font=("Arial", 10), borderwidth=1, relief="solid", anchor='w').grid(row=row, column=0, sticky='w', padx=5, pady=5, columnspan=3)  

            entry = tk.Entry(self.signal_frame, width=15)  
            entry.insert(0, default_value)  
            self.signal_entries[signal.name] = (start_bit, entry)  # Store bit position and the entry widget  
            entry.grid(row=row, column=3, padx=5, pady=5, sticky='w')  

            last_end_bit = start_bit + length - 1  
            row += 1  

        if last_end_bit < 31:  
            reserved_start = last_end_bit + 1  
            reserved_end = 31  
            reserved_description = f"Reserved Bits: {reserved_start} - {reserved_end}"  
            tk.Label(self.signal_frame, text=reserved_description, justify='left', font=("Arial", 10), borderwidth=1, relief="solid", anchor='w').grid(row=row, column=0, sticky='w', padx=5, pady=5, columnspan=3)  

    def on_mouse_wheel(self, event):  
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")  
        

    def generate_hex_data(self):  
        # Initialize an empty bitfield  
        bitfield = ""
        encounter_first_field = 0
        last_end_bit_value = -1
        cur_value = 0


        for signal_name, (start_bit, entry) in self.signal_entries.items():  
            # Get cur_value from entry and convert to integer  
            cur_value = int(entry.get())  
            # Ensure cur_value is within the valid range based on the signal length  
            length = next(signal.length for signal in self.signals if signal.name == signal_name)  
            max_value = (1 << length) - 1  # Maximum cur_value for this length  
            if cur_value < 0 or cur_value > max_value:
                root = tk.Tk()
                root.withdraw()
                messagebox.showerror('Error', 'The {}\'s value is out of range ({}-{})!'.format(signal_name, 0, max_value), parent=root)
                root.destroy()
                return

            # encounter reserved field
            # message is start with reserved bits
            if encounter_first_field == 0 and start_bit != 0:
                bitfield += self.int_to_binary_string(0, start_bit)
            encounter_first_field = 1

            # message's mid is reserved bits
            if last_end_bit_value != -1 and (start_bit - last_end_bit_value) > 1:
                bitfield += self.int_to_binary_string(0, start_bit - last_end_bit_value - 1)

            last_end_bit_value = start_bit + length - 1

            bitfield += self.int_to_binary_string(cur_value, length)

        # Pad the bitfield to ensure it meets the minimum size requirements  
        padding_bits_count = self.calculate_padding_bits_size(len(bitfield))
        if padding_bits_count > 0:
            bitfield += self.int_to_binary_string(0, self.calculate_padding_bits_size(len(bitfield)))

        # Convert bitfield into hexadecimal representation  
        hex_data = self.binary_string_to_hex_array(bitfield)  

        # Build result string for display  
        result_length = len(hex_data)  

        self.result_text.delete(1.0, tk.END)  # Clear previous content  
        self.result_text.insert(tk.END, f"message_id:{self.message_id}\nHex Data:[{', '.join(hex_data)}]\nLength: {result_length}")

    def calculate_padding_bits_size(self, length):  
        if length <= 64:  
            return 64 - length  
        elif length <= 96:  
            return 96 - length  
        elif length <= 128:  
            return 128 - length  
        elif length <= 160:  
            return 160 - length  
        elif length <= 192:  
            return 192 - length  
        elif length <= 256:  
            return 256 - length  
        elif length <= 384:  
            return 384 - length  
        elif length <= 512:  
            return 512 - length
        return 0  # No padding needed
    
    def int_to_binary_string(self, num, length):  
        return format(num, '0{}b'.format(length))  
    

    def binary_string_to_hex_array(self, binary_string):
        while len(binary_string) % 8 != 0:
            binary_string = '0' + binary_string
        
        hex_array = []
        for i in range(0, len(binary_string), 8):
            byte = binary_string[i:i+8]
            hex_value = int(byte, 2)
            hex_array.append(f'0x{hex_value:02x}')

        return hex_array


if __name__ == "__main__":
    app = CANViewerApp()
    app.mainloop()





