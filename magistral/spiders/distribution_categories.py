import os
import inspect

class DistributionCategories:
    currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    open_file = open(currentdir + '\settings_categories.txt', encoding='utf-8')
    description_distribution = open_file.read()

    def build_dictionary_categorise(self):
        string = self.description_distribution
        block_values = string.split(",")
        key_for_categories = dict()
        for elem in block_values:
            split_elem_on_key_and_value = elem.split(':')
            if len(split_elem_on_key_and_value) > 1:
                value_for_key = split_elem_on_key_and_value[1].split('.')
                key_for_categories[split_elem_on_key_and_value[0]] = value_for_key
        return key_for_categories

    def distribution(self, description):
        key_for_categories = self.build_dictionary_categorise()
        for category, arr_key in key_for_categories.items():
            for key in arr_key:
                if key in description.lower():
                    return category
        return None