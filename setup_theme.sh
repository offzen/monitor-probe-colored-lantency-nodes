#!/bin/bash
# 导入 multicolor 主题到 monitor-probe hub
# 用法: ./setup_theme.sh [hub_url] [cookie_file]
# 示例: ./setup_theme.sh http://127.0.0.1:28081 /tmp/cookie.txt

HUB="${1:-http://127.0.0.1:28081}"
COOKIE="${2:-/tmp/cookie.txt}"
THEME_TAR="monitor-theme-multicolor.tar.gz"

if [ ! -f "$THEME_TAR" ]; then
    echo "错误: 找不到 $THEME_TAR"
    exit 1
fi

if [ ! -f "$COOKIE" ]; then
    echo "错误: 找不到 cookie 文件 $COOKIE"
    echo "请先登录: curl -c $COOKIE -X POST $HUB/api/auth/login -H 'Content-Type: application/json' -d '{\"username\":\"admin\",\"password\":\"<password>\"}'"
    exit 1
fi

echo "=== 上传主题 ==="
curl -s -b "$COOKIE" -X POST \
  "$HUB/api/themes?offset=0&total=$(stat -c%s $THEME_TAR)" \
  -H "Content-Type: application/gzip" \
  --data-binary @"$THEME_TAR" | python3 -c "import sys,json; d=json.load(sys.stdin); print(json.dumps(d, ensure_ascii=False, indent=2))"

echo ""
echo "=== 选择主题 ==="
curl -s -b "$COOKIE" -X PUT "$HUB/api/settings" \
  -H "Content-Type: application/json" \
  -d '{"theme":"multicolor"}'

echo ""
echo "=== 设置 retention_days=365 ==="
curl -s -b "$COOKIE" -X PUT "$HUB/api/settings" \
  -H "Content-Type: application/json" \
  -d '{"retention_days":"365"}'

echo ""
echo "✓ 完成"
