from pathlib import Path

from PIL import Image, ImageEnhance, ImageOps


SOURCE = Path("assets/profile.png")
OUTPUT = Path("data/profile-prepped.png")


def main():
    if not SOURCE.exists():
        raise FileNotFoundError(
            f"Could not find {SOURCE}. "
            "Make sure your photo exists at assets/profile.png"
        )

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    image = Image.open(SOURCE).convert("L")

    image = ImageOps.fit(
        image,
        (160, 160),
        method=Image.Resampling.LANCZOS,
        centering=(0.5, 0.42),
    )

    image = ImageOps.autocontrast(image)

    contrast = ImageEnhance.Contrast(image)
    image = contrast.enhance(1.55)

    image.save(OUTPUT)

    print(f"Prepared portrait saved to {OUTPUT}")


if __name__ == "__main__":
    main()
