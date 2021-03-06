from django.test import TestCase
from django.core.urlresolvers import reverse 
from utils.factories import UserFactory
from contacts import factories
from contacts import models

class ContactModelTests(TestCase):

    def setUp(self):
        self.book = factories.BookFactory.create()
        self.contact = factories.ContactFactory.create(
            name="Philip James",
            book=self.book,
        )

    def test_contact_name(self):
        """String repr of contact should be name."""

        self.assertEqual(self.contact.name, str(self.contact))

    def test_contact_url(self):
        expected_url = reverse('contacts-view', kwargs={'pk': self.contact.id})
        self.assertEqual(self.contact.get_absolute_url(), expected_url)

    def test_contact_last_contacted(self):
        log = factories.LogFactory.create(contact=self.contact)

        self.assertEqual(self.contact.last_contacted(), log.created)

    def test_contact_can_be_viewed_by(self):
        bookowner = factories.BookOwnerFactory.create(book=self.book)
        user = bookowner.user
        self.assertTrue(self.contact.can_be_viewed_by(user))

    def test_contact_can_be_edited_by(self):
        bookowner = factories.BookOwnerFactory.create(book=self.book)
        user = bookowner.user
        self.assertTrue(self.contact.can_be_edited_by(user))

    def test_get_contacts_for_user(self):
        bookowner = factories.BookOwnerFactory.create(book=self.book)
        user = bookowner.user
        self.assertEqual(
            [self.contact],
            list(models.Contact.objects.get_contacts_for_user(user)),
        )

    def test_get_contacts_for_user_bad_user(self):
        user = UserFactory.create(username="nicholle")
        self.assertFalse(
            list(models.Contact.objects.get_contacts_for_user(user)),
        )


class TagModelTests(TestCase):

    def setUp(self):
        self.book = factories.BookFactory.create()
        self.contact = factories.ContactFactory.create(
            name="Philip James",
            book=self.book,
        )
        self.tag = factories.TagFactory.create(
            tag='Family',
            book=self.book,
        )

    def test_tag_name(self):
        self.assertEqual(self.tag.tag, str(self.tag))

    def test_get_tags_for_user(self):
        bookowner = factories.BookOwnerFactory.create(book=self.book)
        user = bookowner.user
        self.assertEqual(
            [self.tag],
            list(models.Tag.objects.get_tags_for_user(user)),
        )


class BookModelTests(TestCase):

    def test_book_name(self):
        book = factories.BookFactory.create(name="James Family")
        self.assertEqual(book.name, str(book))


class BookOwnerModelTests(TestCase):

    def setUp(self):
        self.book = factories.BookFactory.create(name="James Family")
        self.user = UserFactory(username="phildini")

    def test_book_owner_repr(self):
        bookowner = factories.BookOwnerFactory(book=self.book, user=self.user)
        expected = "{} is an owner of {}".format(self.user, self.book)
        self.assertEqual(str(bookowner), expected)


class LogEntryModelTests(TestCase):

    def setUp(self):
        self.contact = factories.ContactFactory.create(
            name="Philip James",
        )

    def test_tag_repr(self):
        log = factories.LogFactory.create(contact=self.contact)
        expected = "Log on %s" % (self.contact)
        self.assertEqual(str(log), expected)
