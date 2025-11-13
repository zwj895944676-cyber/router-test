# -*- coding:utf-8 -*-
import re
import json
"""
编写一个日志分析脚本：分析一段模拟的路由器系统日志。
使用正则表达式统计"错误"和"警告"出现的次数，并将结果输出到json文件中。
"""


class Syslog:
    def __init__(self, syslog) :
        self.syslog_read = []
        self.syslog_content = ""
        self.syslog = syslog
        self.error_count = 0
        self.warning_count = 0

    def get_log(self):
        """
        读取系统日志文件
        """
        try:
            with open(self.syslog, "r", encoding="utf-8") as file:
                self.syslog_read = []
                self.syslog_content = ""
                while True:
                    text = file.readline()
                    if not text:
                        break
                    self.syslog_read.append(text.strip())
                    self.syslog_content += text
            print(f"成功读取日志文件，共{len(self.syslog_read)}行")
            return self.syslog_content
        except FileNotFoundError:
            print(f"发生错误：找不到文件 '{self.syslog}'")
            return ""
        except Exception as e:
            print(f"读取日志时出错：{str(e)}")
            return ""

    def calculate(self):
        """
        统计错误和警告出现的次数
        """
        if not self.syslog_content:
            print("错误：请先调用get_log方法读取日志")
            return
        
        # 统计错误次数（不区分大小写）
        self.error_count = len(re.findall(r"error", self.syslog_content, re.IGNORECASE))
        # 统计警告次数（不区分大小写）
        self.warning_count = len(re.findall(r"warning", self.syslog_content, re.IGNORECASE))
        
        # 统计中文的错误和警告
        self.error_count += len(re.findall(r"错误", self.syslog_content))
        self.warning_count += len(re.findall(r"警告", self.syslog_content))
        
        print(f"统计结果：错误 {self.error_count} 次，警告 {self.warning_count} 次")
        return {"error": self.error_count, "warning": self.warning_count}

    def show(self):
        """
        展示错误和警告次数
        """
        print("=" * 60)
        print(f"日志分析结果：")
        print(f"  - 错误次数: {self.error_count}")
        print(f"  - 警告次数: {self.warning_count}")
        print("=" * 60)
        
    def save_to_json(self, output_file="result/log_analysis_result.json"):
        """
        将分析结果保存到JSON文件
        """
        result = {
            "log_file": self.syslog,
            "total_lines": len(self.syslog_read),
            "error_count": self.error_count,
            "warning_count": self.warning_count,
            "timestamp": "2024"
        }
        
        try:
            with open(output_file, "w", encoding="utf-8") as file:
                json.dump(result, file, ensure_ascii=False, indent=2)
            print(f"分析结果已保存到文件: {output_file}")
            return True
        except Exception as e:
            print(f"保存JSON文件时出错: {str(e)}")
            return False
    
    def __str__(self) -> str:
        return f"Syslog对象: 文件'{self.syslog}'，{len(self.syslog_read)}行日志，{self.error_count}个错误，{self.warning_count}个警告"


# 主程序运行
if __name__ == "__main__":
    print("开始分析路由器系统日志...")
    s = Syslog("data/syslog.txt")
    s.get_log()
    s.calculate()
    s.show()
    s.save_to_json()
    print("\n日志分析完成！")
