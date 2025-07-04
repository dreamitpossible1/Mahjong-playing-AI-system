import socket
from uarm.wrapper import SwiftAPI
import time

# 创建 socket 对象
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 1. 先主动发一条消息给服务端，暴露自己的地址
server_address = ("192.168.1.26", 9090)  # 服务端实际IP
message = "Hello, UDP Server!"
client_socket.sendto(message.encode(), server_address)

# 2. 连接 uArm
swift = SwiftAPI(port='/dev/ttyACM0')
swift.connect()

print("等待服务端指令...")

latest_distance = None  # 新增变量

def map_value(value):
    mapping = {
        35: 1,
        34: 5,
        33: 10,
    }
    return mapping.get(int(value), None)  # 未知值返回 None

def wait_for_tile():
    while True:
        data, _ = client_socket.recvfrom(1024)
        tile = data.decode().strip()
        print(f"收到服务器推荐的牌: {tile}")
        return tile

def wait_for_distance():
    while True:
        data, _ = client_socket.recvfrom(1024)
        cmd = data.decode().strip()
        if cmd.startswith("Distance:"):
            try:
                value = cmd.split(":")[1].replace("cm", "").strip()
                latest_distance = float(value)
                print(f"收到距离: {latest_distance} cm")
                return latest_distance
            except Exception as e:
                print(f"距离解析失败: {e}")

try:
    # 等待服务器发送推荐的牌
    recommended_tile = wait_for_tile()
    print(f"准备执行机械臂动作，处理牌: {recommended_tile}")
    
    if recommended_tile == "伍万":
        # 处理伍万的机械臂动作
        swift.set_position(x=95, y=100, z=100, wait=True)
        print("到达地面:", swift.get_position())
        time.sleep(1)

        swift.set_position(x=95, y=155, z=100, wait=True)
        print("到达地面:", swift.get_position())
        time.sleep(1)

        swift.set_position(x=95, y=155, z=42, wait=True)
        print("到达地面:", swift.get_position())
        time.sleep(1)

        swift.set_pump(on=True)
        time.sleep(1)

        swift.set_position(x=95, y=155, z=100, wait=True)
        print("到达地面:", swift.get_position())
        time.sleep(1)

        swift.set_position(x=210, y=155, z=100, wait=True)
        print("到达地面:", swift.get_position())
        time.sleep(1)

        swift.set_position(x=210, y=155, z=47, wait=True)
        print("到达地面:", swift.get_position())
        time.sleep(1)

        swift.set_pump(on=False)
        time.sleep(1)

        swift.set_position(x=210, y=155, z=80, wait=True)
        print("到达地面:", swift.get_position())
        time.sleep(1)

        swift.set_position(x=180, y=155, z=80, wait=True)
        print("到达地面:", swift.get_position())
        time.sleep(1)

        swift.set_position(x=180, y=155, z=42, wait=True)
        print("到达地面:", swift.get_position())
        time.sleep(1)

        swift.set_position(x=260, y=155, z=42, wait=True)
        print("到达地面:", swift.get_position())
        time.sleep(1)

        swift.set_position(x=260, y=155, z=100, wait=True)
        print("到达地面:", swift.get_position())
        time.sleep(1)

        swift.set_position(x=260, y=0, z=100, wait=True)
        print("到达地面:", swift.get_position())
        time.sleep(1)

        # ...（此处可继续添加伍万的动作流程）...
    elif recommended_tile == "六万":
        swift.set_position(x=95, y=100, z=100, wait=True)
        print("到达地面:", swift.get_position())
        time.sleep(1)

        swift.set_position(x=95, y=190, z=100, wait=True)
        print("到达地面:", swift.get_position())
        time.sleep(1)

        swift.set_position(x=95, y=190, z=42, wait=True)
        print("到达地面:", swift.get_position())
        time.sleep(1)

        swift.set_pump(on=True)
        time.sleep(1)

        swift.set_position(x=95, y=190, z=100, wait=True)
        print("到达地面:", swift.get_position())
        time.sleep(1)

        swift.set_position(x=210, y=155, z=100, wait=True)
        print("到达地面:", swift.get_position())
        time.sleep(1)

        swift.set_position(x=210, y=155, z=47, wait=True)
        print("到达地面:", swift.get_position())
        time.sleep(1)

        swift.set_pump(on=False)
        time.sleep(1)

        swift.set_position(x=210, y=155, z=80, wait=True)
        print("到达地面:", swift.get_position())
        time.sleep(1)

        swift.set_position(x=180, y=155, z=80, wait=True)
        print("到达地面:", swift.get_position())
        time.sleep(1)

        swift.set_position(x=180, y=155, z=42, wait=True)
        print("到达地面:", swift.get_position())
        time.sleep(1)

        swift.set_position(x=260, y=155, z=42, wait=True)
        print("到达地面:", swift.get_position())
        time.sleep(1)

        swift.set_position(x=260, y=155, z=100, wait=True)
        print("到达地面:", swift.get_position())
        time.sleep(1)

        swift.set_position(x=260, y=0, z=100, wait=True)
        print("到达地面:", swift.get_position())
        time.sleep(1)
    elif recommended_tile == "七万":
        swift.set_position(x=95, y=100, z=100, wait=True)
        print("到达地面:", swift.get_position())
        time.sleep(1)

        swift.set_position(x=95, y=225, z=100, wait=True)
        print("到达地面:", swift.get_position())
        time.sleep(1)

        swift.set_position(x=95, y=225, z=42, wait=True)
        print("到达地面:", swift.get_position())
        time.sleep(1)

        swift.set_pump(on=True)
        time.sleep(1)

        swift.set_position(x=95, y=225, z=100, wait=True)
        print("到达地面:", swift.get_position())
        time.sleep(1)

        swift.set_position(x=210, y=155, z=100, wait=True)
        print("到达地面:", swift.get_position())
        time.sleep(1)

        swift.set_position(x=210, y=155, z=47, wait=True)
        print("到达地面:", swift.get_position())
        time.sleep(1)

        swift.set_pump(on=False)
        time.sleep(1)

        swift.set_position(x=210, y=155, z=80, wait=True)
        print("到达地面:", swift.get_position())
        time.sleep(1)

        swift.set_position(x=180, y=155, z=80, wait=True)
        print("到达地面:", swift.get_position())
        time.sleep(1)

        swift.set_position(x=180, y=155, z=42, wait=True)
        print("到达地面:", swift.get_position())
        time.sleep(1)

        swift.set_position(x=260, y=155, z=42, wait=True)
        print("到达地面:", swift.get_position())
        time.sleep(1)

        swift.set_position(x=260, y=155, z=100, wait=True)
        print("到达地面:", swift.get_position())
        time.sleep(1)

        swift.set_position(x=260, y=0, z=100, wait=True)
        print("到达地面:", swift.get_position())
        time.sleep(1)
    elif recommended_tile == "八万":
        swift.set_position(x=95, y=100, z=100, wait=True)
        print("到达地面:", swift.get_position())
        time.sleep(1)

        swift.set_position(x=95, y=260, z=100, wait=True)
        print("到达地面:", swift.get_position())
        time.sleep(1)

        swift.set_position(x=95, y=260, z=42, wait=True)
        print("到达地面:", swift.get_position())
        time.sleep(1)

        swift.set_pump(on=True)
        time.sleep(1)

        swift.set_position(x=95, y=260, z=100, wait=True)
        print("到达地面:", swift.get_position())
        time.sleep(1)

        swift.set_position(x=210, y=155, z=100, wait=True)
        print("到达地面:", swift.get_position())
        time.sleep(1)

        swift.set_position(x=210, y=155, z=47, wait=True)
        print("到达地面:", swift.get_position())
        time.sleep(1)

        swift.set_pump(on=False)
        time.sleep(1)

        swift.set_position(x=210, y=155, z=80, wait=True)
        print("到达地面:", swift.get_position())
        time.sleep(1)

        swift.set_position(x=180, y=155, z=80, wait=True)
        print("到达地面:", swift.get_position())
        time.sleep(1)

        swift.set_position(x=180, y=155, z=42, wait=True)
        print("到达地面:", swift.get_position())
        time.sleep(1)

        swift.set_position(x=260, y=155, z=42, wait=True)
        print("到达地面:", swift.get_position())
        time.sleep(1)

        swift.set_position(x=260, y=155, z=100, wait=True)
        print("到达地面:", swift.get_position())
        time.sleep(1)

        swift.set_position(x=260, y=0, z=100, wait=True)
        print("到达地面:", swift.get_position())
        time.sleep(1)
    elif recommended_tile == "九万":
        swift.set_position(x=95, y=100, z=100, wait=True)
        print("到达地面:", swift.get_position())
        time.sleep(1)

        swift.set_position(x=95, y=295, z=100, wait=True)
        print("到达地面:", swift.get_position())
        time.sleep(1)

        swift.set_position(x=95, y=295, z=42, wait=True)
        print("到达地面:", swift.get_position())
        time.sleep(1)

        swift.set_pump(on=True)
        time.sleep(1)

        swift.set_position(x=95, y=295, z=100, wait=True)
        print("到达地面:", swift.get_position())
        time.sleep(1)

        swift.set_position(x=210, y=155, z=100, wait=True)
        print("到达地面:", swift.get_position())
        time.sleep(1)

        swift.set_position(x=210, y=155, z=47, wait=True)
        print("到达地面:", swift.get_position())
        time.sleep(1)

        swift.set_pump(on=False)
        time.sleep(1)

        swift.set_position(x=210, y=155, z=80, wait=True)
        print("到达地面:", swift.get_position())
        time.sleep(1)

        swift.set_position(x=180, y=155, z=80, wait=True)
        print("到达地面:", swift.get_position())
        time.sleep(1)

        swift.set_position(x=180, y=155, z=42, wait=True)
        print("到达地面:", swift.get_position())
        time.sleep(1)

        swift.set_position(x=260, y=155, z=42, wait=True)
        print("到达地面:", swift.get_position())
        time.sleep(1)

        swift.set_position(x=260, y=155, z=100, wait=True)
        print("到达地面:", swift.get_position())
        time.sleep(1)

        swift.set_position(x=260, y=0, z=100, wait=True)
        print("到达地面:", swift.get_position())
        time.sleep(1)
    else:
        print(f"未定义的推荐牌: {recommended_tile}")
    
    swift.disconnect()
    client_socket.sendto("动作完成".encode(), server_address)
except Exception as e:
    print(f"发生异常: {e}")
finally:
    swift.disconnect()
    client_socket.close()
    print("客户端已关闭")
