import os
import json
from PIL import Image

root = "."

# 输出 JSON 文件路径
output_json = "images.json"

# 支持的图片格式
image_exts = [".png", ".jpg", ".jpeg", ".bmp", ".gif", ".tiff", ".webp"]

result = {}

for folder, subfolders, files in os.walk(root):
    for filename in files:
        ext = os.path.splitext(filename)[1].lower()

        if ext in image_exts:
            img_path = os.path.join(folder, filename)

            # 相对路径（用于 Hexo）
            rel_path = os.path.relpath(img_path, root).replace("\\", "/")

            try:
                img = Image.open(img_path)
                width, height = img.size

                result[rel_path] = {
                    "width": width,
                    "height": height
                }

                print(f"读取成功: {rel_path} → {width}x{height}")

            except Exception as e:
                print(f"读取失败: {img_path}, 错误: {e}")

# 写入 JSON 文件
with open(output_json, "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)

print(f"\n已生成尺寸 JSON: {output_json}")
