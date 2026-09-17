#!/usr/bin/env python3
"""创建 24 条省级三网 TCP 延迟探测任务到 monitor-probe hub。

用法: python3 setup_tasks.py --hub http://127.0.0.1:28081 --cookie /tmp/cookie.txt
"""
import json, urllib.request, urllib.error, sys, argparse

PROVINCES = [
    ("hb", "北京", "bj"),
    ("hd", "上海", "sh"),
    ("hd", "江苏", "js"),
    ("hd", "辽宁", "ln"),
    ("hn", "广东", "gd"),
    ("hn", "广西", "gx"),
    ("xb", "新疆", "xj"),
    ("xb", "陕西", "sn"),
]

ISPS = [("cm", "cm"), ("ct", "ct"), ("cu", "cu")]

def create_task(hub, cookie, name, target, nodes, interval=60):
    body = json.dumps({
        "name": name,
        "target": target,
        "interval": interval,
        "nodes": nodes,
    }).encode()
    req = urllib.request.Request(
        hub + "/api/ping-tasks",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    req.add_header("Cookie", "monitor_session=" + cookie)
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read().decode())

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--hub", default="http://127.0.0.1:28081")
    parser.add_argument("--cookie", required=True, help="cookie 文件路径")
    parser.add_argument("--nodes", default="1,2,3", help="节点 ID 列表 (逗号分隔)")
    parser.add_argument("--interval", type=int, default=60, help="探测间隔 (秒)")
    parser.add_argument("--dry-run", action="store_true", help="仅打印不执行")
    args = parser.parse_args()

    with open(args.cookie) as f:
        cookie = f.read().strip()

    nodes = [int(n) for n in args.nodes.split(",")]
    tasks = []

    for region, province, prefix in PROVINCES:
        for isp_name, isp_suffix in ISPS:
            name = f"{region}-{province}-{isp_suffix}"
            target = f"{prefix}-{isp_suffix}-v4.ip.zstaticcdn.com:80"
            tasks.append((name, target))

    print(f"将创建 {len(tasks)} 条任务 (nodes={nodes}, interval={args.interval}s)")
    if args.dry_run:
        for name, target in tasks:
            print(f"  {name:20s}  {target}")
        return

    created = 0
    for name, target in tasks:
        try:
            result = create_task(args.hub, cookie, name, target, nodes, args.interval)
            created += 1
            print(f"  ✓ {name} → {target}")
        except urllib.error.HTTPError as e:
            body = e.read().decode()
            if "duplicate" in body.lower() or "unique" in body.lower():
                print(f"  ○ {name} 已存在, 跳过")
            else:
                print(f"  ✗ {name} 失败: HTTP {e.code} {body[:100]}")

    print(f"\n完成: 新建 {created} 条, 共 {len(tasks)} 条")

if __name__ == "__main__":
    main()
