# monitor-probe-colored-lantency-nodes

[monitor-probe](https://github.com/monitor-probe/monitor) 彩色延迟节点部署包。

## 包含内容

| 路径 | 用途 |
|---|---|
| `monitor-theme-multicolor/` | 彩色延迟主题 (5 色实线 + 9 档时间范围) |
| `setup_tasks.py` | 创建 24 条延迟探测任务 (直接 SQLite，无需登录) |
| `setup_tasks_api.py` | API 版本 (需要 hub 地址，自动登录) |

## 安装主题

```bash
mkdir -p /opt/monitor/data/themes/multicolor
curl -sL https://raw.githubusercontent.com/offzen/monitor-probe-colored-lantency-nodes/main/monitor-theme-multicolor.tar.gz | tar xz -C /opt/monitor/data/themes/multicolor/
```

然后在面板中切换主题: 外观 → 主题 → multicolor

## 创建延迟任务

```bash
curl -sL https://raw.githubusercontent.com/offzen/monitor-probe-colored-lantency-nodes/main/setup_tasks.py | python3 - /opt/monitor/data/monitor.db 1,2,3
```

24 条任务：8 省 × 3 运营商，每条 60 秒间隔，目标 `<区域>-<运营商>-v4.ip.zstaticcdn.com:80`。

## 主题配色

| 系列 | 颜色 | 时间范围 |
|---|---|---|
| 1 绿 / 2 蓝 / 3 黄 / 4 橙 / 5 红 | oklch 高对比 | 1h / 6h / 1d / 7d / 15d / 30d / 45d / 60d / 90d |

## License

MIT
