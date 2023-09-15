from playwright.sync_api import Page


class ModelPage(Page):
    def __init__(self, page: Page):
        self.page = page
    
    def model_function(self): ...