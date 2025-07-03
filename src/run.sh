#yland 显示环境变量
export XDG_RUNTIME_DIR=/dev/socket/weston
export WAYLAND_DISPLAY=wayland-1

# 运行 test_w2.py
echo "启动麻将AI助手..."
echo "环境变量已设置："
echo "XDG_RUNTIME_DIR=$XDG_RUNTIME_DIR"
echo "WAYLAND_DISPLAY=$WAYLAND_DISPLAY"
echo ""
echo "注意：此程序不需要 ML 参数（如 -f, -ml, --model 等），"
echo "因为它是简单的摄像头显示和图像分析应用。"
echo ""


python3 socket_server_majiang.py
