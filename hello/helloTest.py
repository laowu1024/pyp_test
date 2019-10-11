import asyncio
from pyppeteer import launch
from time import sleep


def screen_size():
    """使用tkinter获取屏幕大小"""
    import tkinter
    tk = tkinter.Tk()
    width = tk.winfo_screenwidth()
    height = tk.winfo_screenheight()
    tk.quit()
    return width, height


async def main():
    exepath = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
    browser = await launch(
        {'executablePath': exepath, 'headless': False,
         "args": [
             # 浏览器代理 配合某些中间人代理使用
             # "--proxy-server=http://127.0.0.1:8008",
             # 最大化窗口
             "--start-maximized",
             # 取消沙盒模式 沙盒模式下权限太小
             "--no-sandbox",
             # 不显示信息栏  比如 chrome正在受到自动测试软件的控制 ...
             "--disable-infobars",
             # log等级设置 在某些不是那么完整的系统里 如果使用默认的日志等级 可能会出现一大堆的warning信息
             "--log-level=3",
             # 设置UA
             "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
         ],
         # 用户数据保存目录 这个最好也自己指定一个目录
         # 如果不指定的话，chrome会自动新建一个临时目录使用，在浏览器退出的时候会自动删除临时目录
         # 在删除的时候可能会删除失败（不知道为什么会出现权限问题，我用的windows） 导致浏览器退出失败
         # 然后chrome进程就会一直没有退出 CPU就会狂飙到99%
         # "userDataDir": "/usr/local/tmp",
         })
    page = await browser.newPage()
    print(page.viewport)
    width, height = screen_size()
    # 设置网页可视区域大小
    await page.setViewport({
        "width": width,
        "height": height
    })
    await page.goto('http://fund.eastmoney.com/')

    head_ele = await page.xpath('//*[@id="tb_jjcs"]/thead')
    title_elements = await page.xpath('//*[@id="tb_jjcs"]/tbody')
    list1 = []
    list2 = []
    for head in head_ele:
        head_str = await (await head.getProperty('textContent')).jsonValue()
        # head_str =  await page.evaluate('(element) => element.textContent', head)
        list1.append(head_str)
    # title_elements = await page.querySelectorAll('#tb_jjcs')
    # print(await page.content())
    print(list1)
    for item in title_elements:
        # 获取文本
        title_str = await (await item.getProperty('textContent')).jsonValue()
        list2.append(title_str)
        # print(await item.getProperty('textContent'))
        # 获取链接
        # title_link = await (await item.getProperty('href')).jsonValue()
        # print(title_str)
        # print(title_link)
    print(list2)
    await page.evaluate('window.scrollBy(0, window.innerHeight)')
    sleep(5)
    await browser.close()


asyncio.get_event_loop().run_until_complete(main())
