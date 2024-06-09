from dbmodel import Staff, db

def create_dummy_staff():
    # Dummy data
    dummy_staff = [
        {'username': 'dr_john_doe', 'email': 'john.doe@example.com', 'password': 'kelompok1', 'profile_picture_url': 'http://example.com/profile1.jpg', 'activity_log_path': '/logs/john_doe.log'},
        {'username': 'dr_jane_smith', 'email': 'jane.smith@example.com', 'password': 'kelompok1', 'profile_picture_url': 'http://example.com/profile2.jpg', 'activity_log_path': '/logs/jane_smith.log'},
        {'username': 'dr_andi_suhendra', 'email': 'andi.suhendra@example.com', 'password': 'kelompok1', 'profile_picture_url': 'http://example.com/profile3.jpg', 'activity_log_path': '/logs/andi_suhendra.log'},
        {'username': 'dr_ayu_wardani', 'email': 'ayu.wardani@example.com', 'password': 'kelompok1', 'profile_picture_url': 'http://example.com/profile4.jpg', 'activity_log_path': '/logs/ayu_wardani.log'},
        {'username': 'dr_budi_santoso', 'email': 'budi.santoso@example.com', 'password': 'kelompok1', 'profile_picture_url': 'http://example.com/profile5.jpg', 'activity_log_path': '/logs/budi_santoso.log'}
    ]

    for staff in dummy_staff:
        hashed_password = bcrypt.generate_password_hash(staff['password']).decode('utf-8')
        new_staff = Staff(
            username=staff['username'],
            email=staff['email'],
            password_salted=hashed_password,
            profile_picture_url=staff['profile_picture_url'],
            activity_log_path=staff['activity_log_path']
        )
        db.session.add(new_staff)

    db.session.commit()
    print('comitted')