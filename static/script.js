let gridDiv = document.getElementById("grid");
let R = 4, C = 4;

// draw empty grid
function draw(rows, cols){
    R = rows;
    C = cols;

    gridDiv.innerHTML = "";
    gridDiv.style.display = "grid";
    gridDiv.style.gridTemplateColumns = `repeat(${C}, 50px)`;

    for(let i = 0; i < R * C; i++){
        let d = document.createElement("div");
        d.className = "cell";
        gridDiv.appendChild(d);
    }
}

// initialize world
function init(){
    const rows = parseInt(document.getElementById("rows").value);
    const cols = parseInt(document.getElementById("cols").value);

    fetch("/init", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({rows, cols})
    })
    .then(res => res.json())
    .then(data => {
        draw(data.rows, data.cols);   // ✅ FIX: draw grid here
    });
}

// step simulation
function step(){
    fetch("/step")
    .then(res => res.json())
    .then(data => {

        draw(data.rows, data.cols);  // redraw grid

        let cells = document.querySelectorAll(".cell");

        // visited cells
        data.visited.forEach(([r,c])=>{
            cells[r * C + c].classList.add("visited");
        });

        // safe cells
        data.safe.forEach(([r,c])=>{
            cells[r * C + c].classList.add("safe");
        });

        // inferred danger only
        data.danger.forEach(([r,c])=>{
            cells[r * C + c].classList.add("danger");
        });

        // agent position
        let [r,c] = data.pos;
        cells[r * C + c].classList.add("agent");

        // info
        document.getElementById("p1").innerText =
            "Breeze: " + data.percept.breeze + " | Stench: " + data.percept.stench;

        document.getElementById("p2").innerText =
            "Inference Steps: " + data.steps;

        document.getElementById("p3").innerText =
            "Status: " + data.status;
    });
}