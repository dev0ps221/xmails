from managers.credsmanager import CredsManager,CredsInstance


credsman = CredsManager()
credsprofiles = credsman.get_creds_profiles()

class XMAIL:
    credsman
    credsprofiles
    is_logged  = 0
    actual_view = '/login'
    views = None
    login_view = None
    logged_profile = None
    view = None
    def login_success(page,profile):
        global imap_server
        global is_logged
        global logged_profile
        is_logged = 1
        logged_profile = profile
        update_actual_view('/home')
        refresh_view(page,logged_profile)

    def logout(page,profile):
        print('disconnecting ',profile)


    def isin_login_view(self):
        return self.actual_view == '/login'

    def  refresh_view(self):
        page.clean()
        self.view.show()
        self.page.add(view)

        self.refresh_page()

    def refresh_page(self):
        self.page.update()

    def view_exists(self,view):
        return view in self.views

    def update_actual_view(self,view):
        if self.view_exists(view) : 
            self.actual_view = view
            self.view = self.views[self.actual_view]


    def app_loop(page: Page):
        global actual_view
        global views
        login_view=Login(page,credsprofiles,refresh_page,refresh_view,login_success)
        page.vertical_alignment = "center"
        views = {
            "/login": login_view.show,
            "/home": home_view
        }
        if view_exists(actual_view):
            refresh_view(page,None)

    
    def loop(self,page:Page)
        self.page = page

    def __init__(self):
        self.LoginView = Login(self)
        self.HomeView = Home(self)
        self.views = {
            '/login':self.LoginView,
            '/home':self.HomeView
        }

    
