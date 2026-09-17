#!/usr/bin/env python3
"""直接通过 SQLite 创建 24 条延迟任务，无需登录 hub。

用法: python3 setup_tasks_sql.py <monitor.db> [node_ids]
示例: python3 setup_tasks_sql.py /opt/monitor/data/monitor.db 1,2,3
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

def main():
    if len(sys.argv) < 2:
        print("用法: python3 setup_tasks_sql.py <monitor.db> [node_ids]")
        sys.exit(1)

    db_path = sys.argv[1]
    node_ids = [int(n) for n in sys.argv[2].split(",")] if len(sys.argv) > 2 else [1, 2, 3]

    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA journal_mode=WAL")

    # 获取 ping_node 表中每个 task_id 对应的 node_id
    # 如果 ping_node 表中没有记录，则使用用户提供的 node_ids
    existing = conn.execute("SELECT task_id, node_id FROM ping_node").fetchall()
    task_nodes = {}
    for task_id, node_id in existing:
        if task_id not in task_nodes:
            task_nodes[task_id] = []
        task_nodes[task_id].append(node_id)

    created = 0
    skipped = 0
    for region, province, prefix in PROVINCES:
        for isp_name, isp_suffix in ISPS:
            name = f"{region}-{province}-{isp_suffix}"
            target = f"{prefix}-{isp_suffix}-v4.ip.zstaticcdn.com:80"

            # 检查是否已存在
            existing_task = conn.execute(
                "SELECT id FROM ping_task WHERE name = ?", (name,)
            ).fetchone()

            if existing_task:
                skipped += 1
                continue

            # 插入任务
            conn.execute(
                "INSERT INTO ping_task (name, target, interval) VALUES (?, ?, 60)",
                (name, target)
            )
            task_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]

            # 插入 ping_node 关联
            for node_id in node_ids:
                conn.execute(
                    "INSERT INTO ping_node (task_id, node_id) VALUES (?, ?)",
                    (task_id, node_id)
                )

            created += 1
            print(f"  ✓ {name} → {target} (nodes={node_ids})")

    conn.commit()
    conn.close()

    print(f"\n完成: 新建 {created} 条, 跳过 {skipped} 条已存在")

if __name__ == "__main__":
    main()
