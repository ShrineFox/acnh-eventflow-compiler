import unittest

from funcparserlib.lexer import Token, LexerError
from parse import tokenize

class TestTokenize(unittest.TestCase):
    def test_indent_dedent_simple(self):
        tokens = list(tokenize('\n \n'))
        token_types = [t.type for t in tokens]
        self.assertEqual(token_types, ['NL', 'INDENT', 'NL', 'DEDENT'])

    def test_multiple_dedent(self):
        tokens = list(tokenize('\n \n  \n   \n    \n  \n'))
        token_types = [t.type for t in tokens]
        expected = [
                'NL', 'INDENT', 'NL', 'INDENT', 'NL', 'INDENT',
                'NL', 'INDENT', 'NL', 'DEDENT', 'DEDENT', 'NL',
                'DEDENT', 'DEDENT'
        ]
        self.assertEqual(token_types, expected)

    def test_bad_indent(self):
        with self.assertRaises(LexerError):
            list(tokenize('\n\t\n \t'))

    def test_bad_dedent(self):
        with self.assertRaises(LexerError):
            list(tokenize('\n\t\n\t \n '))

    def test_paren_mismatch1(self):
        with self.assertRaises(LexerError):
            list(tokenize('(]'))

    def test_paren_mismatch2(self):
        with self.assertRaises(LexerError):
            list(tokenize('[)'))

    def test_paren_mismatch_nested1(self):
        with self.assertRaises(LexerError):
            list(tokenize('[(([])])'))

    def test_paren_mismatch_nested2(self):
        with self.assertRaises(LexerError):
            list(tokenize('([[()])]'))

    def test_paren_unopened1(self):
        with self.assertRaises(LexerError):
            list(tokenize(')'))

    def test_paren_unopened2(self):
        with self.assertRaises(LexerError):
            list(tokenize(']'))

    def test_paren_unclosed1(self):
        with self.assertRaises(LexerError):
            list(tokenize('('))

    def test_paren_unclosed2(self):
        with self.assertRaises(LexerError):
            list(tokenize('['))

    def test_id(self):
        with self.assertRaises(LexerError):
            next(tokenize('-abc'))
        with self.assertRaises(LexerError):
            next(tokenize('_abc'))
        with self.assertRaises(LexerError):
            list(tokenize('abc-'))
        with self.assertRaises(LexerError):
            list(tokenize('abc_'))
        self.assertEqual(list(tokenize('abc_d0-3')), [
            Token('ID', 'abc_d0-3'),
            Token('NL', '')
        ])
        self.assertEqual(list(tokenize('0ab34')), [
            Token('ID', '0ab34'),
            Token('NL', '')
        ])
        self.assertEqual(list(tokenize('013-34')), [
            Token('ID', '013-34'),
            Token('NL', '')
        ])
        self.assertNotEqual(list(tokenize('01334')), [
            Token('ID', '01334'),
            Token('NL', '')
        ])
        self.assertEqual(list(tokenize('01-a')), [
            Token('ID', '01-a'),
            Token('NL', '')
        ])
        self.assertEqual(list(tokenize('01A_B_C')), [
            Token('ID', '01A_B_C'),
            Token('NL', '')
        ])
        with self.assertRaises(LexerError):
            list(tokenize('01-'))

    def test_example(self):
        src = ''' \
            flow Test(a: int = 5, b: float = 3.0): # comment
                if SubflowResults[+5] in (1, 2):
                    System.EventFlags['a'] = 3
                else:
                    fork:
                        branch0:
                            System.EventFlags["b"] = 7
                        branch1:
                            System.EventFlags["c"] = 7
                        branch2:
                            pass'''
        expected = [
            'FLOW', 'ID', 'LPAREN', 'ID', 'COLON', 'TYPE', 'ASSIGN',
                'INT', 'COMMA', 'ID', 'COLON', 'TYPE', 'ASSIGN', 'FLOAT',
                'RPAREN', 'COLON', 'NL',
            'INDENT', 'IF', 'ID', 'LSQUARE', 'INT', 'RSQUARE', 'IN',
                'LPAREN', 'INT', 'COMMA', 'INT', 'RPAREN', 'COLON', 'NL',
            'INDENT', 'ID', 'DOT', 'ID', 'LSQUARE', 'STRING', 'RSQUARE',
                'ASSIGN', 'INT', 'NL',
            'DEDENT', 'ELSE', 'COLON', 'NL',
            'INDENT', 'FORK', 'COLON', 'NL',
            'INDENT', 'BRANCH', 'COLON', 'NL',
            'INDENT', 'ID', 'DOT', 'ID', 'LSQUARE', 'STRING', 'RSQUARE',
                'ASSIGN', 'INT', 'NL',
            'DEDENT', 'BRANCH', 'COLON', 'NL',
            'INDENT', 'ID', 'DOT', 'ID', 'LSQUARE', 'STRING', 'RSQUARE',
                'ASSIGN', 'INT', 'NL',
            'DEDENT', 'BRANCH', 'COLON', 'NL',
            'INDENT', 'PASS', 'NL',
            'DEDENT', 'DEDENT', 'DEDENT', 'DEDENT',
        ]

        tokens = list(tokenize(src))
        token_types = [t.type for t in tokens]
        self.assertEqual(token_types, expected)
