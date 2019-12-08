import unittest
from app import app, db
from app.models import User, List, Item

class UserModelCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_setting(self):
        u = User(username='susan')
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))

    def test_getting_lists(self):
        u1 = User(username='john', email='john@example.com')
        u2 = User(username='mary', email='mary@example.com')
        u3 = User(username='david', email='david@example.com')
        db.session.add_all([u1, u2, u3])

        li1 = List(listname='food', author=u1)
        li2 = List(listname='clothes', author=u2)
        li3 = List(listname='medicine', author=u3)
        li4 = List(listname='food', author=u2)
        db.session.add_all([li1, li2, li3, li4])
        db.session.commit()

        r1 = u1.get_lists()
        r2 = u2.get_lists()
        r3 = u3.get_lists()
        self.assertEqual(r1, [li1])
        self.assertEqual(r2, [li2, li4])
        self.assertEqual(r3, [li3])

    def test_getting_items(self):
        u1 = User(username='john', email='john@example.com')
        u2 = User(username='mary', email='mary@example.com')
        u3 = User(username='david', email='david@example.com')
        db.session.add_all([u1, u2, u3])

        li1 = List(listname='food', author=u1)
        li2 = List(listname='clothes', author=u2)
        li3 = List(listname='medicine', author=u3)
        li4 = List(listname='food', author=u1)
        db.session.add_all([li1, li2, li3, li4])
        db.session.commit()

        it1 = Item(itemname='milk', dir=li1)
        it2 = Item(itemname='bread', dir=li1)
        it3 = Item(itemname='trousers', dir=li2)
        it4 = Item(itemname='pills', dir=li3)
        db.session.add_all([it1, it2, it3, it4])
        db.session.commit()

        r1 = li1.get_items()
        r2 = li2.get_items()
        r3 = li3.get_items()
        r4 = li4.get_items()
        self.assertEqual(r1, [it1, it2])
        self.assertEqual(r2, [it3])
        self.assertEqual(r3, [it4])
        self.assertEqual(r4, [])

    """
    def test_creating_list(self):
        u1 = User(username='john', email='john@example.com')
        u2 = User(username='mary', email='mary@example.com')
        db.session.add_all([u1, u2])

        u1.create_list('first_list')
        u1.create_list('second_list')
        u2.create_list('first_list')
        db.session.commit()

        r1 = u1.get_lists()
        r2 = u2.get_lists()
        self.assertEqual(r1, [])
    """

if __name__ == '__main__':
    unittest.main(verbosity=2)