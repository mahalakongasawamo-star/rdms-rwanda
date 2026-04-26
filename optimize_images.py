"""
Compress images in assets/img/ losslessly (PNG) or visually-losslessly (JPEG q=85).
Skips files smaller than 30 KB. Reports before/after sizes.
"""
from pathlib import Path
from PIL import Image

IMG_DIR = Path(__file__).parent / "assets" / "img"
SKIP_BELOW = 30 * 1024  # 30 KB
JPEG_QUALITY = 85

total_before = 0
total_after = 0
skipped = 0
optimized = 0

for path in sorted(IMG_DIR.glob("*")):
    if not path.is_file():
        continue
    if path.suffix.lower() not in {".png", ".jpg", ".jpeg"}:
        continue

    before = path.stat().st_size
    if before < SKIP_BELOW:
        skipped += 1
        continue

    try:
        img = Image.open(path)
        img.load()  # decode upfront (some formats are lazy)
        ext = path.suffix.lower()

        # Save to a temp file first so we can compare sizes and skip if it grew
        tmp_path = path.with_suffix(path.suffix + ".tmp")
        if ext == ".png":
            img.save(tmp_path, "PNG", optimize=True)
        else:  # .jpg / .jpeg
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            img.save(tmp_path, "JPEG", quality=JPEG_QUALITY, optimize=True, progressive=True)

        new_size = tmp_path.stat().st_size
        if new_size >= before:
            # Re-encoding made it larger (original already well-compressed) — keep original
            tmp_path.unlink()
            print(f"  {path.name:40s} {before/1024:7.1f}K  (kept — would grow)")
            skipped += 1
            continue

        tmp_path.replace(path)
        after = path.stat().st_size
        total_before += before
        total_after += after
        optimized += 1
        delta = before - after
        pct = (delta / before * 100) if before else 0
        sign = "-" if delta > 0 else "+"
        print(f"  {path.name:40s} {before/1024:7.1f}K -> {after/1024:7.1f}K  ({sign}{abs(pct):.1f}%)")
    except Exception as e:
        print(f"  SKIP {path.name}: {e}")

print()
print(f"Optimized: {optimized} files | Skipped (<30KB): {skipped}")
if total_before:
    saved = (total_before - total_after) / 1024
    pct = (total_before - total_after) / total_before * 100
    print(f"Total: {total_before/1024:.0f}K -> {total_after/1024:.0f}K  (saved {saved:.0f}K / {pct:.1f}%)")
