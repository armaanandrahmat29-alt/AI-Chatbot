import tkinter as tk
from tkinter import filedialog, messagebox, ttk

class NoWaterAIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("no water AI")
        self.root.geometry("850x600")
        self.root.configure(bg="#202123")

        # State Variables
        self.is_pro = tk.BooleanVar(value=False)
        self.message_count = 0
        self.max_normal_messages = 30
        self.chat_history_data = []

        self.setup_styles()
        self.create_widgets()
        self.start_new_chat()

    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TCheckbutton", background="#202123", foreground="white", font=("Arial", 11))

    def create_widgets(self):
        # ---------------- SIDEBAR ----------------
        self.sidebar = tk.Frame(self.root, bg="#171717", width=220)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)

        # App Title
        title_label = tk.Label(self.sidebar, text="no water AI", bg="#171717", fg="#ffffff", font=("Arial", 16, "bold"))
        title_label.pack(pady=20, padx=10, anchor="w")

        # New Chat Button (Available for both versions)
        self.new_chat_btn = tk.Button(
            self.sidebar, text="+ New Chat", bg="#343541", fg="white", 
            font=("Arial", 11, "bold"), bd=0, cursor="hand2", command=self.start_new_chat
        )
        self.new_chat_btn.pack(fill=tk.X, padx=15, pady=10)

        # Pro Version Toggle Switch
        self.pro_toggle = tk.Checkbutton(
            self.sidebar, text="💎 Activate Pro Mode", variable=self.is_pro,
            onvalue=True, offvalue=False, bg="#171717", fg="#e2e8f0",
            selectcolor="#202123", activebackground="#171717", activeforeground="white",
            font=("Arial", 11), command=self.toggle_version_mode
        )
        self.pro_toggle.pack(anchor="w", padx=15, pady=15)

        # File Upload Section (Normal version perk)
        self.upload_frame = tk.LabelFrame(self.sidebar, text="Upload Attachments", bg="#171717", fg="#9ca3af", font=("Arial", 9))
        self.upload_frame.pack(fill=tk.X, padx=15, pady=20)

        self.btn_upload_file = tk.Button(
            self.upload_frame, text="📁 Post UPD / Document", bg="#2d2d30", fg="white",
            bd=0, cursor="hand2", font=("Arial", 10), command=lambda: self.handle_upload("Document/UPD")
        )
        self.btn_upload_file.pack(fill=tk.X, padx=10, pady=5)

        self.btn_upload_video = tk.Button(
            self.upload_frame, text="🎬 Post Video", bg="#2d2d30", fg="white",
            bd=0, cursor="hand2", font=("Arial", 10), command=lambda: self.handle_upload("Video")
        )
        self.btn_upload_video.pack(fill=tk.X, padx=10, pady=5)

        # Status Label
        self.status_label = tk.Label(self.sidebar, text="Mode: Normal (0/30)", bg="#171717", fg="#10b981", font=("Arial", 10))
        self.status_label.pack(side=tk.BOTTOM, pady=15)

        # ---------------- MAIN CHAT WINDOW ----------------
        self.main_container = tk.Frame(self.root, bg="#202123")
        self.main_container.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Chat display area
        self.chat_display = tk.Text(self.main_container, bg="#202123", fg="#ececf1", font=("Arial", 12), wrap=tk.WORD, bd=0, padx=15, pady=15)
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        self.chat_display.config(state=tk.DISABLED)

        # Message input area container
        self.input_container = tk.Frame(self.main_container, bg="#202123")
        self.input_container.pack(fill=tk.X, side=tk.BOTTOM, padx=20, pady=20)

        self.message_input = tk.Entry(self.input_container, bg="#40414f", fg="white", insertbackground="white", font=("Arial", 12), bd=0, relief=tk.FLAT)
        self.message_input.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=12, padx=(0, 10))
        self.message_input.bind("<Return>", lambda event: self.send_message())

        self.send_btn = tk.Button(self.input_container, text="Send", bg="#19c37d", fg="white", font=("Arial", 11, "bold"), bd=0, cursor="hand2", padx=15, command=self.send_message)
        self.send_btn.pack(side=tk.RIGHT, ipady=8)

    def append_chat(self, sender, message):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"{sender}: {message}\n\n")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)

    def start_new_chat(self):
        """Clears the current window and resets counters for a fresh chat session."""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete('1.0', tk.END)
        self.chat_display.config(state=tk.DISABLED)
        self.message_count = 0
        self.update_status_bar()
        self.append_chat("System", "Started a clean chat room. How can no water AI assist you today?")

    def toggle_version_mode(self):
        self.start_new_chat()
        if self.is_pro.get():
            self.upload_frame.pack_forget()  # Hide upload items in Pro mode if requested
            self.append_chat("no water AI (PRO)", "Pro Mode Activated! Enjoy unlimited messages and hyper-advanced AI help algorithms.")
        else:
            self.upload_frame.pack(fill=tk.X, padx=15, pady=20)
            self.append_chat("no water AI (Normal)", "Switched to Normal Mode. You have a limit of 30 text messages, but file/video posting is ready.")
        self.update_status_bar()

    def update_status_bar(self):
        if self.is_pro.get():
            self.status_label.config(text="Mode: Premium Pro (🔏 Unlimited)", fg="#a855f7")
        else:
            remaining = self.max_normal_messages - self.message_count
            self.status_label.config(text=f"Mode: Normal ({self.message_count}/{self.max_normal_messages} Sent)", fg="#10b981")

    def handle_upload(self, file_type):
        """Allows posting UPD files/documents and videos in the Normal tier."""
        file_path = filedialog.askopenfilename(title=f"Select {file_type} to Post")
        if file_path:
            file_name = file_path.split("/")[-1]
            self.append_chat("You", f"[Posted {file_type} File]: {file_name}")
            # Mocking AI help response to data attachment
            ai_response = f"Successfully parsed your uploaded {file_type} ({file_name}). I am processing this data to assist you!"
            self.append_chat("no water AI", ai_response)

    def send_message(self):
        user_text = self.message_input.get().strip()
        if not user_text:
            return

        # Check limits on Normal tier
        if not self.is_pro.get() and self.message_count >= self.max_normal_messages:
            messagebox.showwarning("Limit Reached", "You have reached your 30-message limit on the Normal version.\nToggle 'Activate Pro Mode' for unlimited access.")
            return

        self.append_chat("You", user_text)
        self.message_input.delete(0, tk.END)

        if not self.is_pro.get():
            self.message_count += 1
            self.update_status_bar()
            ai_reply = f"This is a standard helpful answer to your prompt: '{user_text}'."
            self.append_chat("no water AI", ai_reply)
        else:
            # Pro Tier: Unlimited and handles advanced logic simulations
            ai_reply = f"[Advanced Reasoning Engine]: Analyzed context deeply. Here is your complex solution regarding: '{user_text}'."
            self.append_chat("no water AI (PRO)", ai_reply)

if __name__ == "__main__":
    root = tk.Tk()
    app = NoWaterAIApp(root)
    root.mainloop()
