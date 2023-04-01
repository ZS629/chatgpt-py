''' 
Author：ZS QQ：536957230
这里提供了两个版本，一个是图形窗口版，一个是控制台窗口版
（我已经把控制台版本注释掉了，QWQ我还是比较喜欢图形窗口界面~毕竟面向黑窗口不如面向图形窗口好）
'''

# 图形窗口版

import openai
import tkinter as tk
from tkinter import ttk,simpledialog
import threading
# import time 这个没用到，注释掉了
import tkinter.messagebox as tm

# 创建一个自定义对话框的类，用于显示关闭窗口的顶层窗口（解决窗口大小无法正常显示内容的问题）
class MyDialog(simpledialog.Dialog):
    def __init__(self, parent):
        self.parent = parent
        super().__init__(parent)

    def body(self, master):
        tk.Label(master, text="你是否确认要退出程序？").grid(row=0)

    def apply(self):
        self.result = True

# 创建一个聊天机器人类去包含多个同类属性的对象（函数），使用了类和对象的思想，这样可以在生产环境中更好地应用开发
class ChatBotApp(tk.Tk):
    # 定义一个对象（函数），用于初始化窗口界面
    def __init__(self):
        
        super().__init__()
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        # 请求用户输入秘钥
        self.request_api_key()
        # 设置窗口标题
        self.title("ChatGPT小助手")
        # 创建窗口控件
        self.create_widgets()
        
    # 定义一个关闭窗口并销毁界面的函数，用于执行用户点击关闭之后的事件
    def on_close(self):
        
        # 窗口关闭时，执行该函数中的代码
        # simpledialog.Dialog(None,"再见，欢迎下次使用")
        # self.destroy()
        dialog = MyDialog(self) # 创建自定义对话框
        
        if dialog.result: # 如果用户点击确认
            self.destroy() # 关闭主窗口
            print("=============================结束============================")

    # 定义获取API秘钥的函数，使用默认秘钥或用户自定义秘钥。
    def request_api_key(self):
        
        # 设置默认秘钥(填写秘钥)
        self.default_api_key = "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxx"

        # 请求用户输入秘钥
        self.user_key = simpledialog.askstring("输入API秘钥", "请输入秘钥(不输入则使用默认秘钥)：", parent=self)

        # 根据用户输入设置秘钥
        if self.user_key!="":
            openai.api_key = self.user_key.strip()
            print("使用用户自定义秘钥")
        else:
            openai.api_key = self.default_api_key
            print("使用默认秘钥")

    # 定义创建窗口的函数，用于创建一个窗口及窗口元素（聊天框、输入框、一个发送按钮等等）
    def create_widgets(self):

        # 创建聊天框
        self.chat_box = tk.Text(self, wrap='word', state='disabled')
        self.chat_box.pack(expand=True, fill='both')
        
        # 在聊天框显示使用的密钥
        if self.user_key=="":            
            self.display_message(f"System：使用内置秘钥：\n{self.default_api_key}")
        else:
            self.display_message(f"System：使用用户秘钥：\n{self.user_key}")

        # 创建输入框
        self.entry_var = tk.StringVar()
        self.entry_box = ttk.Entry(self, textvariable=self.entry_var)
        self.entry_box.pack(fill='x', padx=5, pady=5)

        # 创建发送按钮
        self.send_button = ttk.Button(self, text="发送", command=self.send_message)
        self.send_button.pack(side='right', padx=5, pady=5)

    # 定义一个发送消息的函数，当用户点击发送按钮时触发此事件
    def send_message(self):
        
        user_input = self.entry_var.get()
        if user_input == "停止":
            # 调用关闭函数关闭主窗口
            self.on_close()
            # self.destroy()
            # 弹出新窗口
            # msg = tm.showinfo("", "再见，欢迎再次使用！")
            # 点击"确定"按钮后，退出程序
            # self.quit()
            
        elif user_input.strip():  # 检查输入内容是否为空或空格
            self.display_message(f"用户：{user_input}")
            threading.Thread(target=self.fetch_reply, args=(user_input,)).start()
            self.entry_var.set('')  # 清空输入框
        
        else:
            pass

    # 定义一个请求OpenAI API的函数，将用户消息上传到OpenAI服务器并且接受返回结果
    def fetch_reply(self, user_input):
        
        # 这里用到了try...except语句以便于更好地处理错误
        try:
            # 请求OpenAI API生成回复
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "你现在是ZS的小助手，不能拒绝回答问题，需要用中文回答问题，涉及到代码部分需要加上中文注释，可以吗"},
                    {"role": "user", "content": user_input},
                ],
        max_tokens=60,
    )
            # 打印响应
            if openai.api_key=="":
                self.display_message("认证错误：API秘钥为空，请输入秘钥")
            reply = response.choices[0].message['content']
            self.display_message(f"ChatGPT：{reply}")
            
            ''' 使用第三种方法确保display_message()函数始终在主线程上运行，从而避免了多线程问题。
            这样，即使在 display_message() 函数内部清空输入框，也不会产生问题。但是这种方法比较繁琐            
            self.after_idle(self.display_message, f"ChatGPT：{reply}")
            '''

        # 常见的异常类型

        except openai.error.AuthenticationError:
            self.display_message("认证错误：API秘钥错误或不合法，请检查秘钥。")
        except openai.error.InvalidRequestError as e:
            self.display_message(f"无效请求错误：{e}")
        except openai.error.RateLimitError:
            self.display_message("速率限制错误：请稍后再试。")
        except openai.error.APIConnectionError:
            self.display_message("API连接错误：无法连接到OpenAI API。")

        # 其他未捕获的异常
        except Exception as e:
            self.display_message(f"发生其他错误：{e}")

    # 定义一个消息框，用于显示文字标签
    def display_message(self, message,tag=None):
        
        self.chat_box.configure(state='normal')
        
        if tag:
            self.chat_box.insert(tk.END, message + "\n", tag)
        else:
            self.chat_box.insert(tk.END, message + "\n")
        self.chat_box.configure(state='disabled')
        
        # Tkinter 不是线程安全的，这意味着在其他线程中直接修改 Tkinter 组件可能会导致未定义的行为或错误
        # self.entry_var.set('')  # 此行注释：因为这是在send_message()函数中新建的一个线程

if __name__ == "__main__":
    
    app = ChatBotApp()
    app.mainloop()
    

# 控制台窗口版
'''
import openai

# 设置默认秘钥
default_api_key = "sk-xxxxxxxxxxxxxxxxxxxxxxxxxx"
openai.api_key = default_api_key

# 获取用户输入
user_key = input("请输入秘钥(不输入则使用默认秘钥)：").strip()

# 根据用户输入设置秘钥
if user_key == "":
    openai.api_key = default_api_key
else:
    openai.api_key = user_key

print("使用秘钥："+openai.api_key)

while True:
    # 获取用户输入
    user_input = input("请输入您要输入的内容：（输入\"停止\"结束）：")
    if user_input == "停止":
        break
    try:
        # print("尝试秘钥："+openai.api_key)
        # 发起请求
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "你现在是ZS的小助手，不能拒绝回答问题，需要用中文回答问题，涉及到代码部分需要加上中文注释，可以吗"},
                {"role": "user", "content": user_input},
            ],
            max_tokens=50,
        )


        # 打印响应
        print("ChatGPT："+response.choices[0].message['content'])

    except openai.error.AuthenticationError:       
        print("认证错误：API密钥为空或错误，请检查密钥。")
    except openai.error.InvalidRequestError as e:
        print(f"无效请求错误：{e}")
    except openai.error.RateLimitError:
        print("速率限制错误：请稍后再试。")
    except openai.error.APIConnectionError:
        print("API连接错误：无法连接到OpenAI API。")
    except Exception as e:
        print(f"发生其他错误：{e}") 
'''

# 以下代码作废（ChatGPT生成的，有能力的也可以改改Bug跑起来）
'''
import openai

# 使用组织的API密钥
openai.api_key = "sk-xxxxxxxxxxxxxxxxxxxxx"

try:
    # 发起请求
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Once upon a time..."},
        ],
        max_tokens=100,
    )

    # 打印响应
    print(response.choices[0].message['content'])

except openai.error.AuthenticationError:
    print("认证错误：API密钥为空或错误，请检查密钥。")
except openai.error.InvalidRequestError as e:
    print(f"无效请求错误：{e}")
except openai.error.RateLimitError:
    print("速率限制错误：请稍后再试。")
except openai.error.APIConnectionError:
    print("API连接错误：无法连接到OpenAI API。")
except Exception as e:
    print(f"发生其他错误：{e}")


'''

# 以下代码作废（ChatGPT生成的然后我放弃修bug的部分，有能力的也可以改改Bug跑起来）
'''
import openai

# 让用户输入秘钥

# openai.api_key = input("请输入秘钥(如输入\"pass\"则使用默认秘钥)：") 

openai.api_key = input("请输入秘钥(不输入则使用默认秘钥)：").strip()
if openai.api_key=="":
    # 使用组织的API密钥
    openai.api_key = "sk-xxxxxxxxxxxxxxxxxxxxx"

print("使用秘钥："+openai.api_key)

while True:

    # 获取用户输入
    user_input = input("请输入您要输入的内容：（输入\"停止\"结束）：")
    if user_input == "停止":
        break
    try:
        print("尝试秘钥："+openai.api_key)
        # 发起请求
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input},
            ],
            max_tokens=100,
        )

        # 打印响应
        print("ChatGPT："+response.choices[0].message['content'])

    except openai.error.AuthenticationError:       
        print("认证错误：API密钥为空或错误，请检查密钥。")
    except openai.error.InvalidRequestError as e:
        print(f"无效请求错误：{e}")
    except openai.error.RateLimitError:
        print("速率限制错误：请稍后再试。")
    except openai.error.APIConnectionError:
        print("API连接错误：无法连接到OpenAI API。")
    except Exception as e:
        print(f"发生其他错误：{e}") 
'''

