var AuthService = {
  user: null,

  login: function(username, success, error) {
    var self = this;

    return Vue.http.post('/api/login', { user_id: username }).then(
      function(res) {
        self.user = {
          username: res.body.user_id,
          authenticated: true
        };
        success();
      },
      error
    );
  },

  logout: function() {
    var self = this;

    return Vue.http.post('/api/logout').then(
      function() {
        self.user = null;
      }
    );
  },

  check: function() {
    return this.user && this.user.authenticated;
  },

  getUser: function() {
    return this.user;
  }
};