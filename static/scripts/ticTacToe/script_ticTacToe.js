const socket = io();

const statusField = document.getElementById('status-field');
const gameBoard = document.getElementById('gameboard');

const STATUS_WAIT = "Waiting for opponent to join";
const STATUS_DISCONNECT = "User disconnected: waiting...";
const STATUS_PLAYER = "Your turn to move";
const STATUS_OPPONENT = "Waiting for opponent to move";
const STATUS_DRAW = "Game ended in a draw: Click on the grid to rematch";
const STATUS_PLAYER_WIN = "You won the game: Click on the grid to rematch";
const STATUS_OPPONENT_WIN = "Opponent won the game: Click on the grid to rematch";

const SYMBOL_X = 'X'
const SYMBOL_O = 'O'

const ROWS = 3;
const COLUMNS = 3;

const STATE_DRAW = -1;
const STATE_CONTINUE = 0
const PLAYER_1 = 1;
const PLAYER_2 = 2;

const CELL_MARKED = 1;

let opponentConnected = false;
let turn = undefined;
let state = undefined;

let SYMBOL_1 = SYMBOL_X
let SYMBOL_2 = SYMBOL_O


socket.on("content-to-client", function(data) {
    const content = JSON.parse(data);
    turn = content.turn;
    state = content.state;
    setBoard(content.board);
    setStatus()
});

socket.on("start-game-client", function() {
    opponentConnected = true;
    setStatus();
});

socket.on("pause-game-client", function() {
    opponentConnected = false;
    statusField.innerHTML = STATUS_DISCONNECT;
});

function addSquareListeners() {
    for (let row = 0; row < ROWS; row++) {
        for (let col = 0; col < COLUMNS; col++) {
            let cell = document.querySelector('#row-' + (row + 1) + '-col-' + (col + 1));
            cell.addEventListener('click', function(e) {
                let player = "{{ session['player'] }}";
                console.log(turn);
                console.log(opponentConnected);
                console.log(cell.value);
                console.log(player);
                if ((opponentConnected) && (cell.value == '') && (turn == player)) {
                    data = {'row': row, 'row': col};
                    socket.emit("content-to-server", data);
                }
            });
        }
    }
}

function setBoard(content_board) {
    for (const content_cell in content_board) {
        let cell = document.querySelector('#row-' + (content_cell.row + 1) + '-col-' + (content_cell.col + 1));
        if (content_cell.color == PLAYER_1) {
            cell.value = SYMBOL_1;
        }
        if (content_cell.color == PLAYER_2) {
            cell.value = SYMBOL_2
        }
        if (content_cell.marked == CELL_MARKED) {
            cell.style.color = 'red';
        }
    }
}

function setStatus() {
    let player = "{{ session['player'] }}";
    if (!opponentConnected) {
        statusField.innerHTML = STATUS_WAIT;
    }
    else {
        switch (state) {
        case STATE_DRAW:
            statusField.innerHTML = STATUS_DRAW;
            break;
        case STATE_CONTINUE:
            statusField.innerHTML = (turn == player) ? STATUS_PLAYER : STATUS_OPPONENT;
            break;
        case PLAYER_1:
            statusField.innerHTML = (turn != player) ? STATUS_PLAYER_WIN : STATUS_OPPONENT_WIN;
            break;
        case PLAYER_2:
            statusField.innerHTML = (turn != player) ? STATUS_PLAYER_WIN : STATUS_OPPONENT_WIN;
            break;
        }
    }
}

function resetBoard() {
    for (let row = 0; row < 3; row++) {
        for (let col = 0; col < 3; col++) {
            let cell = document.querySelector('#row-' + (row + 1) + '-col-' + (col + 1));
            cell.value = '';
            cell.style.color = 'black';
        }
    }
}

function swapSymbols() {
    SYMBOL_1 = (SYMBOL_1 == SYMBOL_X) ? SYMBOL_O : SYMBOL_X;
    SYMBOL_2 = (SYMBOL_2 == SYMBOL_O) ? SYMBOL_X : SYMBOL_O;
}

function addRematchListener() {
    gameBoard.addEventListener('click', function(e) {
        if (state != STATE_CONTINUE) {
            resetBoard()
            statusField.innerHTML = STATUS_WAIT;
            swapSymbols();
        }
    });
}

addSquareListeners()
addRematchListener()
setStatus()