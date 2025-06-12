const canvas = document.getElementById('game');
const ctx = canvas.getContext('2d');

canvas.width = 800;
canvas.height = 800;

// Изображения (замените на свои пути)
const birdImg = new Image();
birdImg.src = '/static/img/b0.png';

const pipeTopImg = new Image();
pipeTopImg.src = './static/img/toppipe.png';

const pipeBottomImg = new Image();
pipeBottomImg.src = './static/img/botpipe.png';

const bgImg = new Image();
bgImg.src = '/static/img/BG.png';

// Игровые переменные
let bird = {
    x: 50,
    y: canvas.height / 2,
    width: 40,
    height: 30,
    velocity: 0,
    gravity: 0.5,
    jump: -10
};

let pipes = [];
let score = 0;
let gameOver = false;
let frameCount = 0;

// Управление
document.addEventListener('keydown', (e) => {
    if (e.code === 'Space') {
        bird.velocity = bird.jump;
    }
});

canvas.addEventListener('click', () => {
    bird.velocity = bird.jump;
});

// Генерация труб
function generatePipes() {
    if (frameCount % 100 === 0) {
        const gap = 150;
        const pipeHeight = Math.floor(Math.random() * (canvas.height - gap - 150)) + 50;
        pipes.push({
            x: canvas.width,
            y: 0,
            width: 50,
            height: pipeHeight,
            passed: false
        });
        pipes.push({
            x: canvas.width,
            y: pipeHeight + gap,
            width: 50,
            height: canvas.height - pipeHeight - gap,
            passed: false
        });
    }
}

// Обновление игры
function update() {
    bird.velocity += bird.gravity / 1.5;
    bird.y += bird.velocity / 1.5;

    // Проверка столкновений
    if (bird.y + bird.height > canvas.height || bird.y < 0) {
        gameOver = true;
    }

    generatePipes();

    pipes.forEach((pipe, index) => {
        pipe.x -= 2;

        // Столкновение с трубой
        if (
            bird.x < pipe.x + pipe.width / 2 &&
            bird.x + bird.width / 2 > pipe.x &&
            bird.y < pipe.y + pipe.height / 2 &&
            bird.y + bird.height / 2 > pipe.y
        ) {
            gameOver = true;
        }

        // Подсчет очков
        if (pipe.x + pipe.width < bird.x && !pipe.passed && pipe.y > 0) {
            pipe.passed = true;
            score++;
        }

        // Удаление труб за пределами экрана
        if (pipe.x + pipe.width < 0) {
            pipes.splice(index, 1);
        }
    });
}

// Отрисовка игры
function draw() {
    ctx.drawImage(bgImg, 0, 0, canvas.width, canvas.height);

    // Птица
    ctx.drawImage(birdImg, bird.x, bird.y, bird.width, bird.height);

    // Трубы
    pipes.forEach(pipe => {
        if (pipe.y === 0) {
            ctx.drawImage(pipeTopImg, pipe.x, pipe.y, pipe.width, pipe.height);
        } else {
            ctx.drawImage(pipeBottomImg, pipe.x, pipe.y, pipe.width, pipe.height);
        }
    });

    // Очки
    ctx.fillStyle = '#000';
    ctx.font = '30px Arial';
    ctx.fillText(score, canvas.width / 2, 50);

    // Конец игры
    if (gameOver) {
        ctx.fillStyle = 'rgba(0, 0, 0, 0.5)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = '#fff';
        ctx.font = '40px Arial';
        ctx.fillText('Game Over!', canvas.width / 2 - 100, canvas.height / 2);
        ctx.font = '20px Arial';
        ctx.fillText('Click to restart', canvas.width / 2 - 70, canvas.height / 2 + 40);
    }
}

// Игровой цикл
function loop() {
    if (!gameOver) {
        update();
    }
    draw();
    frameCount++;
    requestAnimationFrame(loop);
}

// Рестарт игры
function restart() {
    bird.y = canvas.height / 2;
    bird.velocity = 0;
    pipes = [];
    score = 0;
    gameOver = false;
    frameCount = 0;
}

canvas.addEventListener('click', () => {
    if (gameOver) {
        restart();
    }
});

// Запуск игры
loop();