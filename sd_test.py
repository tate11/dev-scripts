import unittest

from sd import process_input


class SudoDockerTestCase(unittest.TestCase):
    def test_empty(self):
        self.assertListEqual(
                process_input([]),
                [],
                'falla sin parametros'
        )

    def test_ps(self):
        self.assertListEqual(
                process_input(['./sd.py', 'ps']),
                ['sudo', 'docker', 'ps'],
                'falle en ps'
        )

    def test_inside(self):
        self.assertListEqual(
                process_input(['./sd.py', 'inside', 'jobiols/backup']),
                ['sudo', 'docker', 'run', '-it', '--rm', '--entrypoint=/bin/bash', 'jobiols/backup'],
                'falle en inside'
        )

    def test_inside_bad(self):
        self.assertListEqual(
                process_input(['./sd.py', 'inside']),
                [],
                'falle cuando no esta la imagen'
        )

if __name__ == '__main__':
    unittest.main()
