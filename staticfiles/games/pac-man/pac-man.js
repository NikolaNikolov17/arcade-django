const scoreEl = document.querySelector('#scoreEL')
const canvas = document.querySelector('canvas')
const c = canvas.getContext('2d')

canvas.width = 1024
canvas.height = 576

function showEndScreen(message) {
    document.getElementById('endMessage').innerText = message;
    document.getElementById('finalScore').innerText = score;
    document.getElementById('endScreen').style.display = 'block';
}

function restartGame() {
    window.location.reload();
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.slice(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

class Boundary {
    static width = 40
    static height = 40

    constructor({ position, image }) {
        this.position = position
        this.width = 40
        this.height = 40
        this.image = image
    }

    draw() {
        // c.fillStyle = 'blue'
        // c.fillRect(this.position.x, this.position.y, this.width, this.height)

        c.drawImage(this.image, this.position.x, this.position.y)
    }

}

class Player {
    constructor({ position, velocity }) {
        this.position = position
        this.velocity = velocity
        this.radius = 15
        this.radians = 0.75
        this.openRate = 0.12
        this.rotation = 0
    }

    draw() {
        c.save()
        c.translate(this.position.x, this.position.y)
        c.rotate(this.rotation)
        c.translate(-this.position.x, -this.position.y)
        c.beginPath()
        c.arc(this.position.x, this.position.y, this.radius, this.radians, Math.PI * 2 - this.radians)
        c.lineTo(this.position.x, this.position.y)
        c.fillStyle = 'yellow'
        c.fill()
        c.closePath()
        c.restore()
    }

    update() {
        this.draw()
        this.position.x += this.velocity.x
        this.position.y += this.velocity.y

        if (this.radians < 0 || this.radians > 0.75)
          this.openRate = -this.openRate

        this.radians += this.openRate
    }

}

class Ghost {
    static speed = 2
    constructor({ position, velocity, color = 'red' }) {
        this.position = position
        this.velocity = velocity
        this.radius = 15
        this.color = color
        this.prevCollisions = []
        this.speed = 2
        this.scared = false
    }

    draw() {
        c.beginPath()
        c.arc(this.position.x, this.position.y, this.radius, 0, Math.PI * 2)
        c.fillStyle = this.scared ? 'blue' : this.color
        c.fill()
        c.closePath()
    }

    update() {
        this.draw()
        this.position.x += this.velocity.x
        this.position.y += this.velocity.y
    }

}

class Pellet {
    constructor({ position }) {
        this.position = position
        this.radius = 3
    }

    draw() {
        c.beginPath()
        c.arc(this.position.x, this.position.y, this.radius, 0, Math.PI * 2)
        c.fillStyle = 'white'
        c.fill()
        c.closePath()
    }

}

class PowerUp {
    constructor({ position }) {
        this.position = position
        this.radius = 10
    }

    draw() {
        c.beginPath()
        c.arc(this.position.x, this.position.y, this.radius, 0, Math.PI * 2)
        c.fillStyle = 'white'
        c.fill()
        c.closePath()
    }

}

const powerUps = []
const pellets = []
const boundaries = []
const ghosts = [
    new Ghost({
        position: {
            x: Boundary.width * 6 + Boundary.width / 2,
            y: Boundary.height + Boundary.height / 2
        },
        velocity: {
            x: Ghost.speed,
            y: 0
        }
    }),
    new Ghost({
        position: {
            x: Boundary.width * 6 + Boundary.width / 2,
            y: Boundary.height * 3 + Boundary.height / 2
        },
        velocity: {
            x: Ghost.speed,
            y: 0
        },
        color: 'pink'
    })
]
const player = new Player({
    position: {
        x: Boundary.width + Boundary.width / 2,
        y: Boundary.height + Boundary.height / 2
    },
    velocity: {
        x: 0,
        y: 0
    }
})

const keys = {
    w: {
        pressed: false
    },
    a: {
        pressed: false
    },
    s: {
        pressed: false
    },
    d: {
        pressed: false
    },
}

let lastKey = ''
let score = 0

const map = [
  ['1', '-', '-', '-', '-', '-', '-', '-', '-', '-', '2'],
  ['|', '.', '.', '.', '.', '.', '.', '.', '.', '.', '|'],
  ['|', '.', 'b', '.', '[', '7', ']', '.', 'b', '.', '|'],
  ['|', '.', '.', '.', '.', '_', '.', '.', '.', '.', '|'],
  ['|', '.', '[', ']', '.', '.', '.', '[', ']', '.', '|'],
  ['|', '.', '.', '.', '.', '^', '.', '.', '.', '.', '|'],
  ['|', '.', 'b', '.', '[', '+', ']', '.', 'b', '.', '|'],
  ['|', '.', '.', '.', '.', '_', '.', '.', '.', '.', '|'],
  ['|', '.', '[', ']', '.', '.', '.', '[', ']', '.', '|'],
  ['|', '.', '.', '.', '.', '^', '.', '.', '.', '.', '|'],
  ['|', '.', 'b', '.', '[', '5', ']', '.', 'b', '.', '|'],
  ['|', '.', '.', '.', '.', '.', '.', '.', '.', 'p', '|'],
  ['4', '-', '-', '-', '-', '-', '-', '-', '-', '-', '3']
]

function createImage(src) {
    const image = new Image()
    image.src = src
    return image
}

map.forEach((row, i) => {
  row.forEach((symbol, j) => {
    switch (symbol) {
      case '-':
        boundaries.push(
          new Boundary({
            position: {
              x: Boundary.width * j,
              y: Boundary.height * i
            },
            image: createImage('/static/games/pac-man/img/pipeHorizontal.png')
          })
        )
        break
      case '|':
        boundaries.push(
          new Boundary({
            position: {
              x: Boundary.width * j,
              y: Boundary.height * i
            },
            image: createImage('/static/games/pac-man/img/pipeVertical.png')
          })
        )
        break
      case '1':
        boundaries.push(
          new Boundary({
            position: {
              x: Boundary.width * j,
              y: Boundary.height * i
            },
            image: createImage('/static/games/pac-man/img/pipeCorner1.png')
          })
        )
        break
      case '2':
        boundaries.push(
          new Boundary({
            position: {
              x: Boundary.width * j,
              y: Boundary.height * i
            },
            image: createImage('/static/games/pac-man/img/pipeCorner2.png')
          })
        )
        break
      case '3':
        boundaries.push(
          new Boundary({
            position: {
              x: Boundary.width * j,
              y: Boundary.height * i
            },
            image: createImage('/static/games/pac-man/img/pipeCorner3.png')
          })
        )
        break
      case '4':
        boundaries.push(
          new Boundary({
            position: {
              x: Boundary.width * j,
              y: Boundary.height * i
            },
            image: createImage('/static/games/pac-man/img/pipeCorner4.png')
          })
        )
        break
      case 'b':
        boundaries.push(
          new Boundary({
            position: {
              x: Boundary.width * j,
              y: Boundary.height * i
            },
            image: createImage('/static/games/pac-man/img/block.png')
          })
        )
        break
      case '[':
        boundaries.push(
          new Boundary({
            position: {
              x: j * Boundary.width,
              y: i * Boundary.height
            },
            image: createImage('/static/games/pac-man/img/capLeft.png')
          })
        )
        break
      case ']':
        boundaries.push(
          new Boundary({
            position: {
              x: j * Boundary.width,
              y: i * Boundary.height
            },
            image: createImage('/static/games/pac-man/img/capRight.png')
          })
        )
        break
      case '_':
        boundaries.push(
          new Boundary({
            position: {
              x: j * Boundary.width,
              y: i * Boundary.height
            },
            image: createImage('/static/games/pac-man/img/capBottom.png')
          })
        )
        break
      case '^':
        boundaries.push(
          new Boundary({
            position: {
              x: j * Boundary.width,
              y: i * Boundary.height
            },
            image: createImage('/static/games/pac-man/img/capTop.png')
          })
        )
        break
      case '+':
        boundaries.push(
          new Boundary({
            position: {
              x: j * Boundary.width,
              y: i * Boundary.height
            },
            image: createImage('/static/games/pac-man/img/pipeCross.png')
          })
        )
        break
      case '5':
        boundaries.push(
          new Boundary({
            position: {
              x: j * Boundary.width,
              y: i * Boundary.height
            },
            color: 'blue',
            image: createImage('/static/games/pac-man/img/pipeConnectorTop.png')
          })
        )
        break
      case '6':
        boundaries.push(
          new Boundary({
            position: {
              x: j * Boundary.width,
              y: i * Boundary.height
            },
            color: 'blue',
            image: createImage('/static/games/pac-man/img/pipeConnectorRight.png')
          })
        )
        break
      case '7':
        boundaries.push(
          new Boundary({
            position: {
              x: j * Boundary.width,
              y: i * Boundary.height
            },
            color: 'blue',
            image: createImage('/static/games/pac-man/img/pipeConnectorBottom.png')
          })
        )
        break
      case '8':
        boundaries.push(
          new Boundary({
            position: {
              x: j * Boundary.width,
              y: i * Boundary.height
            },
            image: createImage('/static/games/pac-man/img/pipeConnectorLeft.png')
          })
        )
        break
      case '.':
        pellets.push(
          new Pellet({
            position: {
              x: j * Boundary.width + Boundary.width / 2,
              y: i * Boundary.height + Boundary.height / 2
            }
          })
        )
        break
      case 'p':
        powerUps.push(
          new PowerUp({
            position: {
              x: j * Boundary.width + Boundary.width / 2,
              y: i * Boundary.height + Boundary.height / 2
            }
          })
        )
        break
    }
  })
})

function circleCollidesWithRectangle({ circle, rectangle }) {
    const padding = Boundary.width / 2 - circle.radius - 1
    return (circle.position.y - circle.radius + circle.velocity.y <= rectangle.position.y + rectangle.height + padding &&
            circle.position.x + circle.radius + circle.velocity.x >= rectangle.position.x - padding &&
            circle.position.y + circle.radius + circle.velocity.y >= rectangle.position.y - padding &&
            circle.position.x - circle.radius + circle.velocity.x <= rectangle.position.x + rectangle.width + padding
        )
}

let animationId
function animate() {
    animationId = requestAnimationFrame(animate)
    c.clearRect(0, 0, canvas.width, canvas.height)



    // power ups
    for (let i = powerUps.length - 1; 0 <= i; i--) {
        const powerUp = powerUps[i]
        powerUp.draw()

        // player gets power up
        if (Math.hypot(powerUp.position.x - player.position.x, powerUp.position.y - player.position.y) <
            powerUp.radius + player.radius
        ) {
          powerUps.splice(i, 1)

          // make ghosts scared
          ghosts.forEach(ghost => {
            ghost.scared = true

            setTimeout(() => {
              ghost.scared = false
            }, 5000)
          })
        }
    }

    // touch pellets here
    for (let i = pellets.length - 1; 0 <= i; i--) {
        const pellet = pellets[i]
        pellet.draw()

        if (Math.hypot(pellet.position.x - player.position.x, pellet.position.y - player.position.y) <
            pellet.radius + player.radius
        ) {
            pellets.splice(i, 1)
            score += 10
            scoreEl.innerHTML = score
        }
    }


    boundaries.forEach((boundary) => {
        boundary.draw()

        if (
            circleCollidesWithRectangle({
                circle: player,
                rectangle: boundary
            })
        ) {
            console.log('dadawd')
            player.velocity.y = 0
            player.velocity.x = 0
        }
    })

    if (keys.w.pressed && lastKey === 'w') {
        let collision = false
        for (let i = 0; i < boundaries.length; i++) {
            const boundary = boundaries[i]
            if (circleCollidesWithRectangle({
                circle: { ...player, velocity: { x: 0, y: -5 } },
                rectangle: boundary
            })) {
                collision = true
                break
            }
        }
        if (!collision) {
            player.velocity.y = -5
            player.velocity.x = 0
        } else {
            player.velocity.y = 0
        }
    }

    else if (keys.a.pressed && lastKey === 'a') {
        let collision = false
        for (let i = 0; i < boundaries.length; i++) {
            const boundary = boundaries[i]
            if (circleCollidesWithRectangle({
                circle: { ...player, velocity: { x: -5, y: 0 } },
                rectangle: boundary
            })) {
                collision = true
                break
            }
        }
        if (!collision) {
            player.velocity.x = -5
            player.velocity.y = 0
        } else {
            player.velocity.x = 0
        }
    }

    else if (keys.s.pressed && lastKey === 's') {
        let collision = false
        for (let i = 0; i < boundaries.length; i++) {
            const boundary = boundaries[i]
            if (circleCollidesWithRectangle({
                circle: { ...player, velocity: { x: 0, y: 5 } },
                rectangle: boundary
            })) {
                collision = true
                break
            }
        }
        if (!collision) {
            player.velocity.y = 5
            player.velocity.x = 0
        } else {
            player.velocity.y = 0
        }
    }

    else if (keys.d.pressed && lastKey === 'd') {
        let collision = false
        for (let i = 0; i < boundaries.length; i++) {
            const boundary = boundaries[i]
            if (circleCollidesWithRectangle({
                circle: { ...player, velocity: { x: 5, y: 0 } },
                rectangle: boundary
            })) {
                collision = true
                break
            }
        }
        if (!collision) {
            player.velocity.x = 5
            player.velocity.y = 0
        } else {
            player.velocity.x = 0
        }
    }

    player.update()

    ghosts.forEach(ghost => {
        ghost.update()

      // detect collision between ghosts and player
      for (let i = ghosts.length - 1; 0 <= i; i--) {
        const ghost = ghosts[i]
        // ghost touches player
        if (Math.hypot(ghost.position.x - player.position.x, ghost.position.y - player.position.y) <
            ghost.radius + player.radius
        ) {

          if (ghost.scared) {
            ghosts.splice(i, 1)
          } else {
              cancelAnimationFrame(animationId)
              console.log('You lose')
              showEndScreen('You Lose')
              fetch('/games/save-score/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    body: JSON.stringify({
                        game: 'Pac-Man',
                        score: score
                    })
                });
          }
        }
      }


        const collisions = []
        boundaries.forEach(boundary => {
            if (
                !collisions.includes('right') &&
                circleCollidesWithRectangle({
                circle: {...ghost, velocity: {
                    x: ghost.speed,
                    y: 0
                }},
                rectangle: boundary
                })
            ) {
                collisions.push('right')
            }
            if (
                !collisions.includes('left') &&
                circleCollidesWithRectangle({
                circle: {...ghost, velocity: {
                    x: -ghost.speed,
                    y: 0
                }},
                rectangle: boundary
                })
            ) {
                collisions.push('left')
            }
            if (
                !collisions.includes('up') &&
                circleCollidesWithRectangle({
                circle: {...ghost, velocity: {
                    x: 0,
                    y: -ghost.speed
                }},
                rectangle: boundary
                })
            ) {
                collisions.push('up')
            }
            if (
                !collisions.includes('down') &&
                circleCollidesWithRectangle({
                circle: {...ghost, velocity: {
                    x: 0,
                    y: ghost.speed
                }},
                rectangle: boundary
                })
            ) {
                collisions.push('down')
            }
        })

        if (collisions.length > ghost.prevCollisions.length)
            ghost.prevCollisions = collisions

        if (JSON.stringify(collisions) !== JSON.stringify(ghost.prevCollisions)) {
            // console.log('gogo')

            console.log(collisions)
            console.log(ghost.prevCollisions)
            if (ghost.velocity.x > 0) ghost.prevCollisions.push('right')
            else if (ghost.velocity.x < 0) ghost.prevCollisions.push('left')
            else if (ghost.velocity.y < 0) ghost.prevCollisions.push('up')
            else if (ghost.velocity.y > 0) ghost.prevCollisions.push('down')

            const pathways = ghost.prevCollisions.filter(collision => {
              return !collisions.includes(collision)
            })
             console.log({ pathways })

             const direction = pathways[Math.floor(Math.random() * pathways.length)]

             switch (direction) {
              case 'down':
                ghost.velocity.y = ghost.speed
                ghost.velocity.x = 0
                break

                case 'up':
                ghost.velocity.y = -ghost.speed
                ghost.velocity.x = 0
                break

                case 'right':
                ghost.velocity.y = 0
                ghost.velocity.x = ghost.speed
                break

                case 'left':
                ghost.velocity.y = 0
                ghost.velocity.x = -ghost.speed
                break
             }

            ghost.prevCollisions = []
        }

    })
    if (player.velocity.x > 0)
      player.rotation = 0
    else if (player.velocity.x < 0)
      player.rotation = Math.PI
    else if (player.velocity.y > 0)
      player.rotation = Math.PI / 2
    else if (player.velocity.y < 0)
      player.rotation = Math.PI * 1.5

    // win condition
    if (pellets.length === 0) {
        cancelAnimationFrame(animationId)
        console.log('You win')
        showEndScreen('You Win')
        fetch('/games/save-score/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                game: 'Pac-Man',
                score: score
            })
        });
    }
}

animate()

addEventListener('keydown', ({ key }) => {
    switch (key) {
        case 'w':
            keys.w.pressed = true
            lastKey = 'w'
            break
        case 'a':
            keys.a.pressed = true
            lastKey = 'a'
            break
        case 's':
            keys.s.pressed = true
            lastKey = 's'
            break
        case 'd':
            keys.d.pressed = true
            lastKey = 'd'
            break
    }

    console.log(player.velocity)
})

addEventListener('keyup', ({ key }) => {
    switch (key) {
        case 'w':
            keys.w.pressed = false
            break
        case 'a':
            keys.a.pressed = false
            break
        case 's':
            keys.s.pressed = false
            break
        case 'd':
            keys.d.pressed = false
            break
    }

    console.log(player.velocity)
})
