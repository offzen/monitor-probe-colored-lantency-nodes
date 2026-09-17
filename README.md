# monitor-probe-colored-lantency-nodes

[monitor-probe](https://github.com/monitor-probe/monitor) 彩色延迟节点部署包，含 24 条省级三网 TCP 延迟探测任务。

## 包含内容

| 文件 | 用途 |
|---|---|
| `monitor-theme-multicolor/` | 彩色延迟主题 (5 色实线 + 9 档时间范围) |
| `setup_tasks.py` | 创建 24 条延迟探测任务 (8 省 × 3 运营商) |
| `setup_theme.sh` | 导入主题 + 设置 retention_days |

## 快速部署

```bash
# 1. 克隆仓库
git clone https://github.com/offzen/monitor-probe-colored-lantency-nodes.git
cd monitor-probe-colored-lantency-nodes

# 2. 登录 hub 获取 cookie
curl -c /tmp/cookie.txt -X POST http://<hub>:28080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"<password>"}'

# 3. 导入主题 + 设置保留期
./setup_theme.sh http://<hub>:28080 /tmp/cookie.txt

# 4. 创建延迟任务
python3 setup_tasks.py --hub http://<hub>:28080 --cookie /tmp/cookie.txt --nodes 1,2,3
```

## 24 条延迟探测任务

8 省 × 3 运营商 = 24 目标，每条 60 秒间隔：

| 区域 | 省份 | 区域代码 | 运营商 |
|---|---|---|---|
| 华北 | 北京 | hb | ct/cm/cu |
| 华东 | 上海 | hd | ct/cm/cu |
| 华东 | 江苏 | hd | ct/cm/cu |
| 东北 | 辽宁 | ln | ct/cm/cu |
| 华南 | 广东省 | hn | ct/cm/cu |
| 华南 | 广西 | hn | ct/cm/cu |
| 西北 | 新疆 | xb | ct/cm/cu |
| 西北 | 陕西 | xb | ct/cm/cu |

目标格式: `<区域>-<运营商>-v4.ip.zstaticcdn.com:80`

## 主题配色

| 系列 | 颜色 | oklch (亮色) |
|---|---|---|
| 1 | 绿 | oklch(62% 0.25 145) |
| 2 | 蓝 | oklch(55% 0.22 250) |
| 3 | 黄 | oklch(72% 0.18 85) |
| 4 | 橙 | oklch(68% 0.22 55) |
| 5 | 红 | oklch(60% 0.25 25) |

时间范围: 1h / 6h / 1d / 7d / 15d / 30d / 45d / 60d / 90d

## 依赖

- Python 3.10+
- monitor-probe hub v1.1.0+

## License

MIT
