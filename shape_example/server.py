import mesa

from .model import ShapeExample, Walker, Wall


def agent_draw(agent):
    portrayal = None

    # Перевірка, якщо агент — Walker
    if isinstance(agent, Walker):
        print(f"Uid: {agent.unique_id}, Heading: {agent.heading}")
        portrayal = {
            "Shape": "arrowHead",
            "Filled": "true",
            "Layer": 2,
            "Color": ["#00FF00", "#99FF99"],
            "stroke_color": "#666666",
            "heading_x": agent.heading[0],
            "heading_y": agent.heading[1],
            "text": agent.unique_id,
            "text_color": "white",
            "scale": 0.8,
        }

    # Те як буде відображатись стіна
    elif isinstance(agent, Wall):
        portrayal = {
            "Shape": "circle",
            "Filled": "true",
            "Layer": 1,
            "Color": "blue",
            "r": 0.5
        }

    return portrayal

width = 100
height = 80
num_agents = 100
pixel_ratio = 10
grid = mesa.visualization.CanvasGrid(
    agent_draw, width, height, width * pixel_ratio, height * pixel_ratio
)
server = mesa.visualization.ModularServer(
    ShapeExample,
    [grid],
    "Shape Model Example",
    {"N": num_agents, "width": width, "height": height},
)
server.max_steps = 0
server.port = 8521
