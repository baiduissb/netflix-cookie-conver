#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cookie 自动转换工具 - 全自动版
运行即可自动检测并转换
"""

import json
import os
import glob
from pathlib import Path


def convert_file(input_file):
    """转换单个文件"""
    cookies = []
    
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except:
        try:
            with open(input_file, "r", encoding="latin-1") as f:
                lines = f.readlines()
        except:
            return None

    for line in lines:
        if line.startswith("#") or not line.strip():
            continue
        
        parts = line.strip().split("\t")
        if len(parts) < 7:
            continue
        
        name = parts[5]
        if name not in ["NetflixId", "SecureNetflixId", "nfvdid"]:
            continue
        
        cookies.append({
            "domain": parts[0],
            "name": name,
            "value": parts[6],
            "path": parts[2],
            "secure": parts[3] == "TRUE",
            "httpOnly": name in ["NetflixId", "SecureNetflixId"]
        })

    return cookies if cookies else None


def main():
    print("\n🔍 正在自动检测文件...")
    
    # 自动检测当前目录及子目录的所有可能文件
    patterns = ["*.txt", "*.cookie", "*.cookies", "*.netscape"]
    files = []
    for p in patterns:
        files.extend(glob.glob(p))
        files.extend(glob.glob(f"**/{p}", recursive=True))
    
    # 去重
    files = list(set(files))
    
    if not files:
        print("❌ 未找到任何文件！")
        print("请将此脚本放到 cookie 文件同目录后重试")
        input("\n按回车键退出...")
        return
    
    print(f"📂 检测到 {len(files)} 个文件\n")
    
    # 创建输出目录
    os.makedirs("converted", exist_ok=True)
    
    # 转换
    success = 0
    for i, f in enumerate(sorted(files), 1):
        print(f"[{i}/{len(files)}] {f}...", end=" ")
        
        cookies = convert_file(f)
        if cookies:
            output_name = f"converted/{Path(f).stem}_converted.json"
            with open(output_name, "w", encoding="utf-8") as out:
                json.dump(cookies, out, indent=2)
            print(f"✅ ({len(cookies)} cookies)")
            success += 1
        else:
            print("⏭️ 跳过（无有效cookie）")
    
    print(f"\n{'='*50}")
    print(f"✅ 完成！成功转换 {success} 个文件")
    print(f"📁 输出目录: converted/")
    print("="*50)
    input("\n按回车键退出...")


if __name__ == "__main__":
    main()
