from flask import Flask, request, jsonify, render_template_string

class App:
    def __init__(self):
        self.data = None  # Store the most recently posted data
        self.ws = Flask(__name__)
        self.ws.add_url_rule('/', 'display_content', self.display_content, methods=['GET'])
        self.ws.add_url_rule('/data', 'process_data', self.process_data, methods=['POST'])

    def display_content(self):
        # Handle GET requests to display the most recently posted data
        if self.data:
            # Convert the stored JSON data to a string for display
            json_data = jsonify(self.data).get_data(as_text=True)
        else:
            # Default message if no data has been posted yet
            json_data = "No data has been posted yet."

        # HTML template with black background and white text
        html_template = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>JSON Display</title>
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
            <h1>Posted JSON Data</h1>
            <pre>{{ json_data }}</pre>
        </body>
        </html>
        """

        # Render the HTML with the stored JSON data
        return render_template_string(html_template, json_data=json_data)

    def process_data(self):
        # Handle POST requests to process JSON data
        self.data = request.get_json()
        if not self.data:
            return jsonify({"error": "No data provided"}), 400

        # Return a success message
        return jsonify({"message": "Data received successfully"}), 200

    def run(self):
        self.ws.run(host='127.0.0.1', port=8080)


if __name__ == '__main__':
    app = App()
    app.run()