from flask import Flask, jsonify, make_response
from flask import request, current_app
from functools import wraps
import pprint
import json
import re

app = Flask(__name__)

@app.route('/hello', methods=['GET'])
def hello():
    return """
    hello
    <table style='width: 120px; height: 120px; border-collapse: collapse;'>
        <tbody>
            <tr>
                <td style='border-style: solid none none solid; width: 30px;'>&nbsp;</td>
                <td style='border-style: none none none none; width: 30px;'>here</td>
                <td style='border-style: solid none solid none; width: 30px;'>&nbsp;</td>
                <td style='border-style: solid solid none none; width: 30px;'>&nbsp;</td>
            </tr>
            <tr>
                <td style='border-style: none solid none solid; width: 30px;'>&nbsp;</td>
                <td style='border-style: none none solid solid; width: 30px;'>&nbsp;</td>
                <td style='border-style: solid solid none none; width: 30px;'>&nbsp;</td>
                <td style='border-style: none solid solid solid; width: 30px;'>&nbsp;</td>
            </tr>
            <tr>
                <td style='border-style: none solid none solid; width: 30px;'>&nbsp;</td>
                <td style='border-style: solid solid none solid; width: 30px;'>&nbsp;</td>
                <td style='border-style: none none solid solid; width: 30px;'>&nbsp;</td>
                <td style='border-style: solid solid none none; width: 30px;'>&nbsp;</td>
            </tr>
            <tr>
                <td style='border-style: none none solid solid; width: 30px;'>&nbsp;</td>
                <td style='border-style: none solid solid none; width: 30px;'>&nbsp;</td>
                <td style='border-style: solid none none solid; width: 30px;'>&nbsp;</td>
                <td style='border-style: none solid solid none; width: 30px;'>&nbsp;</td>
            </tr>
        </tbody>
    </table>
    """
    
@app.route('/maze1', methods=['GET'])
def maze1():
    maze_json = import_json('maze/maze1.json')
    return build_maze(maze_json)
    
def import_json(json_file, debug=0):
    maze_json = []
    with open(json_file) as data_file:
        data = data_file.read()
        if debug == 1:
            print data

        maze_json = json.loads(data)
        
    return maze_json
    
def build_maze(json_obj):
    width = json_obj["row_count"] * json_obj["cell_width"]
    height = json_obj["col_count"] * json_obj["cell_width"]
    maze = json_obj["maze"]
    
    table_head = """
    <table style='width: %spx; height: %spx; border-collapse: collapse;'>
        <tbody>
    """ % (width, height)
    
    table_footer = """
        </tbody>
    </table>
    """
    
    table_body = build_maze_body(json_obj)
    
    return table_head + table_body + table_footer
    
def build_maze_body(json_obj):
    maze = json_obj["maze"]
    cell_width = json_obj["cell_width"]
    start = json_obj["start"]
    
    solid_or_none = {
        1: "solid",
        0: "none"
    }

    body = ""
    
    row_idx = 0
    for row in maze:
        col_idx = 0
        
        body += "<tr>\n"
        for cell in row:
            top = solid_or_none[ cell["top"] ]
            right = solid_or_none[ cell["right"] ]
            bottom = solid_or_none[ cell["bottom"] ]
            left = solid_or_none[ cell["left"] ]
            cell_content = "&nbsp;"
            if row_idx == start[0] and col_idx == start[1]:
                cell_content = "s"
            
            style = """style='text-align: center; 
                       border-style: %s %s %s %s; 
                       width: %spx;'""" % (
                top,
                right,
                bottom,
                left,
                cell_width
            )
            body += "<td %s>%s</td>\n" % (style, cell_content)
            
            col_idx += 1
            
        body += "</tr>\n"
        row_idx += 1

    return body
    

if __name__ == '__main__':
    #maze_json = import_json('maze/maze1.json')
    #build_maze(maze_json)
    app.run(debug=True, host='0.0.0.0')