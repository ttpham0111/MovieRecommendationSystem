var checkAuth = function(to, from, next) {
  var isAuthenticated = AuthService.check();

  if (to.path === '/login') {
    redirect = isAuthenticated ? '/home' : undefined;
  } else {
    redirect = isAuthenticated ? undefined : '/login';
  }

  next(redirect);
};

router = new VueRouter({
  mode: 'history',
  
  routes: [
    {
      path: '/',
      redirect: '/home'
    },
    {
      name: 'login',
      path: '/login',
      component: Vue.component('mr-login'),
      beforeEnter: checkAuth
    },
    {
      name: 'home',
      path: '/home',
      component: Vue.component('mr-home'),
      beforeEnter: checkAuth
    },
  ]
});