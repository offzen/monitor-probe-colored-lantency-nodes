#!/usr/bin/env python3
"""创建 24 条省级三网 TCP 延迟探测任务到 monitor-probe hub。

用法:
  python3 setup_tasks.py <monitor.db>           # 交互式选择节点
  python3 setup_tasks.py <monitor.db> 1,2,3     # 直接指定节点
  python3 setup_tasks.py <monitor.db> --all     # 所有节点
"""
import sqlite3, sys

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

def list_nodes(db_path):
    """列出所有可用节点"""
    conn = sqlite3.connect(db_path)
    nodes = conn.execute("SELECT id, name, hostname FROM node ORDER BY id").fetchall()
    conn.close()
    return nodes

def create_tasks(db_path, node_ids):
    """创建任务"""
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA journal_mode=WAL")

    created = 0
    skipped = 0
    for region, province, prefix in PROVINCES:
        for isp_name, isp_suffix in ISPS:
            name = f"{region}-{province}-{isp_suffix}"
            target = f"{prefix}-{isp_suffix}-v4.ip.zstaticcdn.com:80"

            existing = conn.execute("SELECT id FROM ping_task WHERE name = ?", (name,)).fetchone()
            if existing:
                skipped += 1
                continue

            conn.execute(
                "INSERT INTO ping_task (name, target, interval) VALUES (?, ?, 60)",
                (name, target)
            )
            task_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]

            for node_id in node_ids:
                conn.execute(
                    "INSERT INTO ping_node (task_id, node_id) VALUES (?, ?)",
                    (task_id, node_id)
                )
            created += 1
            print(f"  ✓ {name} → {target}")

    conn.commit()
    conn.close()
    print(f"\n完成: 新建 {created} 条, 跳过 {skipped} 条已存在")

def main():
    if len(sys.argv) < 2:
        print("用法: python3 setup_tasks.py <monitor.db> [节点ID]")
        print("示例: python3 setup_tasks.py /opt/monitor/data/monitor.db 1,2,3")
        print("      python3 setup_tasks.py /opt/monitor/data/monitor.db --all")
        sys.exit(1)

    db_path = sys.argv[1]
    nodes = list_nodes(db_path)

    if not nodes:
        print("错误: 没有可用节点")
        sys.exit(1)

    print("可用节点:")
    for nid, name, hostname in nodes:
        print(f"  {nid}. {name} ({hostname})")
    print()

    # 解析节点参数
    if len(sys.argv) >= 3:
        arg = sys.argv[2]
        if arg == "--all":
            node_ids = [n[0] for n in nodes]
        else:
            node_ids = [int(n) for n in arg.split(",")]
    else:
        # 交互式选择
        try:
            raw = input("选择节点 (逗号分隔, 或输入 all 选择全部): ").strip()
            if raw.lower() == "all":
                node_ids = [n[0] for n in nodes]
            else:
                node_ids = [int(n) for n in raw.split(",")]
        except (EOFError, KeyboardInterrupt):
            print("\n已取消")
            sys.exit(0)

    print(f"\n已选节点: {node_ids}")
    create_tasks(db_path, node_ids)

if __name__ == "__main__":
    main()
