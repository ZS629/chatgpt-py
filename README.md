# 基于Python的ChatGPT聊天室

## 1. 项目简介

图形窗口界面版 Ver1.0

对之前的控制台窗口版进行了调整
(原控制台版的代码已经注释掉，需要可以取消注释)

有能力的可以将两个版本集成然后用一个控制语句去让用户选择用什么版本
(提示：可以使用函数将两个版本的功能交叉部分封装一下)

## 2. 环境配置

安装所需的库（这里只需要安装openai库即可）。

```shell
pip install openai
```

## 3. 使用说明

安装好所需的模块（openai库）直接运行即可

程序相关截图

![运行](https://github.com/ZS629/chatgpt-py/blob/master/img/run.jpg)

![指令关闭](https://github.com/ZS629/chatgpt-py/blob/master/img/closerw.png)

![用户关闭窗口](https://github.com/ZS629/chatgpt-py/blob/master/img/close.png)

## 4. 已知问题和解决方案

在处理一些问题上，我询问了ChatGPT（懒得百度QWQ），以下是一个小总结：

一、处理多线程的问题

①直接在send_message()函数中使用GUI清空输入框，简单明了QWQ

②通过将 self.entry_var 作为一个参数传递给 display_message() 函数，然后在该函数中清空输入框。
需要在每次调用 display_message() 函数时传递self.entry_var作为参数。如：

```python
def display_message(self, message, entry_var, tag=None):
```

然后需要在每次调用这个函数时引入一个entry_var作为参数，如：

```python
self.display_message(..., self.entry_var)
```

为什么要这样改呢（ChatGPT给出的解释是这样的）：

```markdown
self.entry_var 是 ChatBotApp 类的一个属性，如果您将 self.entry_var.set('') 放在 display_message() 函数中。
由于 self 指代的是 ChatBotApp 类的实例，display_message() 函数将无法识别 self.entry_var。
```

③在display_message()函数中使用GUI清空输入框，
但这需要将所有self.display_message(...)函数替换为

```python
self.after_idle(self.display_message, ...)
```

这样做可以确保display_message()函数始终在主线程上运行，从而避免了多线程问题。
此时，即使在 display_message() 函数内部清空输入框，也不会产生问题。但这种方法比较繁琐

总之，在实际应用中，选择哪种方法取决于你的具体需求和编程风格。
如果你希望保持代码简洁并专注于解决当前问题，将清空输入框的操作放在 send_message() 函数中可能是更好的选择（这里为了简洁我就采用第一种方法了）。
但是，如果你希望程序更具通用性，可以在多线程环境中正常工作，并确保GUI操作始终在主线程上执行，那么使用 

```python
self.after_idle(self.display_message, ...) 的方法可能更适合你。
```

二、处理引发异常的真正原因（是由于秘钥为空还是秘钥不正确）的问题

吃个饭再写QWQ，算了，还是不写了，代码里有(懒QWQ)

## 5. 更新日志和贡献者

图形窗口版 Ver1.0(2023/4/1 14:36)
如你所见

## 6. 许可证和版权声明

本项目遵循Apache2.0协议开源，仅供交流学习，请勿用于非法用途
此项目仅提供给开发者一个参考，不是什么卖号、卖秘钥、卖产品的

## 7. 联系信息

QQ：536957230

QQ交流群（开发者交流群）：782164105

QQ交流群（交流学习，后面放个机器人玩QWQ）：526308313
