@main.route('/edit-profile', methods=[ 'GET' , 'POST' ])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data

        current_user.about_me = form.about_me.data
        db.session.add(current_user._get_current_object ())
        db.session.commit()
        flash('Your profile has been updated.')
        return redirect(url_for('.user' , username = current_user.username ))
        form.name.data = current_user.name
        form.location.data = current_user.location
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html' , form = form ) 

Grinberg, Miguel. Flask Web Development: Developing Web Applications with Python (Kindle Locations 4435-4453). O'Reilly Media. Kindle Edition.
