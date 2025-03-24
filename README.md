# SPIKE Prime Teaching Repository

The objective of this repository is to host a set of teaching sessions (example: motor_pair_session.md, etc.) for kids to follow and learn from. As kids go through each session, they can check-in their own code in this repository if desired. We will keep all code organized by team-name/student-name/session-name. So, a student named John in team Kiwis will commit his files into kiwis/john/motor-pair-session folder.

## Repository Structure

```
fll-koala-kiwis/
├── session-plans/         # Teaching session materials
│   ├── motor_pair_session.md
│   └── ...
├── kiwis/                 # Team Kiwis
│   ├── john/              # Student folders
│   │   ├── motor-pair-session/
│   │   │   ├── my_program.py
│   │   │   └── ...
│   └── ...
├── koalas/                # Team Koalas
│   └── ...
├── docs/                  # Documentation files
│   └── spike_prime_api_doc.md  # Complete API documentation
└── README.md              # This file
```

## Git Setup Instructions (Windows)

### Step 1: Install Git

1. Download Git from [git-scm.com](https://git-scm.com/download/win)
2. Run the installer with default settings (you can customize if you know what you're doing)
3. Open the Start menu and search for "Git Bash"
4. Open Git Bash - this will be your terminal for Git commands

### Step 2: Configure Git

In the Git Bash terminal, set up your identity:

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### Step 3: Clone the Repository

1. Create a folder where you want to store the project (e.g., on your Desktop or Documents folder)
2. In Git Bash, navigate to that folder using the `cd` command:

```bash
cd "C:/Users/YourUsername/Documents"
```

3. Clone the repository:

```bash
git clone https://github.com/js15-gh/fll-koala-kiwis.git
```

4. Navigate into the project folder:

```bash
cd fll-koala-kiwis
```

### Step 4: Create Your Student Folder Structure

Follow this structure for organizing your work:

1. Create your team and personal folders (replace "kiwis" and "john" with your team and name):

```bash
mkdir -p kiwis/john/motor-pair-session
```

2. Now you can add your Python files inside this folder structure

### Step 5: Commit and Push Your Changes

After creating or modifying files:

1. Check what files have been changed:

```bash
git status
```

2. Add your files to the staging area:

```bash
git add kiwis/john/motor-pair-session/my_program.py
```

3. Commit your changes:

```bash
git commit -m "Add my motor pair session program"
```

4. Push your changes to the remote repository:

```bash
git pull  # Always pull first to get latest changes
git push  # Push your changes
```

If this is your first time pushing, you might need to set up authentication with GitHub.

### Troubleshooting

- If you get authentication errors, you may need to use a GitHub personal access token
- If you're having trouble with Git commands, ask your instructor for help

## SPIKE Prime API Quick Reference

> **Note:** The complete SPIKE Prime API documentation is available in the `docs/spike_prime_api_doc.md` file. This section provides a brief overview of the most commonly used functions.

### Python Basics

Python is a popular text-based coding language that is excellent for beginners because it's concise and easy-to-read. With SPIKE Prime, you'll be using MicroPython, which is a lightweight version optimized for microcontrollers with limited memory.

#### Python Syntax

In Python:
- Each statement begins with indentation and ends with a line break
- Indentation (spaces before a statement) defines code blocks
- The SPIKE App uses 4 spaces for each indentation level

Example:
```python
# This is a comment
print('LEGO')
if True:
    print(123)  # Notice the indentation
```

### Key SPIKE Prime Modules

- `motor` - For controlling individual motors
- `motor_pair` - For controlling paired motors
- `hub` - For accessing hub features (display, buttons, ports)
- `runloop` - For async/await functionality
- `color_sensor` - For color sensor functions
- `distance_sensor` - For distance sensor functions
- `force_sensor` - For force sensor functions

### Common Program Structure

```python
import motor_pair
from hub import port
import runloop

# Setup code here
motor_pair.pair(motor_pair.PAIR_1, port.C, port.D)

async def main():
    # Your program here
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 360, 0, velocity=300)
    
# Start the program
runloop.run(main())
```

### Essential Motor Pair Functions

```python
# Pair motors on ports C and D
motor_pair.pair(motor_pair.PAIR_1, port.C, port.D)

# Move straight
motor_pair.move(motor_pair.PAIR_1, 0, velocity=300)

# Move for a specific distance
await motor_pair.move_for_degrees(motor_pair.PAIR_1, 360, 0, velocity=300)

# Tank steering
motor_pair.move_tank(motor_pair.PAIR_1, 300, -300)

# Tank steering for a specific amount
await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, 360, 100, -100)

# Stop motors
motor_pair.stop(motor_pair.PAIR_1)
```

For a complete list of all SPIKE Prime modules, functions, and parameters, please refer to the detailed API documentation in `docs/spike_prime_api_doc.md`. 