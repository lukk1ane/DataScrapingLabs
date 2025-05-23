#!/usr/bin/env python3
"""
LAB8 Main Runner: Execute all scraping tasks
Runs Task 1, Task 2, Task 3, and Bonus in sequence.
"""

import sys
import os
import subprocess
import time
from datetime import datetime


def print_header(title, width=60):
    """Print a formatted header."""
    print("\n" + "=" * width)
    print(f" {title} ".center(width))
    print("=" * width)


def run_task(script_name, task_description):
    """Run a task script and return success status."""
    print_header(f"Running {task_description}")
    
    script_path = os.path.join(os.path.dirname(__file__), script_name)
    
    if not os.path.exists(script_path):
        print(f"❌ Script {script_name} not found!")
        return False
    
    try:
        print(f"🚀 Executing: {script_name}")
        print(f"📝 Task: {task_description}")
        print(f"⏰ Started at: {datetime.now().strftime('%H:%M:%S')}")
        print("-" * 60)
        
        # Run the script
        result = subprocess.run([sys.executable, script_path], 
                              capture_output=False, 
                              text=True, 
                              cwd=os.path.dirname(__file__))
        
        print("-" * 60)
        print(f"⏰ Completed at: {datetime.now().strftime('%H:%M:%S')}")
        print(f"📊 Exit code: {result.returncode}")
        
        if result.returncode == 0:
            print(f"✅ {task_description} completed successfully!")
            return True
        else:
            print(f"❌ {task_description} failed with exit code {result.returncode}")
            return False
            
    except Exception as e:
        print(f"❌ Error running {script_name}: {e}")
        return False


def check_dependencies():
    """Check if required dependencies are installed."""
    print_header("Checking Dependencies")
    
    required_packages = ['requests', 'bs4', 'lxml']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} - NOT FOUND")
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("Install them with: pip install -r requirements.txt")
        return False
    
    print("\n✅ All dependencies are installed!")
    return True


def main():
    """Main function to run all LAB8 tasks."""
    print_header("LAB8 Data Scraping - All Tasks Runner", 70)
    print("This script will run all LAB8 tasks in sequence:")
    print("• Task 1: Basic Login Form Scraping")
    print("• Task 2: CSRF Token Login Form Scraping") 
    print("• Task 3: Cookie Management and Session Persistence")
    print("• Bonus: Multi-Session Manager")
    
    # Check dependencies first
    if not check_dependencies():
        print("\n❌ Please install missing dependencies before running tasks.")
        sys.exit(1)
    
    # Task definitions
    tasks = [
        ("task1_basic_login.py", "Task 1: Basic Login Form Scraping"),
        ("task2_csrf_login.py", "Task 2: CSRF Token Login Form Scraping"),
        ("task3_cookie_management.py", "Task 3: Cookie Management and Session Persistence"),
        ("bonus_session_manager.py", "Bonus: Multi-Session Manager")
    ]
    
    # Track results
    results = {}
    start_time = datetime.now()
    
    print(f"\n🏁 Starting all tasks at {start_time.strftime('%H:%M:%S')}")
    
    # Run each task
    for script_name, task_description in tasks:
        task_start = datetime.now()
        success = run_task(script_name, task_description)
        task_duration = datetime.now() - task_start
        
        results[task_description] = {
            'success': success,
            'duration': task_duration
        }
        
        # Wait a bit between tasks
        if script_name != tasks[-1][0]:  # Don't wait after last task
            print(f"\n⏳ Waiting 3 seconds before next task...")
            time.sleep(3)
    
    # Summary report
    total_duration = datetime.now() - start_time
    successful_tasks = sum(1 for result in results.values() if result['success'])
    total_tasks = len(tasks)
    
    print_header("LAB8 Execution Summary", 70)
    
    print(f"📊 Overall Results:")
    print(f"   Total Tasks: {total_tasks}")
    print(f"   Successful: {successful_tasks}")
    print(f"   Failed: {total_tasks - successful_tasks}")
    print(f"   Success Rate: {(successful_tasks/total_tasks)*100:.1f}%")
    print(f"   Total Duration: {total_duration}")
    
    print(f"\n📋 Task Details:")
    for task_name, result in results.items():
        status = "✅ PASS" if result['success'] else "❌ FAIL"
        duration = str(result['duration']).split('.')[0]  # Remove microseconds
        print(f"   {status} {task_name} ({duration})")
    
    # Final status
    if successful_tasks == total_tasks:
        print(f"\n🎉 All LAB8 tasks completed successfully!")
        print("Check the individual script outputs above for detailed results.")
    elif successful_tasks > 0:
        print(f"\n⚠️  {successful_tasks}/{total_tasks} tasks completed successfully.")
        print("Some tasks may have failed due to network issues or website changes.")
    else:
        print(f"\n❌ All tasks failed. Check network connection and website availability.")
    
    print(f"\n📁 Generated files in LAB8 directory:")
    for filename in os.listdir('.'):
        if filename.endswith(('.pkl', '.json')) and 'session' in filename:
            print(f"   📄 {filename}")
    
    print(f"\n💡 Tips:")
    print("   • Run individual tasks with: python task1_basic_login.py")
    print("   • Check requirements.txt for dependencies")
    print("   • Some failures may be due to website anti-bot measures")
    
    return successful_tasks == total_tasks


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 