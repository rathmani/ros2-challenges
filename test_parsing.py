import unittest

def parse_command(cmd):
    parts = cmd.strip().lower().split()
    result = {'linear': 0.0, 'angular': 0.0}
    if len(parts) == 2 and parts[0] == 'avance':
        result['linear'] = float(parts[1])
    elif len(parts) == 2 and parts[0] == 'recule':
        result['linear'] = -float(parts[1])
    elif len(parts) == 2 and parts[0] == 'tourne_gauche':
        result['angular'] = float(parts[1])
    elif len(parts) == 2 and parts[0] == 'tourne_droite':
        result['angular'] = -float(parts[1])
    elif parts[0] == 'stop':
        pass
    return result

class TestParsing(unittest.TestCase):
    def test_avance(self):
        r = parse_command('avance 2')
        self.assertEqual(r['linear'], 2.0)

    def test_recule(self):
        r = parse_command('recule 1.5')
        self.assertEqual(r['linear'], -1.5)

    def test_tourne_gauche(self):
        r = parse_command('tourne_gauche 0.5')
        self.assertEqual(r['angular'], 0.5)

    def test_tourne_droite(self):
        r = parse_command('tourne_droite 1')
        self.assertEqual(r['angular'], -1.0)

    def test_stop(self):
        r = parse_command('stop')
        self.assertEqual(r['linear'], 0.0)
        self.assertEqual(r['angular'], 0.0)

if __name__ == '__main__':
    unittest.main()
