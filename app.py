from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from notebook_script import process_links  # Import your function

app = Flask(__name__)

def extract_youtube_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a', href=True)
    youtube_links = [link['href'] for link in links if 'youtube.com/watch' in link['href']]
    return youtube_links

@app.route('/extract', methods=['POST'])
def extract():
    data = request.json
    url = data.get('url')
    if not url:
        return jsonify({'error': 'URL is required'}), 400

    try:
        youtube_links = extract_youtube_links(url)
        processed_links = process_links(youtube_links)  # Use the function from your notebook script
        return jsonify({'youtube_links': processed_links})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
