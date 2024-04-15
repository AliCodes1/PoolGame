$(document).ready(function() {
    $('form').on('submit', function(event) {
        event.preventDefault(); // Prevent the form from submitting the traditional way

        // Collect form data
        var formData = {
            'gameName': $('input[name=gameName]').val(),
            'player1': $('input[name=player1]').val(),
            'player2': $('input[name=player2]').val()
        };

        console.log("Game Name:", formData.gameName);
        console.log("Player 1:", formData.player1);
        console.log("Player 2:", formData.player2);
        var jsonFormData = JSON.stringify(formData);

        // Send the form data to the server
        sendFormDataToServer(jsonFormData);
    });

    // Function to send form data to the server using jQuery for the AJAX call
    function sendFormDataToServer(formData) {
        $.ajax({
            type: 'POST',
            cache: false,
            url: 'http://localhost:51668/game.html', // Adjust this URL to match your server endpoint
            data: formData,
            dataType: 'json' // Expect JSON response
        })
        .done(function(response) {
            console.log(response)
            if(response.success) {
                window.location.href = response.redirectURL; // Redirecting as per server's response
            } else {
                console.error("Error: ", response);
            }
        })
        .fail(function(jqXHR, textStatus, errorThrown) {
            console.error('AJAX call failed: ', textStatus, errorThrown);
        });

    }
});
