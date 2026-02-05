import os
import subprocess
import sys

def run_command(command, ignore_errors=False):
    """Run a shell command and print output."""
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        if not ignore_errors:
            print(f"[ERROR] Command failed: {command}")
            print(e.stderr)
            return None
        return e.stderr

def main():
    print("---------------------------------------------------")
    print("🦄 Unicorn Signal: GitHub Deploy Helper")
    print("---------------------------------------------------")

    # 1. Check Git Installation
    print("[1/6] Checking Git...")
    git_version = run_command("git --version")
    if not git_version:
        print("Git is not installed. Please install it from https://git-scm.com/download/win")
        input("Press Enter to exit...")
        return

    # 2. Check & Configure Identity
    print("[2/6] Configuring Identity...")
    user_email = run_command("git config user.email", ignore_errors=True)
    
    if not user_email:
        print("\n[SETUP] GitHub identity not found. Let's set it up.")
        email = input("Enter your GitHub Email: ").strip()
        name = input("Enter your Name (or Nickname): ").strip()
        
        if email and name:
            run_command(f'git config user.email "{email}"')
            run_command(f'git config user.name "{name}"')
            print("[SETUP] Identity saved!")
        else:
            print("[ERROR] Email and Name are required.")
            input("Press Enter to exit...")
            return
    else:
        print(f"Identity confirmed: {user_email}")

    # 3. Initialize & Add
    print("[3/6] Initializing Repository...")
    if not os.path.exists(".git"):
        run_command("git init")
    else:
        print("Git repository already initialized.")
        
    run_command("git add .")

    # 4. Commit
    print("[4/6] Committing Changes...")
    # Check if there are changes to commit
    status = run_command("git status --porcelain")
    if status:
        run_command('git commit -m "Unicorn Signal v1.0 Release"')
    else:
        print("No changes to commit. Proceeding...")

    # 5. Remote Interaction
    print("[5/6] Configuration Remote...")
    run_command("git branch -M main")
    
    # Remove existing origin just in case to start fresh or set-url
    run_command("git remote remove origin", ignore_errors=True)
    
    repo_url = "https://github.com/thinkingkorean-jpg/Unicorn-Signal.git"
    run_command(f"git remote add origin {repo_url}")

    # 6. Push
    print("[6/6] Pushing to GitHub...")
    print("\n[IMPORTANT] A browser window or login box might pop up.")
    print("Please sign in with your GitHub account if prompted.\n")
    
    push_result = run_command("git push -u origin main")
    
    if push_result is not None:
        print("\n---------------------------------------------------")
        print("🎉 SUCCESS! Uploaded to GitHub.")
        print(f"🔗 URL: {repo_url}")
        print("---------------------------------------------------")
    else:
        print("\n[FAIL] Push failed. Read the error message above.")

    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
