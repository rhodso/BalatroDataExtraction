from flask import Flask, request, jsonify, render_template_string, send_file

from GameClasses import Game
from Card_Image_Creator import CardImageCreator

import os
from io import BytesIO
from PIL import Image

import base64

class App:
    upload = os.path.join(os.getcwd(), 'static', 'uploads')

    def __init__(self):
        self.data = None  # Store the most recently posted data
        self.ws = Flask(__name__, static_folder='static')

        self.ws.config['UPLOAD_DIRECTORY'] = App.upload

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
    
    def serve_pil_image(self, image):
        img_io = BytesIO()
        image.save(img_io, 'PNG')
        img_io.seek(0)
        return send_file(img_io, mimetype='image/png')

    def display_content(self):
        card_uris = []
        jkr_uris = []
        display_data = ""
        
        # Handle GET requests to display the most recently posted data
        if self.data:
            G = Game()
            G.deserialize(self.data)
            display_data = str(G)

            # Generate card images
            hand_images = []
            hand_image_fp = []
            for card in G.Hand:
                hand_images.append(CardImageCreator.translate_playing_card(card))
            hand_image_count = len(hand_images)

            joker_images = []
            joker_image_fp = []
            for card in G.Jokers:
                joker_images.append(CardImageCreator.translate_joker_card(card))
            joker_image_count = len(joker_images)
            
            def image_to_data_uri(img):
                buffer = BytesIO()
                img.save(buffer, format="PNG")
                encoded= base64.b64encode(buffer.getvalue()).decode('utf-8')
                return f"data:image/png;base64,{encoded}"
            
            jkr_uris = [image_to_data_uri(img) for img in joker_images]
            card_uris = [image_to_data_uri(img) for img in hand_images]

            # all_images = hand_images + joker_images
            # img_uris = [image_to_data_uri(img) for img in all_images]

        else:
            display_data = "No data has been posted yet."
            img_uris = []

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
                .cards {
                    display: flex;
                    flex-direction: row;
                    gap: 10px;
                    flex-wrap: nowrap;
                    align-items: flex-start;
                    margin-bottom: 20px;
                }
                .card img {
                    width: auto;
                    height: auto;
                    border: 1px solid #ccc;
                    box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
                    border-radius: 4px;
                }
            </style>
        </head>
        <body>
            <h1>Posted Data</h1>
            <h3>Joker Cards:</h3>
            <div class="cards">
                {% for img_uri in jkr_uris %}
                    <div class="card">
                        <img src="{{ img_uri }}" alt="Card Image"/>
                    </div>
                {% endfor %}
            </div>
            <br><br>
            <h3>Hand Cards:</h3>
            <div class="cards">
                {% for img_uri in card_uris %}
                    <div class="card">
                        <img src="{{ img_uri }}" alt="Card Image"/>
                    </div>
                {% endfor %}
            </div>
            <br><br>
            <h2>Data:</h2>
            <pre>{{ display_data }}</pre>
        </body>
        </html>
        """

        # Render the HTML with the stored JSON data
        return render_template_string(
            html_template, 
            jkr_uris=jkr_uris,
            card_uris=card_uris, 
            display_data=display_data
        )

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