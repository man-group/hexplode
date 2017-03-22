function makeID(i, j) {
    return "tile_" + i + "_" + j;
}

function makeNeighbours(i, j, boardsize) {
    var maxi = 2 * boardsize - 1;
    var maxj = Math.min(boardsize + i, 3 * boardsize - 2 - i);
    var neighbours = [];
    
    if (j - 1 >= 0) {
        neighbours.push(makeID(i, j - 1)); // North neighbour
    }
    if (j + 1 < maxj) {
        neighbours.push(makeID(i, j + 1)); // South neighbour
    }
    if (i < ((maxi - 1) / 2)) {
        // West of the central column
        neighbours.push(makeID(i+1, j)); // Northeast neighbour
        neighbours.push(makeID(i+1, j+1)); // Southeast neighbour
        if (i - 1 >= 0) {
              // East of the first column
            if (j - 1 >= 0) {
                neighbours.push(makeID(i-1, j-1)); // Northwest neighbour
            }
            if (j < maxj - 1) {
                neighbours.push(makeID(i-1, j)); // Southwest neighbour
            }
        }
    } else if (i > ((maxi - 1) / 2)) {
        // East of the central column
        neighbours.push(makeID(i-1, j)); // Northwest neighbour
        neighbours.push(makeID(i-1, j+1)); // Soutwest neighbour
        if (i + 1 < maxi) {
              // West of the last column
            if (j - 1 >= 0) {
                neighbours.push(makeID(i+1, j-1)); // Northeast neighbour
            }
            if (j < maxj - 1) {
                neighbours.push(makeID(i+1, j)); // Southeast neighbour
            }
        }
    } else {
        // On the central column
        if (j - 1 >= 0) {
            neighbours.push(makeID(i-1, j-1)); // Northwest neighbour
            neighbours.push(makeID(i+1, j-1)); // Northeast neighbour
        }
        if (j < maxj - 1) {
            neighbours.push(makeID(i-1, j)); // Southwest neighbour
            neighbours.push(makeID(i+1, j)); // Southeast neighbour
        }
    }
    return neighbours;
}

function getBoardData() {
    var boardData = {};
    $("#board .tile").each(function(){
        boardData[this.id] = {counters: parseInt(this.attributes.counters.value),
                              player: parseInt(this.attributes.player.value),
                              neighbours: this.attributes.neighbours.value.split(","),
                             };
    });
    return boardData;
}

function drawBoard() {
    var board = $("#board");
    board.empty();

    var tile = { width: 60,
                 height: 55, // include css margin
                 hoverlap: 48,
                 voverlap: 27 };

    var boardsize = parseInt($("#boardsize")[0].value);
    
    var probabilityOfDamage = $("#damagedCells").is(':checked') * 0.2;
                 
    board.width((2*boardsize-2)*tile.hoverlap + tile.width);
    board.height((2*boardsize-1)*tile.height);

    for(var i=0; i<2*boardsize-1; ++i) {
        var numtilesinslice = Math.min(boardsize + i, 3*boardsize - 2 - i);

        $('<div/>', {id: "row" + i,
                     class: "row",
                     style: "left:" + (i*tile.hoverlap) + "px;top:" + ((2*boardsize-1-numtilesinslice)*tile.voverlap) + "px;",
                     }).appendTo('#board');

        for(var j=0; j<numtilesinslice; ++j) {
        	var initialCounters = "";
        	if (Math.random() < probabilityOfDamage) {
        		initialCounters = "-" + (1 + Math.floor(Math.random() * 5));
        	}
            $('<div/>', {id: makeID(i, j),
                         class: "tile",
                         counters: initialCounters,
                         player: "",
                         neighbours: makeNeighbours(i, j, boardsize),
                     }).appendTo("#row" + i);
        }
    }
}

function winGame(msg, gameId, playerId) {
	handleEndOfGame("#winner", msg, gameId, playerId, playerId);
}

function forfeitGame(msg, gameId, playerId) {
	handleEndOfGame("#error", msg, gameId, playerId, (playerId + 1) % 2);
}

function handleEndOfGame(dialog, msg, gameId, playerId, winnerId) {
    $(dialog).text(msg);
    $(".current-player").removeClass("current-player");

    for (var playerId=0; playerId<2; ++playerId) {
		sendRemoteGameOver($(PLAYER_ALGO_SELECT_LISTS[playerId] + " option:selected").text(), gameId, playerId, winnerId)
 	}
    
    $(dialog).dialog("open");
}

function errorMessage(msg) {
    $("#error").text(msg);
    $(".current-player").removeClass("current-player");
    $("#error").dialog("open");
}

function playRemoteCounter(tileId, algo, gameId, scores, playerId) {
    var tile = $("#"+tileId);
    if (tile.length!=1 || ["", "" + playerId].indexOf(tile.attr("player"))==-1) {
        forfeitGame(algo +" playing as player_" + (playerId+1) + " made an illegal move: " + tileId + " so forfeits the game.",
        		  gameId, playerId);
    } else {
        placeCounter(tileId, scores, playerId);
        next_move(gameId, scores, playerId);
    }
}

function sum(a) {
	return a.reduce(function (x,y) { return x+y; });
}

function placeCounter(tileId, scores, playerId) {
    if (!playerHasAllTheCounters(scores, playerId)) {
        var tile = $("#" + tileId);
        
        if ((tile.attr("player") != "") && (tile.attr("counters") != "")) {
        	scores[parseInt(tile.attr("player"))] -= parseInt(tile.attr("counters"));
        }
        
        var txtCounters = tile.attr("counters");
        var counters = (txtCounters=="" ? 0 : parseInt(txtCounters)) + 1;
        var neighbours = tile.attr("neighbours").split(",");
        if (counters == neighbours.length) {
            tile.attr("player", "");
            tile.attr("counters", "");
            for(var i=0; i<neighbours.length; ++i) {
                placeCounter(neighbours[i], scores, playerId);
            }
        } else {
            tile.attr("counters", counters);
        	if (counters > 0) {
            	tile.attr("player", playerId);
	            scores[playerId] += counters;
            }
        }
    }
}

function playerHasAllTheCounters(scores, playerId) {
	return (sum(scores) > scores.length) && (sum(scores.filter(function (v, i) { return i!=playerId; })) <= 0);
}

var TIMEOUT = 5;

function requestRemoteMove(algo, gameId, scores, playerId) {
    $(".current-player").removeClass("current-player");
    $("#player" + (playerId+1)).addClass("current-player");

    if (algo=="Human") {
        requestLocalMove(gameId, scores, playerId);
    } else {
        $.ajax("/algos/" + algo,
        {type: "POST",
        timeout: TIMEOUT * 1000,
        data: JSON.stringify({ board: getBoardData(),
                               playerId: playerId,
                               gameId: gameId[playerId],
                             }),
        cache: false,
        crossDomain: false,
        contentType: "application/json; charset=utf-8",
        dataType: "json"
        }).done(function(data, textStatus, jqXHR)
        {
            if ("error" in data) {
                forfeitGame(data.error, gameId, playerId);
            } else {
                playRemoteCounter(data.ok, algo, gameId, scores, playerId);
            }
        }).fail(function(jqXHR, textStatus, errorThrown) 
        {
            if (textStatus=='timeout') {
                var msg = algo + " playing as player_" + (playerId+1) + " took longer than " + TIMEOUT + "s to play its move so forfeits the game.";
            	forfeitGame(msg, gameId, playerId);
            } else {
                forfeitGame(textStatus + ' ' + errorThrown, gameId, playerId);
            }
        });
    }
}

function sendRemoteGameOver(algo, gameId, playerId, winnerId) {
    if (algo!="Human") {
        $.ajax("/gameover/" + algo,
        {type: "POST",
        timeout: TIMEOUT * 1000,
        data: JSON.stringify({ board: getBoardData(),
                               playerId: playerId,
                               gameId: gameId[playerId],
                               winnerId: winnerId
                             }),
        cache: false,
        crossDomain: false,
        contentType: "application/json; charset=utf-8",
        dataType: "json"
        }).done(function(data, textStatus, jqXHR)
        {
            if ("error" in data) {
                console.log("Error sending game over message: " + data.error);
            }
        }).fail(function(jqXHR, textStatus, errorThrown) 
        {
            console.log("Error sending game over message: " + textStatus + ' ' + errorThrown);
        });
    }
}

function requestLocalMove(gameId, scores, playerId) {
    function onClick() {
        $("#board .tile").unbind("click");
        placeCounter(this.id, scores, playerId);
        next_move(gameId, scores, playerId);
    }
    $("#board .tile[player=" + playerId + "]").click(onClick);
    $("#board .tile[player='']").click(onClick);
}

function displayScores(scores) {
    $.each(scores, function(i) {
        $("#score" + (i + 1)).text(this);
    });
}

function isGameOver(gameId, scores, playerId) {
	for(var playerId = 0; playerId < 2; ++playerId) {
	    if (playerHasAllTheCounters(scores, playerId)) {
	        winGame("Player " + (playerId + 1) + " wins", gameId, playerId);
	        return true;
	    }
    }
    return false;
}

var PLAYER_ALGO_SELECT_LISTS = ["#player1_algo", "#player2_algo"];

function next_move(gameId, scores, playerId) {
    displayScores(scores);

    if (!isGameOver(gameId, scores, playerId)) {
        playerId = (playerId + 1) % 2        
        requestRemoteMove($(PLAYER_ALGO_SELECT_LISTS[playerId] + " option:selected").text(), gameId, scores, playerId);
    }
}

function start() {
    $.ajax("/newgame", {
    	type: "POST",
		timeout: TIMEOUT * 1000,
		data: JSON.stringify({
			player1: $(PLAYER_ALGO_SELECT_LISTS[0] + " option:selected").text(),
			player2: $(PLAYER_ALGO_SELECT_LISTS[1] + " option:selected").text(),
			boardsize: parseInt($("#boardsize")[0].value)
		}),
		cache: false,
		crossDomain: false,
		contentType: "application/json; charset=utf-8",
		dataType: "json"
    }).done(function(data, textStatus, jqXHR) {
        if ("error" in data) {
            errorMessage(data.error);
        } else {
            next_move(data.ok, [0, 0], 1);
        }
    }).fail(function(jqXHR, textStatus, errorThrown) 
    {
        if (textStatus=='timeout') {
            console.log("Timeout getting game id.");
            start();
        } else {
            errorMessage(textStatus + ' ' + errorThrown);
        }
    });
}

function onClickStart() {
    drawBoard();
    $("#newgame").dialog("close");
    start();
}

function setToolTip() {
    $(this).attr('title', $(this).val());
}

function loadAlgoList() {
    $.ajax("/algos", { type: "GET",
                       timeout: 5000,
                       cache: false,
                         crossDomain: false,
                       dataType: "json" }
    ).done(function(data, textStatus, jqXHR) {
        if ("error" in data) {
            alert("Error reading list of available algos.");
            console.log(data.error);
        } else {
            var lists = $(PLAYER_ALGO_SELECT_LISTS.join(","));
            $.each(data.ok, function(key, value) {
                lists.append($('<option>', { value : value }).text(key)); 
            });
            $(PLAYER_ALGO_SELECT_LISTS[1])[0].options[1].selected = true;
            $(".settings select").each(setToolTip);
        }
    }).fail(function(jqXHR, textStatus, errorThrown) 
    {
        if (textStatus=='timeout') {
            console.log("Timeout reading list of available algos.");
            loadAlgoList();
        } else {
            alert("Error reading list of available algos.");
            console.log(textStatus);
            console.log(errorThrown);
        }    
    });
}

$(function () {

    drawBoard();
    
    $("#infopopup").dialog({width: "60%",
                            modal: true,
                            autoOpen:false,
                            buttons: [ { text: "History", click: function() { window.open("/static/history.html", "_blank"); }},
                                       { text: "OK", click: function() { $( this ).dialog( "close" ); }, autofocus:true },     ]
                            });

    $("#info").click(function(){
        $("#infopopup").dialog("open");
    });
        
    $("#exitpopup").dialog({width: "250px",
                            modal: true,
                            autoOpen:false,
                            buttons: [ { text: "No", click: function() { $( this ).dialog( "close" ); }, autofocus:true },
                                       { text: "Yes", click: function() { location.reload();  }},     ]
                            });
    
    $("#exit").click(function(){
        $("#exitpopup").dialog("open");
    });
    
    $("#winner").dialog({width: "250px",
                         modal: true,
                           autoOpen:false,
                         buttons: [ { text: "New Game", click: function() {
                                    $("#newgame").dialog("open");
                                    $(this).dialog("close");
                                }},     ]
                        });
    
    $("#error").dialog({width: "90%",
                         modal: true,
                           autoOpen:false,
                         buttons: [ { text: "New Game", click: function() {
                                    $("#newgame").dialog("open");
                                    $(this).dialog("close");
                                }},     ]
                        });
    
    $("#newgame").dialog({width: "400px",
                          modal: true,
                          buttons: [ { text: "Help", click: function() { $("#infopopup").dialog("open"); } },
                                     { text: "Start", click: onClickStart, autofocus:true }, ]
                        });
                        
    $('.ui-dialog-titlebar-close').hide();
    
    $(".settings select").change(setToolTip);
    
    // Because IE doesn't provide a spinner
    $("#boardsize").spinner({ change: drawBoard,
                              stop: drawBoard });
    
    loadAlgoList();
});
