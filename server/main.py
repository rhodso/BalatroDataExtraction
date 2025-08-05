from flask import Flask, request, jsonify, render_template_string

from GameClasses import Game

class App:
    def __init__(self):
        self.data = None  # Store the most recently posted data
        self.ws = Flask(__name__)
        self.ws.add_url_rule('/', 'display_content', self.display_content, methods=['GET'])
        self.ws.add_url_rule('/data', 'process_data', self.process_data, methods=['POST'])

        self.content_fp = "content.txt"
        
        # Test if the content file exists. If not, create it and write "No data has been posted yet."
        try:
            with open(self.content_fp, 'r', encoding="utf-8") as f:
                self.data = f.read()
        except FileNotFoundError:
            with open(self.content_fp, 'w', encoding="utf-8") as f:
                f.write("No data has been posted yet.")
            self.data = None
        else:
            if self.data.strip() == "":
                self.data = None
            else:
                self.data = self.data.strip()  # Remove whitespace
        
    def display_content(self):
        # Handle GET requests to display the most recently posted data
        if self.data:
            G = Game()
            G.deserialize(self.data)
            display_data = str(G)
        else:
            display_data = "No data has been posted yet."

        # HTML template with auto-refresh every 5 seconds
        html_template = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>JSON Display</title>
            <meta http-equiv="refresh" content="10">
            <style>
                body {
                    background-color: black;
                    color: white;
                    font-family: monospace;
                    padding: 20px;
                }
                pre {
                    white-space: pre-wrap;
                    word-wrap: break-word;
                }
            </style>
        </head>
        <body>
            <h1>Posted Data</h1>
            <pre>{{ display_data }}</pre>
        </body>
        </html>
        """

        # Render the HTML with the stored JSON data
        return render_template_string(html_template, display_data=display_data)

    def process_data(self):
        # Handle POST requests to process JSON data
        self.data = request.get_data(as_text=True)

        with open(self.content_fp, 'w', encoding="utf-8") as f:
            if self.data:
                f.write(str(self.data))

        if not self.data:
            return jsonify({"error": "No data provided"}), 400

        # Return a success message
        return jsonify({"message": "Data received successfully"}), 200



    def run(self):
        self.ws.run(host='127.0.0.1', port=8080)


if __name__ == '__main__':
    app = App()
    app.run()