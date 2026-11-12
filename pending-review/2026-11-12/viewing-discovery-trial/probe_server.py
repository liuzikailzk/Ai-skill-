from urllib.request import urlopen
import sys
with urlopen('http://127.0.0.1:8765/form',timeout=3) as response:
    text=response.read().decode()
    assert '资格材料' in text and '下一步' in text
    print('Server returned expected fixture fields; browser behavior not tested.')
sys.exit(int(sys.argv[1]) if len(sys.argv)>1 else 0)
