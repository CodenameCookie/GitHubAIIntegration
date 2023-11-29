from flask import Flask, render_template, request, jsonify
import requests
from decouple import config

print('Working Version')

app = Flask(__name__)

# Access the GitHub token securely from environment variables
github_token = config('GITHUB_TOKEN')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_user_info', methods=['POST'])
def get_user_info():
    username = request.form.get('username')

    # Create a session with authentication
    session = requests.Session()
    session.headers.update({"Authorization": f"token {github_token}"})

    # Define the API endpoint to get user information
    url = f"https://api.github.com/users/{username}"

    # Make a GET request to retrieve user information
    response = session.get(url)

    if response.status_code != 200:
        return jsonify({"error": f"Failed to fetch user information. Status code: {response.status_code}"})
    user_info = response.json()
    return jsonify(user_info)  # Return user information as JSON

if __name__ == '__main__':
    #app.run(debug=True)
    #app.run(host='0.0.0.0', port=5000)
    app.run()

