This project implements two parts:

An HTML/CSS/JS front-end that shows a Wikipedia game. The goal is for the user to move from the main page of wikipedia to a random page in the shortest amount of clicks possible. This is implemented using an iFrame window and a Python/Flask backend to query API requests to Wikipedia.

The Python/Flask backend also calculates the optimal path between the two pages using a bi-directional BFS algorithm.
