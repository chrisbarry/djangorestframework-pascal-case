from copy import deepcopy
from unittest import TestCase, mock

from django.conf import settings
from django.http import QueryDict
from django.utils.functional import lazy
from django.test.client import RequestFactory
from rest_framework.utils.serializer_helpers import ReturnDict

from djangorestframework_pascal_case.util import pascalize, underscoreize

settings.configure()

from djangorestframework_pascal_case.middleware import PascalCaseMiddleWare

class ImportTest(TestCase):
    def test_import_all(self):
        """
        A quick test that just imports everything, should crash in case any Django or DRF modules change
        """
        from djangorestframework_pascal_case import parser
        from djangorestframework_pascal_case import render
        from djangorestframework_pascal_case import settings
        from djangorestframework_pascal_case import middleware

        assert parser
        assert render
        assert settings
        assert middleware


class UnderscoreToPascalTestCase(TestCase):
    def test_under_to_pascal_keys(self):
        data = {
            "two_word": 1,
            "long_key_with_many_underscores": 2,
            "only_1_key": 3,
            "only_one_letter_a": 4,
            "b_only_one_letter": 5,
            "only_c_letter": 6,
            "mix_123123a_and_letters": 7,
            "mix_123123aa_and_letters_complex": 8,
            "no_underscore_before123": 9,
        }
        output = {
            "TwoWord": 1,
            "LongKeyWithManyUnderscores": 2,
            "Only1Key": 3,
            "OnlyOneLetterA": 4,
            "BOnlyOneLetter": 5,
            "OnlyCLetter": 6,
            "Mix123123aAndLetters": 7,
            "Mix123123aaAndLettersComplex": 8,
            "NoUnderscoreBefore123": 9,
        }
        self.assertEqual(pascalize(data), output)

    def test_tuples(self):
        data = {"multiple_values": (1, 2), "data": [1, 3, 4]}
        output = {"MultipleValues": [1, 2], "Data": [1, 3, 4]}
        self.assertEqual(pascalize(data), output)

    def test_pascal_to_under_input_untouched_for_sequence(self):
        data = [{"FirstInput": 1}, {"SecondInput": 2}]
        reference_input = deepcopy(data)
        pascalize(data)
        self.assertEqual(data, reference_input)

    def test_recursive_pascalize_with_ignored_fields_and_keys(self):
        ignore_fields = ("ignored_field", "NewKeyIgnoredField", "ignored_field_and_key", "IgnoredFieldAndKey2")
        ignore_keys = ("ignored_key", "NewKeyIgnoredKey", "ignored_field_and_key", "IgnoredFieldAndKey2")
        data = {
            "ignored_field": {"no_change_recursive": 1},
            "change_me": {"change_recursive": 2},
            "new_key_ignored_field": {"also_no_change": 3},
            "ignored_key": {"also_change_recursive": 4},
            "new_key_ignored_key": {"change_is_here_to_stay": 5},
            "ignored_field_and_key": {"no_change_here": 6},
            "ignored_field_and_key2": {"no_change_here_either": 7},
        }
        output = {
            "IgnoredField": {"no_change_recursive": 1},
            "ChangeMe": {"ChangeRecursive": 2},
            "NewKeyIgnoredField": {"also_no_change": 3},
            "ignored_key": {"AlsoChangeRecursive": 4},
            "new_key_ignored_key": {"ChangeIsHereToStay": 5},
            "ignored_field_and_key": {"no_change_here": 6},
            "ignored_field_and_key2": {"no_change_here_either": 7},
        }
        self.assertEqual(pascalize(data, ignore_fields=ignore_fields, ignore_keys=ignore_keys), output)


class PascalToUnderscoreTestCase(TestCase):
    """Tests for converting PascalCase to underscore_case (parsing incoming requests)."""
    def test_pascal_to_under_keys(self):
        data = {
            "TwoWord": 1,
            "LongKeyWithManyUnderscores": 2,
            "Only1Key": 3,
            "OnlyOneLetterA": 4,
            "BOnlyOneLetter": 5,
            "OnlyCLetter": 6,
            "Mix123123aAndLetters": 7,
            "Mix123123aaAndLettersComplex": 8,
            "WordWITHCaps": 9,
            "Key10": 10,
            "AnotherKey1": 11,
            "AnotherKey10": 12,
            "OptionS1": 13,
            "OptionS10": 14,
            "UPPERCASE": 15,
            "PascalCase": 16,
            "Pascal10Case": 17,
        }
        output = {
            "two_word": 1,
            "long_key_with_many_underscores": 2,
            "only_1_key": 3,
            "only_one_letter_a": 4,
            "b_only_one_letter": 5,
            "only_c_letter": 6,
            "mix_123123a_and_letters": 7,
            "mix_123123aa_and_letters_complex": 8,
            "word_with_caps": 9,
            "key_10": 10,
            "another_key_1": 11,
            "another_key_10": 12,
            "option_s_1": 13,
            "option_s_10": 14,
            "uppercase": 15,
            "pascal_case": 16,
            "pascal_10_case": 17,
        }
        self.assertEqual(underscoreize(data), output)

    def test_pascal_to_under_keys_with_no_underscore_before_number(self):
        data = {"NoUnderscoreBefore123": 1}
        output = {"no_underscore_before123": 1}
        options = {"no_underscore_before_number": True}
        self.assertEqual(underscoreize(data, **options), output)

    def test_under_to_pascal_input_untouched_for_sequence(self):
        data = [{"first_input": 1}, {"second_input": 2}]
        reference_input = deepcopy(data)
        underscoreize(data)
        self.assertEqual(data, reference_input)

    def test_recursive_underscoreize_with_ignored_fields_and_keys(self):
        ignore_fields = ("IgnoredField", "new_key_ignored_field", "IgnoredFieldAndKey", "ignored_field_and_key_2")
        ignore_keys = ("IgnoredKey", "new_key_ignored_key", "IgnoredFieldAndKey", "ignored_field_and_key_2")
        data = {
            "IgnoredField": {"NoChangeRecursive": 1},
            "ChangeMeField": {"ChangeRecursive": 2},
            "NewKeyIgnoredField": {"AlsoNoChange": 3},
            "IgnoredKey": {"ChangeRecursiveAgain": 4},
            "NewKeyIgnoredKey": {"ChangeIsHereToStay": 5},
            "IgnoredFieldAndKey": {"NoChangeHere": 6},
            "IgnoredFieldAndKey2": {"NoChangeHereEither": 7},
        }
        output = {
            "ignored_field": {"NoChangeRecursive": 1},
            "change_me_field": {"change_recursive": 2},
            "new_key_ignored_field": {"AlsoNoChange": 3},
            "IgnoredKey": {"change_recursive_again": 4},
            "NewKeyIgnoredKey": {"change_is_here_to_stay": 5},
            "IgnoredFieldAndKey": {"NoChangeHere": 6},
            "IgnoredFieldAndKey2": {"NoChangeHereEither": 7},
        }
        self.assertEqual(underscoreize(data, ignore_fields=ignore_fields, ignore_keys=ignore_keys), output)


class NonStringKeyTest(TestCase):
    def test_non_string_key(self):
        data = {1: "test"}
        self.assertEqual(underscoreize(pascalize(data)), data)


def return_string(text):
    return text


lazy_func = lazy(return_string, str)


class PromiseStringTest(TestCase):
    def test_promise_strings(self):
        data = {lazy_func("test_key"): lazy_func("test_value value")}
        pascalized = pascalize(data)
        self.assertEqual(pascalized, {"TestKey": "test_value value"})
        result = underscoreize(pascalized)
        self.assertEqual(result, {"test_key": "test_value value"})


class ReturnDictTest(TestCase):
    def test_return_dict(self):
        data = ReturnDict({"id": 3, "value": "val"}, serializer=object())
        pascalized = pascalize(data)
        # Keys should be PascalCase now
        self.assertEqual(pascalized, {"Id": 3, "Value": "val"})
        self.assertEqual(data.serializer, pascalized.serializer)


class NumberToPascalTestCase(TestCase):
    def test_dict_with_numbers_as_keys(self):
        data = {1: 'test', 'a': 'abc'}
        # Number keys stay as-is, string keys get PascalCased
        self.assertEqual(pascalize(data), {1: 'test', 'A': 'abc'})


class GeneratorAsInputTestCase(TestCase):
    def _underscore_generator(self):
        yield {"simple_is_better": "than complex"}
        yield {"that_is": "correct"}

    def _pascal_generator(self):
        yield {"SimpleIsBetter": "than complex"}
        yield {"ThatIs": "correct"}

    def test_pascalize_iterates_over_generator(self):
        data = self._underscore_generator()
        output = [{"SimpleIsBetter": "than complex"}, {"ThatIs": "correct"}]
        self.assertEqual(pascalize(data), output)

    def test_underscoreize_iterates_over_generator(self):
        data = self._pascal_generator()
        output = [{"simple_is_better": "than complex"}, {"that_is": "correct"}]
        self.assertEqual(underscoreize(data), output)


class PascalToUnderscoreQueryDictTestCase(TestCase):
    def test_pascal_to_under_keys(self):
        query_dict = QueryDict("TestList=1&TestList=2", mutable=True)
        data = {
            "TwoWord": 1,
            "LongKeyWithManyUnderscores": 2,
            "Only1Key": 3,
            "OnlyOneLetterA": 4,
            "BOnlyOneLetter": 5,
            "OnlyCLetter": 6,
            "Mix123123aAndLetters": 7,
            "Mix123123aaAndLettersComplex": 8,
            "WordWITHCaps": 9,
            "Key10": 10,
            "AnotherKey1": 11,
            "AnotherKey10": 12,
            "OptionS1": 13,
            "OptionS10": 14,
            "UPPERCASE": 15,
            "PascalCase": 16,
            "Pascal10Case": 17,
        }
        query_dict.update(data)

        output_query = QueryDict("test_list=1&test_list=2", mutable=True)

        output = {
            "two_word": 1,
            "long_key_with_many_underscores": 2,
            "only_1_key": 3,
            "only_one_letter_a": 4,
            "b_only_one_letter": 5,
            "only_c_letter": 6,
            "mix_123123a_and_letters": 7,
            "mix_123123aa_and_letters_complex": 8,
            "word_with_caps": 9,
            "key_10": 10,
            "another_key_1": 11,
            "another_key_10": 12,
            "option_s_1": 13,
            "option_s_10": 14,
            "uppercase": 15,
            "pascal_case": 16,
            "pascal_10_case": 17,
        }
        output_query.update(output)
        self.assertEqual(underscoreize(query_dict), output_query)


class PascalCaseMiddleWareTestCase(TestCase):
    def test_pascal_case_to_underscore_query_params(self):
        get_response_mock = mock.MagicMock()
        middleware = PascalCaseMiddleWare(get_response_mock)
        query_dict = QueryDict("TestList=1&TestList=2", mutable=True)
        data = {
            "TwoWord": "1",
            "LongKeyWithManyUnderscores": "2",
            "Only1Key": "3",
            "OnlyOneLetterA": "4",
            "BOnlyOneLetter": "5",
            "OnlyCLetter": "6",
            "Mix123123aAndLetters": "7",
            "Mix123123aaAndLettersComplex": "8",
            "WordWITHCaps": "9",
            "Key10": "10",
            "AnotherKey1": "11",
            "AnotherKey10": "12",
            "OptionS1": "13",
            "OptionS10": "14",
            "UPPERCASE": "15",
            "PascalCase": "16",
            "Pascal10Case": "17",
        }
        query_dict.update(data)

        output_query = QueryDict("test_list=1&test_list=2", mutable=True)

        output = {
            "two_word": "1",
            "long_key_with_many_underscores": "2",
            "only_1_key": "3",
            "only_one_letter_a": "4",
            "b_only_one_letter": "5",
            "only_c_letter": "6",
            "mix_123123a_and_letters": "7",
            "mix_123123aa_and_letters_complex": "8",
            "word_with_caps": "9",
            "key_10": "10",
            "another_key_1": "11",
            "another_key_10": "12",
            "option_s_1": "13",
            "option_s_10": "14",
            "uppercase": "15",
            "pascal_case": "16",
            "pascal_10_case": "17",
        }
        output_query.update(output)
        request = RequestFactory().get("/", query_dict)

        middleware(request)
        (args, kwargs) = get_response_mock.call_args
        self.assertEqual(args[0].GET, output_query)
