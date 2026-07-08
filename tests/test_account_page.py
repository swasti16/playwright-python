from pages.accountsPage import AccountPage
from playwright.sync_api import expect
from config.settings import Settings


class TestAccount:
    def test_navbar_visiblity(self, account_page: AccountPage):
        account_page.to_be_visible(account_page.navbar.toolshop_heading)
        account_page.to_be_visible(account_page.navbar.home_link)
        account_page.to_be_visible(account_page.navbar.categories_btn)
        account_page.to_be_visible(account_page.navbar.language_btn)
        # account_page.to_be_visible(account_page.navbar.cart_link)
        account_page.to_be_visible(account_page.navbar.contact_link)

    def test_account_page_layout_and_elements(self, account_page: AccountPage):
        account_page.to_be_visible(account_page.get_by_role("heading", "My Account"))
        account_page.to_be_visible(account_page.get_by_text("Here you can manage your profile, favorites and orders."))
        account_page.to_be_visible(account_page.favorites_button)
        account_page.to_be_visible(account_page.profile_button)
        account_page.to_be_visible(account_page.invoices_button)
        account_page.to_be_visible(account_page.messages_button)

    def test_navigation_to_favorites(self, account_page: AccountPage):
        """
        Verifies that clicking the 'Favorites' navigation link redirects
        the user to the appropriate favorites section or URL endpoint.
        """
        account_page.favorites_button.click()
        expect(account_page.page).to_have_url(f"{Settings.ACCOUNTS_URL}/favorites")

    def test_navigation_to_profile(self, account_page: AccountPage):
        """
        Verifies that clicking the 'Profile' navigation link redirects 
        the user to the profile management page.
        """
        account_page.profile_button.click()
        expect(account_page.page).to_have_url(f"{Settings.ACCOUNTS_URL}/profile")

    def test_navigation_to_invoices(self, account_page: AccountPage):
        """
        Verifies that clicking the 'Invoices' navigation link redirects 
        the user to their order invoice history.
        """
        # Click the Invoices option
        account_page.invoices_button.click()

        # Assert that the URL updates to include the invoices path
        expect(account_page.page).to_have_url(f"{Settings.ACCOUNTS_URL}/invoices")

    def test_navigation_to_messages(self, account_page: AccountPage):
        """
        Verifies that clicking the 'Messages' navigation link redirects 
        the user to their messaging inbox dashboard.
        """

        # Click the Messages option
        account_page.messages_button.click()

        # Assert that the URL updates to include the messages path
        expect(account_page.page).to_have_url(f"{Settings.ACCOUNTS_URL}/messages")

    def test_navigation_to_home(self, account_page: AccountPage):
        """
        Verifies that clicking the 'Messages' navigation link redirects 
        the user to their messaging inbox dashboard.
        """

        # Click the home_link option
        account_page.navbar.home_link.click()

        # Assert that the URL updates to include the messages path
        expect(account_page.page).to_have_url(f"{Settings.BASE_URL}/")
