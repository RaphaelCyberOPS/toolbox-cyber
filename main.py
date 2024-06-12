import customtkinter as ctk
from pages.start import StartPage
from pages.menu import MenuPage
from pages.web import WebPage
from pages.network import NetworkPage
from pages.nmap import NmapPage
from pages.map import MapPage
from pages.password import PasswordPage
from pages.ssh import SSHPage
from pages.pdf import PDFPage

class CustomTkinterApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Set window title and size
        self.title("ToolBox @HackMeRaphael")
        self.geometry("800x600")

        # Current language attribute
        self.current_language = "en"

        # Create the main container frame
        self.container = ctk.CTkFrame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Dictionary to hold the different page classes
        self.frames = {
            "StartPage": StartPage,
            "MenuPage": MenuPage,
            "NetworkPage": NetworkPage,
            "WebPage": WebPage,
            "NmapPage": NmapPage,
            "MapPage": MapPage,
            "PasswordPage": PasswordPage,
            "SSHPage": SSHPage,
            "PDFPage": PDFPage         
        }

        self.current_frame = None  # Initialize the current frame to None

        # Create language buttons
        self.create_language_buttons()

        self.show_frame("StartPage")  # Show the start page initially

    def create_language_buttons(self):
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(side="top", fill="x")

        english_button = ctk.CTkButton(button_frame, text="English", command=lambda: self.set_language("en"))
        english_button.pack(side="left")

        french_button = ctk.CTkButton(button_frame, text="Français", command=lambda: self.set_language("fr"))
        french_button.pack(side="left")

    # Method to set the language
    def set_language(self, lang):
        self.current_language = lang
        self.show_frame("StartPage")  # Reload the current page to reflect the language change

    # Method to show a frame for the given page name
    def show_frame(self, page_name):
        if page_name in self.frames:
            if self.current_frame:
                self.current_frame.destroy()  # Destroy the current frame
            FrameClass = self.frames[page_name]
            self.current_frame = FrameClass(parent=self.container, controller=self)
            self.current_frame.pack(fill="both", expand=True)  # Show the new frame
        else:
            print(f"Error: Page '{page_name}' not found")

# Create and start the application
app = CustomTkinterApp()
app.mainloop()
