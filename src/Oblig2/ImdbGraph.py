from __future__ import annotations
from typing import DefaultDict, Dict, List, Tuple, Set, Optional
from dataclasses import dataclass
from itertools import combinations
from collections import deque
from heapq import heappush, heappop

@dataclass
class Movie:
    title: str
    rating: float


@dataclass
class Path:
    nodes: List[Actor]
    edges: List[Movie]
    
    def __iter__(self, ):
        self.n = 0
        return self

    def __next__(self) -> Tuple[Actor, Movie]:
        if self.n < len(self.edges):
            diff = len(self.nodes) - len(self.edges) # diff should be 0 or 1
            res = self.nodes[self.n + diff], self.edges[self.n]
            self.n += 1
            return res
        else:
            raise StopIteration
    
    def pure_append(self, node: Actor, edge: Movie) -> Path:
        return Path(self.nodes + [node], self.edges + [edge])
    
@dataclass
class WeightedPath(Path):
    cost: float
    
    def pure_append(self, node: Actor, edge: Movie, cost: float) -> WeightedPath:
        return WeightedPath(self.nodes + [node], self.edges + [edge], self.cost + cost)

class Actor:
    def __init__(self, nm_id, name) -> None:
        self.nm_id = nm_id
        self.name = name
        self.movies = DefaultDict[Actor, List[Movie]](list)
        self._neighbours_heapq: Optional[List[Tuple[float, Actor, Movie]]] = None
    
    def link_to(self, other: Actor, movie: Movie):
        self.movies[other].append(movie)
    
    def __lt__(self, other):
        return self.name < other.name 

    @property
    def sorted_movies(self) -> List[Tuple[float, Actor, Movie]]:
        return self._neighbours_heapq if self._neighbours_heapq is not None else self._fill_neighbours_heapq()
    
    
    def _fill_neighbours_heapq(self) -> List[Tuple[float, Actor, Movie]]:
        self._neighbours_heapq = []

        for actor in self.movies: 
            if len(self.movies[actor]) == 1:
                heappush(self._neighbours_heapq, (10-self.movies[actor][0].rating, actor, self.movies[actor][0]))
            else:
                best = self.movies[actor][0]
                for movie in self.movies[actor][1:]:
                    if movie.rating > best.rating:
                        best = movie
                heappush(self._neighbours_heapq, (10-best.rating, actor, best))
        return self._neighbours_heapq

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
        v = len(self.vertices)
        e = sum(len(ms) for a in self.vertices.values() for ms in a.movies.values()) // 2
        print(f"{v} \n{e}\n")

    def unweighted_shortest_path(self, start_id: str, end_id: str):
        start = self.vertices[start_id]
        end = self.vertices[end_id]
        queue = deque([start])
        paths: Dict[Actor, Path] = {start: Path([], [])}
        visited = []
        while end not in paths:
            current = queue.popleft()
            for neighbour in current.movies.keys():
                if neighbour not in visited and neighbour not in queue:
                    paths[neighbour] = paths[current].pure_append(current, current.movies[neighbour][0])
                    queue.append(neighbour)
                    if neighbour == end:
                        break
            visited.append(current)
        final_path = Path(paths[end].nodes + [end], paths[end].edges)

        print(f"\n{start.name}")
        for actor, movie in final_path:
            print(f"=== [ {movie.title} {movie.rating} ] ===> {actor.name}")

    def chillest_path(self, start_id: str, end_id: str):
        start = self.vertices[start_id]
        end = self.vertices[end_id]
        heapq: List[Tuple[float, Actor]] = [(0, start)]
        paths = DefaultDict[Actor, WeightedPath](lambda: WeightedPath([], [], float("inf")))
        paths[start] = WeightedPath([], [], 0)
        while heapq:
            (c_w, c_actor) = heappop(heapq)
            for (w, actor, movie) in c_actor.sorted_movies: 
                if paths[actor].cost > paths[c_actor].cost + w:
                    c_path = paths[c_actor]
                    paths[actor] = c_path.pure_append(c_actor, movie, w)
                    heappush(heapq, (paths[actor].cost, actor))

        final_path = WeightedPath(paths[end].nodes + [end], paths[end].edges, paths[end].cost)

        print(f"\n{start.name}")
        for actor, movie in final_path:
            print(f"=== [ {movie.title} {movie.rating} ] ===> {actor.name}")
        print(f"Total cost: {final_path.cost :1f}")

    def component_dfs(self):
        v_count = len(self.vertices)
        visited: Set[Actor] = set()
        unvisited: Set[str] = set(self.vertices.keys())
        component_sizes = DefaultDict[int, int](int)
        while len(visited) < v_count:
            count = len(visited)
            current = self.vertices[unvisited.pop()]
            stack: List[Actor] = [current]
            while stack:
                current = stack[-1]
                for neighbour in current.movies:
                    if neighbour.nm_id not in visited:
                        stack.append(neighbour)
                        break
                if current == stack[-1]:
                    stack.pop()
                if current.nm_id not in visited:
                    visited.add(current.nm_id)

            component_size = len(visited) - count
            component_sizes[component_size] += 1
            unvisited = unvisited - visited

        for size in sorted(component_sizes):
            print(f"There are {component_sizes[size]} components of size {size}")


if __name__ == "__main__":
    graph = IMDbGraph("input/movies.tsv", "input/actors.tsv")
    print("Oppgave  1\n")
    graph.count_vertices_and_edges()

    print("Oppgave 2\n")
    graph.unweighted_shortest_path("nm2255973", "nm0000460")
    graph.unweighted_shortest_path("nm0424060", "nm0000243")
    graph.unweighted_shortest_path("nm4689420", "nm0000365")
    graph.unweighted_shortest_path("nm0000288", "nm0001401")
    graph.unweighted_shortest_path("nm0031483", "nm0931324")

    print("Oppgave 3\n")
    graph.chillest_path("nm0031483", "nm0931324")

    print("Opggave 4\n")
    graph.component_dfs()


