import credGUI
import configGUI

print("""
Hasty v.1.1.1
Authour: Ian Pringle, Joseph Langford, and Colbert Maloy

Initializing...
""")

try:
    import cred

except ModuleNotFoundError:
    credGUI.main()

try:
    import configQN0
    import configQN1
    import configQN2
    import configQN3
    import configQN4

except ModuleNotFoundError:
    configGUI.main()

finally:
    import wxGUI
    wxGUI()
