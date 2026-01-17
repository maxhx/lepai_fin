import subprocess
import locale
 
def safe_decode(data):
    """安全解码字节数据，尝试多种编码"""
    encodings = ['utf-8', 'gbk', 'cp936', 'ansi']
    
    for encoding in encodings:
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            continue
    
    # 如果所有编码都失败，使用错误处理
    return data.decode('utf-8', errors='replace')
 
# 获取wifi列表
try:
    result = subprocess.run(['netsh', 'wlan', 'show', 'profiles'], capture_output=True, text=True, encoding='utf-8', errors='replace')
    output = result.stdout.split('\n')
except:
    # 如果上面的方法失败，使用二进制方式
    result = subprocess.run(['netsh', 'wlan', 'show', 'profiles'], capture_output=True)
    output = safe_decode(result.stdout).split('\n')

wifis = [line.split(':')[1][1:-1] for line in output if "所有用户配置文件" in line]
 
# 查看每个wifi对应的密码
for wifi in wifis:
    try:
        result = subprocess.run(['netsh', 'wlan', 'show', 'profile', wifi, 'key=clear'],
                               capture_output=True, text=True, encoding='utf-8', errors='replace')
        results = result.stdout.split('\n')
    except:
        # 备用方法
        result = subprocess.run(['netsh', 'wlan', 'show', 'profile', wifi, 'key=clear'],
                               capture_output=True)
        results = safe_decode(result.stdout).split('\n')
    
    results = [line.split(':')[1][1:-1] for line in results if "关键内容" in line]
    try:
        print(f'wifi名：{wifi}，密码:{results[0]}')
    except IndexError:
        print(f'wifi名：{wifi}，密码:无法提取')
input('按enter确认并退出')