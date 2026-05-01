let gridDiv = document.getElementById("grid");
let R = 4, C = 4;

function draw(rows, cols){
  R = rows; C = cols;
  gridDiv.style.gridTemplateColumns = `repeat(${C}, 50px)`;
  gridDiv.innerHTML = "";
  for(let i=0;i<R*C;i++){
    let d = document.createElement("div");
    d.className = "cell";
    gridDiv.appendChild(d);
  }
}

function idx(r,c){ return r*C + c; }

function init(){
  const rows = parseInt(document.getElementById("rows").value);
  const cols = parseInt(document.getElementById("cols").value);

  fetch("/init", {
    method: "POST",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify({rows, cols})
  })
  .then(r=>r.json())
  .then(d=>{
    draw(d.rows, d.cols);
    document.getElementById("p1").innerText = "";
    document.getElementById("p2").innerText = "";
    document.getElementById("p3").innerText = "";
  });
}

function step(){
  fetch("/step")
  .then(r=>r.json())
  .then(d=>{
    draw(d.rows, d.cols);

    let cells = document.querySelectorAll(".cell");

    // visited
    d.visited.forEach(([r,c])=>{
      cells[idx(r,c)].classList.add("visited");
    });

    // safe
    d.safe.forEach(([r,c])=>{
      cells[idx(r,c)].classList.add("safe");
    });

    // inferred danger ONLY (no cheating)
    d.danger.forEach(([r,c])=>{
      cells[idx(r,c)].classList.add("danger");
    });

    // agent
    let [r,c] = d.pos;
    cells[idx(r,c)].classList.add("agent");

    document.getElementById("p1").innerText =
      "Breeze: " + d.percept.breeze + " | Stench: " + d.percept.stench;

    document.getElementById("p2").innerText =
      "Inference Steps: " + d.steps;

    document.getElementById("p3").innerText =
      "Status: " + d.status;
  });
}