import http.server
import socketserver
import webbrowser
import threading

# Define the handler to use for incoming requests
handler = http.server.SimpleHTTPRequestHandler

# Set the directory containing your index.html file
handler.directory = "UI"

# Define the port to listen on
port = 8080

# Function to start the server


def start_server():
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Serving on port {port}")
        httpd.serve_forever()


# Start the server in a separate thread
server_thread = threading.Thread(target=start_server)
server_thread.start()

# Open the web browser to the index page
webbrowser.open(f"http://localhost:{port}/UI/index.html")

# Wait for the server thread to finish (optional)
server_thread.join()
