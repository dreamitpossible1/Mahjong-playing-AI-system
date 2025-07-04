import os
import cv2
import base64
import numpy as np
from openai import OpenAI
import gi
import sys
import signal
import datetime
import threading
import time
import socket

gi.require_version('Gst', '1.0')
gi.require_version('GLib', '2.0')
from gi.repository import Gst, GLib, GObject

# UDP 服务器设置
UDP_IP = "192.168.1.26"
UDP_PORT = 9090
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((UDP_IP, UDP_PORT))
print(f"UDP 服务器启动，等待客户端消息... ({UDP_IP}:{UDP_PORT})")
client_address = None

# 等待客户端连接
def udp_wait_client():
    global client_address
    data, client_address = server_socket.recvfrom(1024)
    print(f"收到客户端 {client_address} 的消息：{data.decode()}")

#开始通信
class QwenMultiTurnChat:
    def __init__(self, api_key, base_url):
        # 初始化 OpenAI 客户端
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.history = []  # 保存多轮对话历史
        self.lock = threading.Lock()  # 添加锁确保线程安全

    def add_user_message(self, prompt=None, image_path=None):
        """添加用户消息，支持文本和Base64图像"""
        content = []
        if image_path is not None:
            try:
                # 读取图片并转换为Base64
                with open(image_path, "rb") as image_file:
                    base64_image = base64.b64encode(image_file.read()).decode('utf-8')
                
                # 构建Data URL
                image_data_url = f"data:image/jpeg;base64,{base64_image}"
                content.append({
                    'type': 'image_url',
                    'image_url': {'url': image_data_url}
                })
                print("DEBUG: Image loaded successfully from", image_path)
            except Exception as e:
                print("图片加载失败:", str(e))
        if prompt:
            content.append({'type': 'text', 'text': prompt})
        self.history.append({'role': 'user', 'content': content})

    def get_assistant_response(self):
        """调用 Qwen 模型获取回复"""
        try:
            response = self.client.chat.completions.create(
                model="qwen-vl-plus-latest",
                messages=self.history
            )
            # 根据返回结构提取回复文本
            reply_text = response.choices[0].message.content
            self.history.append({'role': 'assistant', 'content': [{'type': 'text', 'text': reply_text}]})
            return reply_text
        except Exception as e:
            print("API调用失败:", str(e))
            return "抱歉，处理请求时出错"

    def chat_round(self, prompt=None, image_path=None):
        """
        执行一轮对话：用户输入 + 模型回复
        :param prompt: 用户文本输入
        :param image_path: 图像文件路径
        :return: 助手的回复
        """
        with self.lock:  # 使用锁确保线程安全
            self.add_user_message(prompt=prompt, image_path=image_path)
            return self.get_assistant_response()

class ImageCapture:
    def __init__(self):
        self.capture_requested = False
        self.lock = threading.Lock()
        self.captured_image_path = None
        self.capture_complete = threading.Event()
    
    def request_capture(self):
        with self.lock:
            self.capture_requested = True
            self.capture_complete.clear()
    
    def should_capture(self):
        with self.lock:
            if self.capture_requested:
                self.capture_requested = False
                return True
            return False
    
    def set_captured_image(self, path):
        with self.lock:
            self.captured_image_path = path
            self.capture_complete.set()
    
    def get_captured_image(self):
        with self.lock:
            return self.captured_image_path
    
    def wait_for_capture(self, timeout=None):
        return self.capture_complete.wait(timeout)

def on_new_sample(appsink, image_capture, chatbot):
    """Callback for handling new image samples"""
    if not image_capture.should_capture():
        return Gst.FlowReturn.OK
        
    sample = appsink.emit("pull-sample")
    if sample:
        caps = sample.get_caps()
        if caps:
            buffer = sample.get_buffer()
            success, map_info = buffer.map(Gst.MapFlags.READ)
            if success:
                try:
                    # Get buffer data
                    data = map_info.data
                    # 生成唯一文件名
                    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"captured_image_{timestamp}.jpeg"
                    
                    # Save the raw data as JPEG
                    with open(filename, 'wb') as f:
                        f.write(data)
                    
                    print(f"\n成功保存图片: {filename}")
                    
                    # 设置捕获的图片路径
                    image_capture.set_captured_image(filename)
                    
                    # 启动新线程处理图片分析
                    threading.Thread(target=analyze_image, args=(filename, chatbot)).start()
                    
                except Exception as e:
                    print("保存图片时出错:", str(e))
                finally:
                    buffer.unmap(map_info)
            return Gst.FlowReturn.OK
    return Gst.FlowReturn.ERROR

def analyze_image(image_path, chatbot):
    global client_address
    """分析图片并获取模型响应"""
    try:
        print(f"\n开始分析图片: {image_path}")
        start_time = time.time()
        
        # 调用模型分析图片
        prompt = """请帮我识别这张图片中的麻将牌，并告诉我当前手牌是什么？然后根据麻将规则，建议我打哪一张牌？

请按照以下格式回答：
1. 首先识别手牌：[列出所有手牌]
2. 然后给出建议：建议打出 [具体牌名，如：五万、九筒、三条等]

注意：
- 请使用标准的中文数字（一二三四五六七八九）和花色（万、筒、条）
- 推荐时请明确说出"建议打出"或"推荐打出"等关键词
- 如果推荐多张牌，请选择其中一张作为最终推荐"""
        response = chatbot.chat_round(prompt=prompt, image_path=image_path)
        
        end_time = time.time()
        print(f"\n【助手】图片分析结果 ({image_path}, 耗时: {end_time-start_time:.2f}秒):")
        print(response)
        print("-" * 50)
        
        # 从响应中提取推荐的牌
        import re
        recommended_tile = None
        
        # 定义数字映射表（处理"五万"和"伍万"等不同表达）
        number_mapping = {
            '一': '一', '二': '二', '三': '三', '四': '四', '五': '伍', '伍': '伍',
            '六': '六', '七': '七', '八': '八', '九': '九'
        }
        
        # 定义花色映射表
        suit_mapping = {
            '万': '万', '萬': '万',  # 处理繁体字
            '筒': '筒', '饼': '筒',  # 处理不同叫法
            '条': '条', '條': '条', '索': '条'  # 处理不同叫法
        }
        
        # 多种模式匹配推荐牌
        patterns = [
            # 模式1: "建议你打出/打/出 五万"
            r'建议你[打出|打|出].*?([一二三四五六七八九伍][万筒条萬條])',
            # 模式2: "推荐打出 五万"
            r'推荐[打出|打|出].*?([一二三四五六七八九伍][万筒条萬條])',
            # 模式3: "可以打出 五万"
            r'可以[打出|打|出].*?([一二三四五六七八九伍][万筒条萬條])',
            # 模式4: "选择打出 五万"
            r'选择[打出|打|出].*?([一二三四五六七八九伍][万筒条萬條])',
            # 模式5: "比如 五万" (处理"比如 九万"这种格式)
            r'比如.*?([一二三四五六七八九伍][万筒条萬條])',
            # 模式6: "随机选择 五万"
            r'随机选择.*?([一二三四五六七八九伍][万筒条萬條])',
            # 模式7: "**五万**" (处理加粗格式)
            r'\*\*([一二三四五六七八九伍][万筒条萬條])\*\*',
            # 模式8: 直接匹配牌名
            r'([一二三四五六七八九伍][万筒条萬條])'
        ]
        
        # 尝试所有模式
        print("开始提取推荐牌...")
        for i, pattern in enumerate(patterns):
            matches = re.findall(pattern, response)
            if matches:
                print(f"模式{i+1}匹配成功: {matches}")
                # 取第一个匹配的牌
                raw_tile = matches[0]
                print(f"原始匹配: {raw_tile}")
                
                # 标准化牌名
                number_char = raw_tile[0]
                suit_char = raw_tile[1]
                
                # 转换数字
                if number_char in number_mapping:
                    number = number_mapping[number_char]
                    print(f"数字转换: {number_char} -> {number}")
                else:
                    number = number_char
                    print(f"数字保持原样: {number_char}")
                
                # 转换花色
                if suit_char in suit_mapping:
                    suit = suit_mapping[suit_char]
                    print(f"花色转换: {suit_char} -> {suit}")
                else:
                    suit = suit_char
                    print(f"花色保持原样: {suit_char}")
                
                # 组合成标准格式
                recommended_tile = f"{number}{suit}"
                print(f"标准化后的牌: {recommended_tile}")
                break
            else:
                print(f"模式{i+1}未匹配")
        
        if recommended_tile:
            print(f"提取到推荐打出的牌: {recommended_tile}")
            # 发送推荐的牌给客户端
            if client_address:  # 确保客户端已连接
                server_socket.sendto(recommended_tile.encode(), client_address)
                print(f"已发送推荐牌 {recommended_tile} 给客户端")
        else:
            print("未能从回复中提取到推荐的牌")
            print("完整回复内容:", response)
        
    except Exception as e:
        print(f"分析图片 {image_path} 时出错:", str(e))

def handle_keyboard(pipeline, loop, image_capture):
    """Handle keyboard input for capturing images"""
    import termios
    import tty
    
    def get_char():
        # Save the terminal settings
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            # Set the terminal to raw mode
            tty.setraw(sys.stdin.fileno())
            # Read a single character
            ch = sys.stdin.read(1)
        finally:
            # Restore the terminal settings
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
    
    def keyboard_thread():
        print("按 's' 键拍照并分析，按 'q' 键退出")
        while True:
            char = get_char()
            if char == 's':
                print("\n正在拍照...")
                # Request image capture
                image_capture.request_capture()
            elif char == 'q':
                print("\n正在退出...")
                loop.quit()
                break
    
    # Start keyboard monitoring in a separate thread
    keyboard_thread = threading.Thread(target=keyboard_thread, daemon=True)
    keyboard_thread.start()

# 主程序
if __name__ == '__main__':
    # 等待客户端连接，记录 client_address
    udp_wait_client()

    # 设置 API Key 和 DashScope URL
    api_key = "sk-" # 替换为你的真实 API Key
    base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"

    # 初始化聊天对象
    chatbot = QwenMultiTurnChat(api_key, base_url)

    # 第一轮对话：发送初始提示
    prompt = "你是一个麻将高手，我需要你帮我决策打哪一张，让我们先识别一下每一张牌，你要记住它们"
    response = chatbot.chat_round(prompt=prompt)
    print("【助手】:", response)

    # 第二轮对话：加载图片进行解析
    image_paths = ["wan.jpeg", "tong.jpeg", "tiao.jpeg"]  # 替换为实际的图片文件名
    prompts = [
        "这些牌从左到右是一万到九万",
        "这些牌从左到右是一筒到九筒",
        "这些牌从左到右是一条到九条"
    ]

    for idx, image_path in enumerate(image_paths):
        if not os.path.exists(image_path):
            print("图片不存在:", image_path, "，跳过处理")
            continue
            
        prompt = prompts[idx]
        response = chatbot.chat_round(prompt=prompt, image_path=image_path)
        print("【助手】解析图像", image_path, "的回复:", response)

    # 第三轮对话：启动GStreamer摄像头显示
    print("GStreamer摄像头已启动，按 's' 键拍照并分析，按 'q' 键退出程序")

    Gst.init(None)
    
    # Create pipeline with tee for display and image capture
    pipeline_str = (
        'qtiqmmfsrc camera=0 name=src ! '
        'video/x-raw,format=NV12,width=1280,height=720,framerate=30/1 ! '
        'tee name=t ! queue max-size-buffers=1 leaky=downstream ! '
        'waylandsink fullscreen=true sync=true '
        't. ! queue max-size-buffers=1 leaky=downstream ! '
        'videoconvert ! video/x-raw,format=I420 ! '
        'jpegenc quality=85 ! '
        'appsink name=snapshot emit-signals=true sync=true max-buffers=1 drop=true'
    )
    
    pipeline = Gst.parse_launch(pipeline_str)
    if not pipeline:
        print("无法创建GStreamer pipeline")
        sys.exit(1)

    # Initialize image capture controller
    image_capture = ImageCapture()

    # Get the appsink element
    appsink = pipeline.get_by_name("snapshot")
    if appsink:
        # Set up the callback for new samples with chatbot parameter
        appsink.connect("new-sample", lambda appsink: on_new_sample(appsink, image_capture, chatbot))

    loop = GLib.MainLoop()
    
    def handle_sigint(sig, frame):
        print("\n捕获到中断信号，退出...")
        pipeline.set_state(Gst.State.NULL)
        loop.quit()
    signal.signal(signal.SIGINT, handle_sigint)

    # Start keyboard handling
    handle_keyboard(pipeline, loop, image_capture)

    pipeline.set_state(Gst.State.PLAYING)
    try:
        loop.run()
    except Exception as e:
        print("主循环异常:", e)
    finally:
        pipeline.set_state(Gst.State.NULL)
