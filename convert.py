import json

def convert_netscape_to_json(input_file, output_file):
    cookies = []
    
    with open(input_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        if line.startswith("#") or line.strip() == "":
            continue

        parts = line.strip().split("\t")
        if len(parts) < 7:
            continue

        name = parts[5]
        if name not in ["NetflixId","SecureNetflixId","nfvdid"]:
            continue

        cookie = {
            "domain": parts[0],
            "name": name,
            "value": parts[6],
            "path": parts[2],
            "secure": parts[3] == "TRUE",
            "httpOnly": name in ["NetflixId","SecureNetflixId"]
        }

        cookies.append(cookie)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(cookies, f, indent=2)

    print("转换完成!success！")

convert_netscape_to_json("Premium.txt","output.json")
