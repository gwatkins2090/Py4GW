# Contributing to Py4GW

Thank you for your interest in contributing to Py4GW! This document provides guidelines and instructions for contributing to the project.

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Submitting Changes](#submitting-changes)
- [Bot Script Contributions](#bot-script-contributions)
- [Widget Contributions](#widget-contributions)
- [Documentation Contributions](#documentation-contributions)
- [Reporting Bugs](#reporting-bugs)
- [Feature Requests](#feature-requests)
- [Community Guidelines](#community-guidelines)

---

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive environment for all contributors, regardless of experience level, background, or identity.

### Expected Behavior

- **Be respectful** and considerate in all interactions
- **Be collaborative** and help others learn
- **Be constructive** with feedback and criticism
- **Be patient** with questions and new contributors
- **Be professional** in all communications

### Unacceptable Behavior

- Harassment, discrimination, or hate speech
- Personal attacks or trolling
- Sharing others' private information without permission
- Any conduct that violates Guild Wars Terms of Service
- Malicious code or intentionally harmful contributions

---

## Getting Started

### Prerequisites

Before contributing, ensure you have:

1. **Python 3.13.0 (32-bit)** installed
2. **Guild Wars client** for testing
3. **Git** for version control
4. **GitHub account** for submitting contributions
5. Basic understanding of Python programming

### Fork and Clone

1. **Fork** the repository on GitHub
2. **Clone** your fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/Py4GW.git
   cd Py4GW
   ```
3. **Add upstream** remote:
   ```bash
   git remote add upstream https://github.com/apoguita/Py4GW.git
   ```

### Stay Updated

Keep your fork synchronized with upstream:
```bash
git fetch upstream
git checkout main
git merge upstream/main
```

---

## How to Contribute

### Contribution Types

We welcome various types of contributions:

1. **Bug Fixes** - Fix issues reported in GitHub Issues
2. **New Features** - Add new functionality to core library
3. **Bot Scripts** - Share your farming and automation bots
4. **Widgets** - Create new UI widgets
5. **Documentation** - Improve guides, tutorials, and API docs
6. **Tests** - Add test coverage
7. **Optimization** - Performance improvements
8. **Examples** - Add demo scripts and tutorials

### Contribution Process

1. **Check existing issues** - Look for related work
2. **Create an issue** - Discuss your idea first (for large changes)
3. **Create a branch** - Use a descriptive name
4. **Make changes** - Follow coding standards
5. **Test thoroughly** - Ensure everything works
6. **Submit PR** - Provide clear description
7. **Address feedback** - Respond to review comments
8. **Merge** - Maintainers will merge when ready

---

## Development Setup

### Setting Up Development Environment

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/Py4GW.git
   cd Py4GW
   ```

2. **Install development dependencies** (if any):
   ```bash
   # Currently no external dependencies required
   # All dependencies bundled in DLLs
   ```

3. **Verify setup:**
   ```bash
   # Run a demo script
   python DEMO/DEMO_PyAgent.py
   ```

### Development Tools

**Recommended:**
- **IDE:** PyCharm, VS Code with Python extension
- **Type hints:** Use `stubs/` directory for autocomplete
- **Debugging:** Python debugger (pdb, IDE debugger)
- **Git GUI:** GitKraken, SourceTree, or command line

### Project Structure

```
Py4GW/
├── Py4GWCoreLib/         # Core library (don't modify without discussion)
├── Bots/                 # Bot scripts (add your bots here)
├── Widgets/              # UI widgets (add your widgets here)
├── DEMO/                 # Example scripts
├── Config/               # Configuration files
├── docs/                 # Documentation
└── tests/                # Test scripts
```

---

## Coding Standards

### Python Style Guide

Follow **PEP 8** style guidelines with these specifics:

#### Indentation and Formatting
```python
# Use 4 spaces for indentation (no tabs)
def my_function(param1, param2):
    if condition:
        do_something()
    return result
```

#### Naming Conventions
```python
# Classes: PascalCase
class MyBot:
    pass

# Functions/methods: snake_case
def calculate_distance():
    pass

# Constants: UPPER_SNAKE_CASE
MAX_COMBAT_RANGE = 1200

# Variables: snake_case
player_position = Vector3(0, 0, 0)

# Private members: _leading_underscore
def _internal_method(self):
    pass
```

#### Imports
```python
# Standard library first
import time
import threading

# Third-party libraries
import PyImGui

# Local imports
from Py4GWCoreLib import Py4GW
from Py4GWCoreLib.Botting import Bot
from Py4GWCoreLib.classes import Vector3
```

#### Documentation
```python
def calculate_distance(pos1, pos2):
    """
    Calculate distance between two positions.

    Args:
        pos1 (Vector3): First position
        pos2 (Vector3): Second position

    Returns:
        float: Distance between positions

    Example:
        >>> distance = calculate_distance(Vector3(0, 0, 0), Vector3(100, 100, 0))
        >>> print(distance)
        141.42
    """
    return pos1.distance_to(pos2)
```

#### Comments
```python
# Good: Explain why, not what
# Wait for skill recharge to avoid wasting energy
if Py4GW.Skillbar.IsSkillReady(slot):
    Py4GW.Skillbar.UseSkill(slot, target_id)

# Bad: Obvious comment
# Use skill
Py4GW.Skillbar.UseSkill(slot, target_id)
```

### Code Quality

#### Error Handling
```python
# Good: Check return values
agent_id = Py4GW.Player.GetTargetID()
if agent_id > 0:
    agent = Py4GW.Agent.GetAgentByID(agent_id)
    if agent and agent.IsAlive():
        Py4GW.Player.Attack(agent_id)

# Good: Use try-except for critical operations
try:
    item = Py4GW.Inventory.GetItemBySlot(1, 0)
    Py4GW.Inventory.UseItem(item.GetItemID())
except Exception as e:
    print(f"Error using item: {e}")
```

#### Performance
```python
# Good: Cache frequently accessed data
player_pos = Py4GW.Player.GetPosition()
for agent in agents:
    distance = player_pos.distance_to(agent.GetPosition())

# Bad: Repeated expensive calls
for agent in agents:
    distance = Py4GW.Player.GetPosition().distance_to(agent.GetPosition())
```

#### Type Hints (Recommended)
```python
from typing import List, Optional
from Py4GWCoreLib.classes import Vector3

def find_closest_enemy(position: Vector3, max_range: float) -> Optional[int]:
    """Find closest enemy within range."""
    # Implementation
    pass
```

---

## Submitting Changes

### Branch Naming

Use descriptive branch names:
```
feature/add-vanquish-bot
bugfix/fix-inventory-crash
docs/improve-api-reference
widget/add-quest-tracker
```

### Commit Messages

Write clear, descriptive commit messages:

```
Good:
- Add farming bot for Chahbek Village
- Fix crash when inventory is full
- Improve pathfinding performance by 30%
- Update API documentation for Player module

Bad:
- update
- fix bug
- changes
- asdf
```

**Format:**
```
Short summary (50 chars or less)

Detailed explanation if needed. Wrap at 72 characters.

- Bullet points for multiple changes
- Reference issues: Fixes #123
```

### Pull Request Process

1. **Create a pull request** from your fork
2. **Fill out PR template** with:
   - Description of changes
   - Related issues
   - Testing performed
   - Screenshots (for UI changes)
3. **Ensure CI passes** (if configured)
4. **Address review feedback**
5. **Wait for approval** from maintainers

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Bot script
- [ ] Widget
- [ ] Documentation
- [ ] Performance improvement

## Related Issues
Fixes #123

## Testing
- [ ] Tested in Guild Wars
- [ ] No errors in console
- [ ] Works with existing features

## Screenshots (if applicable)

## Checklist
- [ ] Code follows project style guidelines
- [ ] Comments added for complex logic
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
```

---

## Bot Script Contributions

### Bot Guidelines

1. **Functionality:**
   - Bot should work reliably
   - Handle errors gracefully
   - Include restart logic on failure

2. **Configuration:**
   - Make parameters configurable
   - Document configuration options
   - Provide sensible defaults

3. **Documentation:**
   - Add header comment explaining purpose
   - Document setup requirements
   - List required skills/builds

### Bot Template

```python
"""
Bot Name: Chahbek Village Farmer
Author: YourName
Description: Farms Chahbek Village for drops and gold
Version: 1.0

Requirements:
- Level 20 character
- Recommended build: Earth Elementalist
- Starting location: Kamadan, Jewel of Istan

Configuration:
- combat_range: Range to engage enemies (default: 1200)
- run_count: Number of runs (default: 0 = infinite)
"""

from Py4GWCoreLib.Botting import Bot
from Py4GWCoreLib.classes import Vector3

# Configuration
FARM_LOCATION = Vector3(-15000, 20000, 0)
RETURN_LOCATION = Vector3(-14000, 19000, 0)
COMBAT_RANGE = 1200

class ChabbekFarmer(Bot):
    def __init__(self):
        super().__init__("ChabbekFarmer")

        # Bot configuration
        self.enabled_combat = True
        self.combat_range = COMBAT_RANGE
        self.enabled_loot = True
        self.run_count = 0
        self.runs_completed = 0

    def main_loop(self):
        """Main farming loop"""
        self.log(f"Starting run {self.runs_completed + 1}")

        # Move to farm location
        self.move_to(FARM_LOCATION.x, FARM_LOCATION.y)

        # Clear enemies
        self.kill_all_in_range(self.combat_range)

        # Loot
        self.pickup_loot()

        # Return
        self.move_to(RETURN_LOCATION.x, RETURN_LOCATION.y)

        self.runs_completed += 1

        # Check if done
        if self.run_count > 0 and self.runs_completed >= self.run_count:
            self.log("Completed all runs!")
            self.stop()

    def on_death(self):
        """Handle death"""
        self.log("Died! Resigning and restarting...")
        self.resign()
        self.wait(5.0)

if __name__ == "__main__":
    bot = ChabbekFarmer()
    bot.run()
```

### Submitting Bots

1. **Place bot** in appropriate `Bots/` subdirectory
2. **Name file** descriptively: `chahbek_village_farmer.py`
3. **Test thoroughly** before submitting
4. **Document requirements** in header comment
5. **Submit PR** with description and demo video (optional)

---

## Widget Contributions

### Widget Guidelines

1. **Functionality:**
   - Widget should be useful and non-redundant
   - Handle errors gracefully
   - Minimal performance impact

2. **UI Design:**
   - Clean, intuitive interface
   - Consistent with other widgets
   - Configurable appearance

3. **Configuration:**
   - Save settings to `Py4GW.ini`
   - Provide configuration panel
   - Document all options

### Widget Template

```python
"""
Widget Name: Quest Tracker
Author: YourName
Description: Tracks active quests and displays progress
Version: 1.0
"""

import PyImGui
from Py4GWCoreLib import Py4GW

MODULE_NAME = "QuestTracker"

# Widget state
window_open = True
show_completed = False
font_size = 14

def main():
    """Main render function - called every frame"""
    global window_open, show_completed

    if not window_open:
        return

    window_open = PyImGui.begin("Quest Tracker", window_open)

    if window_open:
        # Widget content here
        PyImGui.text("Active Quests:")

        # TODO: Add quest tracking logic

        PyImGui.separator()

        # Options
        show_completed = PyImGui.checkbox("Show Completed", show_completed)

    PyImGui.end()

def configure():
    """Configuration panel - optional"""
    global font_size

    PyImGui.text("Quest Tracker Configuration")
    font_size = PyImGui.slider_int("Font Size", font_size, 10, 20)

def on_load():
    """Called when widget loads - optional"""
    print("Quest Tracker loaded!")

def on_unload():
    """Called when widget unloads - optional"""
    print("Quest Tracker unloaded!")
```

### Submitting Widgets

1. **Place widget** in `Widgets/` directory
2. **Name file** descriptively: `Quest Tracker.py`
3. **Test thoroughly**
4. **Add configuration** to `Py4GW.ini`
5. **Submit PR** with screenshots

---

## Documentation Contributions

### Documentation Types

1. **API Documentation** - Document new functions/classes
2. **User Guides** - Tutorials and how-to guides
3. **Code Comments** - Explain complex logic
4. **README** - Project overview and quick start
5. **Examples** - Demo scripts and use cases

### Documentation Standards

- Use **Markdown** for documentation files
- Follow existing structure and formatting
- Include code examples
- Keep language clear and concise
- Proofread for grammar and spelling

### Where to Contribute

- `README.md` - Main project documentation
- `ARCHITECTURE.md` - Technical architecture
- `USER_GUIDE.md` - User tutorials and examples
- `API_REFERENCE.md` - API documentation
- `DEMO/` - Example scripts
- Code comments - Inline documentation

---

## Reporting Bugs

### Before Reporting

1. **Check existing issues** - May already be reported
2. **Verify it's a bug** - Not a feature or limitation
3. **Test with latest version** - May already be fixed
4. **Reproduce consistently** - Ensure it's not a fluke

### Bug Report Template

```markdown
**Description**
Clear description of the bug

**Steps to Reproduce**
1. Go to '...'
2. Click on '...'
3. Run script '...'
4. See error

**Expected Behavior**
What should happen

**Actual Behavior**
What actually happens

**Screenshots/Logs**
If applicable, add screenshots or error logs

**Environment**
- OS: Windows 10/11
- Python Version: 3.13.0 (32-bit)
- Py4GW Version: X.X.X
- Guild Wars Version: Current

**Additional Context**
Any other relevant information
```

### Submitting Bug Reports

1. Go to [GitHub Issues](https://github.com/apoguita/Py4GW/issues)
2. Click "New Issue"
3. Select "Bug Report" template
4. Fill out all sections
5. Submit

---

## Feature Requests

### Before Requesting

1. **Check existing requests** - May already be requested
2. **Consider scope** - Should fit project goals
3. **Think about implementation** - Is it feasible?

### Feature Request Template

```markdown
**Feature Description**
Clear description of the feature

**Use Case**
Why is this feature needed? What problem does it solve?

**Proposed Implementation**
How might this feature work?

**Alternatives Considered**
What other approaches have you thought about?

**Additional Context**
Screenshots, mockups, or examples
```

---

## Community Guidelines

### Getting Help

- **GitHub Issues** - For bugs and feature requests
- **GitHub Discussions** - For questions and general discussion
- **README** - For basic usage information
- **Documentation** - For detailed guides

### Helping Others

- Answer questions in Issues and Discussions
- Review pull requests
- Share your bots and widgets
- Write tutorials and guides
- Improve documentation

### Recognition

Contributors are recognized in:
- Git commit history
- Pull request acknowledgments
- Community spotlight (for significant contributions)
- Bot/widget author credits

---

## Review Process

### What We Look For

- **Code quality** - Clean, readable, maintainable
- **Functionality** - Works as intended
- **Testing** - Thoroughly tested
- **Documentation** - Well documented
- **Style** - Follows project conventions
- **No breaking changes** - Or clearly documented

### Review Timeline

- Small fixes: 1-3 days
- New features: 1-2 weeks
- Major changes: 2-4 weeks

### Addressing Feedback

- Respond to review comments promptly
- Make requested changes
- Ask questions if unclear
- Be open to suggestions

---

## License

By contributing to Py4GW, you agree that your contributions will be licensed under the same license as the project.

---

## Questions?

If you have questions about contributing:
- Check existing documentation
- Ask in GitHub Discussions
- Create an issue with the "question" label

---

## Thank You!

Thank you for contributing to Py4GW! Your contributions help make Guild Wars automation accessible and enjoyable for everyone. 🎮

**Happy coding!**

---

**Last Updated:** 2025-12-10
