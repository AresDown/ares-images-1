import os
import json
from PIL import Image
import xml.etree.ElementTree as ET

root = "."

# 输出 JSON 文件路径
output_json = "images.json"

# 支持的图片格式
image_exts = [".png", ".jpg", ".jpeg", ".bmp", ".gif", ".tiff", ".webp", ".svg"]

result = {}

def parse_svg_size(svg_path):
    try:
        tree = ET.parse(svg_path)
        root = tree.getroot()

        width = root.get("width")
        height = root.get("height")
        viewBox = root.get("viewBox")

        # 如果 width/height 存在，直接返回
        if width and height:
            # 去掉单位（如 "100px"）
            width = float(width.replace("px", ""))
            height = float(height.replace("px", ""))
            return width, height

        # 如果没有 width/height，用 viewBox 推算
        if viewBox:
            parts = viewBox.split()
            if len(parts) == 4:
                return float(parts[2]), float(parts[3])

    except Exception as e:
        print(f"SVG 解析失败: {svg_path}, 错误: {e}")

    return None, None


for folder, subfolders, files in os.walk(root):
    for filename in files:
        ext = os.path.splitext(filename)[1].lower()

        if ext in image_exts:
            img_path = os.path.join(folder, filename)
            rel_path = os.path.relpath(img_path, root).replace("\\", "/")

            try:
                if ext == ".svg":
                    width, height = parse_svg_size(img_path)
                    if width is None:
                        print(f"读取失败: {rel_path} → 无法解析 SVG 尺寸")
                        continue
                else:
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
