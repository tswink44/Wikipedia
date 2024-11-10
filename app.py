from flask import Flask, request, jsonify
import requests
from collections import deque
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
WIKI_API_URL = "https://en.wikipedia.org/w/api.php"


def get_links(page):
    """
    :param page: The title of the Wikipedia page from which to extract links.
    :type page: str
    :return: A list of strings containing the titles of the linked Wikipedia pages within the specified page, limited to the main namespace (ns=0). If the page is not found or there are no links, an empty list is returned.
    :rtype: list
    """
    params = {
        "action": "parse",
        "page": page,
        "prop": "links",
        "format": "json",
        "pllimit": "max",
    }
    response = requests.get(WIKI_API_URL, params=params)
    data = response.json()

    if 'parse' in data:
        links = [link['*'] for link in data['parse']['links'] if link['ns'] == 0]
        return links
    return []


def bidirectional_bfs(start_page, end_page):
    """
    :param start_page: The starting node or page from where the search begins.
    :param end_page: The target node or page to be reached.
    :return: A list representing the path from start_page to end_page if one exists, otherwise None.
    """
    queue_start = deque([start_page])
    queue_end = deque([end_page])

    visited_start = {start_page}
    visited_end = {end_page}

    parent_start = {start_page: None}
    parent_end = {end_page: None}

    while queue_start and queue_end:
        current_start = queue_start.popleft()

        if current_start in visited_end:
            return reconstruct_path(parent_start, parent_end, current_start)


        for neighbor in get_links(current_start):
            if neighbor not in visited_start:
                visited_start.add(neighbor)
                parent_start[neighbor] = current_start
                queue_start.append(neighbor)

        current_end = queue_end.popleft()

        if current_end in visited_start:
            return reconstruct_path(parent_start, parent_end, current_end)

        for neighbor in get_links(current_end):
            if neighbor not in visited_end:
                visited_end.add(neighbor)
                parent_end[neighbor] = current_end
                queue_end.append(neighbor)

    return None  # No path found


# Path reconstruction function
def reconstruct_path(parent_start, parent_end, meeting_point):
    """
    :param parent_start: Dictionary containing the parent nodes from the start point.
    :param parent_end: Dictionary containing the parent nodes from the end point.
    :param meeting_point: The node where the search from the start and the end meet.
    :return: List representing the path reconstructed from start to end via the meeting point.
    """
    path_start_to_meeting = []
    current = meeting_point
    while current is not None:
        path_start_to_meeting.append(current)
        current = parent_start.get(current)

    path_start_to_meeting.reverse()

    path_end_to_meeting = []
    current = parent_end.get(meeting_point)
    while current is not None:
        path_end_to_meeting.append(current)
        current = parent_end.get(current)

    return path_start_to_meeting + path_end_to_meeting


@app.route('/find_path', methods=['GET'])
def find_path():
    """
    Handles the endpoint to find a path between two Wikipedia pages.
    Utilizes bidirectional BFS to find the shortest path between the given start and end pages provided as query parameters.

    :return: JSON response containing the path if found, or an error message with appropriate HTTP status code.
    """
    start_page = request.args.get('start_page')
    end_page = request.args.get('end_page')

    if not start_page or not end_page:
        return jsonify({"error": "Both start_page and end_page are required."}), 400

    print(f"Start Page: {start_page}, End Page: {end_page}")  # Debugging
    path = bidirectional_bfs(start_page, end_page)

    if path:
        print(f"Path found: {path}")  # Debugging
        return jsonify({"path": path})
    else:
        print(f"No path found between {start_page} and {end_page}")  # Debugging
        return jsonify({"error": "No path found between the given pages."}), 404

@app.route('/random_wikipedia_page', methods=['GET'])
def random_wikipedia_page():
    """
    View function for Flask route `'/random_wikipedia_page'`. This endpoint retrieves a random Wikipedia page title using Wikipedia's API and returns it as a JSON response.

    :return: JSON object with the title of a random Wikipedia page, or an error message in case of failure.
    """
    try:
        url = 'https://en.wikipedia.org/w/api.php?action=query&format=json&list=random&rnlimit=1&rnnamespace=0'
        response = requests.get(url)
        data = response.json()

        random_page_title = data['query']['random'][0]['title']

        return jsonify({'page': random_page_title})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
