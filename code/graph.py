import os
import re
import random
import graphviz

class Graph:
    def __init__(self) -> None:
        self.graph_dict = {}

    def __str__(self) -> str:
        graph_str = ''
        for (k, v) in self.graph_dict.items():
            graph_str += k + ' -> '
            for (name, weight) in v.items():
                graph_str += f'{name}: {weight}, '
            graph_str += '\n'
        return graph_str

    def add_vertex(self, name: str):
        if name not in self.graph_dict.keys():
            self.graph_dict[name] = {}

    def add_edge(self, from_name: str, to_name: str):
        self.add_vertex(from_name)
        self.add_vertex(to_name)
        if to_name not in self.graph_dict[from_name].keys():
            self.graph_dict[from_name][to_name] = 0
        self.graph_dict[from_name][to_name] += 1

    def get_vertexs(self):
        return self.graph_dict.keys()
    
    def get_edges(self):
        edges = []
        for (k, v) in self.graph_dict.items():
            for (name, weight) in v.items():
                edges.append((k, name, weight))
        return edges
    
    def get_bridge(self, v1, v2):
        if v1 not in self.graph_dict.keys():
            raise KeyError('not exist vertex', v1)
        if v2 not in self.graph_dict.keys():
            raise KeyError('not exist vertex', v2)
        bridge = []
        for mid in self.graph_dict[v1].keys():
            for v in self.graph_dict[mid].keys():
                if v == v2:
                    bridge.append(mid)
                    break
        return bridge

    def _dijkstra(self, from_v):
        dijkstra_data = {
            v: {
                'visited': False, 
                'distance': float('inf'), 
                'prev': None
            } for v in self.graph_dict.keys()
        }
        dijkstra_data[from_v]['distance'] = 0
        while True:
            lowest_dis = float('inf')
            lowest_v = None
            for v in self.graph_dict.keys():
                if dijkstra_data[v]['visited']:
                    continue
                if dijkstra_data[v]['distance'] < lowest_dis:
                    lowest_dis = dijkstra_data[v]['distance']
                    lowest_v = v
            if lowest_v is None:
                break
            dijkstra_data[lowest_v]['visited'] = True
            if all([d['visited'] for d in dijkstra_data.values()]):
                break
            for v, weight in self.graph_dict[lowest_v].items():
                if dijkstra_data[v]['visited']:
                    continue
                if lowest_dis + weight < dijkstra_data[v]['distance']:
                    dijkstra_data[v]['distance'] = lowest_dis + weight
                    dijkstra_data[v]['prev'] = lowest_v
        return dijkstra_data
    
    def shortest_path(self, v1, v2):
        if v1 not in self.graph_dict.keys():
            raise KeyError('not exist vertex', v1)
        if v2 not in self.graph_dict.keys():
            raise KeyError('not exist vertex', v2)
        dijk = self._dijkstra(v1)
        prev = dijk[v2]['prev']
        path = [v2]
        while prev is not None:
            path.append(prev)
            prev = dijk[prev]['prev']
        path.reverse()
        return dijk[v2]['distance'], path
    
    def shortest_all(self, v):
        if v not in self.graph_dict.keys():
            raise KeyError('not exist vertex', v)
        dijk = self._dijkstra(v)
        shortest = {
            v2: {
                'distance': dijk[v2]['distance'], 
                'path': None
            } for v2 in self.graph_dict.keys()
        }
        for v2 in self.graph_dict.keys():
            prev = dijk[v2]['prev']
            path = [v2]
            while prev is not None:
                path.append(prev)
                prev = dijk[prev]['prev']
            path.reverse()
            shortest[v2]['path'] = path
        return shortest

    def random_walk(self):
        v = random.choice(list(self.graph_dict.keys()))
        path = []
        while len(path)<2 or not (path[-1], v) in zip(path[:-1], path[1:]):
            path.append(v)
            if len(self.graph_dict[v].keys()) == 0:
                break
            v = random.choice(list(self.graph_dict[v].keys()))
        return path


class WordGraph:
    def __init__(self, txt: str) -> None:
        self.color_list = ['blue', 'green', 'purple', 'red']
        self.graph = Graph()
        words = re.findall('[a-z]+', txt.lower())
        for i in range(len(words) - 1):
            self.graph.add_edge(words[i], words[i+1])

    def __str__(self) -> str:
        return self.graph.__str__()

    def showDirectedGraph(self):
        draw_graph = graphviz.Digraph()
        draw_graph.graph_attr['dpi'] = '350'
        for v in self.graph.get_vertexs():
            draw_graph.node(v)
        for (start, end, weight) in self.graph.get_edges():
            draw_graph.edge(start, end, str(weight))
        draw_graph.render(os.path.join('output', 'graph'), format='jpg', cleanup=True)

    def queryBridgeWords(self, word1, word2):
        try:
            bridge_words = self.graph.get_bridge(word1, word2)
        except KeyError as e:
            return f'No {e.args[-1]} in the graph!'
        if len(bridge_words) == 0:
            return f'No bridge words from \"{word1}\" to \"{word2}\"!'
        elif len(bridge_words) == 1:
            return f'The bridge words from \"{word1}\" to \"{word2}\" is: {bridge_words[0]}.'
        else:
            return f'The bridge words from \"{word1}\" to \"{word2}\" are: {", ".join(bridge_words[:-1])} and {bridge_words[-1]}.'

    def generateNewText(self, inputText):
        if inputText is None:
            return 'No input text!'
        words = re.findall('[a-z]+', inputText.lower())
        added = 0
        for idx, (word1, word2) in enumerate(zip(words[:-1], words[1:])):
            try:
                bridge_words = self.graph.get_bridge(word1, word2)
            except KeyError as e:
                continue
            if len(bridge_words) != 0:
                words.insert(idx+added+1, random.choice(bridge_words))
                added+=1
        return ' '.join(words)

    def calcShortestPath(self, word1, word2):
        try:
            distance, path = self.graph.shortest_path(word1, word2)
        except KeyError as e:
            return f'not exist word \"{e.args[-1]}\"'
        draw_graph = graphviz.Digraph()
        draw_graph.graph_attr['dpi'] = '350'
        color = random.choice(self.color_list)
        for v in self.graph.get_vertexs():
            draw_graph.node(v)
        for (start, end, weight) in self.graph.get_edges():
            if (start, end) in zip(path[:-1], path[1:]):
                draw_graph.edge(start, end, str(weight), color = color)
            else:
                draw_graph.edge(start, end, str(weight))
        draw_graph.render(os.path.join('output', 'shortest_path'), format='jpg', cleanup=True)
        if distance == float('inf'):
            return f'\"{word1}\" cannot goto \"{word2}\"'
        return f'distance: {distance}, path: {"->".join(path)}'
    
    def calcShortestPathAll(self, word):
        try:
            short_data = self.graph.shortest_all(word)
        except KeyError as e:
            return f'not exist word \"{e.args[-1]}\"'
        out_txt = ''
        for id, w2 in enumerate(self.graph.get_vertexs()):
            if short_data[w2]['distance'] == float('inf'):
                continue
            draw_graph = graphviz.Digraph()
            draw_graph.graph_attr['dpi'] = '350'
            color = random.choice(self.color_list)
            for v in self.graph.get_vertexs():
                draw_graph.node(v)
            for (start, end, weight) in self.graph.get_edges():
                if (start, end) in zip(short_data[w2]['path'][:-1], short_data[w2]['path'][1:]):
                    draw_graph.edge(start, end, str(weight), color = color)
                else:
                    draw_graph.edge(start, end, str(weight))
            draw_graph.render(os.path.join('output', f'shortest_path_{id}'), format='jpg', cleanup=True)
            out_txt += f'{word} to {w2}: \n    distance: {short_data[w2]["distance"]}, path: {"->".join(short_data[w2]["path"])}\n'
        return out_txt

    def randomWalk(self):
        path = self.graph.random_walk()
        txt = ' '.join(path)
        with open(os.path.join('output', 'walk.txt'), 'w+') as f:
            f.write(txt)
        return txt