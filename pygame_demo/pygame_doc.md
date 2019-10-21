- Demo
    - 打飞机
    - 井字棋
    - 贪吃蛇
    - 八分音符
    - 俄罗斯方块
    - 自走棋
    
- 资料：
    - [中文文档](https://blog.csdn.net/qq_41556318/article/details/85880263)
    - [开发pdf](https://evanli.github.io/programming-book-3/Python/用Python%20和%20Pygame%20写游戏%20-%20从入门到精通.pdf)
    - 书单
        - [快速上手](http://down.yabook.org/file/402712-332896173)
        - [编程入门](https://www.zhihu.com/pub/reader/119584851/chapter/1058121444441042944)
        - [开源商业化三维游戏引擎大揭秘 ](https://cread.jd.com/read/startRead.action?bookId=30133881&readType=3)
        - [《云风——我的编程感悟》 ](http://www.xwood.net/_site_domain_/_root/5870/5930/5932/t_c264871.html)
        - [设计模式]()
    - 引擎
        - [panda3d](https://www.panda3d.org/)
    - 美术
        - [blender 斑斓中文社区](https://www.blendercn.org/#top)    
    - 扩展
        - 得到每天读本书：游戏改变世界
        - 张潇予——商业
        - 极客时间    
- 概述：
    - 原理：视觉暂留(余晖效应)，静态画面快速连续播放，形成视觉上的连续活动画面
    - 主循环：不仅要把一幅幅画面播放出来，还需要处理player的操作与游戏中内容的交互
        - 简单的接收player的输入，以及处理game中的各种逻辑判断、运动、碰撞等等
        - 复杂的进行物理运算、计算光线的照射效果、处理大量电脑角色的智能、网络信息通讯等
        
- 基础知识
    - 像素：将笛卡尔坐标（左上角为原点，向左向下数值递增，向左为X轴，向下为Y轴）表示为两个整数的元组，例如：(4,2)，第一个为X轴坐标，第二个为Y轴坐标
    - 区分函数调用、方法调用、调用模块中的函数
        ```
        import whammy
        fizzy() # 函数调用
        egg = Wombat()
        egg.bluhluh() # 方法调用
        whammy.spam() # 模块调用
        ```
    - Surface对象：
        - 表示一个矩形的2D图像的对象，可以通过调用Pygame绘制函数来改变Surface对象的像素，再绘制到屏幕上
        - 通过`pygame.display.set_mode()`获取的Surface对象叫做显示Surface，绘制到显示Surface对象上的任何内容，
        当调用`pygame.display.update()`函数都会显示到窗口上
        - 窗口的边框，标题栏，和按钮并不是Surface对象的一部分
    - Color对象
        - 由RGB三原色构成，0-255，例如：(255,0,0)、(0,255,0)、(0,0,255)
        - 透明度alpha，第四个值，0为完全透明，255为完全不透明 例如：(255,0,0,255);
            - 使用convert_alpha()创建surface对象——`pygame.diplay.set_mode((300, 400)).convert_alpha()`
        -     
    - Rect对象
        
    - 绘制函数        
        
               