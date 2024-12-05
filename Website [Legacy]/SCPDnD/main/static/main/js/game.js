// game.js
$(document).ready(function() {
    // Get the canvas element
    var canvas = document.getElementById("game-canvas");
    var context = canvas.getContext("2d");

    // Variables for grid settings
    var gridSize = 50; // Size of each grid cell in pixels
    var numCellsX = canvas.width / gridSize;
    var numCellsY = canvas.height / gridSize;

    // Variables for tracking objects and characters
    var objects = [];
    var characters = [];

    // Flag to indicate if distance measurement tool is active
    var distanceToolActive = false;
    var distanceStartPoint = null;

    // Function to draw the grid
    function drawGrid() {
        context.beginPath();
        for (var x = 0; x <= canvas.width; x += gridSize) {
            context.moveTo(x, 0);
            context.lineTo(x, canvas.height);
        }
        for (var y = 0; y <= canvas.height; y += gridSize) {
            context.moveTo(0, y);
            context.lineTo(canvas.width, y);
        }
        context.strokeStyle = "lightgray";
        context.stroke();
    }

    // Function to draw objects
    function drawObjects() {
        context.clearRect(0, 0, canvas.width, canvas.height);
        drawGrid();

        // Draw objects
        objects.forEach(function(object) {
            context.fillStyle = object.color;
            context.fillRect(object.x * gridSize, object.y * gridSize, gridSize, gridSize);
        });

        // Draw characters
        characters.forEach(function(character) {
            context.fillStyle = character.color;
            context.fillRect(character.x * gridSize, character.y * gridSize, gridSize, gridSize);
        });

        // Draw distance measurement tool
        if (distanceToolActive && distanceStartPoint) {
            var mousePos = getMousePos(canvas, event);
            var distanceX = Math.abs(distanceStartPoint.x - mousePos.x) * gridSize;
            var distanceY = Math.abs(distanceStartPoint.y - mousePos.y) * gridSize;
            var distance = Math.sqrt(Math.pow(distanceX, 2) + Math.pow(distanceY, 2));
            context.beginPath();
            context.moveTo(distanceStartPoint.x * gridSize, distanceStartPoint.y * gridSize);
            context.lineTo(mousePos.x * gridSize, mousePos.y * gridSize);
            context.strokeStyle = "red";
            context.stroke();
            context.fillStyle = "black";
            context.fillText(distance.toFixed(2) + "m", (distanceStartPoint.x * gridSize + mousePos.x * gridSize) / 2, (distanceStartPoint.y * gridSize + mousePos.y * gridSize) / 2);
        }
    }

    // Function to handle mouse click event
    function handleMouseClick(event) {
        if (distanceToolActive) {
            if (!distanceStartPoint) {
                distanceStartPoint = getMousePos(canvas, event);
            } else {
                distanceStartPoint = null;
            }
        } else {
            // Handle object placement or character movement logic
            // ...
        }
    }

    // Function to get mouse position relative to the canvas
    function getMousePos(canvas, event) {
        var rect = canvas.getBoundingClientRect();
        return {
            x: Math.floor((event.clientX - rect.left) / gridSize),
            y: Math.floor((event.clientY - rect.top) / gridSize)
        };
    }

    // Event listeners
    canvas.addEventListener("click", function(event) {
        handleMouseClick(event);
    });

    // Render the initial game state
    drawObjects();
});
