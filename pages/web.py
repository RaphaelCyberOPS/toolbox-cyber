import customtkinter as ctk
from scapy.all import sr1, IP, TCP, send
import ipaddress
import subprocess
import re
import json
import os
import time
import threading
from tkinter import Label
from PIL import Image, ImageTk, ImageSequence

class WebPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.is_request_pending = False
        self.loading_label = None
        self.loading_frames = []
        self.setup_ui()

    def setup_ui(self):
        # Setup the main canvas
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
        for text, command in buttons:
            btn = ctk.CTkButton(button_frame, text=text, command=command)
            btn.pack(fill="x", padx=10, pady=5)

        # Add a quit button
        quit_button = ctk.CTkButton(button_frame, text="Quitter", command=self.quit_app, fg_color="#d05e5e")
        quit_button.pack(fill="x", padx=10, pady=5)

        # Add labels and entry field for target IP
        ctk.CTkLabel(self.canvas, text="Web Page", text_color="Black", font=(None, 20)).pack(side="top", pady=10, anchor="n")
        ctk.CTkLabel(self.canvas, text="WARNING ! Windows Defender can block the file nikto.pl, check if this is not the case", text_color="Red", font=(None, 14)).pack(side="top", pady=10, anchor="n")
        
        self.entry = ctk.CTkEntry(self.canvas, placeholder_text="Enter the target IP")
        self.entry.pack(padx=200, pady=5)

        # Button to generate report
        generate_button = ctk.CTkButton(self.canvas, text="Generate Report", command=self.run_scans)
        generate_button.pack(fill="x", padx=150, pady=5)

        self.setup_loading_animation()

    def setup_loading_animation(self):
        # Setup loading animation
        self.loading_image = Image.open("asset/loading.gif")
        self.loading_frames = [ImageTk.PhotoImage(frame.copy()) for frame in ImageSequence.Iterator(self.loading_image)]
        self.loading_label = Label(self.canvas, bg="#f0f0f0")
        self.loading_label.pack_forget()  # Hide it initially

    def start_loading_animation(self):
        # Start loading animation
        self.loading_label.pack(side="top", pady=10)
        self.animate_loading(0)

    def stop_loading_animation(self):
        # Stop loading animation
        self.loading_label.pack_forget()

    def animate_loading(self, frame_index):
        # Animate the loading gif
        if not self.is_request_pending:
            return  # Stop animation if no request is pending
        
        frame_image = self.loading_frames[frame_index]
        self.loading_label.config(image=frame_image)
        self.loading_label.image = frame_image
        next_frame_index = (frame_index + 1) % len(self.loading_frames)
        self.loading_label.after(100, self.animate_loading, next_frame_index)

    def run_scans(self):
        # Run scans when the button is clicked
        if self.is_request_pending:
            return
        ip = self.entry.get()

        try:
            ipaddress.ip_address(ip)
            self.is_request_pending = True
            self.start_loading_animation()
            threading.Thread(target=self.perform_scans, args=(ip,)).start()
        except ValueError:
            self.show_error_message("Incorrect/unreachable IP!", self.canvas)
            self.stop_loading_animation()

    def perform_scans(self, ip):
        # Perform the actual scans
        try:
            ports_and_services = self.scan_with_nmap(ip)
            self.handle_services(ip, ports_and_services)
        finally:
            self.is_request_pending = False
            self.stop_loading_animation()

    def scan_with_nmap(self, ip):
        # Scan the target IP with nmap
        command = ["nmap", ip]
        result = subprocess.run(command, capture_output=True, text=True)
        output = result.stdout
        
        ports_services = {}
        for line in output.split("\n"):
            match = re.search(r"(\d+)/tcp\s+open\s+([\w\s]+)", line)
            if match:
                port = int(match.group(1))
                service = match.group(2).strip()
                ports_services[port] = service
        return ports_services

    def handle_services(self, ip, ports_and_services):
        # Handle the services found in the scan
        web_ports = {}
        http_services = {'http', 'apache', 'nginx', 'http-alt', 'http-proxy', 'https', 'apache2', 'apache-ssl'}
        for port, service in ports_and_services.items():
            if any(http_service in service.lower() for http_service in http_services):
                web_ports[port] = service
        if web_ports:
            threads = []
            for port, service in web_ports.items():
                thread = threading.Thread(target=self.run_web_scans, args=(ip, port, service))
                threads.append(thread)
                thread.start()
            
            for thread in threads:
                thread.join()
        else:
            print("No web server found!")
            self.show_error_message("No web server found on this target!", self.canvas)

    def run_web_scans(self, ip, port, service):
        # Run web scans using sqlmap and nikto
        sqlmap_output = self.test_sql_injection(ip, port)
        nikto_output = self.run_nikto_scan(ip, port)
        self.collect_and_update_results(ip, port, service, sqlmap_output, nikto_output)

    def parse_nikto_output(self, output):
        # Parse the output of nikto scan
        lines = output.split('\n')
        cve_patterns = re.compile(r'CVE-\d{4}-\d{4,7}')
        cve_lines = [cve_patterns.search(line).group(0) for line in lines if 'CVE' in line and cve_patterns.search(line)]
        return cve_lines
    
    def parse_sqlmap_output(self, output):
        # Parse the output of sqlmap scan
        critical_lines = []
        for line in output.split('\n'):
            if "[CRITICAL]" in line:
                part = line.split("[CRITICAL] ", 1)[-1]
                if part:
                    critical_lines.append(part)

        return ' '.join(critical_lines)

    def test_sql_injection(self, ip, port):
        # Test for SQL injection using sqlmap
        print("Starting sqlmap on port: " + str(port))
        path_to_sqlmap = "./sqlmap-dev/sqlmap.py"
        url = f"http://{ip}:{port}"
        command = f"python {path_to_sqlmap} -u {url} --batch --level=5 --risk=3 --threads=10 --tamper=space2comment --random-agent -v 0"
        start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        try:
            result = subprocess.run(command, shell=True, text=True, capture_output=True)
            end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            detected = "injection not detected" not in result.stdout
            output = self.parse_sqlmap_output(result.stdout)
            return {"detected": detected, "start_time": start_time, "end_time": end_time, "output": output}
        except Exception as e:
            print(f"Error running sqlmap: {str(e)}")
            return {"detected": False, "start_time": start_time, "end_time": end_time, "output": str(e)}

    def run_nikto_scan(self, ip, port):
        # Run nikto scan on the target
        print("Starting nikto on port: " + str(port))
        path_to_nikto = "./nikto/program/nikto.pl"
        command = ["perl", path_to_nikto, "-h", ip, "-p", str(port)]
        start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        try:
            result = subprocess.run(command, text=True, capture_output=True, timeout=300)
            end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            output = self.parse_nikto_output(result.stdout)
            return {"start_time": start_time, "end_time": end_time, "CVE": output}
        except subprocess.TimeoutExpired:
            return {"start_time": start_time, "end_time": end_time, "output": ["Nikto scan timed out after 3 minutes on port: " + str(port)]}
        except Exception as e:
            return {"start_time": start_time, "end_time": end_time, "output": [str(e)]}

    def update_json(self, ip, port_details):
        # Update the result.json file with scan results
        json_path = os.path.join(os.getcwd(), 'result.json')
        data = {}
        if os.path.exists(json_path):
            with open(json_path, 'r') as file:
                data = json.load(file)

        if ip not in data:
            data[ip] = {}
        data[ip].setdefault("web_scans", [])
        data[ip]["web_scans"].append(port_details)

        with open(json_path, 'w') as file:
            json.dump(data, file, indent=4)

    def collect_and_update_results(self, ip, port, service, sqlmap_output, nikto_output):
        # Collect and update scan results in JSON
        port_details = {
            "port": port,
            "service": service,
            "sqlmap_results": sqlmap_output,
            "nikto_results": nikto_output
        }
        self.update_json(ip, port_details)

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