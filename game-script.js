$(document).ready(function() {
    // Assuming you have an endpoint like /api/game-data?gameID=1234 to fetch game data
    // The gameID can be extracted from the URL if passed as a query parameter to game.html
    const queryParams = new URLSearchParams(window.location.search);
    const gameID = queryParams.get('gameID'); // Assuming the game ID is passed as a query parameter
    var tableID;
    var currentTime = 0.0;
    var interval = 10; // milliseconds between updates, adjust as necessary
    var simulationRate = 0.01; // increase to speed up the simulation, decrease to slow down
    var intervalId;
    var maxTime=1;
    var shootOver=false;

    if (gameID) {
        fetchGameData(gameID);
    } else {
        console.error("Game ID not provided.");
    }

    // Function to fetch game data from the server
    function fetchGameData(gameID) {
        console.log("game id"+gameID)
        $.ajax({
            url: `/api/game-data?gameID=${gameID}`,
            type: 'GET',
            dataType: 'json', // Expect JSON response from the server
            success: function(response) {
                // Update the webpage with the fetched game data
                $('#game-title').text(`Game: ${response[0]}`);
                $('#player2-name').text(`Player 2: ${response[2]}`);
                $('#player1-name').text(`Player 1: ${response[1]}`);
                
                initTable()
            },
            error: function(xhr, status, error) {
                console.error('Failed to fetch game data:', error);
            }
        });
    }

    // Reset game button functionality (example)
    $('#reset-game').click(function() {
        // Confirm with the user that they want to reset the game
        var confirmReset = confirm("Are you sure you want to reset the game?");
        if (confirmReset) {
            // Make an AJAX call to your server endpoint to reset the game
            $.ajax({
                type: 'POST', // or 'GET', depending on how your server expects to receive the request
                url: '/api/reset-game', // Adjust this URL to your server's reset endpoint
                success: function(response) {
                    // Handle successful game reset
                    console.log("Game reset successfully");
                    // Optionally, refresh the page or update the UI to reflect the reset state
                    location.reload(); // This line reloads the page. You might choose to update the UI in another way.
                },
                error: function(xhr, status, error) {
                    // Handle errors
                    console.error("Failed to reset game:", status, error);
                }
            });
        }
    });

    
    // Initially load the pool table setup
    function initTable(){
        $.ajax({
            type: 'GET',
            url: 'http://localhost:51668/init-table', // Adjust this URL to your server endpoint
            dataType: 'json', // Expecting JSON response
            success: function(response) {
                // Parse the JSON response
                var svgContent = response.svgContent; // Access the SVG content
                tableID = response.tableId; // Access the table ID
                
                // Insert the SVG content into the 'svgs' div
                $('#svgs').html(svgContent);
                
        
                initializeCueBallInteraction();
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.error('Error fetching table initialization:', textStatus, errorThrown);
            }
        });
    }
    function initializeCueBallInteraction() {
        var tracking = false;
        var overlaySvg = $('#overlay-svg').get(0); // Get the overlay SVG DOM element
        var cueBall = $('#svgs circle[fill="WHITE"]');
        var line = $('#drawLine');
    
        // Adjust mouse coordinates to be relative to the overlay SVG
        function adjustMouseCoord(event) {
            var pt = overlaySvg.createSVGPoint();
            pt.x = event.clientX;
            pt.y = event.clientY;
            return pt.matrixTransform(overlaySvg.getScreenCTM().inverse());
        }
    
        // Listen for mousedown events on the cue ball
        cueBall.on('mousedown', function(event) {
            event.preventDefault();
            tracking = true;
    
            // Convert cue ball's position to the overlay SVG's coordinate system
            var cueBallRect = this.getBoundingClientRect();
            var cueBallCenter = adjustMouseCoord({ clientX: cueBallRect.left + cueBallRect.width / 2, clientY: cueBallRect.top + cueBallRect.height / 2 });
            console.log("cueball center "+cueBallCenter.x+" "+cueBallCenter.y)
            // Initialize the line's starting position at the cue ball's center
            line.attr({
                'x1': cueBallCenter.x,
                'y1': cueBallCenter.y,
                'x2': cueBallCenter.x,
                'y2': cueBallCenter.y,
                'visibility': 'visible'
            });

            // Update the line as the mouse moves
            $(document).on('mousemove', function(event) {
                if (tracking) {
                    var mousePos = adjustMouseCoord(event);
                    line.attr({
                        'x2': mousePos.x,
                        'y2': mousePos.y,
                        'visibility': 'visible'
                    });
                }
            });
            
        });
    
        
    
        // Finalize the line position on mouseup
        $(document).on('mouseup', function(event) {
            if (tracking) {
                tracking = false;
                var releasePos = adjustMouseCoord(event);
                var deltaX = releasePos.x - parseFloat(line.attr('x1')+100);
                var deltaY = releasePos.y - parseFloat(line.attr('y1')+50);
                var velX=deltaX * 0.1;
                var velY=deltaY *0.1;
                sendShotData(tableID,velX,velY);
                line.attr('visibility', 'hidden');
                console.log("Initial Velocity X:", velX, "Initial Velocity Y:", velY);
                // Here, perform the shot using deltaX and deltaY as the initial velocities
            }
        });
    }
    

    // function sendShotData(tableId, velocityX, velocityY) {
    //     var postData = {
    //         tableId: tableId,
    //         velocityX: velocityX,
    //         velocityY: velocityY,
    //         gameId:gameID
    //     };
    
    //     $.ajax({
    //         type: 'POST',
    //         url: 'http://localhost:51668/api/submit-shot', // Adjust this URL to your server endpoint
    //         data: JSON.stringify(postData),
    //         contentType: 'application/json; charset=utf-8', // Specify the content type of the request
    //         dataType: 'json', // Expecting JSON response from the server
    //         success: function(response) {
    //             // Handle successful response
    //             console.log("Shot data submitted successfully:", response);
    //             // Additional logic to handle response goes here
    //             // var intervalId = setInterval(updateSimulation, interval);
                
    //         },
    //         error: function(jqXHR, textStatus, errorThrown) {
    //             console.error('Error submitting shot data:', textStatus, jqXHR.status, jqXHR.responseText);
    //         }
            
    //     });
    // }
    function sendShotData(tableId, velocityX, velocityY) {
        console.log("velocity ",velocityX,velocityY)
        var postData = {
            tableId: tableId,
            velocityX: velocityX,
            velocityY: velocityY,
            gameId: gameID
        };
    
        fetch('http://localhost:51668/api/submit-shot', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json; charset=utf-8'
            },
            body: JSON.stringify(postData)
        })
        .then(response => response.json())
        .then(data => {
            console.log("Shot data submitted successfully:", data);
            // Perform further actions based on the response
            var i=0;
            while (i<100){
                fetchAndUpdateTable(0.01*i)
                i+=1;
            }
        })
        .catch(error => {
            console.error('Error submitting shot data:', error);
        });
    }
    

    
    function fetchAndUpdateTable(time) {
        $.ajax({
            url: `/api/get-table-at-time?time=${time}`,
            type: 'GET',
            success: function(svgData) {
                console.log(svgData)
                $('#svgs').html(svgData);
                console.log("got table");

            },
            error: function(error) {
                console.error("Error fetching table data:", error);
            }
        });
    }

    function updateSimulation() {
        // Stop the simulation when current time exceeds maxTime
        if (currentTime > maxTime) {
            clearInterval(intervalId);
            console.log('Animation stopped.');
            return; // Exit the function to avoid further execution
        }
    
        fetchAndUpdateTable(currentTime);
        // currentTime += simulationRate;
    }



    

});
