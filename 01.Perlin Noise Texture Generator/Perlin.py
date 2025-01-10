import numpy as np
from noise import pnoise2
from PIL import Image, ImageTk
import tkinter as tk

def generate_perlin_noise(width, height, scale=10, octaves=6, persistence=0.5, lacunarity=2.0, seed=42 ):
    noise = np.zeros((height, width))
    for y in range(height):
        for x in range(width):
            value = pnoise2(
                x / scale,
                y / scale,
                octaves=octaves,
                persistence=persistence,
                lacunarity=lacunarity,
                repeatx=width,
                repeaty=height,
                base=seed
            )
            noise[y][x] = value

    noise = (noise - noise.min()) / (noise.max() - noise.min()) * 255
    return noise.astype(np.uint8)

def save_texture(noise_array, filename):
    img = Image.fromarray(noise_array, mode='L')
    img.save(filename)

def update_texture():
    try:
        scale = float(scale_var.get())
        octaves = int(octaves_var.get())
        persistence = float(persistence_var.get())
        lacunarity = float(lacunarity_var.get())
        seed = int(seed_var.get())

        noise = generate_perlin_noise(256, 256, scale, octaves, persistence, lacunarity,seed)
        img = Image.fromarray(noise, mode='L').resize((256, 256))
        tk_img = ImageTk.PhotoImage(img)

        texture_label.config(image=tk_img)
        texture_label.image = tk_img
    except ValueError:
        texture_label.image = None
        print("Error: Please ensure all input values are valid.")

def save_current_texture():
    try:
        # Get user input values
        scale = float(scale_var.get())
        octaves = int(octaves_var.get())
        persistence = float(persistence_var.get())
        lacunarity = float(lacunarity_var.get())
        width = int(size_x_var.get())
        height = int(size_y_var.get())
        seed = int(seed_var.get())

        # Generate and save the texture
        noise = generate_perlin_noise(width, height, scale, octaves, persistence, lacunarity, seed)
        save_texture(noise, "perlin_texture.png")
        print("Texture saved as perlin_texture.png")
    except ValueError:
        print("Error: Please ensure all input values are valid.")

if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(width=False, height=False)
    root.title("Perlin Noise Generator")

    # Input fields
    root.resizable(width=False, height=False)
    frame_size = tk.Frame(root)
    frame_size.grid(row=0, column=0, sticky="W", padx=9 )

    tk.Label(frame_size, text="Texture size:").grid(row=0, column=0, sticky="W")
    tk.Label(frame_size, text="", width=0).grid(row=0, column=1, sticky="W")
    tk.Label(frame_size, text="X:").grid(row=0, column=2, sticky="W")
    size_x_var = tk.StringVar(value="256")
    tk.Entry(frame_size, textvariable=size_x_var, width=11).grid(row=0, column=3, sticky="E", padx=5)
    tk.Label(frame_size, text="Y:").grid(row=0, column=4, sticky="W")
    size_y_var = tk.StringVar(value="256")
    tk.Entry(frame_size, textvariable=size_y_var, width=11).grid(row=0, column=5, sticky="E")

    botoom_size = tk.Frame(root)
    botoom_size.grid(row=1, column=0, sticky="W", padx=10)

    tk.Label(botoom_size, text="Scale:").grid(row=1, column=0, sticky="W")
    scale_var = tk.StringVar(value="100")
    tk.Entry(botoom_size, textvariable=scale_var, width=30).grid(row=1, column=1, sticky="E")

    tk.Label(botoom_size, text="Octaves:").grid(row=2, column=0, sticky="W")
    octaves_var = tk.StringVar(value="6")
    tk.Entry(botoom_size, textvariable=octaves_var, width=30).grid(row=2, column=1, sticky="E")

    tk.Label(botoom_size, text="Persistence:").grid(row=3, column=0, sticky="W")
    persistence_var = tk.StringVar(value="0.5")
    tk.Entry(botoom_size, textvariable=persistence_var, width=30).grid(row=3, column=1, sticky="E")

    tk.Label(botoom_size, text="Lacunarity:").grid(row=4, column=0, sticky="W")
    lacunarity_var = tk.StringVar(value="2.0")
    tk.Entry(botoom_size, textvariable=lacunarity_var, width=30).grid(row=4, column=1, sticky="E")

    tk.Label(botoom_size, text="Seed:").grid(row=5, column=0, sticky="W")
    seed_var = tk.StringVar(value="42")
    tk.Entry(botoom_size, textvariable=seed_var, width=30).grid(row=5, column=1, sticky="E")

    # Texture preview
    texture_label = tk.Label(botoom_size)
    texture_label.grid(row=6, column=0, columnspan=2)

    # Buttons
    tk.Button(botoom_size, text="Update", command=update_texture).grid(row=7, column=0)
    tk.Button(botoom_size, text="Save", command=save_current_texture).grid(row=7, column=1)

    update_texture()

    root.mainloop()
