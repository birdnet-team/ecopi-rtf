import yaml

class Strings:
    def __init__(self, locale):
        self.locale = locale
        with open('assets/strings.yaml', 'r') as file:
            self.strings = yaml.safe_load(file)

    def get(self, key):
        return self.strings.get(key, {}).get(self.locale, self.strings.get(key, {}).get('en', ''))

# Usage example:
# strings = Strings(locale)
# welcome_message = strings.get('welcome_message')