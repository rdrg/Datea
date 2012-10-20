
// INIT MY USER MODELS/VIEWS FROM THE START
Datea.init_my_user_views = function () {
	Datea.my_user_head_view = new Datea.MyUserHeadView({ model: Datea.my_user});
	Datea.my_user_edit_view = new Datea.MyUserEditView({ model: Datea.my_user});
}

Datea.is_logged = function () {
	if (Datea.my_user.get('id')) return true;
	else return false;
}