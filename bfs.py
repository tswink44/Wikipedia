import requests
from collections import deque

# Fetch links from a Wikipedia page using the Wikipedia API
def get_links(page_title):
    url = f"https://en.wikipedia.org/w/api.php?action=query&titles={page_title}&prop=links&pllimit=max&format=json&origin=*"
    response = requests.get(url)
    data = response.json()

    # Get the page ID from the response
    page_id = list(data["query"]["pages"].keys())[0]
    if "links" in data["query"]["pages"][page_id]:
        links = [link["title"] for link in data["query"]["pages"][page_id]["links"]]
        return links
    else:
        return []

# Perform BFS to find the shortest path from start_page to target_page
def bfs(start_page, target_page):
    # Initialize the queue and visited set
    queue = deque([(start_page, [start_page])])  # (current_page, path_taken)
    visited = set()

    # Start BFS loop
    while queue:
        current_page, path = queue.popleft()

        # If we've reached the target page, return the path and click count
        if current_page == target_page:
            return path, len(path) - 1  # Number of clicks is length of path - 1

        # Otherwise, fetch the links from the current page
        if current_page not in visited:
            visited.add(current_page)
            links = get_links(current_page)

            # Add unvisited links to the queue
            for link in links:
                if link not in visited:
                    queue.append((link, path + [link]))

    # If no path is found
    return None, -1

# Main execution
if __name__ == "__main__":
    # Start and target pages
    start_page = "Main Page"
    target_page = "Python (programming language)"

    # Run BFS to find the shortest path
    path, clicks = bfs(start_page, target_page)

    if path:
        print(f"Shortest path to {target_page}:")
        print(" -> ".join(path))
        print(f"Click count: {clicks}")
    else:
        print("No path found.")
