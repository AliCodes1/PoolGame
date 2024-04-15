import sys
import cgi
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs,parse_qsl
import os
import glob
import Physics
import json
import random
import math
# Compute acceleration based on collision physics
def compute_acceleration(rolling_ball):
    # Compute speeds after collision
    speed_a = Physics.phylib.phylib_length(rolling_ball.obj.rolling_ball.vel)
    
    # Update accelerations based on the new velocities
    if speed_a > Physics.VEL_EPSILON:
        rolling_ball.obj.rolling_ball.acc.x = -(rolling_ball.obj.rolling_ball.vel.x / speed_a) * Physics.DRAG
        rolling_ball.obj.rolling_ball.acc.y = -(rolling_ball.obj.rolling_ball.vel.y / speed_a) * Physics.DRAG
    
    return rolling_ball

def delete_svg_files():
    files = glob.glob('table-*.svg')
    for f in files:
        os.remove(f)
def nudge():
        return random.uniform( -1.5, 1.5 );


class MyHandler(BaseHTTPRequestHandler):
    global game
    def _set_headers(self, content_type="text/html"):
        self.send_response(200)
        self.send_header('Content-type', content_type)
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):

        parsed = urlparse(self.path)
        query_params = parse_qs(parsed.query)
        
        print(parsed)
        if parsed.path == '/' or parsed.path == '/index.html':
            self.serve_file('/templates/index.html', "text/html")
        
        elif parsed.path == '/game.html':
            self.serve_file('/templates/game.html', "text/html")
        elif parsed.path == '/table.html':
            self.serve_file('/templates/table.html', "text/html")

        elif parsed.path == '/api/get-table-at-time':
            query_params = dict(parse_qsl(parsed.query))
            time=query_params.get('time')
            if(time):
                svg=game.tableTime(time)
                # print(svg)
                if svg:
                    self.send_response(200)
                    self.send_header('Content-Type', 'text/html')
                    self.end_headers()
                    
                    self.wfile.write(svg.encode('utf-8'))
                else:
                    # Handle case where no SVG is found for the given time
                    self.send_error(404, "No table found for the given time.")
            else:
                # Handle missing or invalid time parameter
                self.send_error(400, "Missing or invalid 'time' query parameter.")



        elif parsed.path == '/api/game-data':
                # Extract gameID from query parameters
                query_params = dict(parse_qsl(parsed.query))
                gameID = query_params.get('gameID')
                
                if gameID:
                    # Fetch game data based on gameID. This is a placeholder function.
                    # You need to replace it with actual database fetching logic.
                    print("game id"+gameID)
                    game_data = db.getGame(int(gameID))
                    print("game data",game_data)
                    if game_data:
                        self._set_headers(content_type="application/json")
                        self.wfile.write(bytes(json.dumps(game_data), "utf-8"))
                    else:
                        self.send_error(404, "Game not found")
                else:
                    self.send_error(400, "Missing gameID parameter")


        elif parsed.path == '/init-table':            
            table = Physics.Table();
            # 1 ball
            pos = Physics.Coordinate( 
                            Physics.TABLE_WIDTH / 2.0,
                            Physics.TABLE_WIDTH / 2.0,
                            );

            sb = Physics.StillBall( 1, pos );
            table += sb;

            # 2 ball
            pos = Physics.Coordinate(
                            Physics.TABLE_WIDTH/2.0 - (Physics.BALL_DIAMETER+4.0)/2.0 +
                            nudge(),
                            Physics.TABLE_WIDTH/2.0 - 
                            math.sqrt(3.0)/2.0*(Physics.BALL_DIAMETER+4.0) +
                            nudge()
                            );
            sb = Physics.StillBall( 2, pos );
            table += sb;

            # 3 ball
            pos = Physics.Coordinate(
                            Physics.TABLE_WIDTH/2.0 + (Physics.BALL_DIAMETER+4.0)/2.0 +
                            nudge(),
                            Physics.TABLE_WIDTH/2.0 - 
                            math.sqrt(3.0)/2.0*(Physics.BALL_DIAMETER+4.0) +
                            nudge()
                            );
            sb = Physics.StillBall( 3, pos );
            table += sb;

            

            pos = Physics.Coordinate(
                            614 +
                            nudge(),
                            569 +
                            nudge()
                            );
            sb = Physics.StillBall( 4, pos );
            table += sb;

            pos = Physics.Coordinate(
                            676 +
                            nudge(),
                            569 +
                            nudge()
                            );
            sb = Physics.StillBall( 5, pos );
            table += sb;
            pos = Physics.Coordinate(
                            736+
                            nudge(),
                            568 +
                            nudge()
                            );
            sb = Physics.StillBall( 6, pos );
            table += sb;

            pos = Physics.Coordinate(
                            584 +
                            nudge(),
                            516 +
                            nudge()
                            );
            sb = Physics.StillBall( 7, pos );
            table += sb;


            pos = Physics.Coordinate(
                            644+
                            nudge(),
                            516 +
                            nudge()
                            );
            sb = Physics.StillBall( 8, pos );
            table += sb;


            pos = Physics.Coordinate(
                            706 +
                            nudge(),
                            515 +
                            nudge()
                            );
            sb = Physics.StillBall( 9, pos );
            table += sb;

            pos = Physics.Coordinate(
                            765 +
                            nudge(),
                            515 +
                            nudge()
                            );
            sb = Physics.StillBall( 10, pos );
            table += sb;

            pos = Physics.Coordinate(
                            553 +
                            nudge(),
                            462 +
                            nudge()
                            );
            sb = Physics.StillBall( 11, pos );
            table += sb;

            pos = Physics.Coordinate(
                            613 +
                            nudge(),
                            463 +
                            nudge()
                            );
            sb = Physics.StillBall( 12, pos );
            table += sb;

            pos = Physics.Coordinate(
                            675 +
                            nudge(),
                            463 +
                            nudge()
                            );
            sb = Physics.StillBall( 13, pos );
            table += sb;

            pos = Physics.Coordinate(
                            737 +
                            nudge(),
                            464 +
                            nudge()
                            );
            sb = Physics.StillBall( 14, pos );
            table += sb;

            pos = Physics.Coordinate(
                            797 +
                            nudge(),
                            464 +
                            nudge()
                            );
            sb = Physics.StillBall( 15, pos );
            table += sb;

            
            pos = Physics.Coordinate( Physics.TABLE_WIDTH/2.0 + random.uniform( -3.0, 3.0 ),
                                    Physics.TABLE_LENGTH - Physics.TABLE_WIDTH/2.0 );
            # vel = Physics.Coordinate( 0.0, 0.0 );
            # acc = Physics.Coordinate( 0.0, 0.0 );
            sb  = Physics.StillBall( 0, pos);

            table += sb;
            tableid=db.writeTable( table );   
            svg_content=table.svg()
            # Respond with the SVG
            # Combine the SVG content and table ID in a dictionary
            response_data = {
                'svgContent': svg_content,
                'tableId': tableid
            }
            
            # Convert the dictionary to a JSON string
            response_json = json.dumps(response_data)
            
            # Send the response with JSON content type
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(response_json.encode('utf-8'))

        elif parsed.path.endswith(".css"):
            self.serve_file(parsed.path, "text/css")
        elif parsed.path.endswith(".js"):
            self.serve_file(parsed.path, "application/javascript")
        elif parsed.path.startswith("/table-") and parsed.path.endswith(".svg"):
            self.serve_file(parsed.path, "image/svg+xml")
        else:
            self.send_error(404, 'File Not Found: %s' % self.path)
    
    
    def do_POST(self):
        global game
        parsed = urlparse(self.path)
        print(parsed)

        if self.path == '/api/reset-game':
            # Here you would add your logic to reset the game state.
            # This could involve resetting the database entries for the game state,
            # moving all balls back to their starting positions, resetting scores, etc.
            
            # For demonstration, let's just print a message to the console.
            print("Resetting game state...")
            
            # After resetting the game, send a success response back to the client.
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {'status': 'success', 'message': 'Game reset successfully'}
            self.wfile.write(json.dumps(response).encode())

        elif parsed.path == '/game.html':
            content_length = int(self.headers['Content-Length']) # Gets the size of data
            post_data = self.rfile.read(content_length) # Reads the data itself
        
            try:
                # Parse the JSON data
                form_data = json.loads(post_data.decode('utf-8'))
                
                # Extract game and player names from form data
                gameName = form_data.get('gameName')
                player1Name = form_data.get('player1')
                player2Name = form_data.get('player2')
                if gameName and player1Name and player2Name:
                    gameData = db.setGame(gameName, player1Name, player2Name)

                    # self.send_response(200)
                    response = {
                            'success': True,
                            'redirectURL': '/game.html?gameID={}'.format(gameData)  # Assuming you want to pass gameID
                        }

                    # # Assuming you want to redirect to a game page where gameID is passed as a query parameter
                    self._set_headers(content_type="application/json")
                    self.wfile.write(bytes(json.dumps(response), "utf-8"))

                else:
                    # Missing form data, send error response
                    self.send_error(400, "Missing game or player names in form data")
            
            except json.JSONDecodeError as e:
                # Handle JSON parsing error
                self.send_error(400, "Bad Request: Invalid JSON data")
        
        elif self.path == '/api/submit-shot':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            # Parse JSON data from the request
            shot_data = json.loads(post_data.decode('utf-8'))
            tableId = int(shot_data['tableId'])
            gameID = int(shot_data['gameId'])
            print("game ID ", gameID)
            print("table ID ", tableId)

            velocityX = float(shot_data['velocityX'])
            velocityY = float(shot_data['velocityY'])
            # tableIdtable=db.readTable(tableId)
            # print("\nserver read", table)
            print("tested ",velocityX,velocityY)
            # cueBall=table.cueBall()
            # print("Test")
            # print(cueBall,table)
            # if cueBall.type==Physics.StillBall:
            #     cueBall.type=Physics.RollingBall
            # cueBall.obj.rolling_ball.vel.x=velocityX
            # cueBall.obj.rolling_ball.vel.y=velocityY
            # cueBall=compute_acceleration(cueBall)
            # print("before shoot",cueBall)

            game=Physics.Game(db,gameID)
            # playerid=db.getPlayerID(game.player1Name)
            # print(playerid)
            game.shoot(game.gameName,game.player1Name,tableId,velocityX,velocityY)
            print("after shoot")
            # Process the shot data (e.g., update table state, calculate shot outcome)
            # This part depends on your application logic
            
            # Prepare a response (this is just an example response)
            response = {'status': 'success', 'message': 'Shot data processed successfully'}
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))


    # def do_POST(self):
    #     parsed = urlparse(self.path)
    #     delete_svg_files()  

    #     if parsed.path == '/display.html':

    #         # Parse form data
    #         form_data = self.parse_form_data()

    #         # Placeholder for actual physics simulation and SVG generation logic
    #         still_ball_number = int(form_data['sb_number'])
    #         still_ball_position = Physics.Coordinate(float(form_data['sb_x']), float(form_data['sb_y']))
    #         still_ball = Physics.StillBall(still_ball_number, still_ball_position)

    #         rolling_ball_number = int(form_data['rb_number'])
    #         rolling_ball_position = Physics.Coordinate(float(form_data['rb_x']), float(form_data['rb_y']))
    #         rolling_ball_velocity = Physics.Coordinate(float(form_data['rb_dx']), float(form_data['rb_dy']))
    #         rolling_ball_acceleration = Physics.Coordinate(0.0, 0.0)
    #         rolling_ball = Physics.RollingBall(rolling_ball_number, rolling_ball_position, rolling_ball_velocity, rolling_ball_acceleration)

    #         rolling_ball = compute_acceleration(rolling_ball)
    #         table = Physics.Table()
            

    #         # sb2_pos=Physics.Coordinate(575.0,575.0)
    #         # sb_2=Physics.StillBall(6,sb2_pos)
    #         # table+=sb_2

    #         # sb3_pos=Physics.Coordinate(575.0,650.0)
    #         # sb_3=Physics.StillBall(7,sb3_pos)
    #         # table+=sb_3

    #         # sb4_pos=Physics.Coordinate(650.0,575.0)
    #         # sb_4=Physics.StillBall(8,sb4_pos)
    #         # table+=sb_4
    #         table += still_ball

    #         table += rolling_ball

    #         index = 0
    #         while table is not None:
    #             with open(f"table-{index}.svg", "w") as svg_file:
    #                 svg_file.write(table.svg())
    #             table = table.segment()
    #             index += 1

    #         # Generate the display.html content
    #         content = self.generate_display_html(form_data,index)

    #         # Send the response
    #         self.send_response(200)
    #         self.send_header("Content-type", "text/html")
    #         self.send_header("Content-length", len(content))
    #         self.end_headers()
    #         self.wfile.write(bytes(content, "utf-8"))
    #     else:
    #         self.send_error(404, "File Not Found2: %s" % self.path)

    def parse_form_data(self):
        form_data = {}
        if 'Content-Length' in self.headers:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            form_data = dict(parse_qsl(post_data))
        return form_data

    
    def serve_game_page(self, gameName, player1Name, player2Name):
        try:
            with open('game.html', 'r') as file:
                content = file.read()

                # Replace placeholders with actual game data
                content = content.replace('{{gameName}}', gameName)
                content = content.replace('{{player1Name}}', player1Name)
                content = content.replace('{{player2Name}}', player2Name)

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(bytes(content, 'utf-8'))
        except FileNotFoundError:
            self.send_error(404, 'File Not Found: game.html')

    def serve_file(self, path, content_type):
        try:
            with open('.' + path, 'rb') as file:
                content = file.read()
                self.send_response(200)
                self.send_header("Content-type", content_type)
                self.send_header("Content-length", len(content))
                self.end_headers()
                self.wfile.write(content)
        except FileNotFoundError:
            self.send_error(404, "File Not Found3: %s" % path)

    def generate_display_html(self, form_data, max_index):
        # Generate HTML content dynamically
        html_content = '<html><body>'
        html_content += '<p>Simulation Results:</p>'
        
        # Add original ball positions and velocities
        html_content += '<p>Original Ball Positions and Velocities:</p>'
        html_content += f'<p>Still Ball Number: {form_data["sb_number"]}</p>'
        html_content += f'<p>Still Ball Position: ({form_data["sb_x"]}, {form_data["sb_y"]})</p>'
        html_content += f'<p>Rolling Ball Number: {form_data["rb_number"]}</p>'
        html_content += f'<p>Rolling Ball Position: ({form_data["rb_x"]}, {form_data["rb_y"]})</p>'
        html_content += f'<p>Rolling Ball Velocity: ({form_data["rb_dx"]}, {form_data["rb_dy"]})</p>'
        
        # Add SVG files as images in order of their index values
        for index in range(max_index + 1):
            svg_file = f'table-{index}.svg'
            if os.path.exists(svg_file):
                html_content += f'<img src="/{svg_file}" alt="{svg_file}"><br>'
        
        # Add Back link
        html_content += '<br><a href="/shoot.html">Back</a>'
        html_content += '</body></html>'
        
        return html_content

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 51668
    global db
    db = Physics.Database(True)
    db.createDB()

    game=None


    server_address = ('', port)
    httpd = HTTPServer(server_address, MyHandler)
    print(f"Starting server on port {port}...")
    httpd.serve_forever()
