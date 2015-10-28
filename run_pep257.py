import sys
import os.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
__import__('pep257').main()
