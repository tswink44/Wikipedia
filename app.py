from flask import Flask, request, jsonify
import requests
from collections import deque
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
# Wikipedia Base API Link
WIKI_API_URL = "https://en.wikipedia.org/w/api.php"


def get_links(page):
    #Purpose: Fetches Wikipedia Links using its API
    params = {
        "action": "parse",
        "page": page,
        "prop": "links",
        "format": "json",
        "pllimit": "max",
    }
    response = requests.get(WIKI_API_URL, params=params)
    data = response.json()

    # Extract the links from the response
    if 'parse' in data:
        links = [link['*'] for link in data['parse']['links'] if link['ns'] == 0]
        return links
    return []


def bidirectional_bfs(start_page, end_page):
    """
    Purpose: Implements a bi-directional breadth first search function to find the optimal path between two wikipedia pages.
    Args:
    start_page (string): the first wikipedia page to start searching from.
    end_page (string): the last wikipedia page to end searching to.
    """
    # Initialize queues for both directions
    queue_start = deque([start_page])
    queue_end = deque([end_page])

    # Visited sets for both directions
    visited_start = {start_page}
    visited_end = {end_page}

    # Parent pointers to reconstruct the path later
    parent_start = {start_page: None}
    parent_end = {end_page: None}

    # Perform the search
    while queue_start and queue_end:
        # Expand from the start side
        current_start = queue_start.popleft()

        # Check if the current node from the start side is already visited on the end side
        if current_start in visited_end:
            return reconstruct_path(parent_start, parent_end, current_start)

        # Explore neighbors of current_start
        for neighbor in get_links(current_start):
            if neighbor not in visited_start:
                visited_start.add(neighbor)
                parent_start[neighbor] = current_start
                queue_start.append(neighbor)

        # Expand from the end side
        current_end = queue_end.popleft()

        # Check if the current node from the end side is already visited on the start side
        if current_end in visited_start:
            return reconstruct_path(parent_start, parent_end, current_end)

        # Explore neighbors of current_end
        for neighbor in get_links(current_end):
            if neighbor not in visited_end:
                visited_end.add(neighbor)
                parent_end[neighbor] = current_end
                queue_end.append(neighbor)

    return None  # No path found


# Path reconstruction function
def reconstruct_path(parent_start, parent_end, meeting_point):
    """ Reconstructs the path from the start to the meeting point and from the end to the meeting point:
    Args:
    parent_start (string): the first wikipedia page to start searching from.
    parent_end (string): the last wikipedia page to end searching to.
    meeting_point (string): the meeting point to be reconstructed.
    """
    # Reconstruct the path from the start to the meeting point
    path_start_to_meeting = []
    current = meeting_point
    while current is not None:
        path_start_to_meeting.append(current)
        current = parent_start.get(current)

    path_start_to_meeting.reverse()

    # Reconstruct the path from the end to the meeting point
    path_end_to_meeting = []
    current = parent_end.get(meeting_point)
    while current is not None:
        path_end_to_meeting.append(current)
        current = parent_end.get(current)

    # Combine the paths
    return path_start_to_meeting + path_end_to_meeting


@app.route('/find_path', methods=['GET'])
def find_path():
    """Implements the bi-directional BFS from above
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
    try:
        # Fetch a random Wikipedia article using the Wikipedia API
        url = 'https://en.wikipedia.org/w/api.php?action=query&format=json&list=random&rnlimit=1&rnnamespace=0'
        response = requests.get(url)
        data = response.json()

        # Extract the random article title
        random_page_title = data['query']['random'][0]['title']

        # Return the title as JSON
        return jsonify({'page': random_page_title})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
