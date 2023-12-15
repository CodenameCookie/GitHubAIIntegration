from flask import Flask, request, jsonify
from flask_restx import Api, Resource
import requests
from decouple import config

app = Flask(__name__)
api = Api(app)

# Configuration
github_token = config('GITHUB_TOKEN')
username = "CodenameCookie"
expected_password = "12345"

# Middleware API Key Authentication
def authenticate_api_key():
    #api_key = request.headers.get('X-API-KEY')
    api_key = request.args.get('password')
    return api_key == expected_password

@api.route('/')
class Index(Resource):
    def get(self):
        """Welcome message for the API."""
        return {'message': 'Welcome to the GitHub Integration API'}

@api.route('/validate')
@api.doc(responses={200: 'Success', 401: 'Invalid Key'})
class Validate(Resource):
    def get(self):
        """Validate the provided API key."""
        if authenticate_api_key():
            return {"status": "API key validated successfully"}, 200
        else:
            return {"error": "Invalid API key"}, 401

@api.route('/list_repos')
class ListRepos(Resource):
    def get(self):
        """List the repositories of the authenticated user."""
        if not authenticate_api_key():
            return {"error": "Unauthorized"}, 401

        session = requests.Session()
        session.headers.update({"Authorization": f"token {github_token}"})
        url = f"https://api.github.com/users/{username}/repos"
        response = session.get(url)

        if response.status_code != 200:
            return {"error": "Failed to fetch repositories"}, response.status_code
        return jsonify(response.json())

@api.route('/repo_full_contents')
@api.doc(responses={200: 'Success', 400: 'Bad Request', 401: 'Unauthorized'})
class RepoFullContents(Resource):
    def get(self):
        """Get full contents of a specified repository."""
        if not authenticate_api_key():
            return {"error": "Unauthorized"}, 401

        repo_name = request.args.get('repo')
        if not repo_name:
            return {"error": "Repository name is required"}, 400

        session = requests.Session()
        session.headers.update({"Authorization": f"token {github_token}"})
        
        def fetch_contents(url, path=""):
            """Recursively fetch contents of the repository."""
            response = session.get(url)
            if response.status_code != 200:
                return [{"error": f"Failed to fetch contents at {path}", "status_code": response.status_code}]

            contents = response.json()
            repo_contents = []

            for item in contents:
                if item['type'] == 'file':
                    file_response = session.get(item['download_url'])
                    if file_response.status_code == 200:
                        repo_contents.append({
                            "name": item['name'],
                            "path": f"{path}/{item['name']}" if path else item['name'],
                            "content": file_response.text
                        })
                elif item['type'] == 'dir':
                    repo_contents.extend(fetch_contents(item['url'], path=f"{path}/{item['name']}" if path else item['name']))

            return repo_contents

        url = f"https://api.github.com/repos/{username}/{repo_name}/contents"
        full_contents = fetch_contents(url)

        return jsonify(full_contents)

@api.route('/test')
class TestRoute(Resource):
    def get(self):
        return {'message': 'Test successful'}        


if __name__ == '__main__':
    app.run(debug=True)