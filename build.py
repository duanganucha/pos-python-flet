"""
POS System - Build Script
สคริปต์สำหรับสร้าง EXE ไฟล์
"""
import os
import sys
import subprocess
import shutil

def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)

def check_pyinstaller():
    """Check if PyInstaller is installed"""
    print_header("ตรวจสอบ PyInstaller")
    try:
        import PyInstaller
        print(f"✓ PyInstaller version {PyInstaller.__version__} installed")
        return True
    except ImportError:
        print("✗ PyInstaller not found")
        print("\nInstalling PyInstaller...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✓ PyInstaller installed successfully")
        return True

def clean_build():
    """Clean old build files"""
    print_header("ทำความสะอาดไฟล์เก่า")

    dirs_to_clean = ['build', 'dist']
    files_to_clean = ['pos.spec', 'POS-System.spec']

    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"Removing {dir_name}/")
            shutil.rmtree(dir_name)

    for file_name in files_to_clean:
        if os.path.exists(file_name):
            print(f"Removing {file_name}")
            os.remove(file_name)

    print("✓ Cleanup completed")

def build_exe(mode='onefile'):
    """Build EXE file"""
    print_header(f"กำลัง Build EXE ({mode})")

    # Build command
    cmd = [
        'pyinstaller',
        '--name=POS-System',
        '--windowed',  # No console window
        '--add-data=data;data',  # Include data folder
        '--hidden-import=ttkbootstrap',
        '--hidden-import=PIL',
        '--hidden-import=PIL._tkinter_finder',
    ]

    if mode == 'onefile':
        cmd.append('--onefile')

    # Optional: Add icon if exists
    if os.path.exists('icon.ico'):
        cmd.append('--icon=icon.ico')
        print("✓ Using icon.ico")

    cmd.append('src/pos_app.py')

    print(f"\nRunning command:")
    print(' '.join(cmd))
    print("\nThis may take a few minutes...\n")

    # Run PyInstaller
    result = subprocess.run(cmd)

    if result.returncode == 0:
        print_header("Build สำเร็จ!")
        return True
    else:
        print_header("Build ล้มเหลว!")
        return False

def create_portable_package():
    """Create portable package"""
    print_header("สร้าง Portable Package")

    portable_dir = "POS-System-Portable"

    # Create portable directory
    if os.path.exists(portable_dir):
        shutil.rmtree(portable_dir)
    os.makedirs(portable_dir)

    # Copy EXE
    exe_path = "dist/POS-System.exe"
    if os.path.exists(exe_path):
        shutil.copy(exe_path, portable_dir)
        print(f"✓ Copied {exe_path}")
    else:
        print(f"✗ {exe_path} not found")
        return False

    # Copy data folder
    if os.path.exists("data"):
        shutil.copytree("data", os.path.join(portable_dir, "data"))
        print("✓ Copied data folder")

    # Create README
    readme_content = """
===========================================
    POS System - Point of Sale
===========================================

วิธีใช้งาน:
1. ดับเบิลคลิก POS-System.exe
2. เลือกสินค้าและเพิ่มลงตะกร้า
3. กด Checkout เพื่อชำระเงิน
4. สามารถปริ้นใบเสร็จได้

โครงสร้างไฟล์:
- POS-System.exe    : โปรแกรมหลัก
- data/             : ข้อมูลสินค้าและใบเสร็จ
  - products.json   : รายการสินค้า
  - receipts.json   : ประวัติการขาย (สร้างอัตโนมัติ)
  - printed_receipts/ : ใบเสร็จที่ปริ้น

การแก้ไขสินค้า:
แก้ไขไฟล์ data/products.json

ระบบต้องการ:
- Windows 10/11 (64-bit)
- ไม่ต้องติดตั้ง Python

เวอร์ชัน: 1.0
สร้างโดย: Claude Code
===========================================
"""

    with open(os.path.join(portable_dir, "README.txt"), 'w', encoding='utf-8') as f:
        f.write(readme_content)
    print("✓ Created README.txt")

    print(f"\n✓ Portable package created: {portable_dir}/")
    print(f"  Size: {get_dir_size(portable_dir):.2f} MB")

    return True

def get_dir_size(path):
    """Get directory size in MB"""
    total = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            total += os.path.getsize(filepath)
    return total / (1024 * 1024)

def main():
    """Main build process"""
    print("""
    ╔══════════════════════════════════════════╗
    ║     POS System - EXE Builder             ║
    ║     สร้างไฟล์ติดตั้ง Windows             ║
    ╚══════════════════════════════════════════╝
    """)

    # Step 1: Check PyInstaller
    if not check_pyinstaller():
        print("Error: Failed to install PyInstaller")
        sys.exit(1)

    # Step 2: Clean old files
    clean_build()

    # Step 3: Ask user for build mode
    print("\nเลือกรูปแบบการ Build:")
    print("1. Single File (onefile) - ไฟล์เดียว (ช้ากว่า)")
    print("2. Directory (onedir) - มีโฟลเดอร์ (เร็วกว่า)")

    choice = input("\nเลือก (1 or 2) [1]: ").strip() or "1"

    mode = 'onefile' if choice == '1' else 'onedir'

    # Step 4: Build EXE
    if not build_exe(mode):
        print("\nBuild failed. Check the error messages above.")
        sys.exit(1)

    # Step 5: Create portable package (only for onefile)
    if mode == 'onefile':
        create_portable = input("\nสร้าง Portable Package? (y/n) [y]: ").strip().lower() or 'y'
        if create_portable == 'y':
            create_portable_package()

    # Final message
    print_header("เสร็จสิ้น!")

    if mode == 'onefile':
        print(f"\n✓ ไฟล์ EXE: dist/POS-System.exe")
        print(f"✓ ขนาด: {os.path.getsize('dist/POS-System.exe') / (1024*1024):.2f} MB")
    else:
        print(f"\n✓ โฟลเดอร์โปรแกรม: dist/POS-System/")

    print("\nคำแนะนำ:")
    print("- ต้องคัดลอกโฟลเดอร์ 'data' ไปด้วยเสมอ")
    print("- สามารถแจกจ่ายโปรแกรมได้ทันที")
    print("- ไม่ต้องติดตั้ง Python บนเครื่องผู้ใช้\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nBuild cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)
