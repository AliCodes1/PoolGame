import phylib;
import sqlite3
import os
import math
################################################################################
# import constants from phylib to global variables
BALL_RADIUS   = phylib.PHYLIB_BALL_RADIUS;
BALL_DIAMETER   = phylib.PHYLIB_BALL_DIAMETER;
HOLE_RADIUS   = phylib.PHYLIB_HOLE_RADIUS;
TABLE_LENGTH   = phylib.PHYLIB_TABLE_LENGTH;
TABLE_WIDTH   = phylib.PHYLIB_TABLE_WIDTH;

SIM_RATE   = phylib.PHYLIB_SIM_RATE;
VEL_EPSILON   = phylib.PHYLIB_VEL_EPSILON;
DRAG   = phylib.PHYLIB_DRAG;
MAX_TIME   = phylib.PHYLIB_MAX_TIME;
MAX_OBJECTS   = phylib.PHYLIB_MAX_OBJECTS;
FRAME_INTERVAL = 0.01
# add more here
HEADER = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg width="700" height="1375" viewBox="-25 -25 1400 2750"
xmlns="http://www.w3.org/2000/svg"
xmlns:xlink="http://www.w3.org/1999/xlink">
<rect width="1350" height="2700" x="0" y="0" fill="#C0D0C0" />""";
FOOTER = """</svg>\n""";


################################################################################
# the standard colours of pool balls
# if you are curious check this out:  
# https://billiards.colostate.edu/faq/ball/colors/

BALL_COLOURS = [ 
    "WHITE",
    "YELLOW",
    "BLUE",
    "RED",
    "PURPLE",
    "ORANGE",
    "GREEN",
    "BROWN",
    "BLACK",
    "LIGHTYELLOW",
    "LIGHTBLUE",
    "PINK",             # no LIGHTRED
    "MEDIUMPURPLE",     # no LIGHTPURPLE
    "LIGHTSALMON",      # no LIGHTORANGE
    "LIGHTGREEN",
    "SANDYBROWN",       # no LIGHTBROWN 
    ];

################################################################################
class Coordinate( phylib.phylib_coord ):
    """
    This creates a Coordinate subclass, that adds nothing new, but looks
    more like a nice Python class.
    """
    pass;


################################################################################
class StillBall( phylib.phylib_object ):
    """
    Python StillBall class.
    """

    def __init__( self, number, pos ):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_STILL_BALL, 
                                       number, 
                                       pos, None, None, 
                                       0.0, 0.0 );
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = StillBall;

    def updateState(self,xvel,yvel):
        xpos, ypos = self.obj.still_ball.pos.x, self.obj.still_ball.pos.y
        self.type = phylib.PHYLIB_ROLLING_BALL
        
        self.obj.rolling_ball.pos.x, self.obj.rolling_ball.pos.y = xpos, ypos
        self.obj.rolling_ball.vel.x, self.obj.rolling_ball.vel.y = xvel, yvel
        self.obj.rolling_ball.number = 0
        print("self ",self)
        speed_a = phylib.phylib_length(self.obj.rolling_ball.vel)
        
        # Update accelerations based on the new velocities
        if speed_a > VEL_EPSILON:
            self.obj.rolling_ball.acc.x = -(self.obj.rolling_ball.vel.x / speed_a) * DRAG
            self.obj.rolling_ball.acc.y = -(self.obj.rolling_ball.vel.y / speed_a) * DRAG
        print("self 2 ",self)

    
        # self.compute_acceleration()
        # velocityCoord = Coordinate(xpos, ypos)
        # speed = phylib.phylib_length(velocityCoord)
        # self.obj.rolling_ball.acc.x = (-xvel / speed) * DRAG
        # self.obj.rolling_ball.acc.y = (-yvel / speed) * DRAG

    # add an svg method here
    def svg(self):
        # Assuming pos is a Coordinate object with x and y attributes
        ballColor=BALL_COLOURS[self.obj.still_ball.number % len(BALL_COLOURS)]
        print(ballColor)
        if(ballColor=="WHITE"):
            return f'<circle id="cueBall" cx="{int(self.obj.still_ball.pos.x)}" cy="{int(self.obj.still_ball.pos.y)}" r="{int(BALL_RADIUS)}" fill="{ballColor}" />\n'
            # return f'<circle id="cueBall" cx="{int(self.obj.still_ball.pos.x)}" cy="{int(self.obj.still_ball.pos.y)}" r="{int(BALL_RADIUS)}" fill="{ballColor}" />\n<line id="drawLine" x1="0" y1="0" x2="0" y2="0" stroke="black" stroke-width="10" visibility="hidden"/>\n'

        else:
            return f'<circle cx="{int(self.obj.still_ball.pos.x)}" cy="{int(self.obj.still_ball.pos.y)}" r="{int(BALL_RADIUS)}" fill="{ballColor}" />\n'



class RollingBall( phylib.phylib_object ):
    """
    Python RollBall class.
    """

    def __init__( self, number, pos, vel, acc ):
        """
        Constructor function. Requires ball number, position (x,y), velocity and acceleration as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, phylib.PHYLIB_ROLLING_BALL, number, pos, vel, acc, 0.0, 0.0 );
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = RollingBall;


    # add an svg method here
    def svg(self):
        return f'<circle cx="{int(self.obj.rolling_ball.pos.x)}" cy="{int(self.obj.rolling_ball.pos.y)}" r="{int(BALL_RADIUS)}" fill="{BALL_COLOURS[self.obj.rolling_ball.number % len(BALL_COLOURS)]}" />\n'

    def compute_acceleration(self): 
        # Compute speeds after collision
        speed_a = phylib.phylib_length(self.obj.rolling_ball.vel)
        
        # Update accelerations based on the new velocities
        if speed_a > VEL_EPSILON:
            self.obj.rolling_ball.acc.x = -(self.obj.rolling_ball.vel.x / speed_a) * DRAG
            self.obj.rolling_ball.acc.y = -(self.obj.rolling_ball.vel.y / speed_a) * DRAG
        
    

class Hole( phylib.phylib_object ):
    """
    Python Hole class.
    """

    def __init__( self,pos ):
        """
        Constructor function. Requires position (x,y) as and
        argument.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, phylib.PHYLIB_HOLE, 0, pos, None, None, 0.0, 0.0);
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = Hole;


    # add an svg method here
    def svg(self):
        return f'<circle cx="{int(self.obj.hole.pos.x)}" cy="{int(self.obj.hole.pos.y)}" r="{int(phylib.PHYLIB_HOLE_RADIUS)}" fill="black" />\n'


class HCushion( phylib.phylib_object ):
    """
    Python HCushion class.
    """

    def __init__( self,y ):
        """
        Constructor function. Requires the y position as an
        argument.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, phylib.PHYLIB_HCUSHION, 0, None, None, None, 0.0, y);
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = HCushion;
    
        


    # add an svg method here
    def svg(self):
        y_pos = -25 if self.obj.hcushion.y < 1350 / 2 else 2700
        svg_str = f'<rect width="1400" height="25" x="-25" y="{y_pos}" fill="darkgreen" />\n'
        return svg_str


class VCushion( phylib.phylib_object ):
    """
    Python VCushion class.
    """

    def __init__( self,x ):
        """
        Constructor function. Requires the x position as an
        argument.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self,phylib.PHYLIB_VCUSHION, 0, None, None, None, x, 0.0);

        # this converts the phylib_object into a StillBall class
        self.__class__ = VCushion;


    # add an svg method here
    def svg(self):
        x = -25 if self.obj.vcushion.x < 675 else 1350
        return f'<rect width="25" height="2750" x="{x}" y="-25" fill="darkgreen" />\n'



################################################################################

class Table( phylib.phylib_table ):
    """
    Pool table class.
    """

    def __init__( self ):
        """
        Table constructor method.
        This method call the phylib_table constructor and sets the current
        object index to -1.
        """
        phylib.phylib_table.__init__( self );
        self.current = -1;

    def __iadd__( self, other ):
        """
        += operator overloading method.
        This method allows you to write "table+=object" to add another object
        to the table.
        """
        self.add_object( other );
        return self;

    def __iter__( self ):
        """
        This method adds iterator support for the table.
        This allows you to write "for object in table:" to loop over all
        the objects in the table.
        """
        return self;

    def __next__( self ):
        """
        This provides the next object from the table in a loop.
        """
        self.current += 1;  # increment the index to the next object
        if self.current < MAX_OBJECTS:   # check if there are no more objects
            return self[ self.current ]; # return the latest object

        # if we get there then we have gone through all the objects
        self.current = -1;    # reset the index counter
        raise StopIteration;  # raise StopIteration to tell for loop to stop

    def __getitem__( self, index ):
        """
        This method adds item retreivel support using square brackets [ ] .
        It calls get_object (see phylib.i) to retreive a generic phylib_object
        and then sets the __class__ attribute to make the class match
        the object type.
        """
        result = self.get_object( index ); 
        if result==None:
            return None;
        if result.type == phylib.PHYLIB_STILL_BALL:
            result.__class__ = StillBall;
        if result.type == phylib.PHYLIB_ROLLING_BALL:
            result.__class__ = RollingBall;
        if result.type == phylib.PHYLIB_HOLE:
            result.__class__ = Hole;
        if result.type == phylib.PHYLIB_HCUSHION:
            result.__class__ = HCushion;
        if result.type == phylib.PHYLIB_VCUSHION:
            result.__class__ = VCushion;
        return result;

    def __str__( self ):
        """
        Returns a string representation of the table that matches
        the phylib_print_table function from A1Test1.c.
        """
        result = "";    # create empty string
        result += "time = %6.1f;\n" % self.time;    # append time
        for i,obj in enumerate(self): # loop over all objects and number them
            result += "  [%02d] = %s\n" % (i,obj);  # append object description
        return result;  # return the string

    def segment( self ):
        """
        Calls the segment method from phylib.i (which calls the phylib_segment
        functions in phylib.c.
        Sets the __class__ of the returned phylib_table object to Table
        to make it a Table object.
        """

        result = phylib.phylib_table.segment( self );
        if result:
            result.__class__ = Table;
            result.current = -1;
        return result;

    # add svg method here
    def svg(self):
        svg_content = HEADER
        for obj in self:
            if(obj!=None):
                svg_content += obj.svg()

        svg_content += FOOTER
        return svg_content
    
    def roll( self, t ):
        new = Table();
        for ball in self:
            if isinstance( ball, RollingBall ):
                # create4 a new ball with the same number as the old ball
                new_ball = RollingBall( ball.obj.rolling_ball.number,
                                        Coordinate(0,0),
                                        Coordinate(0,0),
                                        Coordinate(0,0) );
                # compute where it rolls to
                phylib.phylib_roll( new_ball, ball, t );
               
                # add ball to table
                new += new_ball;
            if isinstance( ball, StillBall ):
                # create a new ball with the same number and pos as the old ball
                new_ball = StillBall( ball.obj.still_ball.number,
                                        Coordinate( ball.obj.still_ball.pos.x,
                                                    ball.obj.still_ball.pos.y ) );
                # add ball to table
                new += new_ball;
        # return table
        return new;
    
    def cueBall(self):
        # Find and return the cue ball (number 0)
        for ball in self:
            if isinstance( ball, StillBall ):
                if ball.obj.still_ball.number == 0:
                    return ball
            elif isinstance( ball, RollingBall ):
                if ball.obj.rolling_ball.number == 0:
                    return ball
        return None



    
class Database():
    def __init__(self, reset=False):
        if reset and os.path.exists('phylib.db'):
            os.remove('phylib.db')
        self.conn = sqlite3.connect('phylib.db')
        self.cursor = self.conn.cursor()





    def createDB(self):
        # List of SQL commands to create tables
        table_commands = [
            '''
            CREATE TABLE IF NOT EXISTS Ball (
                BALLID INTEGER PRIMARY KEY AUTOINCREMENT,
                BALLNO INTEGER NOT NULL,
                XPOS FLOAT NOT NULL,
                YPOS FLOAT NOT NULL,
                XVEL FLOAT,
                YVEL FLOAT
            )
            ''',
            '''
            CREATE TABLE IF NOT EXISTS TTable (
                TABLEID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                TIME FLOAT NOT NULL
            );
            ''',
            '''
            CREATE TABLE IF NOT EXISTS BallTable (
                BALLID INTEGER NOT NULL,
                TABLEID INTEGER NOT NULL,
                FOREIGN KEY (BALLID) REFERENCES Ball(BALLID),
                FOREIGN KEY (TABLEID) REFERENCES TTable(TABLEID)

            );
            ''',
            '''
            CREATE TABLE IF NOT EXISTS Shot (
                SHOTID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                PLAYERID INTEGER NOT NULL,
                GAMEID INTEGER NOT NULL,
                FOREIGN KEY (PLAYERID) REFERENCES Player(PLAYERID),
                FOREIGN KEY (GAMEID) REFERENCES Game(GAMEID)
            );
            ''',
            '''
            CREATE TABLE IF NOT EXISTS TableShot (
                TABLEID INTEGER NOT NULL,
                SHOTID INTEGER NOT NULL,
                FOREIGN KEY (TABLEID) REFERENCES TTable(TABLEID),
                FOREIGN KEY (SHOTID) REFERENCES Shot(SHOTID)
            );
            ''',
            '''
            CREATE TABLE IF NOT EXISTS Game (
                GAMEID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                GAMENAME VARCHAR(64) NOT NULL
            );
            ''',
            '''
            CREATE TABLE IF NOT EXISTS Player (
                PLAYERID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                GAMEID INTEGER NOT NULL,
                PLAYERNAME VARCHAR(64) NOT NULL,
                FOREIGN KEY (GAMEID) REFERENCES Game(GAMEID)
            );
            '''
        ]
        # Execute each command
        for command in table_commands:
            self.cursor.execute(command)

        # Commit changes and close cursor
        self.cursor.close()        
        self.conn.commit()    
    
    def readTable(self,tableID):
        self.open()

        adjusted_tableID = tableID + 1
        # Try to fetch the table's time attribute
        self.cursor.execute("SELECT TIME FROM TTable WHERE TABLEID = ?", (adjusted_tableID,))
        time_result = self.cursor.fetchone()
        print(time_result)
        if not time_result:
            return None
        table_time = time_result[0]

        # Fetch all balls associated with the table, including their velocity for type determination
        self.cursor.execute('''
            SELECT b.BALLID, b.BALLNO, b.XPOS, b.YPOS, b.XVEL, b.YVEL
            FROM BallTable bt
            JOIN Ball b ON bt.BALLID = b.BALLID
            WHERE bt.TABLEID = ?
        ''', (adjusted_tableID,))
        balls_data = self.cursor.fetchall()

        # Assuming the existence of a Table class that can be instantiated with time and supports adding balls
        table = Table()  # Initialize the table with its time attribute
        table.time=table_time
        # Process each ball's data to create StillBall or RollingBall instances as appropriate
        for ball_data in balls_data:
            ball_id, ball_no, xpos, ypos, xvel, yvel = ball_data
            print("ball data",ball_id, ball_no, xpos, ypos, xvel, yvel)
            if xvel == 0.0 and yvel == 0.0:
                # Instantiate StillBall (replace with your actual class and parameters)
                ball = StillBall(ball_no, Coordinate(xpos, ypos))
            else:
                # Instantiate RollingBall and set acceleration (replace with your actual class and parameters)
                ball = RollingBall(ball_no, Coordinate(xpos, ypos), Coordinate(xvel, yvel), Coordinate(0, 0))
                
                # set acceleration here based on your A2 logic
                ball.compute_acceleration()
            # Add the ball to the table
            table+=ball

        self.cursor.close()        
        self.conn.commit()  
        print("read",table)
        return table

    def open(self):
        # Establish a new database conn
        self.conn = sqlite3.connect("phylib.db")
        self.cursor = self.conn.cursor()

    def writeTable(self, table):
        self.cursor = self.conn.cursor()
        # Insert table time into TTable and retrieve TABLEID
        insert_table_query = 'INSERT INTO TTable (TIME) VALUES (?)'
        self.cursor.execute(insert_table_query, (table.time,))
        table_id = self.cursor.lastrowid  # Retrieve autoincremented TABLEID
        
        for obj in table:
            if isinstance(obj, (StillBall, RollingBall)):
                # Process ball objects - assume we have a table called 'Ball'
                xvel, yvel = (obj.obj.rolling_ball.vel.x, obj.obj.rolling_ball.vel.y) if isinstance(obj, RollingBall) else (0, 0)
                insert_query = '''INSERT INTO Ball (BALLNO, XPOS, YPOS, XVEL, YVEL) VALUES (?, ?, ?, ?, ?)'''
                self.cursor.execute(insert_query, (obj.obj.rolling_ball.number, obj.obj.rolling_ball.pos.x, obj.obj.rolling_ball.pos.y, xvel, yvel))
                ball_id = self.cursor.lastrowid

                # Link the ball to the current table state in BallTable
                insert_balltable_query = 'INSERT INTO BallTable (BALLID, TABLEID) VALUES (?, ?)'
                self.cursor.execute(insert_balltable_query, (ball_id, table_id))

        # Commit changes to the database
        self.conn.commit()
        self.cursor.close()


        # Return adjusted TABLEID (for zero-based indexing preference)
        return table_id - 1
    def commit(self):
        self.conn.commit()

    def close(self):
        # Commit any pending transactions and close the conn
        self.conn.commit()
        self.conn.close()

    def getGame(self, gameID):
        self.cursor = self.conn.cursor()
        adjusted_gameID = int(gameID) + 1  # Adjust for SQL's 1-based indexing
        query = '''
        SELECT g.gameName, p1.playerName AS player1Name, p2.playerName AS player2Name
        FROM Game g
        JOIN Player p1 ON g.GAMEID = p1.GAMEID AND p1.PLAYERID < p2.PLAYERID
        JOIN Player p2 ON g.GAMEID = p2.GAMEID
        WHERE g.GAMEID = ?
        '''
        self.cursor.execute(query, (adjusted_gameID,))
        result = self.cursor.fetchone()
        # self.close()
        if result:
            # Assuming the Game object has a method or process to update attributes based on fetched data
            gameName, player1Name, player2Name = result
            return [gameName, player1Name, player2Name]
        else:
            return None


    def setGame(self,gameName, player1Name, player2Name):
        #Insert the new game
        self.cursor = self.conn.cursor()

        insert_game_query = 'INSERT INTO Game (gameName) VALUES (?)'
        self.cursor.execute(insert_game_query, (gameName,))
        game_id = self.cursor.lastrowid  # Retrieve autoincremented GAMEID
        
        #Insert players ensuring player1Name gets the lower PLAYERID
        insert_player_query = 'INSERT INTO Player (playerName, GAMEID) VALUES (?, ?)'
        # Insert player1
        self.cursor.execute(insert_player_query, (player1Name, game_id))
        # Insert player2
        self.cursor.execute(insert_player_query, (player2Name, game_id))
        
        # self.close()
        # Return the GAMEID adjusted for zero-based indexing
        return game_id - 1

    def newShot(self,gameID,playerID):
        insert_shot_query = '''
        INSERT INTO Shot (PLAYERID, GAMEID) VALUES (?, ?)
        '''
        self.cursor = self.conn.cursor()

        self.cursor.execute(insert_shot_query, (playerID, gameID))
        self.conn.commit()
        shotID = self.cursor.lastrowid
        return shotID
    
    def getPlayerID(self, playerName):
        query = "SELECT PLAYERID FROM Player WHERE PLAYERNAME = ?"
        self.cursor.execute(query, (playerName,))
        result = self.cursor.fetchone()
        if result:
            return result[0]  # Return the PLAYERID
        else:
            return None  # Player not found



# class Game:
#     def __init__(self, gameID=None, gameName=None, player1Name=None, player2Name=None):
#         # Scenario (i): gameID is provided, and all other arguments are None
#         self.conn = sqlite3.connect('phylib.db')
#         self.cursor = self.conn.cursor()

#         if isinstance(gameID, int) and gameName is None and player1Name is None and player2Name is None:
#             self.gameID = gameID
#             # Retrieve game details from the database
#             gameInfo=Database.getGame(gameID)
#             self.gameName = gameInfo[0]
#             self.player1Name = gameInfo[1]
#             self.player2Name = gameInfo[2]


#         # Scenario (ii): gameID is None, and names are provided
#         elif gameID is None and all(isinstance(name, str) for name in [gameName, player1Name, player2Name]):
#             self.gameID = Database.setGame(self.cursor,gameName,player1Name,player2Name)
#             self.gameName = gameName
#             self.player1Name = player1Name
#             self.player2Name = player2Name
#             # Set new game details in the database
#         else:
#             raise TypeError("Invalid arguments provided to the constructor")

#         # Placeholder for the Table class object, to be assigned later
#         self.table = None

    
#     def shoot(self, gameName, playerName, table, xvel, yvel):        
#         # Assuming Database class has a method to get a playerID by name
#         query = "SELECT PLAYERID FROM Player WHERE PLAYERNAME = ?"
#         self.cursor.execute(query, (playerName,))
#         result = self.cursor.fetchone()
#         print(table)
#         playerID = result

#         # Assuming Database class has a method to record a new shot and return its ID
#         shotID = Database.newShot(self,playerID, self.gameID)

#         cue_ball = table.cueBall()
#         print(cue_ball)

#         if cue_ball:
#             cue_ball.updateState(xvel, yvel)  # Ensure this updates ball state as needed
            
#             initial_time = table.time
#             while True:
#                 new_table = table.segment()  # Assume this updates the table or returns None when done
#                 if new_table!=None:
#                     print("test2")
#                     time_difference = new_table.time - initial_time
#                 else: 
#                     print("test1")
#                     break

                
#                 frames = int(time_difference / FRAME_INTERVAL)
#                 print(frames)
#                 for i in range(frames):
#                     roll_time = i * FRAME_INTERVAL
#                     new_table = new_table.roll(roll_time)  # Assume this correctly rolls to the new state
#                     new_table.time = initial_time + roll_time
                    
#                     table_id = Database.writeTable(self, new_table)  # Pass cursor, assume handling
#                     self.conn = sqlite3.connect("phylib.db")
#                     self.cursor = self.conn.cursor() 

#                     self.cursor.execute("INSERT INTO TableShot (SHOTID, TABLEID) VALUES (?, ?)", (shotID, table_id))

#             print(f"Shot executed successfully. Shot ID: {shotID}")
#             self.conn.commit()  # Commit once after all operations
#             return shotID

#         else:
#             print("none")
#             return None


class Game ():

    def __init__ (self, db,gameID=None, gameName = None, player1Name = None, player2Name = None) :
        self.db=db
        
        if gameID is not None and (gameName is not None or player1Name is not None or player2Name is not None):
            raise TypeError("Invalid constructor arguments")
        elif gameID is None and (gameName is None or player1Name is None or player2Name is None):
            raise TypeError("Invalid constructor arguments")

        # Initialize member variables
        self.gameID = None
        self.gameName = None
        self.player1Name = None
        self.player2Name = None

        # If gameID is provided, retrieve game details from the database
        if gameID is not None:
            game_data = self.db.getGame(gameID)
            print(f"Game data is {game_data}")
            if game_data:
                self.gameID = gameID 
                self.gameName = game_data[0]
                # Retrieve player names from the Player table based on GAMEID
                player_data = self.db.cursor.execute("SELECT PLAYERNAME FROM Player WHERE GAMEID = ?", (self.gameID+1,)).fetchall()
                if len(player_data) >= 2:
                    self.player1Name = player_data[0][0]
                    self.player2Name = player_data[1][0]

        # If gameID is None, create a new game and add it to the database
        else:
            cursor = self.db.cursor()
            cursor.execute("INSERT INTO Game (GAMENAME) VALUES (?)", (gameName,))
            self.gameID = cursor.lastrowid-1

            cursor.execute("INSERT INTO Player (PLAYERNAME, GAMEID) VALUES (?, ?)", (player1Name, self.gameID))
            cursor.execute("INSERT INTO Player (PLAYERNAME, GAMEID) VALUES (?, ?)", (player2Name, self.gameID))

            # Assign player names directly from the provided arguments
            self.player1Name = player1Name
            self.player2Name = player2Name           

    
    def shoot(self, gameName, playerName, tableID, xvel, yvel):
        # Get the playerID from the playerName
        # def write_svg( table_id, table ):
        #     print("svg Table",table)
        #     with open( "table%02d.svg" % table_id, "w" ) as fp:
        #         fp.write( table.svg() );
        
        cursor = self.db.cursor
        player_data = cursor.execute("SELECT PLAYERID FROM Player WHERE PLAYERNAME=?", (playerName,)).fetchone()
        if player_data is None:
            raise ValueError("Player not found")

        playerID = player_data[0]

        # Add a new shot to the Shot table
        shotID = self.db.newShot(self.gameID, playerID)
        print("velocities ",xvel,yvel)
        update_query = """
        UPDATE Ball
        SET XVEL = ?, YVEL = ?
        WHERE BALLNO = 0 AND BALLID IN (
            SELECT Ball.BALLID
            FROM Ball
            INNER JOIN BallTable ON Ball.BALLID = BallTable.BALLID
            WHERE BallTable.TABLEID = ? AND Ball.BALLNO = 0
        );
        """
        

        # Execute the query with the new values
        try:
            print(f"Updating velocity for tableID: {tableID} with XVEL: {xvel}, YVEL: {yvel}")
            cursor.execute(update_query, (xvel, yvel, tableID+1))
            self.db.commit()
            print("Update successful.")
        except Exception as e:
            print(f"Error updating ball velocity: {e}")


        table=self.db.readTable(tableID)
        # print("table",table)
        # cue_ball=table.cueBall()
        # if cue_ball is None:
        #     raise ValueError("Cue ball not found")
        # cue_ball.compute_acceleration()
        # print("after cueball table",table)

        segment_length = 0
        start_time = table.time
        # write_svg(0,table)

        # index=1
        while table:
            # with open( "table%02d.svg" % index, "w" ) as fp:
            #     fp.write( table.svg() );
            # write_svg(index,table)
            table = table.segment()
            # print("table", table)
            if table is None:
                break

            # index+=1
            end_time = table.time
            segment_length = (end_time - start_time) / FRAME_INTERVAL
            segment_length = int(segment_length)
            for i in range(segment_length):
                time_passed = i * FRAME_INTERVAL
                new_table = table.roll(time_passed)
                new_table.time = start_time + time_passed
                new_table.id = self.db.writeTable(new_table)
                
                shotID = self.db.newShot(self.gameID, playerID)  # Get the shot ID
                self.db.cursor.execute("INSERT INTO TableShot (SHOTID, TABLEID) VALUES (?, ?)", (shotID, new_table.id))
                self.db.commit()

        
            start_time = end_time

    
    
    def tableTime(self, time):
        self.conn = sqlite3.connect('phylib.db')
        cursor = self.conn.cursor()


        # query1 = "SELECT TABLEID FROM TTable ORDER BY TABLEID DESC LIMIT 1"

        # # Execute the query
        # cursor.execute(query1)

        # Fetch one result
        last_table_id = cursor.fetchone()


        # Prepare the SQL query to select the table state closest to and preceding the specified time
        query = """
        SELECT TABLEID
        FROM TTable
        WHERE TIME <= ?
        ORDER BY TIME DESC
        LIMIT 1
        """


        # Execute the query with the provided time
        cursor.execute(query, (time,))

        # Fetch the result
        result = cursor.fetchone()

        if result:
            # if result[0]==last_table_id:
            #     return None
            
            tableId = result[0]
            table=self.db.readTable(tableId-1)
            tableSVG=table.svg()
        
            return tableSVG
        return None

