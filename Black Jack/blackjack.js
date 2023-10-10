let p = {
    n : "Per",
    c : 145
}
let carr = []
let sum = 0
let hasbj = false
let isalive = false
let msg = ""
let message = document.getElementById("messg")
let addn = document.getElementById("add")
let cd = document.getElementById("card")

let play = document.getElementById("player")
play.textContent = p.n + ": $" + p.c


function getrand() {
    return Math.floor(Math.random()*12) + 2
}

function start() {
    isalive = true
    let card1 = getrand()
    let card2 = getrand()
    carr = [card1, card2]
    sum = card1 + card2
    render()
}

function render() {
    cd.textContent = "Cards: "
    for(let i=0; i <carr.length; i++) {
        cd.textContent += carr[i] + " "
    }
    addn.textContent = "Sum is: " + sum
   if (sum <= 20) {
      msg = "Do u wanna draw?"
    }
   else if (sum === 21) {
      msg = "Wohoo u hav a blackjack"
      hasbj = true
    }
   else {
      msg = "U r out of game"
      isalive = false
    }
    message.textContent = msg
}
function newc() {
    if (hasbj === false && isalive === true) {
    let card3 = getrand()
    sum += card3
    carr.push(card3)
    console.log(card3)
    render()
    }
}