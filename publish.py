#!/usr/bin/env python3
"""
发布脚本 - 自动化发布到 PyPI
"""

import os
import subprocess
import sys

def run_command(cmd, description):
    """运行命令并显示结果"""
    print(f"\n🔧 {description}")
    print(f"执行: {cmd}")
    
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.stdout:
        print(f"输出: {result.stdout}")
    if result.stderr:
        print(f"错误: {result.stderr}")
    
    if result.returncode != 0:
        print(f"❌ 命令执行失败，退出码: {result.returncode}")
        sys.exit(1)
    else:
        print("✅ 成功")

def main():
    print("🚀 开始发布 Kiro Process Manager 到 PyPI")
    print("=" * 50)
    
    # 检查必要文件
    required_files = ['setup.py', 'pyproject.toml', 'README.md', 'LICENSE']
    for file in required_files:
        if not os.path.exists(file):
            print(f"❌ 缺少必要文件: {file}")
            sys.exit(1)
    
    print("✅ 所有必要文件都存在")
    
    # 清理旧的构建文件
    run_command("rm -rf build dist *.egg-info", "清理旧的构建文件")
    
    # 构建包
    run_command("python -m build", "构建发布包")
    
    # 检查包
    run_command("twine check dist/*", "检查包的完整性")
    
    # 询问用户是否要上传
    print("\n📦 包构建完成！")
    print("dist/ 目录中的文件:")
    for file in os.listdir("dist"):
        print(f"  - {file}")
    
    choice = input("\n是否要上传到 PyPI？(y/N): ").lower().strip()
    
    if choice == 'y':
        # 先上传到 TestPyPI
        test_choice = input("是否先上传到 TestPyPI 进行测试？(Y/n): ").lower().strip()
        
        if test_choice != 'n':
            print("\n🧪 上传到 TestPyPI...")
            run_command("twine upload --repository testpypi dist/*", "上传到 TestPyPI")
            print("\n✅ 已上传到 TestPyPI")
            print("你可以访问 https://test.pypi.org/project/kiro-process-manager/ 查看")
            
            final_choice = input("\n确认要上传到正式 PyPI 吗？(y/N): ").lower().strip()
            if final_choice != 'y':
                print("取消上传到正式 PyPI")
                return
        
        # 上传到正式 PyPI
        run_command("twine upload dist/*", "上传到正式 PyPI")
        print("\n🎉 发布成功！")
        print("你的包现在可以通过以下命令安装：")
        print("pip install kiro-process-manager")
        print("\n包页面: https://pypi.org/project/kiro-process-manager/")
    else:
        print("取消上传")

if __name__ == '__main__':
    main()