
class XMAIL:
    is_logged  = 0
    actual_view = '/login'
    views = None
    login_view = None
    logged_profile = None

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
        self.getbackfunc = logout
        if self.isin_login_view():
            self.getbackfunc = login_success
            if self.is_logged : 
                self.update_actual_view('/home')
                self.getbackfunc = logout
        
          
        self.getbackfunc = self.login_success if self.actual_view == '/login' else logout
        args = (page,credsprofiles,refresh_page,refresh_view,login_success) if actual_view == '/login' else (page,logged_profile,refresh_page,refresh_view,getbackfunc)
        view = views[actual_view](*args)
        page.add(view)

        refresh_page(page)

    def refresh_page(page):
        page.update()

    def view_exists(view):
        return view in views

    def update_actual_view(view):
        global actual_view
        if view_exists(view) : actual_view = view


    def home_view(*args):
        return Home(*args).show()

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

    
