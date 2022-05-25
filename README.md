# memory_game

## 逻辑
### 开始游戏

0. 实例化翻牌游戏类
1. 用户登录 -> `login_click_callback` 回调函数 -> `run_juior` -> 调用`create_game_window`初始化游戏窗口-> `run_game` 显示游戏窗口 进行游戏
2. 游客登录 -> 游客登录按钮绑定`run_junior`回调函数 -> 调用`create_game_window`初始化游戏窗口 -> `run_game` 显示游戏窗口 进行游戏

### 选择难度

1. 点击选择难度, 触发`run_junior` or `run_mediate` or  `run_advanced`回调函数 -> 调用`create_game_window` 初始化游戏窗口, 内部先销毁已经存在的窗口，重新开始新窗口

### 排行榜
1. 点击排行榜, 触发`junior_window` or `mediate_window` or `advanced_window` 回调函数 -> `rander_window` 查询数据 -> 将数据交给 `ranking_window`渲染排行榜页面