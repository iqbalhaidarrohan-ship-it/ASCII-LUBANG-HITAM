from io import BytesIO

import pygame
from flask import Flask, Response

from lubanghitam import (
    H,
    LOOP,
    MONO,
    W,
    Canvas,
    draw_screen,
    glyphs,
)

app = Flask(__name__)

PAGE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Black Hole - JIN2</title>
  <style>
    html, body { height: 100%; margin: 0; background: #050408; }
    body { display: grid; place-items: center; }
    img { display: block; width: min(100vw, 112.5vh); height: auto; }
  </style>
</head>
<body>
  <img src="/stream" alt="Animated ASCII black hole">
</body>
</html>"""


@app.get("/")
def index():
    return PAGE


def frames():
    pygame.font.init()
    screen = pygame.Surface((W, H))
    small = pygame.font.SysFont(MONO, 17)
    canvas = Canvas(glyphs())
    clock = pygame.time.Clock()
    t = 0.0
    art, info, count = canvas.draw(t)

    while True:
        t += min(clock.tick(30) / 1000, 1 / 15)
        if t > LOOP:
            t = 0.0
            canvas.reset()
        art, info, count = canvas.draw(t)
        draw_screen(screen, art, info, count, t, small)

        image = BytesIO()
        pygame.image.save(screen, image, "frame.jpg")
        yield b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + image.getvalue() + b"\r\n"


@app.get("/stream")
def stream():
    return Response(
        frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame",
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, threaded=True)
