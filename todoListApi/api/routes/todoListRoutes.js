'use strict';
module.exports = function(app) {
var todoList = require('../controllers/todoListController'),
 userHandlers = require('../controllers/userController.js');

  // todoList Routes
  app.route('/users')
    .get(todoList.list_all_users)

  app.route('/tasks/:userId')
    .get(todoList.read_a_user)
    .put(todoList.update_a_user)
    .delete(todoList.delete_a_user);

  app.route('/auth/loginRequired')
    .post(userHandlers.loginRequired);

  app.route('/auth/register')
    .post(userHandlers.register);

  app.route('/auth/sign_in')
    .post(userHandlers.sign_in);
};