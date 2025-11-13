# -*- coding:utf-8
import pytest
from datetime import datetime
"""
此文档为存放测试用例的前置操作和后置操作函数
"""
@pytest.fixture(scope="session")
def boot_router():

    print(datetime.now(),"路由器上电，LAN口正常启动，WIFI正常启动")

    yield 1

    print(datetime.now(),"路由器掉电")

# @pytest.fixture(autouse=True,scope="session") # 自动使用fixture
@pytest.fixture(scope="session")
def activate_device(boot_router):

    print(datetime.now(),"设备已激活\n设备开始连接路由器")

    yield 1

    print(datetime.now(),"设备开始断开连接")
