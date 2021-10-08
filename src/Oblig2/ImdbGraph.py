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
        v = 0
        e = 0
        for nm_id in self.vertices:
            actor = self.vertices[nm_id]
            v += 1
            for neighbour in actor.movies.keys():
                e += len(actor.movies[neighbour])
        print("Oppgave 1\n")
        print(f"Nodes: {v} \nEdges: {e // 2}")

    def unweighted_shortest_path(self, start, end):
        queue_s = [start]
        paths = {start: []}
        visited = []
        while end not in paths:
            current = queue_s.pop(0)
            for neigbour in self.vertices[current].movies.keys():
                if neigbour.nm_id not in visited and neigbour.nm_id not in queue_s:
                    paths[neigbour.nm_id] = paths[current].copy() + [current]
                    queue_s.append(neigbour.nm_id)
                    if neigbour.nm_id == end:
                        break
            visited.append(current)
        final_path = paths[end].copy() + [end]

        print(f"\n{self.vertices[start].name}")
        for i, nm_id in enumerate(final_path[1:]):
            current_actor = self.vertices[nm_id]
            film = current_actor.movies[self.vertices[final_path[i]]][0]
            print(f"=== [ {film.title} {film.rating} ] ===> {current_actor.name}")


if __name__ == "__main__":
    graph = IMDbGraph("input/movies.tsv", "input/actors.tsv")
    #graph.count_vertices_and_edges()

    print("Oppgave 2\n")
    graph.unweighted_shortest_path("nm2255973", "nm0000460")
    graph.unweighted_shortest_path("nm0424060", "nm0000243")
    graph.unweighted_shortest_path("nm4689420", "nm0000365")
    graph.unweighted_shortest_path("nm0000288", "nm0001401")
    graph.unweighted_shortest_path("nm0031483", "nm0931324")

