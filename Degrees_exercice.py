from util import Node, StackFrontier, QueueFrontier
import pandas as pd
import sys
import os

names = {}
movie = {}
people = {}

#Guarda e filtra os dados do csv
def get_csv(directory):
    

    #Guarda todas as informações de um id de ator
    df = pd.read_csv(f"{directory}\\people.csv")
    a = 0
    for row in df.itertuples(index=False):
        birth_year = int(row.birth) if not pd.isna(row.birth) else None
        people[row.id] = {
                "name" : row.name,
                "birth" : birth_year,
                "movies" : set()
            }
        
        name_key = row.name.lower()
        if name_key not in names:
            names[name_key] = {row.id}
        else:
            names[name_key].add(row.id)

    #Guarda todas as informações de um id de filme
    df = pd.read_csv(f"{directory}/movies.csv")
    for row in df.itertuples(index=False):
        movie_year = int(row.year) if not pd.isna(row.year) else None
        movie[row.id] = {
            "title" : row.title,
            "year" : movie_year,
            "stars" : set()
        }

    #Vincula os atores com os filmes
    df = pd.read_csv(f"{directory}\\stars.csv")
    for row in df.itertuples(index=False):
            try:
                people[row.person_id]["movies"].add(row.movie_id)
                movie[row.movie_id]["stars"].add(row.person_id)
            except KeyError: 
                pass

#Retorna o id do ator usando o nome
def name_to_id(name):
    person_id = list(names.get(name.lower(), set()))
    if len(person_id) == 0:
        return None 
    elif len(person_id) > 1:
        print(f"With {name}?")
        for id in person_id:
            person = people[id]
            name = person["name"]
            birth = person["birth"]

            print(f"ID:{id} Name:{name} birth:{birth}")
            
        try:
            id = int(input("Intendent person ID: "))
            if id in person_id:
                return id
        except ValueError:
            pass
        return None

    else: 
        return person_id[0]

#Retorna pares (movie_id, person_id) para pessoas que atuaram com uma determinada pessoa.
def neighbors_for_person(person_id):
    neighbors = set()
    movie_ids = people[person_id]["movies"]
    for movie_id in movie_ids:
        for actor_id in movie[movie_id]["stars"]:
            neighbors.add((movie_id, actor_id))
    return neighbors

#Encontra o caminho mais curto que junta os atores
def shortest_path(source, target):
    start_node = Node(state=source, parent=None, action=None)

    frontier = QueueFrontier()
    visited = set()
    frontier_states = set()
    frontier.add(start_node)
    frontier_states.add(start_node.state)

    while True:
        if frontier.empty():
            return None
        node = frontier.remove()
        visited.add(node.state)
        
        if node.state == target:
            path = []
            

            while node is not None and node.state is not None:
                path.append((node.action, node.state))
                node = node.parent 
            path.reverse()
            return path
        for movie_id, person_id in neighbors_for_person(node.state):
            if person_id not in frontier_states and person_id not in visited:
                
                child_node = Node(state=person_id, parent=node, action=movie_id)
                frontier.add(child_node)
                frontier_states.add(person_id)
        

#Roda as funções
def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")

    folder = sys.argv[1] if len(sys.argv) == 2 else "large"
    base_path = "C:\\Users\\mathe\\Downloads\\degrees"
    directory = os.path.join(base_path, folder)
    get_csv(directory)
    
    source = name_to_id(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = name_to_id(input("Name: "))
    if target is None:
        sys.exit("Person not found.")
    
    print(shortest_path(source, target))

#main() é chamado apenas se o script for executado diretamente
if __name__ == "__main__":
    main