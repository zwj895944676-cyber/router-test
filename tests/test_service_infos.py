# -*- coding: utf-8 -*-
import pytest
from commons.csv_utils import csv_read
import allure

"""
路由器设备信息管理器
功能：使用类来模拟设备（属性包括IP、型号、状态），并能通过函数实现设备的增删改查。
"""


class Device:
    """
    设备类，用于表示单个设备的基本信息
    """

    def __init__(self, ip, model, status):
        self.ip = ip
        self.model = model
        self.status = status

    def __str__(self):
        return f"IP: {self.ip}, 型号: {self.model}, 状态: {self.status}"

    def update(self, model=None, status=None):
        """更新设备信息"""
        if model is not None:
            self.model = model
        if status is not None:
            self.status = status


class RouterDeviceManager:
    """
    路由器设备信息管理类，用于存储和管理路由器的设备信息。
    提供设备的增删改查功能。
    """

    def __init__(self):
        # 实例化列表来存储设备信息
        self.devices = []

    def add_device(self, ip, model, status):
        """
        新增设备

        Args:
            ip: 设备IP地址
            model: 设备型号
            status: 设备状态

        Returns:
            bool: True表示添加成功，False表示IP已存在
        """
        # 检查IP是否已存在
        if self._find_device_by_ip(ip):
            print(f"添加失败：IP地址 {ip} 已存在")
            return False

        # 创建新设备并添加
        new_device = Device(ip, model, status)
        self.devices.append(new_device)
        print(f"新增设备: {new_device}")
        return True

    def delete_device(self, ip):
        """
        删除设备

        Args:
            ip: 要删除设备的IP地址

        Returns:
            bool: True表示删除成功，False表示未找到设备
        """
        device = self._find_device_by_ip(ip)
        if device:
            self.devices.remove(device)
            print(f"删除设备: IP={ip}")
            return True
        else:
            print(f"删除失败：未找到IP为 {ip} 的设备")
            return False

    def update_device(self, ip, model=None, status=None):
        """
        修改设备信息，可以只修改部分属性

        Args:
            ip: 要修改设备的IP地址
            model: 新的设备型号（可选）
            status: 新的设备状态（可选）

        Returns:
            bool: True表示修改成功，False表示未找到设备
        """
        device = self._find_device_by_ip(ip)
        if device:
            device.update(model, status)
            print(f"修改设备成功: {device}")
            return True
        else:
            print(f"修改失败：未找到IP为 {ip} 的设备")
            return False

    def find_device(self, ip):
        """
        查找指定IP的设备

        Args:
            ip: 要查找设备的IP地址

        Returns:
            Device: 找到的设备对象，未找到返回None
        """
        device = self._find_device_by_ip(ip)
        if device:
            print(f"找到设备: {device}")
            return device
        else:
            print(f"未找到IP为 {ip} 的设备")
            return None

    def list_all_devices(self):
        """
        显示所有设备信息
        """
        if not self.devices:
            print("\n终端设备管理器 - 当前无设备信息")
            return

        print("\n终端设备管理器 - 设备列表")
        print("=" * 60)
        print(f"{'IP地址':<20} {'设备型号':<25} {'状态':<10}")
        print("=" * 60)

        # 遍历打印每一台设备的信息
        for device in self.devices:
            print(f"{device.ip:<20} {device.model:<25} {device.status:<10}")

        print("=" * 60)
        print(f"总计设备数: {len(self.devices)}\n")

    def _find_device_by_ip(self, ip):
        """
        内部辅助方法：根据IP地址查找设备

        Args:
            ip: 设备IP地址

        Returns:
            Device: 找到的设备对象，未找到返回None
        """
        for device in self.devices:
            if device.ip == ip:
                return device
        return None


# 测试用例
class TestRouterDeviceManager():
    """
    单元测试：测试路由器设备信息管理器
    """

    # 测试增加功能
    @allure.epic("MD04-V1.0 国内版")
    @allure.feature("设备信息管理器")
    @allure.story("新增设备")
    @allure.title("新增一台设备")
    @pytest.mark.parametrize("a,b,c", csv_read("data/data.csv"))
    @pytest.mark.base # 增加base标记
    def test_add_device(self,activate_device,a,b,c): # 主动使用fixture
        # 创建对象
        new_obj = RouterDeviceManager()

        # 输入具体参数
        new_obj.add_device(a,b,c)

        # 断言存在 用辅助方法查询是否添加进去，返回非None
        assert new_obj._find_device_by_ip(a) != None

    # 测试删除功能
    @allure.epic("MD04-V1.0 国内版")
    @allure.feature("设备信息管理器")
    @allure.story("删除设备")
    @allure.title("删除一台设备")
    @pytest.mark.parametrize("a,b,c", csv_read("../data/data.csv"))
    @pytest.mark.base # 增加base标记
    def test_delete_device(self,activate_device,a,b,c): # 主动使用fixture
        # 创建对象
        new_obj = RouterDeviceManager()

        # 增加设备
        new_obj.add_device(a,b,c)

        # 删除新增加的设备
        new_obj.delete_device(a)

        # 断言不存在，用辅助方法查询是否删除，返回None
        assert new_obj._find_device_by_ip(a) == None

    # 测试修改功能
    @allure.epic("MD04-V1.0 国内版")
    @allure.feature("设备信息管理器")
    @allure.story("修改更新设备")
    @allure.title("修改更新一台设备")
    @pytest.mark.parametrize("a,b,c", csv_read("../data/data.csv"))
    @pytest.mark.base # 增加base标记
    def test_update_device(self,activate_device,a,b,c):
        # 创建对象
        new_obj = RouterDeviceManager()

        # 增加设备
        new_obj.add_device(a, b, c)

        # 修改设备信息
        new_obj.update_device(a,b,c)

        # 断言前：获取当前IP的设备信息(IP不可修改)
        device = new_obj._find_device_by_ip(a)

        # 断言现在查询的设备信息是否等于修改的信息
        assert (device.model == b) and (device.status == c)

    # 测试查询功能
    @allure.epic("MD04-V1.0 国内版")
    @allure.feature("设备信息管理器")
    @allure.story("查询设备信息")
    @allure.title("查询一台设备信息")
    @pytest.mark.parametrize("a,b,c", csv_read("../data/data2.csv"))
    @pytest.mark.base # 增加base标记
    def test_find_device(self,activate_device,a,b,c):
        # 创建对象
        new_obj = RouterDeviceManager()

        # 增加设备
        new_obj.add_device(a,b,c)

        # 因为查询功能已包含内部辅助方法_find_device_by_ip，所以这里用line 38 中用存储设备信息的列表devices来验证
        # 将查询功能得到的信息存储到列表
        lst2 = []
        lst2.append(new_obj.find_device(a))

        # 断言 查询得到的新列表 是否等于 对象里原本的储存列表
        assert lst2 == new_obj.devices
