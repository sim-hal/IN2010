from __future__ import annotations
from collections import defaultdict
from re import T
from typing import DefaultDict, Dict, List, Tuple, Generator, DefaultDict
from dataclasses import dataclass
from itertools import combinations


@dataclass
class Movie:
    title: str
    rating: float


class Actor:
    def __init__(self, id, name) -> None:
        self.id = id
        self.name = name
        self.movies = DefaultDict[Actor, List[Movie]](list)
    
    def link_to(self, other: Actor, movie: Movie):
        self.movies[other].append(movie)
    

def read_movies(moviesTsv):
    with open(moviesTsv, encoding="UTF-8") as moviesFile:
        for line in moviesFile:
            tt_id, title, rating, _ = line.strip().split("\t")
            yield tt_id, title, float(rating)

def read_actors(actorsTsv):
    with open(actorsTsv, encoding="UTF-8") as actorsFile:
        for line in actorsFile:
            nm_id, name, *tt_ids = line.strip().split("\t")
            yield nm_id, name, tt_ids


class IMDbGraph:
    def __init__(self, moviesTsv: str, actorsTsv: str) -> None:
        movies: Dict[str, Movie] = {}
        self.vertices: Dict[str, Actor] = {}

        for tt_id, title, rating in read_movies(moviesTsv):
            movies[tt_id] = Movie(title, float(rating))
        
        movies_to_actors = DefaultDict[str, List[Actor]](list)
        for nm_id, name, tt_ids in read_actors(actorsTsv):
            actor = Actor(nm_id, name)
            self.vertices[nm_id] = actor
            for tt_id in tt_ids:
                if tt_id not in movies:
                    continue
                movies_to_actors[tt_id].append(actor)
        
        for tt_id in movies_to_actors:
            movie = movies[tt_id]
            actors = movies_to_actors[tt_id]
            for actor1, actor2 in combinations(actors, 2):
                actor1.link_to(actor2, movie)
                actor2.link_to(actor1, movie)

    def count_vertices_and_edges(self) -> None:
        v = 0
        e = 0
        for nm_id in self.vertices:
            actor = self.vertices[nm_id]
            v += 1
            for neighbour in actor.movies.keys():
                e += len(actor.movies[neighbour])
        print("Oppgave 1\n")
        print(f"Nodes: {v} \nEdges: {e // 2}")

    def bfs(self, start, end):
        checked = set()


        pass

if __name__ == "__main__":
    graph = IMDbGraph("input/movies.tsv", "input/actors.tsv")
    graph.count_vertices_and_edges()
    glover = graph.vertices["nm2255973"]

