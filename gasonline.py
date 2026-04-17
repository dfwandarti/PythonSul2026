import re
from typing import Optional
from playwright.sync_api import FloatRect, Playwright, sync_playwright, expect
from playwright._impl._locator import Locator


def check_visibility(input_element: Locator) -> bool:
    bouding_box: Optional[FloatRect] = input_element.bounding_box()
    print(f"Bounding box: {bouding_box}")

    return (  
        bouding_box is not None
        and bouding_box["width"] > 0
        and bouding_box["height"] > 0
        and bouding_box["x"] >= 0
        and bouding_box["y"] >= 0
    )


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://gasonline.galp.com/")
    page.get_by_role("button", name="Aceitar").click()

    # ---------------------
    count_input: int = page.locator("input").count()
    print(f"Número de inputs encontrados: {count_input}")
    all_inputs: list = page.locator("input").all()
    for index, input_element in enumerate(all_inputs):
        input_visibility: bool = input_element.is_visible()
        input_enabled: bool = input_element.is_enabled()
        input_hidden: bool = input_element.is_hidden()
        input_seams_visibile: bool = check_visibility(input_element)

        print(f"Input {index + 1}: visible {input_visibility}, enabled {input_enabled}, hidden {input_hidden}, seems visible {input_seams_visibile}")

        if input_visibility and not input_hidden and input_enabled and input_seams_visibile:
            print(f"Clicando no input {index + 1}")
            input_element.highlight()
            input_element.click()

    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
