from PIL import Image, ImageSequence
import os

root = "."

image_exts = [".png", ".jpg", ".jpeg", ".bmp", ".gif", ".tiff"]

for folder, subfolders, files in os.walk(root):
    for filename in files:
        ext = os.path.splitext(filename)[1].lower()

        if ext in image_exts:
            img_path = os.path.join(folder, filename)
            webp_path = os.path.join(folder, os.path.splitext(filename)[0] + ".webp")

            try:
                # 使用 with 自动关闭文件句柄
                with Image.open(img_path) as img:

                    if ext == ".gif" and getattr(img, "is_animated", False):
                        frames = []
                        durations = []

                        for frame in ImageSequence.Iterator(img):
                            frames.append(frame.convert("RGBA"))
                            durations.append(frame.info.get("duration", 100))

                        frames[0].save(
                            webp_path,
                            format="WEBP",
                            save_all=True,
                            append_images=frames[1:],
                            duration=durations,
                            loop=0,
                            quality=85,
                        )

                    else:
                        img.convert("RGBA").save(webp_path, "webp", quality=85)

                print(f"转换成功: {img_path} → {webp_path}")

                # 现在文件句柄已经关闭，可以安全删除
                os.remove(img_path)
                print(f"已删除原图: {img_path}")

            except Exception as e:
                print(f"转换失败: {img_path}, 错误: {e}")
