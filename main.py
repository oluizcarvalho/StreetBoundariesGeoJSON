from xml.etree import ElementTree as ET
from shapely.geometry import LineString, MultiLineString, Polygon, mapping
import json

# Carregar o XML
tree = ET.parse('teste.xml')
root = tree.getroot()

# Dicionário para armazenar os nós por rua
nodes_by_street = {}

# Percorrer os ways e agrupar os nós por rua
for way in root.findall('.//way'):
    street_id = way.attrib['id']
    nodes = [nd.attrib['ref'] for nd in way.findall('nd')]
    nodes_by_street[street_id] = nodes

# Função para criar uma linha suavizada a partir dos nós de uma rua
def create_smooth_line(nodes):
    points = [(float(root.find(f".//node[@id='{node_id}']").attrib['lon']),
               float(root.find(f".//node[@id='{node_id}']").attrib['lat'])) for node_id in nodes]
    line = LineString(points)
    return line.simplify(0.0005, preserve_topology=True)

# Lista para armazenar as linhas suavizadas das ruas
smooth_lines = []

# Criar as linhas suavizadas para cada rua
for street_id, nodes in nodes_by_street.items():
    smooth_line = create_smooth_line(nodes)
    smooth_lines.append(smooth_line)

# Criar um objeto MultiLineString
multi_line_string = MultiLineString(smooth_lines)

# Criar um polígono fechado a partir das linhas suavizadas
polygon = multi_line_string.convex_hull

# Converter o polígono para um dicionário GeoJSON
geojson_dict = mapping(polygon)

# Salvar o polígono GeoJSON em um arquivo
with open('output_polygon.geojson', 'w') as f:
    json.dump(geojson_dict, f)
