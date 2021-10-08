from __future__ import annotations
from typing import DefaultDict, Dict, List, DefaultDict
from dataclasses import dataclass
from itertools import combinations
from collections import deque

@dataclass
class Movie:
    title: str
    rating: float

class Actor:
    def __init__(self, nm_id, name) -> None:
        self.nm_id = nm_id
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
                movies_to_actors[tt_id].append(actor) ## TODO: Kan vi bytte 'actor' med nm_id her?
        
        for tt_id in movies_to_actors:
            movie = movies[tt_id]
            actors = movies_to_actors[tt_id]
            for actor1, actor2 in combinations(actors, 2):
                actor1.link_to(actor2, movie)         ## TODO: Og her da? mtp det over
                actor2.link_to(actor1, movie)

    def count_vertices_and_edges(self) -> None:
        v = len(self.vertices)
        e = sum(len(ms) for a in self.vertices.values() for ms in a.movies.values()) // 2
        print(f"{v} \n{e}")

    def unweighted_shortest_path(self, start_id: str, end_id: str):
        start = self.vertices[start_id]
        end = self.vertices[end_id]
        queue = deque([start])
        paths: Dict[Actor, List[Actor]] = {start: []}
        visited = []
        while end not in paths:
            current = queue.popleft()
            for neigbour in current.movies.keys():
                if neigbour not in visited and neigbour not in queue:
                    paths[neigbour] = paths[current] + [current]
                    queue.append(neigbour)
                    if neigbour == end:
                        break
            visited.append(current)
        final_path = paths[end] + [end]

        print(f"\n{start.name}")
        for i, actor in enumerate(final_path[1:]):
            film = actor.movies[final_path[i]][0]
            print(f"=== [ {film.title} {film.rating} ] ===> {actor.name}")


if __name__ == "__main__":
    graph = IMDbGraph("input/movies.tsv", "input/actors.tsv")
    #graph.count_vertices_and_edges()

    print("Oppgave 2\n")
    graph.unweighted_shortest_path("nm2255973", "nm0000460")
    graph.unweighted_shortest_path("nm0424060", "nm0000243")
    graph.unweighted_shortest_path("nm4689420", "nm0000365")
    graph.unweighted_shortest_path("nm0000288", "nm0001401")
    graph.unweighted_shortest_path("nm0031483", "nm0931324")

