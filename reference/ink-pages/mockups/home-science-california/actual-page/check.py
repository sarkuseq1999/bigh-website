"""Inspect the built science section: tabs, all ages, labels, and transparent-layer coverage."""
from pathlib import Path
from io import BytesIO
import os
import sys
from PIL import Image, ImageChops
from playwright.sync_api import sync_playwright

HERE = Path(os.environ.get('SCIENCE_CAPTURE_DIR', str(Path(__file__).resolve().parent)))
HERE.mkdir(parents=True, exist_ok=True)
URL = os.environ.get('SCIENCE_PREVIEW_URL', 'http://localhost:3007')
TOPICS = ['Mitochondria', 'Free radicals', 'Aging cells']
EXPECTED = ['workshop-fuel-v2.webp', 'workshop-sparks-v1.webp', 'cell-middle-v3.webp']

def move_age(page, age):
    control = page.locator('#science input[type=range]')
    control.fill(str(age))
    page.wait_for_timeout(700)
    assert page.locator('#science label strong').inner_text() == str(age)

def record(page, name, width):
    assert not page.evaluate('document.documentElement.scrollWidth > innerWidth')
    page.screenshot(path=str(HERE / f'{width}-{name}.jpg'), type='jpeg', quality=90)

with sync_playwright() as p:
    browser = p.chromium.launch(args=['--use-gl=angle','--use-angle=d3d11','--enable-gpu','--ignore-gpu-blocklist'])
    for width, height in [(1440,1000),(390,844),(1024,768),(360,800)]:
        if len(sys.argv)>1 and str(width) not in sys.argv[1:]:
            continue
        context = browser.new_context(viewport={'width':width,'height':height},is_mobile=width<900,has_touch=width<900,device_scale_factor=1)
        page = context.new_page()
        errors=[]
        page.on('pageerror',lambda e:errors.append(str(e)))
        response=page.goto(URL,wait_until='networkidle')
        assert response.status == 200
        page.evaluate('document.fonts.ready')
        page.locator('#science-title').evaluate('(e)=>scrollTo(0,scrollY+e.getBoundingClientRect().top-110)')
        page.wait_for_timeout(3400)
        record(page,'opening',width)
        for i,topic in enumerate(TOPICS):
            page.locator('#science button').filter(has_text=topic).first.click()
            page.wait_for_timeout(350)
            record(page,f'topic-{i}-moving',width)
            page.wait_for_timeout(3400)
            if width<900:
                page.locator('#science [role=tablist]').evaluate('(e)=>scrollTo(0,scrollY+e.getBoundingClientRect().top-100)')
                page.wait_for_timeout(300)
                figure=page.locator(f'#ink-topic-panel-{i} figure')
                assert page.locator(f'#ink-topic-{i}').get_attribute('aria-selected')=='true'
            else:
                figure=page.locator('#science figure')
                if page.locator('#science').get_attribute('data-story')=='true':
                    assert figure.get_attribute('data-topic') == str(i)
            art=figure.locator(f'img[src$="{EXPECTED[i]}"]')
            assert art.evaluate('(i)=>i.complete && i.naturalWidth===1448')
            label=figure.locator('figcaption').bounding_box()
            stage=figure.locator(':scope > div').first.bounding_box()
            assert label['y']+label['height'] <= stage['y'], (label,stage)
            record(page,f'topic-{i}',width)
            if width<900:
                page.locator('#science').screenshot(path=str(HERE/f'{width}-topic-{i}-section.jpg'),type='jpeg',quality=90)
            if i==2:
                for age in [30,42,43,67,68,80,45]:
                    move_age(page,age)
                    name='young' if age<43 else 'middle' if age<68 else 'old'
                    top=figure.locator(f'img[src$="cell-{name}-v3.webp"]')
                    assert top.evaluate('(i)=>+getComputedStyle(i).opacity')==1
                    if age in [30,45,80]:
                        record(page,f'age-{age}',width)
                    if age==80:
                        layer=top.locator('..')
                        actual=layer.screenshot()
                        younger=layer.locator('img:not([src$="cell-old-v3.webp"])')
                        younger.evaluate_all('(images)=>images.forEach(i=>i.style.visibility="hidden")')
                        solo=layer.screenshot()
                        younger.evaluate_all('(images)=>images.forEach(i=>i.style.removeProperty("visibility"))')
                        # Pixel comparison: the settled older cell must equal that cell alone,
                        # within one 8-bit channel step of GPU multiply/compositing rounding.
                        difference=ImageChops.difference(Image.open(BytesIO(actual)).convert('RGB'),Image.open(BytesIO(solo)).convert('RGB'))
                        max_delta=max(high for low,high in difference.getextrema())
                        if max_delta>1:
                            (HERE/f'{width}-cell-stack.png').write_bytes(actual)
                            (HERE/f'{width}-cell-solo.png').write_bytes(solo)
                            difference.save(HERE/f'{width}-cell-difference.png')
                            print(f'{width}px cell comparison: {difference.getbbox()}, extrema={difference.getextrema()}',flush=True)
                        assert max_delta<=1, 'Younger cells leak through the older painting'
        assert not errors, errors
        print(f'{width}px: 3 topics; 7 age positions; labels clear; older cell equals solo image; no overflow or page errors',flush=True)
        context.close()
    browser.close()
