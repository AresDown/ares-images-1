from PIL import Image
import os

# 要转换的根目录
root = "."

# 支持的图片格式
image_exts = [".png", ".jpg", ".jpeg", ".bmp", ".gif", ".tiff"]

for folder, subfolders, files in os.walk(root):
    for filename in files:
        ext = os.path.splitext(filename)[1].lower()

        if ext in image_exts:
            img_path = os.path.join(folder, filename)
            webp_path = os.path.join(folder, os.path.splitext(filename)[0] + ".webp")

            try:
                img = Image.open(img_path)

                # GIF 转 WebP 只取第一帧
                if ext == ".gif":
                    img = img.convert("RGBA")
                else:
                    img = img.convert("RGBA")

                img.save(webp_path, "webp", quality=85)

                print(f"转换成功: {img_path} → {webp_path}")

                # 转换成功后删除原图
                os.remove(img_path)
                print(f"已删除原图: {img_path}")

            except Exception as e:
                print(f"转换失败: {img_path}, 错误: {e}")
