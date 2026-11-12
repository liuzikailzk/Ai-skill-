from playwright.sync_api import sync_playwright
import json
from pathlib import Path
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium')
 page=browser.new_page(viewport={'width':1100,'height':750})
 page.goto('http://127.0.0.1:8765/');page.wait_for_load_state('networkidle')
 Path('rendered.html').write_text(page.content())
 page.screenshot(path='webapp-initial.png',full_page=True)
 print(json.dumps({'title':page.title(),'buttons':page.get_by_role('button').all_text_contents(),'checkboxes':page.get_by_role('checkbox').count(),'labels':page.locator('label').all_text_contents(),'browser':browser.version},ensure_ascii=False))
 browser.close()
