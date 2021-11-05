import json
from igraph import Graph, EdgeSeq
import plotly.graph_objects as go


class GraphGenerator:
    nodes = []
    relation = []
    matrix = []

    def __init__(self):
        pass

    def jsontonode(self, data, parent_step):
        node_string = ""
        step = ""

        if "step" in data:
            step = data["step"]
            self.relation.append((parent_step, step))
        for (k, v) in data.items():
            if k == "actual" or k == "estimated":
                continue
            elif k == "children":
                for j in v:
                    self.jsontonode(j, step)
            elif k == "subplans":
                for j in v:
                    self.jsontonode(j, step)
            else:
                node_string += "{} : {} | ".format(k, v)

            print('k,v: {}'.format(k, v))
        self.nodes.append(node_string)

    def plot(self, data):
        self.jsontonode(data, 0)

        length = len(self.nodes)
        for i in range(length):
            temp = []
            for i in range(length):
                temp.append(0)
            self.matrix.append(temp)
        for i in self.relation:
            print(i)
            parent = i[0] - 1
            child = i[1] - 1

            self.matrix[parent][child] = 1

        v_label = self.nodes
        nr_vertices = len(self.nodes)

        # v_label = list(map(str, range(nr_vertices)))
        # G = Graph.Tree(nr_vertices, 2)  # 2 stands for children number
        G = Graph.Adjacency(self.matrix)
        print("G: {}".format(G))
        lay = G.layout('tree')

        position = {k: lay[k] for k in range(nr_vertices)}
        Y = [lay[k][1] for k in range(nr_vertices)]
        M = max(Y)

        es = EdgeSeq(G)  # sequence of edges
        E = [e.tuple for e in G.es]  # list of edges

        L = len(position)
        Xn = [position[k][0] for k in range(L)]
        Yn = [2 * M - position[k][1] for k in range(L)]
        Xe = []
        Ye = []
        for edge in E:
            Xe += [position[edge[0]][0], position[edge[1]][0], None]
            Ye += [2 * M - position[edge[0]][1], 2 * M - position[edge[1]][1], None]

        labels = v_label
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=Xe,
                                 y=Ye,
                                 mode='lines',
                                 line=dict(color='rgb(210,210,210)', width=1),
                                 hoverinfo='none'
                                 ))
        fig.add_trace(go.Scatter(x=Xn,
                                 y=Yn,
                                 mode='markers + text',
                                 name='bla',
                                 marker=dict(symbol='diamond',
                                             size=18,
                                             color='#6175c1',  # '#DB4551',
                                             line=dict(color='rgb(50,50,50)', width=1)
                                             ),
                                 text=labels,
                                 hoverinfo='text',
                                 opacity=0.8,
                                 textposition="bottom center"
                                 ))

        fig.update_traces(textposition='top center')
        axis = dict(showline=False,  # hide axis line, grid, ticklabels and  title
                    zeroline=False,
                    showgrid=False,
                    showticklabels=True,
                    )

        fig.update_layout(title='Tree View of Query Plan',
                          annotations=self.make_annotations(position, v_label, M, position),
                          font_size=12,
                          showlegend=False,
                          xaxis=axis,
                          yaxis=axis,
                          margin=dict(l=40, r=40, b=85, t=100),
                          hovermode='closest',
                          plot_bgcolor='rgb(248,248,248)'
                          )
        fig.show()

    def make_annotations(self, pos, text, M, position, font_size=10, font_color='rgb(250,250,250)'):
        L = len(pos)
        if len(text) != L:
            raise ValueError('The lists pos and text must have the same len')
        annotations = []
        for k in range(L):
            annotations.append(
                dict(
                    text=self.nodes[k].split("|")[-2][7:],  # or replace labels with a different list for the text within the circle
                    x=pos[k][0], y=2 * M - position[k][1],
                    xref='x1', yref='y1',
                    font=dict(color=font_color, size=font_size),
                    showarrow=False)
            )
        return annotations

    def generate(self):
        self.nodes = []
        self.relation = []
        self.matrix = []
        f = open('qep.json', )
        # open and load json data
        data = json.load(f)
        self.plot(data)
