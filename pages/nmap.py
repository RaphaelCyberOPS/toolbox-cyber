import customtkinter as ctk
import subprocess
import ipaddress
import re
import json
import os
import threading
from tkinter import Label
from PIL import Image, ImageTk, ImageSequence

class NmapPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.is_request_pending = False
        self.loading_label = None
        self.loading_frames = []
        self.setup_ui()

    def setup_ui(self):
        # Set up the main canvas
        self.canvas = ctk.CTkCanvas(self, highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True)
        
        # Create a frame for the buttons
        button_frame = ctk.CTkFrame(self.canvas)
        self.canvas.create_window((0, 0), window=button_frame, anchor="nw")
        button_frame.pack(fill="y", side="left")

        # Define navigation buttons
        buttons = [
            ("Menu", lambda: self.controller.show_frame("MenuPage")),
            ("Network", lambda: self.controller.show_frame("NetworkPage")),
            ("Web", lambda: self.controller.show_frame("WebPage")),
            ("Nmap", lambda: self.controller.show_frame("NmapPage")),
            ("Map", lambda: self.controller.show_frame("MapPage")),
            ("Password", lambda: self.controller.show_frame("PasswordPage")),
            ("SSH", lambda: self.controller.show_frame("SSHPage")),
            ("PDF", lambda: self.controller.show_frame("PDFPage"))
        ]

        # Add navigation buttons to the button frame
        for text, command in buttons:
            btn = ctk.CTkButton(button_frame, text=text, command=command)
            btn.pack(fill="x", padx=10, pady=5)

        # Add a quit button
        quit_button = ctk.CTkButton(button_frame, text="Quitter", command=self.quit_app, fg_color="#d05e5e")
        quit_button.pack(fill="x", padx=10, pady=5)

        # Add labels and entry widget
        ctk.CTkLabel(self.canvas, text="Nmap Page", text_color="Black", font=(None, 20)).pack(side="top", pady=10, anchor="n")
        ctk.CTkLabel(self.canvas, text="Enter the target IP", text_color="Black", font=(None, 14)).pack(side="top", pady=10, anchor="n")

        self.entry = ctk.CTkEntry(self.canvas, placeholder_text="Enter the target IP")
        self.entry.pack(padx=200, pady=5)

        # Add a button to generate the report
        generate_button = ctk.CTkButton(self.canvas, text="Generate Report", command=self.generate_report)
        generate_button.pack(fill="x", padx=150, pady=5)

        # Set up loading animation
        self.setup_loading_animation()

    def setup_loading_animation(self):
        # Load the loading animation GIF
        self.loading_image = Image.open("asset/loading.gif")
        self.loading_frames = [ImageTk.PhotoImage(frame.copy()) for frame in ImageSequence.Iterator(self.loading_image)]
        self.loading_label = Label(self.canvas, bg="#f0f0f0")
        self.loading_label.pack_forget()  # Hide it initially

    def start_loading_animation(self):
        # Show and start the loading animation
        self.loading_label.pack(side="top", pady=10)
        self.animate_loading(0)

    def stop_loading_animation(self):
        # Stop and hide the loading animation
        self.loading_label.pack_forget()

    def animate_loading(self, frame_index):
        # Animate the loading GIF
        if not self.is_request_pending:
            return  # Stop animation if no request is pending
        
        frame_image = self.loading_frames[frame_index]
        self.loading_label.config(image=frame_image)
        self.loading_label.image = frame_image
        next_frame_index = (frame_index + 1) % len(self.loading_frames)
        self.loading_label.after(100, self.animate_loading, next_frame_index)

    def generate_report(self):
        # Start the scanning process
        if self.is_request_pending:
            return
        ip = self.entry.get()

        try:
            ipaddress.ip_address(ip)
            self.is_request_pending = True
            self.start_loading_animation()
            threading.Thread(target=self.perform_scan, args=(ip,)).start()
        except ValueError:
            self.show_error_message("Incorrect/unreachable IP!", self.canvas)
            self.stop_loading_animation()

    def perform_scan(self, ip):
        # Perform the scan and update the JSON file
        try:
            report = self.run_nmap_scan(ip)
            self.after(0, self.update_json, ip, report)
            print(json.dumps(report, indent=4))
        finally:
            self.is_request_pending = False
            self.after(0, self.stop_loading_animation)

    def run_nmap_scan(self, ip):
        # Run the Nmap scan and return the parsed results
        try:
            command = f"nmap -sV --script=vulners {ip} -p 0-10000"
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            return self.parse_nmap_output(result.stdout)
        except Exception as e:
            print(f"Failed to run Nmap: {e}")
            return []

    def parse_nmap_output(self, output):
        # Parse the Nmap output to extract service and CVE information
        service_pattern = re.compile(r'(\d+)/tcp\s+open\s+(\S+)\s+(.*)')
        cve_pattern = re.compile(r'(CVE-\d{4}-\d{4,5})\s+(\d+\.\d+)')
        services = []
        current_service = {}

        for line in output.split('\n'):
            service_match = service_pattern.search(line)
            if service_match:
                if current_service:
                    services.append(current_service)
                port, service, version = service_match.groups()
                current_service = {'service': service, 'port': port, 'version': version.strip(), 'CVE': []}
            elif current_service:
                cve_match = cve_pattern.findall(line)
                for cve, cvss in cve_match:
                    if float(cvss) >= 7.0:
                        current_service['CVE'].append(cve)

        if current_service:
            services.append(current_service)

        return services
    
    def update_json(self, ip, new_data):
        # Update the JSON file with the new scan data
        json_path = os.path.join(os.getcwd(), 'result.json')
        try:
            if os.path.exists(json_path):
                with open(json_path, 'r') as file:
                    data = json.load(file)
                if ip not in data:
                    data[ip] = {'nmap': []}
                data[ip]['nmap'] = new_data
            else:
                data = {ip: {'nmap': new_data}}
            with open(json_path, 'w') as file:
                json.dump(data, file, indent=4)
        except Exception as e:
            print(f"Error updating results file: {e}")

    def show_error_message(self, message, canvas):
        # Show an error message on the canvas
        label_error = ctk.CTkLabel(canvas, text=message, text_color="Red", font=(None, 11))
        label_error.pack(side="top", pady=10, anchor="n")
        self.after(3000, lambda: label_error.destroy())

    def reset_request_state(self):
        # Reset the request state
        self.is_request_pending = False

    def quit_app(self):
        # Quit the application
        self.is_request_pending = False
        self.controller.quit()